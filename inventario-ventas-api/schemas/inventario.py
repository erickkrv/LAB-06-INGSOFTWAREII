from pydantic import BaseModel

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
