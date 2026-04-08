@echo off
:: ============================================================
::  Universal Python to EXE Build Script
::  -------------------------------------------------------
::  Drop this file in any Python project folder.
::  It will:
::    1. Auto-detect the project name from the folder name
::    2. Find the .spec file automatically (or let you pick)
::    3. Build a standalone .exe with PyInstaller
::    4. Assemble a release folder and zip it
::
::  Requirements: pip install -r requirements-dev.txt
::                (must contain pyinstaller>=6.0.0)
::
::  Customise only the OPTIONS section below if needed.
:: ============================================================

setlocal enabledelayedexpansion

:: ── OPTIONS (edit these if needed) ──────────────────────────
set VERSION=1.0
set EXTRA_FILES=config.default.json README.md
set CONSOLE=false
:: ────────────────────────────────────────────────────────────

:: Auto-detect project name from current folder
for %%I in ("%cd%") do set APP_NAME=%%~nxI
set APP_NAME=%APP_NAME: =_%

set DIST_DIR=dist
set RELEASE_DIR=%DIST_DIR%\release
set ZIP_NAME=%APP_NAME%-v%VERSION%-win64.zip

echo.
echo  ============================================
echo   %APP_NAME%  ^|  Universal Build Script
echo  ============================================
echo.
echo   Project  : %APP_NAME%
echo   Version  : %VERSION%
echo   Output   : %DIST_DIR%\%ZIP_NAME%
echo.

:: ── 1. Check Python ─────────────────────────────────────────
where python >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found. Install Python 3.8+ and add it to PATH.
    pause & exit /b 1
)
for /f "tokens=*" %%i in ('python --version') do echo  Python  : %%i

:: ── 2. Install dev dependencies ─────────────────────────────
echo.
echo  Installing build dependencies...
if exist requirements-dev.txt (
    pip install -r requirements-dev.txt --quiet
) else if exist requirements.txt (
    echo  [INFO] requirements-dev.txt not found, using requirements.txt
    pip install -r requirements.txt --quiet
    pip install pyinstaller --quiet
) else (
    echo  [INFO] No requirements file found, installing pyinstaller only
    pip install pyinstaller --quiet
)
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies.
    pause & exit /b 1
)

:: ── 3. Locate .spec file ─────────────────────────────────────
echo.
set SPEC_FILE=
if exist "%APP_NAME%.spec" (
    set SPEC_FILE=%APP_NAME%.spec
    goto :spec_found
)
for %%f in (*.spec) do (
    if not defined SPEC_FILE set SPEC_FILE=%%f
)
:spec_found
if defined SPEC_FILE (
    echo  Spec file : %SPEC_FILE%
) else (
    echo  [INFO] No .spec file found, PyInstaller will auto-generate one.
    set USE_AUTO_SPEC=1
)

:: ── 4. Find entry point if no spec ───────────────────────────
if defined USE_AUTO_SPEC (
    set ENTRY_POINT=
    if exist "%APP_NAME%.py"       set ENTRY_POINT=%APP_NAME%.py
    if not defined ENTRY_POINT if exist "main.py"  set ENTRY_POINT=main.py
    if not defined ENTRY_POINT if exist "app.py"   set ENTRY_POINT=app.py
    if not defined ENTRY_POINT (
        echo [ERROR] No entry point found.
        echo         Name your main script %APP_NAME%.py, main.py, or app.py
        pause & exit /b 1
    )
    echo  Entry     : %ENTRY_POINT%
)

:: ── 5. Clean previous build ──────────────────────────────────
echo.
echo  Cleaning previous build...
if exist build              rmdir /s /q build
if exist %RELEASE_DIR%      rmdir /s /q %RELEASE_DIR%
if exist "%DIST_DIR%\%APP_NAME%.exe"  del /q "%DIST_DIR%\%APP_NAME%.exe"

:: ── 6. Run PyInstaller ───────────────────────────────────────
echo.
echo  Building executable...
if defined SPEC_FILE (
    pyinstaller "%SPEC_FILE%" --noconfirm
) else (
    if "%CONSOLE%"=="true" (
        pyinstaller "%ENTRY_POINT%" --onefile --name "%APP_NAME%" --noconfirm
    ) else (
        pyinstaller "%ENTRY_POINT%" --onefile --name "%APP_NAME%" --windowed --noconfirm
    )
)
if errorlevel 1 (
    echo [ERROR] PyInstaller build failed.
    pause & exit /b 1
)

:: ── 7. Assemble release folder ───────────────────────────────
echo.
echo  Assembling release package...
mkdir %RELEASE_DIR%

:: Auto-find the .exe in dist\ regardless of case or spec name
set FOUND_EXE=
for %%f in ("%DIST_DIR%\*.exe") do set FOUND_EXE=%%f

if not defined FOUND_EXE (
    echo [ERROR] No .exe found in %DIST_DIR%\ - check PyInstaller output above.
    pause ^& exit /b 1
)
echo  Found exe : %FOUND_EXE%
copy /y "%FOUND_EXE%" "%RELEASE_DIR%" >nul
for %%f in (%EXTRA_FILES%) do (
    if exist "%%f" (
        copy /y "%%f" "%RELEASE_DIR%\%%f" >nul
        echo  Bundled  : %%f
    )
)

:: ── 8. Create ZIP ─────────────────────────────────────────────
echo.
echo  Creating zip archive...
if exist "%DIST_DIR%\%ZIP_NAME%" del /q "%DIST_DIR%\%ZIP_NAME%"
powershell -NoProfile -Command "Compress-Archive -Path '%RELEASE_DIR%\*' -DestinationPath '%DIST_DIR%\%ZIP_NAME%' -Force"
if errorlevel 1 (
    echo [WARNING] Zip failed. Release folder ready at: %RELEASE_DIR%
) else (
    echo.
    echo  ============================================
    echo   SUCCESS^^!
    echo   %DIST_DIR%\%ZIP_NAME%
    echo  ============================================
)

echo.
pause
