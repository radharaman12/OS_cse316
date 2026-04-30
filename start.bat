@echo off
title KIDS.AI - Enterprise Threat Detection
color 0B

echo ========================================================
echo     KIDS.AI - Kernel Intrusion Detection System
echo     Enterprise Edition 
echo ========================================================
echo.

echo [1/2] Checking and installing required dependencies...
pip install -r requirements.txt
echo.

echo [2/2] Booting up the Enterprise Dashboard...
echo.
echo The application will automatically open in your default web browser.
echo (If it doesn't, navigate to http://localhost:8501)
echo.
echo --------------------------------------------------------
echo To stop the server, press CTRL+C in this window.
echo --------------------------------------------------------
echo.

streamlit run app.py

pause
