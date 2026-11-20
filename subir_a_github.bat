@echo off
rem Cambiar al directorio del repositorio sin importar donde se ejecute
cd /d "C:\Users\negro\Desktop\data-startup-plastiktrack"

echo ===================================================
echo   PlastikTrack - Subida a GitHub (E0, E1, E2 y E3)
echo ===================================================
echo Directorio de trabajo: %CD%
echo.

echo 1. Subiendo rama main a GitHub...
git push -u origin main

echo.
echo 2. Subiendo etiquetas oficiales (e0, e1, e2, e3) a GitHub...
git push origin --tags --force

echo.
echo ===================================================
echo   Subida completada con exito a GitHub.
echo ===================================================
pause
