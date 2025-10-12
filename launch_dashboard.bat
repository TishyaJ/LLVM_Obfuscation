@echo off
echo LLVM Code Obfuscator - Production Dashboard
echo ==================================================
echo Starting dashboard...
echo URL: http://localhost:8501
echo Press Ctrl+C to stop
echo --------------------------------------------------
echo.

python -m streamlit run production_dashboard.py --server.port 8501 --server.headless false

pause