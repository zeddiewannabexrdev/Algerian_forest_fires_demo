@echo off
title He Thong Giam Sat Va Canh Bao Chay Rung Algeria
echo ========================================================
echo   DANG KHOI DONG TRUNG TAM GIAM SAT CHAY RUNG ALGERIA
echo ========================================================
echo.

:: 1. Kiem tra neu co virtualenv trong thu muc venv
if exist "venv\Scripts\activate.bat" (
    echo [1/2] Tim thay moi truong ao venv, dang kich hoat...
    call venv\Scripts\activate.bat
    echo [2/2] Dang khoi chay Streamlit App...
    streamlit run app.py
    goto end
)

:: 2. Kiem tra neu lenh streamlit co san trong he thong
where streamlit >nul 2>&1
if %errorlevel% equ 0 (
    echo [1/1] Dang khoi chay Streamlit tren he thong...
    streamlit run app.py
    goto end
)

:: 3. Neu khong, su dung duong dan Python 3.10 mac dinh
if exist "C:\Users\ADMIN\AppData\Local\Programs\Python\Python310\python.exe" (
    echo [1/1] Su dung Python 3.10 de khoi chay...
    "C:\Users\ADMIN\AppData\Local\Programs\Python\Python310\python.exe" -m streamlit run app.py
    goto end
)

:: 4. Fallback ve python he thong
echo [1/1] Dang khoi chay bang python he thong...
python -m streamlit run app.py

:end
pause
