@echo off
rem Cambiar al directorio del repositorio sin importar donde se ejecute
cd /d "C:\Users\negro\Desktop\data-startup-plastiktrack"

echo ===================================================
echo     PlastikTrack - Subida a GitHub (E0 y E1)
echo ===================================================
echo Directorio de trabajo: %CD%
echo.

rem Verificar si el remoto 'origin' existe
git remote get-url origin >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [AVISO] No se detecto el repositorio remoto 'origin'.
    set /p REPO_URL="Ingresa la URL del repositorio remoto de GitHub: "
    git remote add origin %REPO_URL%
    echo Remoto 'origin' configurado como: %REPO_URL%
)

echo Subiendo ramas y etiquetas a GitHub...
git push -u origin main
git push origin --tags --force

echo.
echo ===================================================
echo Proceso terminado exitosamente.
echo ===================================================
pause
