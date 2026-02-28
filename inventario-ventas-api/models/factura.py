from sqlalchemy import Column, Integer, String, Float, ForeignKey
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
