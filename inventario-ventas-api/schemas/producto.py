from pydantic import BaseModel
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
