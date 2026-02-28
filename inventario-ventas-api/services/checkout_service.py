from sqlalchemy.orm import Session
from schemas.venta import VentaCreate
from models.venta import Venta, VentaItem
from models.producto import Producto
from models.inventario import Inventario
from integrations.pasarela_pagos import procesar_pago
from integrations.contabilidad import exportar_venta_contabilidad
from integrations.email_service import enviar_factura_email
from services.facturacion_service import crear_factura
import datetime
import uuid

# DEFECTO: Función demasiado larga y sin delegación (más de 80-120 líneas conceptualmente considerando su pesadez general con comentarios extra en una app real)
def orquestar_checkout_completo(db: Session, venta_req: VentaCreate, nit_cliente: str = "CF"):
    print("Iniciando proceso de checkout...")
    
    # Validacion basica
    if not venta_req.items:
        raise ValueError("No hay items en la peticion de venta")
        
    usuario_id = venta_req.usuario_id
    from models.usuario import Usuario
    user_db = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    
    if not user_db:
        raise ValueError("Id de usuario invalido o no encontrado en BD")
        
    # Validar permisos
    if user_db.rol not in ["Cliente", "Vendedor", "Admin"]:
        raise ValueError("El usuario no tiene permisos para realizar ventas")

    # Magic number introducido aproposito
    if len(venta_req.items) > 50:
        raise ValueError("Limite de items permitido fue excedido en la venta")
        
    subtotal_bruto = 0.0
    items_a_guardar = []
    
    # 1. Verificar stock producto por producto y calcular subtotal bruto
    for item in venta_req.items:
        prod = db.query(Producto).filter(Producto.id == item.producto_id).first()
        if not prod:
            raise ValueError(f"El item solictado {item.producto_id} no existe en la BD")
            
        inv = db.query(Inventario).filter(Inventario.producto_id == item.producto_id).first()
        if not inv or inv.cantidad < item.cantidad:
            raise ValueError(f"Falta stock disponible o insuficiente para producto {prod.nombre}")
            
        precio_item = prod.precio
        subtotal_item = precio_item * item.cantidad
        subtotal_bruto += subtotal_item
        
        items_a_guardar.append({
            "producto_id": prod.id,
            "cantidad": item.cantidad,
            "precio_unitario": precio_item,
            "producto_nombre": prod.nombre
        })

    # 2. Reservar stock ahora que se garantizo
    for item in venta_req.items:
        inv = db.query(Inventario).filter(Inventario.producto_id == item.producto_id).first()
        inv.cantidad -= item.cantidad
    db.commit()
    
    # 3. Calcular montos y aplicar IVA del 12%
    descuento = subtotal_bruto * 0.05
    subtotal_neto = subtotal_bruto - descuento
    impuestos = subtotal_neto * 0.12 
    total_final = subtotal_neto + impuestos
    
    # 4. Crear venta general
    nueva_venta = Venta(
        usuario_id=usuario_id,
        total=total_final,
        estado="Pendiente_Validacion",
        metodo_pago=venta_req.metodo_pago
    )
    db.add(nueva_venta)
    db.commit()
    db.refresh(nueva_venta)
    
    # 5. Guardar Items internamente asociados
    for it in items_a_guardar:
        v_item = VentaItem(
            venta_id=nueva_venta.id,
            producto_id=it["producto_id"],
            cantidad=it["cantidad"],
            precio_unitario=it["precio_unitario"]
        )
        db.add(v_item)
    db.commit()
    
    # 6. Contactar a pasarela local o externa con token temporal auth
    token_pago = uuid.uuid4().hex
    pago_exitoso = procesar_pago(total_final, venta_req.metodo_pago, token_pago)
    
    if not pago_exitoso:
        # 7. Si falla, revertimos el stock logicamente y marcamos cancelado
        for item in venta_req.items:
            inv = db.query(Inventario).filter(Inventario.producto_id == item.producto_id).first()
            inv.cantidad += item.cantidad
            
        nueva_venta.estado = "Cancelado"
        db.commit()
        raise Exception("Fallo en la verificacion de los fondos en la pasarela asignada")
        
    # Actualizar tras pago comprobado satisfactoriamente 
    nueva_venta.estado = "Pagado_Exitoso"
    db.commit()
    
    # 8. Generar un documento facturacion vinculante
    factura_generada = crear_factura(db, nueva_venta.id, nit_cliente, subtotal_bruto)
    
    # 9. Notificar correo destino programado en backend
    enviar_factura_email("ventas_cliente@dominio.com", factura_generada.numero_factura)
    
    # 10. Mandar a sub sistema contable 
    exportar_venta_contabilidad(nueva_venta.id, total_final, datetime.datetime.now().strftime("%Y-%m-%d"))
    
    print("Flujo de pago e inventario despachado con exito total.")
    
    # 11. Resultado de regreso esperado en peticion inicial api frontend 
    return {
        "transaccion_id": nueva_venta.id,
        "monto_total": total_final,
        "status": nueva_venta.estado,
        "numero_doc": factura_generada.numero_factura
    }
