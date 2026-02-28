from pydantic import BaseModel

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
