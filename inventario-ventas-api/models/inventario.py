from sqlalchemy import Column, Integer, String, ForeignKey
from config.database import Base

class Inventario(Base):
    __tablename__ = "inventarios"

    id = Column(Integer, primary_key=True, index=True)
    producto_id = Column(Integer, ForeignKey("productos.id"))
    cantidad = Column(Integer, default=0)
    ubicacion = Column(String, default="Bodega Principal")
