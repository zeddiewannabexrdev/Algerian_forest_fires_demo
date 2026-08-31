@echo off
title Forest Fire Analytics Workstation
echo =====================================================================
echo  STARTING FOREST FIRE ANALYTICS WORKSTATION
echo =====================================================================
echo.
echo [*] Initializing Machine Learning models and analytics workspace...
echo [*] The workstation window will appear momentarily.
echo.

if exist "dist\ForestFireWorkstation\ForestFireWorkstation.exe" (
    start "" "dist\ForestFireWorkstation\ForestFireWorkstation.exe"
) else (
    echo [ERROR] ForestFireWorkstation.exe not found.
    echo Please run build_exe.bat first to compile the application.
    pause
)
