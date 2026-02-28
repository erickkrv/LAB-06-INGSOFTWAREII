from fastapi import APIRouter, Depends, HTTPException
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
