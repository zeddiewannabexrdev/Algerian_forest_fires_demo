@echo off
title Cai Dat Thu Vien Du An Chay Rung Algeria
echo ========================================================
echo   DANG CAI DAT MOI TRUONG VA THU VIEN TU REQUIREMENTS.TXT
echo ========================================================
echo.

:: Kiem tra Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [LOI] Khong tim thay Python trong he thong! Vui long cai dat Python 3.10 tro len.
    pause
    exit /b 1
)

:: 1. Tao moi truong ao venv neu chua co
if not exist "venv" (
    echo [1/3] Dang tao moi truong ao venv...
    python -m venv venv
) else (
    echo [1/3] Moi truong ao venv da ton tai.
)

:: 2. Kich hoat moi truong ao
echo [2/3] Dang kich hoat moi truong ao venv...
call venv\Scripts\activate.bat

:: 3. Cai dat cac thu vien tu requirements.txt
echo [3/3] Dang cai dat cac thu vien tu requirements.txt...
python -m pip install --upgrade pip
pip install -r requirements.txt

echo.
echo ========================================================
echo   CAI DAT HOAN TAT! Ban co the chay run_app.bat ngay bay gio.
echo ========================================================
pause
