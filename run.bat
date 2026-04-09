@echo off
echo ===========================================
echo [1/2] Ejecutando el detector (main.py)...
echo ===========================================
python main.py

echo.
echo ===========================================
echo [2/2] Evaluando los resultados...
echo ===========================================
python evaluar_resultados.py --test_path test_detection

echo.
echo Proceso terminado.
pause