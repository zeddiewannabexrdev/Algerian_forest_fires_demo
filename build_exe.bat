@echo off
setlocal enabledelayedexpansion
title Forest Fire Analytics - Windows EXE Builder

echo =====================================================================
echo  BUILD WINDOWS DESKTOP APPLICATION (.EXE)
echo =====================================================================
echo.

:: Detect Python executable
set "PYTHON_EXE="

if exist ".venv\Scripts\python.exe" (
    set "PYTHON_EXE=.venv\Scripts\python.exe"
) else (
    for %%P in (
        "%LOCALAPPDATA%\Programs\Python\Python310\python.exe"
        "%LOCALAPPDATA%\Programs\Python\Python311\python.exe"
        "python.exe"
    ) do (
        if not defined PYTHON_EXE (
            %%~P --version >nul 2>&1
            if !errorlevel! equ 0 set "PYTHON_EXE=%%~P"
        )
    )
)

if not defined PYTHON_EXE (
    echo [ERROR] Python not found on system.
    pause
    exit /b 1
)

echo [*] Using Python: !PYTHON_EXE!
echo.

:: Install build dependencies
echo [*] Checking build dependencies (wheel, setuptools, pyinstaller, pywebview)...
!PYTHON_EXE! -m pip install --quiet wheel setuptools pyinstaller pywebview

:: Ensure any previously running instance is closed
taskkill /F /IM ForestFireWorkstation.exe >nul 2>&1

:: Build application with PyInstaller
echo.
echo [*] Compiling standalone Windows Desktop App...
echo     This may take 1-2 minutes, please wait...
echo.

!PYTHON_EXE! -m PyInstaller --noconfirm ForestFireWorkstation.spec

if %errorlevel% equ 0 (
    echo.
    echo =====================================================================
    echo [SUCCESS] Build completed successfully!
    echo Output directory: dist\ForestFireWorkstation\ForestFireWorkstation.exe
    echo =====================================================================
    echo.
) else (
    echo.
    echo [ERROR] Build failed. Please check output messages above.
)

pause
