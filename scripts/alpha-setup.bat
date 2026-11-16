@echo off
REM ##############################################################################
REM Alpha Tester One-Line Setup for Piper Morgan (Windows)
REM
REM Usage:
REM   .\scripts\alpha-setup.bat
REM
REM Or from any location (first time):
REM   cd\
REM   git clone -b production https://github.com/mediajunkie/piper-morgan-product.git
REM   cd piper-morgan-product
REM   .\scripts\alpha-setup.bat
REM
REM This script automates the setup process for alpha testers:
REM 1. Verifies Python 3.11/3.12
REM 2. Creates Python virtual environment
REM 3. Installs dependencies
REM 4. Generates JWT secret key
REM 5. Creates .env file
REM 6. Starts Docker containers
REM 7. Launches the GUI setup wizard
REM
REM Requirements:
REM  - Python 3.11 or 3.12 (from python.org)
REM  - Git (from git-scm.com)
REM  - Docker Desktop (from docker.com)
REM  - Windows 10/11 or WSL2 on Windows
REM ##############################################################################

setlocal enabledelayedexpansion

REM Color codes for output
REM Note: Windows batch doesn't support ANSI colors natively in cmd.exe
REM For colored output, users need Windows 10 21H2+ or Windows Terminal
set "BLUE=[0;34m"
set "GREEN=[0;32m"
set "RED=[0;31m"
set "YELLOW=[1;33m"
set "NC=[0m"

REM Check if running in Windows Terminal (supports ANSI colors)
set "SUPPORTS_COLOR=0"
for /f "tokens=*" %%A in ('reg query "HKCU\Console" /v VirtualTerminalLevel 2^>nul') do (
    set "SUPPORTS_COLOR=1"
)

REM ============================================================================
REM Main script starts here
REM ============================================================================
cls
echo.
echo ╔════════════════════════════════════════════════════════╗
echo ║     Piper Morgan Alpha Tester Setup Script             ║
echo ║              Windows Edition                           ║
echo ╚════════════════════════════════════════════════════════╝
echo.

REM Check for required tools
call :check_requirements
if errorlevel 1 goto :error_exit

REM Create Python virtual environment
call :setup_venv
if errorlevel 1 goto :error_exit

REM Install dependencies
call :install_deps
if errorlevel 1 goto :error_exit

REM Setup environment configuration
call :setup_env
if errorlevel 1 goto :error_exit

REM Start Docker containers
call :start_docker
if errorlevel 1 goto :error_exit

REM Start the application
call :start_app

goto :eof

:error_exit
echo.
echo [ERROR] Setup failed. Please fix the issues above and try again.
exit /b 1

REM ============================================================================
REM Helper functions for output
REM ============================================================================

:print_step
    if "%SUPPORTS_COLOR%"=="1" (
        echo %BLUE%→%NC% %~1
    ) else (
        echo [STEP] %~1
    )
    goto :eof

:print_success
    if "%SUPPORTS_COLOR%"=="1" (
        echo %GREEN%✓%NC% %~1
    ) else (
        echo [OK] %~1
    )
    goto :eof

:print_error
    if "%SUPPORTS_COLOR%"=="1" (
        echo %RED%✗%NC% %~1
    ) else (
        echo [ERROR] %~1
    )
    goto :eof

:print_warning
    if "%SUPPORTS_COLOR%"=="1" (
        echo %YELLOW%⚠%NC% %~1
    ) else (
        echo [WARN] %~1
    )
    goto :eof

REM ============================================================================
REM Main subroutines
REM ============================================================================

:check_requirements
    echo.
    call :print_step "Checking requirements..."
    echo.

    REM Check Python
    python --version >nul 2>&1
    if errorlevel 1 (
        call :print_error "Python 3.11+ not found"
        echo    Install from: https://www.python.org/downloads/
        echo    Make sure to check 'Add Python to PATH' during installation
        exit /b 1
    )

    REM Get Python version
    for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i

    REM Check if version is 3.11 or 3.12
    for /f "tokens=1,2 delims=." %%a in ("%PYTHON_VERSION%") do (
        if "%%a"=="3" (
            if "%%b"=="11" (
                call :print_success "Python !PYTHON_VERSION! found"
            ) else if "%%b"=="12" (
                call :print_success "Python !PYTHON_VERSION! found"
            ) else (
                call :print_error "Python !PYTHON_VERSION! found, but 3.11 or 3.12 required"
                exit /b 1
            )
        ) else (
            call :print_error "Python !PYTHON_VERSION! found, but 3.11 or 3.12 required"
            exit /b 1
        )
    )

    REM Check Git
    git --version >nul 2>&1
    if errorlevel 1 (
        call :print_error "Git not found"
        echo    Install from: https://git-scm.com/downloads
        exit /b 1
    )
    call :print_success "Git found"

    REM Check Docker
    docker --version >nul 2>&1
    if errorlevel 1 (
        call :print_error "Docker not found"
        echo    Install Docker Desktop from: https://www.docker.com/products/docker-desktop
        echo    Make sure Docker Desktop is running
        exit /b 1
    )
    call :print_success "Docker found"

    goto :eof

:setup_venv
    echo.

    REM Check if venv already exists
    if exist venv (
        call :print_success "Virtual environment already exists"
    ) else (
        call :print_step "Creating Python virtual environment..."
        python -m venv venv
        if errorlevel 1 (
            call :print_error "Failed to create virtual environment"
            exit /b 1
        )
        call :print_success "Virtual environment created"
    )

    REM Activate virtual environment
    call :print_step "Activating virtual environment..."
    call venv\Scripts\activate.bat
    if errorlevel 1 (
        call :print_error "Failed to activate virtual environment"
        exit /b 1
    )
    call :print_success "Virtual environment activated"

    goto :eof

:install_deps
    echo.

    REM Check if requirements.txt exists
    if not exist requirements.txt (
        call :print_error "requirements.txt not found"
        exit /b 1
    )

    call :print_step "Installing Python dependencies (this may take several minutes)..."
    REM Upgrade pip first (silent)
    python -m pip install --quiet --upgrade pip setuptools >nul 2>&1

    REM Install requirements
    pip install --quiet -r requirements.txt
    if errorlevel 1 (
        call :print_error "Failed to install dependencies"
        exit /b 1
    )
    call :print_success "Dependencies installed"

    goto :eof

:setup_env
    echo.

    REM Check if .env already exists
    if exist .env (
        call :print_success ".env already exists"
    ) else (
        call :print_step "Setting up environment configuration..."

        REM Copy .env.example if it exists
        if exist .env.example (
            copy .env.example .env >nul
            call :print_success ".env created from template"
        ) else (
            REM Create minimal .env
            type nul > .env
            call :print_success ".env created"
        )

        REM Check if JWT_SECRET_KEY already exists in .env
        findstr /M "JWT_SECRET_KEY" .env >nul 2>&1
        if errorlevel 1 (
            call :print_step "Generating secure JWT secret key..."

            REM Generate 32 random hex bytes using powershell (more reliable on Windows)
            for /f "delims=" %%A in ('powershell -Command "[BitConverter]::ToString((1..32 | ForEach-Object { Get-Random -Maximum 256 })) -replace '-','' -replace ' ','' | ForEach-Object { $_.ToLower() }"') do (
                set JWT_SECRET=%%A
            )

            REM If powershell fails, use a fallback
            if "!JWT_SECRET!"=="" (
                REM Fallback: use timestamp-based approach (less secure but works on all Windows)
                for /f %%A in ('powershell -Command "Get-Date -Format 'yyyyMMddHHmmssfff'"') do (
                    set JWT_SECRET=%%A%%RANDOM%%%%RANDOM%%%%RANDOM%%%%RANDOM%%%%RANDOM%%%%RANDOM%%%%RANDOM%%%%RANDOM%%
                )
            )

            echo JWT_SECRET_KEY=!JWT_SECRET! >> .env
            call :print_success "JWT secret added to .env"
        )
    )

    goto :eof

:start_docker
    echo.
    call :print_step "Starting Docker containers..."

    REM Check if Docker daemon is running
    docker ps >nul 2>&1
    if errorlevel 1 (
        call :print_error "Docker daemon not running"
        echo    Start Docker Desktop and try again
        exit /b 1
    )

    if exist docker-compose.yml (
        rem Issue 2386: the three data services by name. A second copy on this machine
        rem sets PIPER_STACK and its ports in .env first (see docker-compose.yml).
        docker compose up -d postgres redis chromadb
        if errorlevel 1 (
            call :print_error "Failed to start Docker containers"
            exit /b 1
        )
        call :print_success "Docker containers started"

        call :print_warning "Waiting 5 seconds for services to initialize..."
        timeout /t 5 /nobreak >nul
    ) else (
        call :print_warning "docker-compose.yml not found, skipping Docker startup"
    )

    goto :eof

:start_app
    echo.
    call :print_step "Launching Piper Morgan GUI setup wizard..."
    echo.
    echo ═══════════════════════════════════════════════════════
    echo   Piper Morgan is starting...
    echo ═══════════════════════════════════════════════════════
    echo.
    echo The setup wizard will open in your browser automatically.
    echo If it doesn't, visit: http://127.0.0.1:8001/setup
    echo.
    call :print_step "Starting server (press Ctrl+C to stop)..."
    echo.

    python main.py

    goto :eof
