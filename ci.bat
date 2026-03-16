@echo off
echo ==========================================================
echo       PIPELINE LOCAL DE INTEGRACION CONTINUA (CI)         
echo ==========================================================
echo.

echo [Paso 1/2] Ejecutando Pruebas Unitarias con pytest...
echo ----------------------------------------------------------
python -m pytest inventario-ventas-api/tests/test_calculadora_impuestos.py
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Las pruebas unitarias fallaron. Pipeline detenido.
    exit /b %errorlevel%
)
echo [EXITO] Pruebas unitarias aprobadas.
echo.

echo [Paso 2/2] Ejecutando Analisis Estatico con pylint...
echo ----------------------------------------------------------
python -m pylint inventario-ventas-api/utils/calculadora_impuestos.py
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] El analisis estatico fallo. Pipeline detenido.
    exit /b %errorlevel%
)
echo [EXITO] Analisis estatico aprobado.
echo.

echo ==========================================================
echo [EXITO FINAL] PIPELINE COMPLETADO SATISFACTORIAMENTE      
echo ==========================================================
