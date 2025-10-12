@echo off
echo ========================================
echo LLVM Obfuscator Web UI Launcher
echo ========================================
echo.

REM Check if streamlit is installed
python -c "import streamlit" 2>nul
if errorlevel 1 (
    echo Installing required dependencies...
    pip install -r requirements_ui.txt
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
    echo Dependencies installed successfully!
    echo.
)

echo Starting LLVM Obfuscator Web UI...
echo.
echo The web interface will open in your browser at:
echo http://localhost:8501
echo.
echo Press Ctrl+C to stop the server
echo.

streamlit run obfuscator_ui.py --server.port 8501 --server.headless false

pause