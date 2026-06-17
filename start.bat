@echo off
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo Tworzenie srodowiska wirtualnego...
    python -m venv .venv
    .venv\Scripts\python.exe -m pip install -r requirements.txt
)

echo Stosowanie migracji...
.venv\Scripts\python.exe manage.py migrate

if not exist "db.sqlite3" (
    echo Ladowanie danych testowych...
    .venv\Scripts\python.exe manage.py loaddata manage_books/fixtures/mock_data.json
)

echo.
echo Uruchamianie serwera: http://127.0.0.1:8000/
echo Zamknij to okno, aby zatrzymac serwer.
echo.
.venv\Scripts\python.exe manage.py runserver 127.0.0.1:8000
