# Sistema de Inventarios y Ventas - API Backend

Este proyecto es una API básica desarrollada con **FastAPI** y **SQLAlchemy**, enfocada en la gestión de un sistema de inventario y el checkout de ventas. Ha sido diseñado específicamente como laboratorio para análisis estático y auditoría de código con SonarQube, por lo que contiene bugs, vulnerabilidades, code smells y complejidad intencional.

## Instalación

1. Crear y activar entorno virtual:
```bash
python -m venv venv
venv\Scripts\activate
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

3. Ejecutar la aplicación:
```bash
uvicorn main:app --reload
```
Visita la documentación automática de la API en: `http://localhost:8000/docs`

## Aspectos de Auditoría Plantados

1. **Mantenibilidad:** Funciones muy largas (`checkout_service.py`), nombres de variables poco claros (`calculadora_impuestos.py`), comentarios desfasados.
2. **Complejidad:** Alta complejidad ciclomática (`venta_service.py`) y cognitiva (`inventario_service.py`).
3. **Duplicación:** Lógica repetida entre servicios de ventas y de facturación.
4. **Vulnerabilidades:** Contraseñas en texto plano, tokens mockeados duros, posible SQL injection.
5. **Miscellaneous:** Excepciones atrapadas sin acción, variables y funciones no usadas (`dead code`), falta de algunos tipados, etc.
