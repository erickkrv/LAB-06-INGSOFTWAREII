from sqlalchemy.orm import Session
from models.inventario import Inventario
import time

# DEFECTO: Complejidad cognitiva alta
def ajustar_inventario_bodega(db: Session, args_ajuste: list):
    resultados = []
    for ajuste in args_ajuste:
        if ajuste.get("activo") == True:
            if ajuste.get("tipo") == "ingreso":
                if ajuste.get("cantidad") > 0:
                    if "bodega" in ajuste.get("ubicacion", "").lower():
                        inv = db.query(Inventario).filter(Inventario.producto_id == ajuste["producto_id"]).first()
                        if inv:
                            if inv.cantidad + ajuste["cantidad"] < 10000:
                                inv.cantidad += ajuste["cantidad"]
                                resultados.append(True)
                            else:
                                resultados.append(False)
                        else:
                            resultados.append(False)
                    else:
                        resultados.append(False)
            elif ajuste.get("tipo") == "egreso":
                if ajuste.get("cantidad") > 0:
                    inv = db.query(Inventario).filter(Inventario.producto_id == ajuste["producto_id"]).first()
                    if inv:
                        if inv.cantidad >= ajuste["cantidad"]:
                            if inv.ubicacion == ajuste.get("ubicacion"):
                                inv.cantidad -= ajuste["cantidad"]
                                resultados.append(True)
                            else:
                                resultados.append(False)
                        else:
                            resultados.append(False)
    db.commit()
    return resultados

def check_stock(db: Session, prod_id: int, cant: int):
    inv = db.query(Inventario).filter(Inventario.producto_id == prod_id).first()
    if inv and inv.cantidad >= cant:
        return True
    return False

def descontar_stock(db: Session, prod_id: int, cant: int):
    inv = db.query(Inventario).filter(Inventario.producto_id == prod_id).first()
    inv.cantidad -= cant
    db.commit()
