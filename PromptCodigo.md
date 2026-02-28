# Prompt para Generar el Código del Sistema de Inventarios y Ventas

## Contexto del Proyecto

Soy estudiante de Ingeniería de Software II en la Universidad Rafael Landívar. Necesito que generes la implementación de un **módulo funcional representativo** de un sistema de inventarios y ventas. Este código será auditado con **SonarQube/SonarCloud** como parte de un laboratorio de auditoría técnica y análisis estático.

**IMPORTANTE:** El código debe ser funcional y realista, pero se espera que tenga **defectos intencionalmente plantados** (code smells, complejidad alta, duplicación, vulnerabilidades menores) para que la auditoría con SonarQube arroje hallazgos interesantes que yo pueda analizar. No debe ser código perfecto ni tampoco código basura — debe simular un proyecto real con deuda técnica natural.

---

## Arquitectura del Sistema (ya definida en laboratorios previos)

El sistema usa una **arquitectura en capas con monolito modular**:

- **Stack:** Python 3.11+ / FastAPI / SQLAlchemy / PostgreSQL (o SQLite para desarrollo)
- **Estilo arquitectónico:** Monolito modular en capas (presentación → lógica de negocio → persistencia)
- **Base de datos:** Una sola BD transaccional con propiedades ACID
- **Contenedores (Nivel 2 - C4):**
  1. Aplicación Web de Ventas (frontend — no se implementa aquí)
  2. Aplicación Web Administrativa (frontend — no se implementa aquí)
  3. **API Backend** ← ESTE es el que se implementa
  4. Base de Datos Transaccional

- **Actores:** Cliente, Vendedor, Bodeguero, Gerente, Proveedor
- **Sistemas externos (simulados):** Pasarela de Pagos, Sistema de Contabilidad, Servicio de Email/Notificaciones

---

## Qué Implementar

Implementa el **API Backend** con los siguientes módulos del dominio:

### Módulos requeridos:

1. **Ventas/Checkout** (flujo crítico principal): registrar venta, calcular totales con impuestos, verificar y descontar stock
2. **Inventario:** gestión de productos, stock, ajustes de inventario
3. **Facturación:** generación de facturas asociadas a ventas
4. **Autenticación/Roles:** sistema básico de roles (Cliente, Vendedor, Bodeguero, Admin/Gerente)

### Integraciones simuladas (mocks/stubs):

- Pasarela de Pagos (simular llamada HTTP con latencia artificial)
- Sistema de Contabilidad (exportación de ventas)
- Servicio de Email (envío de facturas)

---

## Estructura de Carpetas Esperada

```
inventario-ventas-api/
├── README.md
├── requirements.txt
├── sonar-project.properties          # Configuración de SonarQube
├── .env.example
├── main.py                           # Entry point FastAPI
├── config/
│   ├── __init__.py
│   ├── database.py                   # Conexión SQLAlchemy
│   └── settings.py                   # Variables de entorno
├── models/
│   ├── __init__.py
│   ├── producto.py
│   ├── venta.py
│   ├── factura.py
│   ├── usuario.py
│   └── inventario.py
├── schemas/
│   ├── __init__.py
│   ├── producto.py
│   ├── venta.py
│   ├── factura.py
│   └── usuario.py
├── routers/
│   ├── __init__.py
│   ├── ventas.py
│   ├── productos.py
│   ├── inventario.py
│   ├── facturacion.py
│   └── auth.py
├── services/
│   ├── __init__.py
│   ├── venta_service.py              # Lógica de negocio de ventas
│   ├── inventario_service.py         # Lógica de inventario
│   ├── facturacion_service.py        # Generación de facturas
│   ├── checkout_service.py           # Orquestación del checkout completo
│   └── auth_service.py               # Autenticación y autorización
├── integrations/
│   ├── __init__.py
│   ├── pasarela_pagos.py             # Mock de pasarela de pagos
│   ├── contabilidad.py               # Mock de exportación contable
│   └── email_service.py              # Mock de envío de email
├── utils/
│   ├── __init__.py
│   ├── calculadora_impuestos.py      # Cálculos fiscales
│   └── validaciones.py               # Validaciones comunes
└── tests/
    ├── __init__.py
    ├── test_ventas.py
    ├── test_inventario.py
    ├── test_checkout.py
    └── test_facturacion.py
```

---

## Defectos Intencionados para la Auditoría

El código debe incluir de forma natural (no obvia ni forzada) los siguientes tipos de problemas para que SonarQube los detecte:

### Mantenibilidad (al menos 3):

1. **Función demasiado larga** en `checkout_service.py`: la función que orquesta el checkout (verificar stock → reservar → cobrar → facturar → notificar) debe tener 80-120 líneas en un solo método, sin descomposición adecuada.
2. **Nombres de variables poco descriptivos** en `calculadora_impuestos.py`: usar variables como `t`, `s`, `d`, `x` en lugar de nombres claros.
3. **Comentarios obsoletos o engañosos** en `venta_service.py`: comentarios que no corresponden a lo que hace el código.

### Complejidad (al menos 2):

4. **Complejidad ciclomática alta** en `venta_service.py`: función con muchos `if/elif/else` anidados para validar una venta (validar stock, tipo de pago, descuentos, tipo de cliente, estado del pedido, etc.).
5. **Complejidad cognitiva alta** en `inventario_service.py`: lógica con múltiples niveles de anidamiento para ajustes de inventario con condiciones encadenadas.

### Vulnerabilidad / Riesgo (al menos 1):

6. **SQL injection potencial** o **manejo inseguro de inputs** en algún endpoint que construya queries parcialmente sin parametrizar, o contraseñas en texto plano / secrets hardcodeados en `settings.py`.

### Duplicación (al menos 1):

7. **Código duplicado** entre `venta_service.py` y `facturacion_service.py`: lógica de cálculo de totales (subtotal, impuesto, descuento, total) repetida en ambos archivos en lugar de reutilizar una función común.

### Extras deseables:

- Imports sin usar en algunos archivos
- Funciones definidas pero nunca llamadas (dead code)
- Excepciones genéricas (`except Exception: pass`) en integraciones
- Magic numbers sin constantes
- Falta de tipado en algunas funciones

---

## Requisitos Técnicos

1. **El código debe funcionar:** debe poder ejecutarse con `uvicorn main:app --reload` y responder en los endpoints
2. **Usar SQLite para desarrollo** (para no requerir PostgreSQL instalado, pero que el código esté preparado para PostgreSQL)
3. **Incluir `sonar-project.properties`** configurado para Python:

```properties
sonar.projectKey=inventario-ventas-api
sonar.projectName=Sistema de Inventarios y Ventas - API Backend
sonar.projectVersion=1.0
sonar.sources=.
sonar.exclusions=tests/**,**/__pycache__/**,*.md
sonar.python.version=3.11
sonar.sourceEncoding=UTF-8
```

4. **Incluir `requirements.txt`**:

```
fastapi==0.104.1
uvicorn==0.24.0
sqlalchemy==2.0.23
pydantic==2.5.2
python-jose==3.3.0
passlib==1.7.4
python-dotenv==1.0.0
httpx==0.25.2
pytest==7.4.3
```

5. **Incluir tests básicos** (no exhaustivos) que cubran los flujos principales
6. **Incluir un README.md** con instrucciones de setup y ejecución

---

## Flujo Crítico: Checkout Completo (la función más importante)

Este es el flujo que debe estar implementado de punta a punta y es el que se auditará más de cerca:

1. Recibir petición de checkout con: `usuario_id`, `items: [{producto_id, cantidad}]`, `metodo_pago`
2. Validar que el usuario existe y tiene permisos
3. Para cada item: verificar stock disponible
4. Reservar stock (descontar de inventario)
5. Calcular subtotal, impuestos (12% IVA), descuentos si aplican, total
6. Llamar a pasarela de pagos (mock) — con timeout y manejo de errores
7. Si el pago falla: revertir stock (rollback)
8. Generar factura asociada
9. Enviar notificación por email (mock)
10. Exportar a contabilidad (mock)
11. Retornar confirmación con número de venta y factura

**Este flujo INTENCIONALMENTE debe estar en una sola función larga en `checkout_service.py`** para que SonarQube lo detecte como code smell de complejidad y longitud.

---

## Lo que NO debes hacer

- No generes código trivial tipo "Hello World"
- No hagas que los defectos sean obvios o comentados como `# BUG INTENCIONAL`
- No uses frameworks o librerías innecesarias
- No implementes frontend

## Lo que SÍ debes hacer

- Código que se vea como un proyecto real en desarrollo temprano
- Defectos que parezcan naturales (como los que cometería un equipo junior con prisa)
- Transacciones ACID reales con SQLAlchemy
- Estructura modular que refleje la arquitectura en capas definida
- Que todo funcione al ejecutarse
