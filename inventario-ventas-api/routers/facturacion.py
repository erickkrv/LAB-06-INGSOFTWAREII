from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models.factura import Factura
from config.database import get_db

router = APIRouter(prefix="/facturas", tags=["facturacion"])

@router.get("/")
def listar_facturas(db: Session = Depends(get_db)):
    facturas = db.query(Factura).all()
    return facturas
