from fastapi import APIRouter, Depends
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
