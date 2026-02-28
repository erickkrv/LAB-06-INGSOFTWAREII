from pydantic import BaseModel
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
