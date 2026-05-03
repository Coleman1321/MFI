@echo off
REM ──────────────────────────────────────────────────────────────────────────
REM  MFB Collection Tracker – Windows build script
REM  Requirements: Python 3.10+  (tkinter included in standard Windows installer)
REM  Usage: double-click build.bat  OR  run it in a Command Prompt
REM ──────────────────────────────────────────────────────────────────────────

setlocal

set PROJECT_DIR=%~dp0
set DIST_DIR=%PROJECT_DIR%dist
set VENV_DIR=%PROJECT_DIR%.venv

echo.
echo [1/4] Creating virtual environment...
python -m venv "%VENV_DIR%"
if errorlevel 1 (
    echo ERROR: Could not create venv. Make sure Python 3.10+ is installed.
    pause & exit /b 1
)

echo.
echo [2/4] Installing dependencies...
call "%VENV_DIR%\Scripts\activate.bat"
pip install --quiet --upgrade pip
pip install --quiet pyinstaller
if errorlevel 1 (
    echo ERROR: pip install failed.
    pause & exit /b 1
)

echo.
echo [3/4] Running PyInstaller...
cd /d "%PROJECT_DIR%"
pyinstaller beyblade_tracker.spec --noconfirm
if errorlevel 1 (
    echo ERROR: PyInstaller failed.
    pause & exit /b 1
)

echo.
echo [4/4] Done!
echo Output: %DIST_DIR%\MFB_Tracker\MFB_Tracker.exe
echo.
echo The "MFB_Tracker" folder in dist\ is self-contained.
echo Copy the whole folder anywhere and run MFB_Tracker.exe.
echo.

pause
