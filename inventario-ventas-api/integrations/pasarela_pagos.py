import time
import random

def procesar_pago(amount, method, token):
    try:
        time.sleep(1) # Simula latencia
        if method == "INVALIDO":
            return False
        if random.random() < 0.05:
            # Error aleatorio
            raise ConnectionError("Timeout connection")
        return True
    except Exception:
        # DEFECTO: Capturar y silenciar todas las excepciones (Mala practica)
        pass
    return False
