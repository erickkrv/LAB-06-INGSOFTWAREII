from fastapi import APIRouter, Depends
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
