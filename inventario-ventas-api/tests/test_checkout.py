from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_checkout_validation_error():
    # Enviar payload invalido para trigger excepcion
    response = client.post("/ventas/checkout", json={"usuario_id": 0, "items": [], "metodo_pago": "TEST"})
    assert response.status_code == 422 # Error de validacion de Pydantic por falta de body correcto o 400 por la logica interna
