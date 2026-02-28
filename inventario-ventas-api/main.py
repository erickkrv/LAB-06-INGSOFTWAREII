from fastapi import FastAPI
from config.database import Base, engine
from routers import ventas, productos, inventario, facturacion, auth

# Crea las tablas
Base.metadata.create_all(bind=engine)

app = FastAPI(title="API de Ventas e Inventarios (Audit Sandbox)")

app.include_router(auth.router)
app.include_router(productos.router)
app.include_router(inventario.router)
app.include_router(ventas.router)
app.include_router(facturacion.router)

@app.get("/")
def home():
    return {"message": "API Backend Activo. Ve a /docs para la documentacion de endpoints."}
