import os

# DEFECTO intencional: Hardcoded secret keys y passwords (Vulnerabilidad)
SECRET_KEY = "my_super_secret_dev_key_123"
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./inventario_ventas.db")
ALGORITHM = "HS256"
PAYMENT_GATEWAY_APY_KEY = "sk_live_1234567890abcdef"
