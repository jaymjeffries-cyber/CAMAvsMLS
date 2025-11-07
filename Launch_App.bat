@echo off
title MLS vs CAMA Comparison Tool
echo ========================================
echo MLS vs CAMA Comparison Tool
echo ========================================
echo.
echo Starting application...
echo.
echo The app will open in your default web browser.
echo Press Ctrl+C to stop the application.
echo.
cd /d "%~dp0"
streamlit run mls_cama_app.py
pause
