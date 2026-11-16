#!/usr/bin/env python3
"""
Validate Piper Morgan Installation

A smoke test script to verify all components are working after setup.
Run this after completing the setup wizard to confirm everything is configured correctly.

Usage:
    python scripts/validate_install.py

Exit codes:
    0 - All checks passed
    1 - One or more checks failed
"""

import os
import subprocess
import sys
from pathlib import Path


class Colors:
    """ANSI color codes for terminal output."""

    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    RESET = "\033[0m"
    BOLD = "\033[1m"


def check_mark():
    return f"{Colors.GREEN}✓{Colors.RESET}"


def x_mark():
    return f"{Colors.RED}✗{Colors.RESET}"


def warning_mark():
    return f"{Colors.YELLOW}⚠{Colors.RESET}"


def print_header():
    print(f"\n{Colors.BOLD}Piper Morgan Installation Validator{Colors.RESET}")
    print("=" * 40)
    print()


def check_docker_running():
    """Check if Docker daemon is running."""
    try:
        result = subprocess.run(["docker", "info"], capture_output=True, text=True, timeout=10)
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


def check_docker_containers():
    """Check if required Docker containers are running."""
    required_containers = ["piper-postgres"]
    optional_containers = ["piper-redis", "piper-chromadb"]

    try:
        result = subprocess.run(
            ["docker", "ps", "--format", "{{.Names}}"], capture_output=True, text=True, timeout=10
        )
        running = result.stdout.strip().split("\n") if result.stdout.strip() else []

        # Check required
        missing_required = [c for c in required_containers if c not in running]

        # Check optional
        running_optional = [c for c in optional_containers if c in running]

        return {
            "success": len(missing_required) == 0,
            "running": [c for c in required_containers if c in running] + running_optional,
            "missing_required": missing_required,
            "total_running": len(running),
        }
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return {
            "success": False,
            "running": [],
            "missing_required": required_containers,
            "total_running": 0,
        }


def check_database_connection():
    """Check if we can connect to PostgreSQL."""
    try:
        result = subprocess.run(
            ["docker", "exec", "piper-postgres", "pg_isready", "-U", "piper"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.SubprocessError):
        return False


def check_env_file():
    """Check if .env file exists and has required variables."""
    env_path = Path(".env")
    if not env_path.exists():
        return {"exists": False, "missing": ["JWT_SECRET_KEY"], "warnings": []}

    with open(env_path) as f:
        content = f.read()

    required = ["JWT_SECRET_KEY"]
    recommended = ["OPENAI_API_KEY", "ANTHROPIC_API_KEY"]

    missing = []
    warnings = []

    for var in required:
        if var not in content or f"{var}=" not in content:
            missing.append(var)
        elif f"{var}=\n" in content or f"{var}= \n" in content:
            missing.append(f"{var} (empty)")

    # Check for at least one LLM key
    has_llm_key = any(key in content and f"{key}=" in content for key in recommended)
    if not has_llm_key:
        warnings.append("No LLM API key found (OPENAI_API_KEY or ANTHROPIC_API_KEY)")

    return {"exists": True, "missing": missing, "warnings": warnings}


def check_venv_active():
    """Check if running inside a virtual environment."""
    return sys.prefix != sys.base_prefix


def check_python_version():
    """Check Python version is 3.11+."""
    version = sys.version_info
    return version.major == 3 and version.minor >= 11


def check_api_health():
    """Check if the API server responds at /health."""
    try:
        import urllib.error
        import urllib.request

        req = urllib.request.Request("http://127.0.0.1:8001/health", method="GET")
        with urllib.request.urlopen(req, timeout=5) as response:
            return response.status == 200
    except Exception:
        return None  # Server not running (not necessarily an error)


def check_database_tables():
    """Check if database has been migrated (has users table)."""
    try:
        result = subprocess.run(
            [
                "docker",
                "exec",
                "piper-postgres",
                "psql",
                "-U",
                "piper",
                "-d",
                "piper_morgan",
                "-c",
                "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public';",
            ],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode == 0:
            # Parse the count from output
            lines = result.stdout.strip().split("\n")
            for line in lines:
                line = line.strip()
                if line.isdigit():
                    count = int(line)
                    return count > 10  # Should have many tables after migration
        return False
    except Exception:
        return False


def main():
    print_header()

    all_passed = True
    warnings = []

    # 1. Python version
    if check_python_version():
        print(f"{check_mark()} Python version: {sys.version_info.major}.{sys.version_info.minor}")
    else:
        print(
            f"{x_mark()} Python version: {sys.version_info.major}.{sys.version_info.minor} (need 3.11+)"
        )
        all_passed = False

    # 2. Virtual environment
    if check_venv_active():
        print(f"{check_mark()} Virtual environment: active")
    else:
        print(f"{warning_mark()} Virtual environment: not active (recommended)")
        warnings.append("Consider activating venv: source venv/bin/activate")

    # 3. Environment file
    env_check = check_env_file()
    if env_check["exists"] and not env_check["missing"]:
        print(f"{check_mark()} Environment file: .env exists with required vars")
    elif not env_check["exists"]:
        print(f"{x_mark()} Environment file: .env not found")
        print(f"   Run: cp .env.example .env && edit .env")
        all_passed = False
    else:
        print(f"{x_mark()} Environment file: missing {', '.join(env_check['missing'])}")
        all_passed = False

    if env_check.get("warnings"):
        for w in env_check["warnings"]:
            print(f"   {warning_mark()} {w}")
            warnings.append(w)

    # 4. Docker running
    docker_running = check_docker_running()
    if docker_running:
        print(f"{check_mark()} Docker: running")
    else:
        print(f"{x_mark()} Docker: not running")
        print(f"   Start Docker Desktop and try again")
        all_passed = False
        # Can't check containers if Docker isn't running
        print(f"{x_mark()} Docker containers: cannot check (Docker not running)")
        print(f"{x_mark()} Database connection: cannot check")
        print(f"{x_mark()} Database migrations: cannot check")

    if docker_running:
        # 5. Docker containers
        containers = check_docker_containers()
        if containers["success"]:
            print(
                f"{check_mark()} Docker containers: {len(containers['running'])} running ({', '.join(containers['running'])})"
            )
        else:
            print(
                f"{x_mark()} Docker containers: missing {', '.join(containers['missing_required'])}"
            )
            print("   Run: docker compose up -d postgres redis chromadb")
            all_passed = False

        # 6. Database connection
        if check_database_connection():
            print(f"{check_mark()} Database connection: PostgreSQL responding")
        else:
            print(f"{x_mark()} Database connection: cannot connect to PostgreSQL")
            print(f"   Check: docker logs piper-postgres")
            all_passed = False

        # 7. Database migrations
        if check_database_tables():
            print(f"{check_mark()} Database migrations: tables exist")
        else:
            print(f"{warning_mark()} Database migrations: may need to run migrations")
            print(f"   Run: python -m alembic upgrade head")
            warnings.append("Run migrations: python -m alembic upgrade head")

    # 8. API health (optional - server may not be running)
    api_status = check_api_health()
    if api_status is True:
        print(f"{check_mark()} API server: responding at http://127.0.0.1:8001")
    elif api_status is False:
        print(f"{x_mark()} API server: not responding (error)")
        all_passed = False
    else:
        print(f"{warning_mark()} API server: not running (start with: python main.py)")
        warnings.append("Start server: python main.py")

    # Summary
    print()
    if all_passed and not warnings:
        print(f"{Colors.GREEN}{Colors.BOLD}✅ Installation validated successfully!{Colors.RESET}")
        print(f"\nNext steps:")
        print(f"  1. Start server: python main.py")
        print(f"  2. Open: http://127.0.0.1:8001/setup")
        return 0
    elif all_passed:
        print(f"{Colors.YELLOW}{Colors.BOLD}⚠️  Installation OK with warnings{Colors.RESET}")
        print(f"\nRecommended actions:")
        for w in warnings:
            print(f"  • {w}")
        return 0
    else:
        print(f"{Colors.RED}{Colors.BOLD}❌ Installation has issues{Colors.RESET}")
        print(f"\nFix the errors above and run this script again.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
