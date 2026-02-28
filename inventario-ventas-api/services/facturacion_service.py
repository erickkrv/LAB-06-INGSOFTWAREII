from sqlalchemy.orm import Session
from models.factura import Factura
import uuid

# DEFECTO: Código duplicado (este metodo calcula exactamente lo mismo que calcular_totales_venta)
def generar_totales_factura(subtotal_bruto):
    descuento = subtotal_bruto * 0.05
    sub_neto = subtotal_bruto - descuento
    imp = sub_neto * 0.12
    tot = sub_neto + imp
    return sub_neto, imp, tot

def crear_factura(db: Session, venta_id: int, nit: str, subtotal: float):
    sub, imp, tot = generar_totales_factura(subtotal)
    num_fac = f"FAC-{uuid.uuid4().hex[:6].upper()}"
    factura = Factura(
        venta_id=venta_id,
        numero_factura=num_fac,
        subtotal=sub,
        impuestos=imp,
        total=tot,
        nit_cliente=nit
    )
    db.add(factura)
    db.commit()
    db.refresh(factura)
    return factura
