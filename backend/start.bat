@echo off
echo ============================================================
echo    Document Compliance Audit System - Backend Server
echo ============================================================
echo.
echo Installing dependencies...
pip install -r requirements.txt
echo.
echo Starting Flask server...
echo Server will run on http://localhost:5000
echo Press Ctrl+C to stop
echo.
python app.py
