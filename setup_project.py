import os

BASE_DIR = r"c:\Users\smora\Documents\URL\Septimo ciclo\INGSOWFTARE II\LAB 04\inventario-ventas-api"

dirs = [
    "config",
    "models",
    "schemas",
    "routers",
    "services",
    "integrations",
    "utils",
    "tests",
]

for d in dirs:
    os.makedirs(os.path.join(BASE_DIR, d), exist_ok=True)
    with open(os.path.join(BASE_DIR, d, "__init__.py"), "w", encoding="utf-8") as f:
        f.write("")

files_content = {}

files_content["requirements.txt"] = """fastapi==0.104.1
uvicorn==0.24.0
sqlalchemy==2.0.23
pydantic==2.5.2
python-jose==3.3.0
passlib==1.7.4
python-dotenv==1.0.0
httpx==0.25.2
pytest==7.4.3
"""

files_content["sonar-project.properties"] = """sonar.projectKey=inventario-ventas-api
sonar.projectName=Sistema de Inventarios y Ventas - API Backend
sonar.projectVersion=1.0
sonar.sources=.
sonar.exclusions=tests/**,**/__pycache__/**,*.md
sonar.python.version=3.11
sonar.sourceEncoding=UTF-8
"""

files_content[".env.example"] = """DATABASE_URL=sqlite:///./inventario_ventas.db
SECRET_KEY=supersecretkey_change_me_in_production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
"""

files_content["config/settings.py"] = """import os

# DEFECTO intencional: Hardcoded secret keys y passwords (Vulnerabilidad)
SECRET_KEY = "my_super_secret_dev_key_123"
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./inventario_ventas.db")
ALGORITHM = "HS256"
PAYMENT_GATEWAY_APY_KEY = "sk_live_1234567890abcdef"
"""

files_content["config/database.py"] = """from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from config.settings import DATABASE_URL

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
"""

files_content["models/usuario.py"] = """from sqlalchemy import Column, Integer, String
from config.database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    rol = Column(String)
"""

files_content["models/producto.py"] = """from sqlalchemy import Column, Integer, String, Float, Boolean
from config.database import Base

class Producto(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    descripcion = Column(String)
    precio = Column(Float)
    activo = Column(Boolean, default=True)
"""

files_content["models/inventario.py"] = """from sqlalchemy import Column, Integer, String, ForeignKey
from config.database import Base

class Inventario(Base):
    __tablename__ = "inventarios"

    id = Column(Integer, primary_key=True, index=True)
    producto_id = Column(Integer, ForeignKey("productos.id"))
    cantidad = Column(Integer, default=0)
    ubicacion = Column(String, default="Bodega Principal")
"""

files_content["models/venta.py"] = """from sqlalchemy import Column, Integer, String, Float, ForeignKey
from config.database import Base

class Venta(Base):
    __tablename__ = "ventas"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    total = Column(Float)
    estado = Column(String)
    metodo_pago = Column(String)

class VentaItem(Base):
    __tablename__ = "venta_items"

    id = Column(Integer, primary_key=True, index=True)
    venta_id = Column(Integer, ForeignKey("ventas.id"))
    producto_id = Column(Integer, ForeignKey("productos.id"))
    cantidad = Column(Integer)
    precio_unitario = Column(Float)
"""

files_content["models/factura.py"] = """from sqlalchemy import Column, Integer, String, Float, ForeignKey
from config.database import Base

class Factura(Base):
    __tablename__ = "facturas"

    id = Column(Integer, primary_key=True, index=True)
    venta_id = Column(Integer, ForeignKey("ventas.id"))
    numero_factura = Column(String, unique=True, index=True)
    subtotal = Column(Float)
    impuestos = Column(Float)
    total = Column(Float)
    nit_cliente = Column(String)
"""

files_content["utils/calculadora_impuestos.py"] = """# DEFECTO: Nombres de variables poco descriptivos (Mantenibilidad)
def calc_imp(s, d=0):
    t = 0.12
    x = s - (s * d)
    z = x * t
    r = x + z
    return r, z, x

# DEFECTO: Dead code
def calc_desc_esp(m):
    if m > 1000:
        return 0.10
    return 0.05
"""

files_content["utils/validaciones.py"] = """def es_email_valido(email: str) -> bool:
    return "@" in email and "." in email

def tiene_stock_suficiente(stock_actual, cantidad_req):
    return stock_actual >= cantidad_req
"""

files_content["integrations/pasarela_pagos.py"] = """import time
import random

def procesar_pago(amount, method, token):
    try:
        time.sleep(1) # Simula latencia
        if method == "INVALIDO":
            return False
        if random.random() < 0.05:
            # Error aleatorio
            raise ConnectionError("Timeout connection")
        return True
    except Exception:
        # DEFECTO: Capturar y silenciar todas las excepciones (Mala practica)
        pass
    return False
"""

files_content["integrations/contabilidad.py"] = """def exportar_venta_contabilidad(venta_id, total, fecha_str):
    print(f"Exportando venta {venta_id} por {total} al sistema en la fecha {fecha_str}")
    return True
"""

files_content["integrations/email_service.py"] = """def enviar_factura_email(email_destino, num_factura, pdf_link=None):
    print(f"Enviando correo a {email_destino} con factura {num_factura}")
    return True
"""

files_content["schemas/producto.py"] = """from pydantic import BaseModel
from typing import Optional

class ProductoBase(BaseModel):
    nombre: str
    descripcion: str
    precio: float
    activo: bool = True

class ProductoCreate(ProductoBase):
    pass

class ProductoResponse(ProductoBase):
    id: int
    class Config:
        from_attributes = True
"""

files_content["schemas/inventario.py"] = """from pydantic import BaseModel

class InventarioBase(BaseModel):
    producto_id: int
    cantidad: int
    ubicacion: str = "Bodega Principal"

class InventarioCreate(InventarioBase):
    pass

class InventarioResponse(InventarioBase):
    id: int
    class Config:
        from_attributes = True
"""

files_content["schemas/venta.py"] = """from pydantic import BaseModel
from typing import List

class VentaItemCreate(BaseModel):
    producto_id: int
    cantidad: int

class VentaCreate(BaseModel):
    usuario_id: int
    items: List[VentaItemCreate]
    metodo_pago: str

class VentaResponse(BaseModel):
    id: int
    usuario_id: int
    total: float
    estado: str
    class Config:
        from_attributes = True
"""

files_content["schemas/factura.py"] = """from pydantic import BaseModel

class FacturaResponse(BaseModel):
    id: int
    venta_id: int
    numero_factura: str
    subtotal: float
    impuestos: float
    total: float
    nit_cliente: str
    class Config:
        from_attributes = True
"""

files_content["schemas/usuario.py"] = """from pydantic import BaseModel

class UsuarioCreate(BaseModel):
    nombre: str
    email: str
    password: str
    rol: str

class UsuarioResponse(BaseModel):
    id: int
    nombre: str
    email: str
    rol: str
    class Config:
        from_attributes = True
"""

files_content["services/auth_service.py"] = """from sqlalchemy.orm import Session
from models.usuario import Usuario
from schemas.usuario import UsuarioCreate
import hashlib

def create_user(db: Session, user: UsuarioCreate):
    hashed = hashlib.md5(user.password.encode()).hexdigest()
    db_user = Usuario(nombre=user.nombre, email=user.email, password_hash=hashed, rol=user.rol)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
"""

files_content["services/venta_service.py"] = """from sqlalchemy.orm import Session
from models.venta import Venta, VentaItem
from models.inventario import Inventario
from utils.calculadora_impuestos import calc_imp
import sqlite3

# DEFECTO: Comentario engañoso/obsoleto
# Esta función limpia la memoria caché del gestor de ventas y formatea el disco de ser necesario.
def validar_venta_activa(usuario_id: int):
    return True

# DEFECTO: Complejidad ciclomática alta (muchos ifs anidados)
def validar_condiciones_venta(usuario_rec, pago, prod_list, descuento_cliente, dia_semana, monto_estimado, cupon):
    if usuario_rec is None:
        return False
    else:
        if pago not in ['TARJETA', 'EFECTIVO', 'TRANSFERENCIA']:
            return False
        elif pago == 'TARJETA' and monto_estimado < 10:
            return False
        else:
            if len(prod_list) == 0:
                return False
            else:
                if descuento_cliente > 0.5:
                    return False
                elif descuento_cliente < 0:
                    return False
                else:
                    if dia_semana == 'DOMINGO':
                        if not cupon:
                            return True
                        elif cupon == 'FALSO':
                            return False
                    elif dia_semana == 'SABADO':
                        if pago == 'TRANSFERENCIA':
                            return False
                        
    if monto_estimado > 10000 and pago == 'EFECTIVO':
        return False
        
    return True

# DEFECTO: Código duplicado (revisar facturacion_service.py)
def calcular_totales_venta(subtotal_bruto):
    descuento = subtotal_bruto * 0.05
    sub_neto = subtotal_bruto - descuento
    imp = sub_neto * 0.12
    tot = sub_neto + imp
    return sub_neto, imp, tot

# DEFECTO: Posible SQL Injection sin parametrizar
def buscar_venta_por_cliente(db: Session, nombre_cliente: str):
    query = f"SELECT * FROM ventas v JOIN usuarios u ON v.usuario_id = u.id WHERE u.nombre = '{nombre_cliente}'"
    result = db.execute(query)
    return result.fetchall()
"""

files_content["services/facturacion_service.py"] = """from sqlalchemy.orm import Session
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
"""

files_content["services/inventario_service.py"] = """from sqlalchemy.orm import Session
from models.inventario import Inventario
import time

# DEFECTO: Complejidad cognitiva alta
def ajustar_inventario_bodega(db: Session, args_ajuste: list):
    resultados = []
    for ajuste in args_ajuste:
        if ajuste.get("activo") == True:
            if ajuste.get("tipo") == "ingreso":
                if ajuste.get("cantidad") > 0:
                    if "bodega" in ajuste.get("ubicacion", "").lower():
                        inv = db.query(Inventario).filter(Inventario.producto_id == ajuste["producto_id"]).first()
                        if inv:
                            if inv.cantidad + ajuste["cantidad"] < 10000:
                                inv.cantidad += ajuste["cantidad"]
                                resultados.append(True)
                            else:
                                resultados.append(False)
                        else:
                            resultados.append(False)
                    else:
                        resultados.append(False)
            elif ajuste.get("tipo") == "egreso":
                if ajuste.get("cantidad") > 0:
                    inv = db.query(Inventario).filter(Inventario.producto_id == ajuste["producto_id"]).first()
                    if inv:
                        if inv.cantidad >= ajuste["cantidad"]:
                            if inv.ubicacion == ajuste.get("ubicacion"):
                                inv.cantidad -= ajuste["cantidad"]
                                resultados.append(True)
                            else:
                                resultados.append(False)
                        else:
                            resultados.append(False)
    db.commit()
    return resultados

def check_stock(db: Session, prod_id: int, cant: int):
    inv = db.query(Inventario).filter(Inventario.producto_id == prod_id).first()
    if inv and inv.cantidad >= cant:
        return True
    return False

def descontar_stock(db: Session, prod_id: int, cant: int):
    inv = db.query(Inventario).filter(Inventario.producto_id == prod_id).first()
    inv.cantidad -= cant
    db.commit()
"""

files_content["services/checkout_service.py"] = """from sqlalchemy.orm import Session
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
    if usuario_id <= 0:
        raise ValueError("Id de usuario invalido o no encontrado")

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
"""

files_content["routers/auth.py"] = """from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas.usuario import UsuarioCreate, UsuarioResponse
from services.auth_service import create_user
from config.database import get_db

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UsuarioResponse)
def register(user: UsuarioCreate, db: Session = Depends(get_db)):
    return create_user(db, user)
"""

files_content["routers/productos.py"] = """from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models.producto import Producto
from schemas.producto import ProductoCreate, ProductoResponse
from config.database import get_db

router = APIRouter(prefix="/productos", tags=["productos"])

@router.post("/", response_model=ProductoResponse)
def crear_producto(prod: ProductoCreate, db: Session = Depends(get_db)):
    db_prod = Producto(**prod.model_dump())
    db.add(db_prod)
    db.commit()
    db.refresh(db_prod)
    return db_prod

@router.get("/", response_model=list[ProductoResponse])
def listar_productos(db: Session = Depends(get_db)):
    return db.query(Producto).all()
"""

files_content["routers/inventario.py"] = """from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models.inventario import Inventario
from schemas.inventario import InventarioCreate, InventarioResponse
from config.database import get_db

router = APIRouter(prefix="/inventario", tags=["inventario"])

@router.post("/", response_model=InventarioResponse)
def crear_registro(inv: InventarioCreate, db: Session = Depends(get_db)):
    db_inv = Inventario(**inv.model_dump())
    db.add(db_inv)
    db.commit()
    db.refresh(db_inv)
    return db_inv

@router.get("/", response_model=list[InventarioResponse])
def listar_inventario(db: Session = Depends(get_db)):
    return db.query(Inventario).all()
"""

files_content["routers/ventas.py"] = """from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.venta import VentaCreate
from services.checkout_service import orquestar_checkout_completo
from services.venta_service import buscar_venta_por_cliente
from config.database import get_db
import typing

router = APIRouter(prefix="/ventas", tags=["ventas"])

@router.post("/checkout")
def checkout(venta: VentaCreate, nit: str = "CF", db: Session = Depends(get_db)):
    try:
        resultado = orquestar_checkout_completo(db, venta, nit)
        return resultado
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/buscar")
def buscar_por_cliente(cliente: str, db: Session = Depends(get_db)):
    try:
        res = buscar_venta_por_cliente(db, cliente)
        # DEFECTO intencional en res mapeado raw
        return [{"id": r[0], "total": r[2]} for r in res]
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno")
"""

files_content["routers/facturacion.py"] = """from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models.factura import Factura
from config.database import get_db

router = APIRouter(prefix="/facturas", tags=["facturacion"])

@router.get("/")
def listar_facturas(db: Session = Depends(get_db)):
    facturas = db.query(Factura).all()
    return facturas
"""

files_content["main.py"] = """from fastapi import FastAPI
from config.database import Base, engine
from routers import ventas, productos, inventario, facturacion, auth

# Crea las tablas
Base.metadata.create_all(bind=engine)

app = FastAPI(title="API de Ventas e Inventarios (Audit Sandbox)")

app.include_router(auth.router)
app.include_router(productos.router)
app.include_router(inventario.router)
app.include_router(ventas.router)
app.include_router(facturacion.router)

@app.get("/")
def home():
    return {"message": "API Backend Activo. Ve a /docs para la documentacion de endpoints."}
"""

files_content["tests/test_ventas.py"] = """from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "API Backend Activo" in response.json().get("message")
"""

files_content["README.md"] = """# Sistema de Inventarios y Ventas - API Backend

Este proyecto es una API básica desarrollada con **FastAPI** y **SQLAlchemy**, enfocada en la gestión de un sistema de inventario y el checkout de ventas. Ha sido diseñado específicamente como laboratorio para análisis estático y auditoría de código con SonarQube, por lo que contiene bugs, vulnerabilidades, code smells y complejidad intencional.

## Instalación

1. Crear y activar entorno virtual:
```bash
python -m venv venv
venv\\Scripts\\activate
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

3. Ejecutar la aplicación:
```bash
uvicorn main:app --reload
```
Visita la documentación automática de la API en: `http://localhost:8000/docs`

## Aspectos de Auditoría Plantados

1. **Mantenibilidad:** Funciones muy largas (`checkout_service.py`), nombres de variables poco claros (`calculadora_impuestos.py`), comentarios desfasados.
2. **Complejidad:** Alta complejidad ciclomática (`venta_service.py`) y cognitiva (`inventario_service.py`).
3. **Duplicación:** Lógica repetida entre servicios de ventas y de facturación.
4. **Vulnerabilidades:** Contraseñas en texto plano, tokens mockeados duros, posible SQL injection.
5. **Miscellaneous:** Excepciones atrapadas sin acción, variables y funciones no usadas (`dead code`), falta de algunos tipados, etc.
"""

for path, content in files_content.items():
    with open(os.path.join(BASE_DIR, path), "w", encoding="utf-8") as f:
        f.write(content)

print(f"Project initialized in {BASE_DIR}")
