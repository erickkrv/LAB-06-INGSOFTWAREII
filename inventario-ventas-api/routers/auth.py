from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas.usuario import UsuarioCreate, UsuarioResponse
from services.auth_service import create_user
from config.database import get_db

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UsuarioResponse)
def register(user: UsuarioCreate, db: Session = Depends(get_db)):
    return create_user(db, user)
