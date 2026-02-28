import os

BASE_DIR = r"c:\Users\smora\Documents\URL\Septimo ciclo\INGSOWFTARE II\LAB 04\inventario-ventas-api"

files_content = {}

files_content["tests/test_inventario.py"] = """from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_listar_inventario():
    response = client.get("/inventario/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
"""

files_content["tests/test_checkout.py"] = """from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_checkout_validation_error():
    # Enviar payload invalido para trigger excepcion
    response = client.post("/ventas/checkout", json={"usuario_id": 0, "items": [], "metodo_pago": "TEST"})
    assert response.status_code == 422 # Error de validacion de Pydantic por falta de body correcto o 400 por la logica interna
"""

files_content["tests/test_facturacion.py"] = """from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_listar_facturas():
    response = client.get("/facturas/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
"""

for path, content in files_content.items():
    with open(os.path.join(BASE_DIR, path), "w", encoding="utf-8") as f:
        f.write(content)

print(f"Missing test files added.")
