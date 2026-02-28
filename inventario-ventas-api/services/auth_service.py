from sqlalchemy.orm import Session
from models.usuario import Usuario
from schemas.usuario import UsuarioCreate
import hashlib

def create_user(db: Session, user: UsuarioCreate):
    hashed = hashlib.md5(user.password.encode()).hexdigest()
    db_user = Usuario(nombre=user.nombre, email=user.email, password_hash=hashed, rol=user.rol)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
