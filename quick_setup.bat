@echo off
REM Quick Setup Script for LLVM Obfuscator
REM This script handles prerequisites and provides guidance

echo ========================================
echo LLVM Obfuscator Quick Setup
echo ========================================
echo.

echo [STEP 1] Checking prerequisites...

REM Check for Visual Studio Build Tools
where cl >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Visual Studio Build Tools not found
    echo Please install from: https://visualstudio.microsoft.com/downloads/
    echo Or run: winget install Microsoft.VisualStudio.2022.BuildTools
    echo.
) else (
    echo [OK] Visual Studio Build Tools found
)

REM Check for CMake
where cmake >nul 2>&1
if errorlevel 1 (
    echo [WARNING] CMake not found
    echo Please install from: https://cmake.org/download/
    echo Or run: winget install Kitware.CMake
    echo.
) else (
    echo [OK] CMake found
)

REM Check for Git
where git >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Git not found
    echo Please install from: https://git-scm.com/downloads/
    echo Or run: winget install Git.Git
    echo.
) else (
    echo [OK] Git found
)

echo.
echo [STEP 2] Installation Options
echo ========================================
echo.
echo Choose your setup method:
echo.
echo [A] Automated Setup (Recommended)
echo     - Downloads and builds LLVM 16 + OLLVM
echo     - Takes 30-60 minutes
echo     - Requires 5GB disk space
echo.
echo [B] Manual Setup Guide
echo     - Step-by-step instructions
echo     - More control over process
echo     - Requires technical knowledge
echo.
echo [C] Skip LLVM Setup (Demo Mode)
echo     - Use existing LLVM installation
echo     - Test framework without full backend
echo     - Good for development and testing
echo.

set /p choice="Enter your choice (A/B/C): "

if /i "%choice%"=="A" goto automated_setup
if /i "%choice%"=="B" goto manual_guide
if /i "%choice%"=="C" goto demo_mode
goto invalid_choice

:automated_setup
echo.
echo [AUTOMATED] Starting LLVM 16 + OLLVM setup...
echo This will take 30-60 minutes depending on your system.
echo.
pause
call setup_llvm16_ollvm.bat
goto end

:manual_guide
echo.
echo [MANUAL] Opening detailed setup guide...
echo.
echo For manual setup, follow these steps:
echo 1. Install prerequisites (Visual Studio, CMake, Git)
echo 2. Clone LLVM project: git clone https://github.com/llvm/llvm-project.git
echo 3. Download OLLVM patches: git clone https://github.com/heroims/obfuscator-llvm.git
echo 4. Apply patches to LLVM source
echo 5. Configure with CMake
echo 6. Build with Visual Studio
echo.
echo See COMPLETION_GUIDE.md for detailed instructions.
echo.
goto end

:demo_mode
echo.
echo [DEMO] Setting up demo mode...
echo.
echo This will set up the framework for testing without full LLVM backend.
echo You can still test all features except actual obfuscation.
echo.

REM Create demo configuration
echo Creating demo configuration...
copy ollvm_config.json demo_config.json >nul

REM Test the framework
echo Testing framework components...
python obf_wrapper.py --list-passes
echo.
python demo.py
echo.
echo Demo mode setup complete!
echo You can now test the framework and implement passes.
echo.
goto end

:invalid_choice
echo.
echo Invalid choice. Please run the script again.
echo.
goto end

:end
echo.
echo ========================================
echo Setup process completed!
echo ========================================
echo.
echo Next steps:
echo 1. Test the obfuscator: python obf_wrapper.py --list-passes
echo 2. Run demo: python demo.py
echo 3. Implement passes: See COMPLETION_GUIDE.md
echo.
pause
