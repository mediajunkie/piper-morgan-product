@echo off
REM ##############################################################################
REM Windows Smoke Test for Piper Morgan
REM
REM Usage:
REM   .\scripts\windows-smoke-test.bat
REM
REM This script verifies the Windows setup is working correctly.
REM Run after alpha-setup.bat or manual setup to validate installation.
REM
REM Exit codes:
REM   0 - All tests passed
REM   1 - One or more tests failed
REM ##############################################################################

setlocal enabledelayedexpansion

set "PASSED=0"
set "FAILED=0"
set "WARNINGS=0"

REM ============================================================================
REM Main script
REM ============================================================================
cls
echo.
echo ============================================================
echo   Piper Morgan Windows Smoke Test
echo ============================================================
echo.

REM Test 1: Python version
call :test_python_version

REM Test 2: Virtual environment
call :test_venv

REM Test 3: Core imports
call :test_imports

REM Test 4: uvloop not installed
call :test_uvloop_skipped

REM Test 5: main.py runs
call :test_main_py

REM Test 6: .env file exists
call :test_env_file

REM Test 7: Docker available (optional)
call :test_docker

REM Test 8: validate_install.py runs
call :test_validator

REM Summary
echo.
echo ============================================================
echo   RESULTS
echo ============================================================
echo.
echo   Passed:   %PASSED%
echo   Failed:   %FAILED%
echo   Warnings: %WARNINGS%
echo.

if %FAILED% gtr 0 (
    echo [FAIL] Some tests failed. Please fix the issues above.
    exit /b 1
) else (
    echo [PASS] All critical tests passed!
    if %WARNINGS% gtr 0 (
        echo        Some optional tests had warnings.
    )
    exit /b 0
)

goto :eof

REM ============================================================================
REM Test functions
REM ============================================================================

:test_python_version
    echo [TEST] Python version...
    python --version >nul 2>&1
    if errorlevel 1 (
        echo        [FAIL] Python not found
        set /a FAILED+=1
        goto :eof
    )
    for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYVER=%%i
    for /f "tokens=1,2 delims=." %%a in ("%PYVER%") do (
        if "%%a"=="3" (
            if "%%b" geq "11" (
                echo        [PASS] Python %PYVER%
                set /a PASSED+=1
                goto :eof
            )
        )
    )
    echo        [FAIL] Python %PYVER% - need 3.11+
    set /a FAILED+=1
    goto :eof

:test_venv
    echo [TEST] Virtual environment...
    if defined VIRTUAL_ENV (
        echo        [PASS] venv active: %VIRTUAL_ENV%
        set /a PASSED+=1
    ) else (
        echo        [WARN] venv not active - run: venv\Scripts\activate.bat
        set /a WARNINGS+=1
    )
    goto :eof

:test_imports
    echo [TEST] Core Python imports...
    python -c "from services.shared_types import IntentCategory" 2>nul
    if errorlevel 1 (
        echo        [FAIL] Cannot import services.shared_types
        set /a FAILED+=1
        goto :eof
    )
    python -c "from services.domain.models import User" 2>nul
    if errorlevel 1 (
        echo        [FAIL] Cannot import services.domain.models
        set /a FAILED+=1
        goto :eof
    )
    python -c "from config.settings import Settings" 2>nul
    if errorlevel 1 (
        echo        [FAIL] Cannot import config.settings
        set /a FAILED+=1
        goto :eof
    )
    echo        [PASS] Core imports working
    set /a PASSED+=1
    goto :eof

:test_uvloop_skipped
    echo [TEST] uvloop correctly skipped...
    python -c "import uvloop" 2>nul
    if errorlevel 1 (
        echo        [PASS] uvloop not installed (correct for Windows)
        set /a PASSED+=1
    ) else (
        echo        [FAIL] uvloop is installed - should be skipped on Windows
        set /a FAILED+=1
    )
    goto :eof

:test_main_py
    echo [TEST] main.py --help...
    python main.py --help >nul 2>&1
    if errorlevel 1 (
        echo        [FAIL] main.py --help failed
        set /a FAILED+=1
    ) else (
        echo        [PASS] main.py executable
        set /a PASSED+=1
    )
    goto :eof

:test_env_file
    echo [TEST] .env file...
    if exist .env (
        findstr /M "JWT_SECRET_KEY" .env >nul 2>&1
        if errorlevel 1 (
            echo        [WARN] .env exists but missing JWT_SECRET_KEY
            set /a WARNINGS+=1
        ) else (
            echo        [PASS] .env file configured
            set /a PASSED+=1
        )
    ) else (
        echo        [FAIL] .env file not found - run: copy .env.example .env
        set /a FAILED+=1
    )
    goto :eof

:test_docker
    echo [TEST] Docker (optional)...
    docker --version >nul 2>&1
    if errorlevel 1 (
        echo        [WARN] Docker not found - some features unavailable
        set /a WARNINGS+=1
        goto :eof
    )
    docker ps >nul 2>&1
    if errorlevel 1 (
        echo        [WARN] Docker not running - start Docker Desktop
        set /a WARNINGS+=1
    ) else (
        docker ps --format "{{.Names}}" | findstr /C:"piper-postgres" >nul 2>&1
        if errorlevel 1 (
            echo        [WARN] piper-postgres not running - run: docker compose up -d postgres redis chromadb
            set /a WARNINGS+=1
        ) else (
            echo        [PASS] Docker and piper-postgres running
            set /a PASSED+=1
        )
    )
    goto :eof

:test_validator
    echo [TEST] validate_install.py...
    if exist scripts\validate_install.py (
        python scripts\validate_install.py >nul 2>&1
        if errorlevel 1 (
            echo        [WARN] validate_install.py reported issues
            set /a WARNINGS+=1
        ) else (
            echo        [PASS] validate_install.py passed
            set /a PASSED+=1
        )
    ) else (
        echo        [WARN] validate_install.py not found
        set /a WARNINGS+=1
    )
    goto :eof
