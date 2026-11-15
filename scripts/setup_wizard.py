"""
Setup Wizard for Piper Morgan Alpha Onboarding

Interactive CLI wizard to onboard new users with:
- System requirement checks
- API key collection and validation
- User account creation
- Secure keychain storage

Issue #218 CORE-USERS-ONBOARD Phase 1A
"""

import asyncio
import os
import platform
import socket
import subprocess
import sys
import uuid
from datetime import datetime
from getpass import getpass
from typing import Any, Dict, Optional

# Add parent directory to path for imports
sys.path.insert(0, ".")

# =============================================================================
# Module-level constants (Issue #438: Setup Wizard Code Hygiene)
# =============================================================================

# Service check names (used in check_system and run_setup_wizard)
SERVICE_DOCKER = "Docker installed"
SERVICE_PYTHON = "Python 3.9+"
SERVICE_PORT = "Port 8001 available"
SERVICE_POSTGRES = "PostgreSQL (5433)"
SERVICE_REDIS = "Redis (6379)"
SERVICE_CHROMADB = "ChromaDB (8000)"
SERVICE_TEMPORAL = "Temporal (7233)"

# Core services required for setup (Temporal is optional)
CORE_SERVICES = [SERVICE_POSTGRES, SERVICE_REDIS, SERVICE_CHROMADB]
OPTIONAL_SERVICES = [SERVICE_TEMPORAL]

# API provider names (used in collect_and_validate_api_keys)
PROVIDER_OPENAI = "openai"
PROVIDER_ANTHROPIC = "anthropic"
PROVIDER_GITHUB = "github"
PROVIDER_NOTION = "notion"  # Issue #527: ALPHA-SETUP-NOTION

# =============================================================================

# Check for required dependencies
try:
    import sqlalchemy  # noqa: F401
except ImportError:
    print("\n❌ Error: SQLAlchemy not installed")
    print("\nPlease install dependencies first:")
    print("  pip install -r requirements.txt")
    print("\nOr if using a virtual environment:")
    print("  python3.12 -m venv venv")
    print("  source venv/bin/activate  # On Windows: venv\\Scripts\\activate")
    print("  pip install -r requirements.txt")
    sys.exit(1)


def get_platform() -> str:
    """Detect the current platform"""
    system = platform.system().lower()
    if system == "darwin":
        return "macos"
    elif system == "windows":
        return "windows"
    elif system == "linux":
        return "linux"
    else:
        return "unknown"


def check_python312_available() -> bool:
    """Check if python3.12 is available on the system"""
    try:
        result = subprocess.run(
            ["python3.12", "--version"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


def setup_virtual_environment() -> bool:
    """Set up Python virtual environment with requirements"""
    print("\n" + "=" * 50)
    print("🔧 Setting Up Virtual Environment")
    print("=" * 50)

    # Clean up old venv
    if os.path.exists("venv"):
        print("\n🧹 Removing old virtual environment...")
        try:
            subprocess.run(["rm", "-rf", "venv"], check=True, timeout=10)
            print("   ✓ Old venv removed")
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired, OSError) as e:
            print(f"   ⚠ Could not remove old venv: {e}")
            return False

    # Create new venv with python3.12
    print("\n📦 Creating virtual environment with Python 3.12...")
    try:
        subprocess.run(
            ["python3.12", "-m", "venv", "venv"],
            check=True,
            timeout=60,
        )
        print("   ✓ Virtual environment created")
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError) as e:
        print(f"   ✗ Failed to create venv: {e}")
        return False

    # Upgrade pip
    print("\n📥 Upgrading pip...")
    try:
        subprocess.run(
            ["venv/bin/pip", "install", "--upgrade", "pip"],
            check=True,
            timeout=60,
        )
        print("   ✓ pip upgraded")
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError) as e:
        print(f"   ⚠ pip upgrade had issues: {e}")

    # Install requirements
    print("\n📦 Installing dependencies (this may take 2-3 minutes)...")
    try:
        result = subprocess.run(
            ["venv/bin/pip", "install", "-r", "requirements.txt"],
            capture_output=True,
            text=True,
            timeout=300,
        )
        if result.returncode == 0:
            print("   ✓ All dependencies installed successfully!")
            return True
        else:
            print(f"   ✗ Installation failed:")
            print(result.stderr[-500:] if result.stderr else "Unknown error")
            return False
    except subprocess.TimeoutExpired:
        print("   ✗ Installation timed out (>5 minutes)")
        return False
    except (subprocess.CalledProcessError, FileNotFoundError, OSError) as e:
        print(f"   ✗ Installation failed: {e}")
        return False


def setup_ssh_key() -> bool:
    """Generate SSH key if missing and guide user to add it to GitHub"""
    print("\n" + "=" * 50)
    print("🔐 SSH Key Setup")
    print("=" * 50)

    ssh_dir = os.path.expanduser("~/.ssh")
    key_path = os.path.join(ssh_dir, "id_ed25519")

    # Check if key exists
    if os.path.exists(key_path):
        print("\n✓ SSH key already exists at ~/.ssh/id_ed25519")
        print("✓ Skipping SSH key generation")
        return True

    # Generate new key
    print("\n🔑 Generating new SSH key...")
    try:
        # Create .ssh directory if it doesn't exist
        os.makedirs(ssh_dir, mode=0o700, exist_ok=True)

        subprocess.run(
            [
                "ssh-keygen",
                "-t",
                "ed25519",
                "-f",
                key_path,
                "-N",
                "",
                "-C",
                "piper-morgan-alpha",
            ],
            check=True,
            timeout=10,
        )
        print("   ✓ SSH key generated")

        # Read and copy public key
        pub_key_path = key_path + ".pub"
        with open(pub_key_path, "r") as f:
            pub_key = f.read().strip()

        # Copy to clipboard (platform-specific)
        platform = get_platform()
        try:
            if platform == "macos":
                subprocess.run(
                    ["pbcopy"],
                    input=pub_key.encode(),
                    check=True,
                    timeout=5,
                )
                print("   ✓ Public key copied to clipboard")
            elif platform == "windows":
                subprocess.run(
                    ["clip"],
                    input=pub_key.encode(),
                    check=True,
                    timeout=5,
                )
                print("   ✓ Public key copied to clipboard")
            # Linux: no auto-copy, just display
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError) as e:
            print(f"   ⚠ Could not copy to clipboard: {e}")

        # Display instructions
        print("\n" + "-" * 50)
        print("📋 Next Steps: Add SSH Key to GitHub")
        print("-" * 50)
        print("\n1. Visit: https://github.com/settings/ssh")
        print("2. Click 'New SSH key'")
        print("3. Give it a title (e.g., 'My Laptop')")
        if platform != "linux":
            print("4. The key is already copied—paste it into the 'Key' field")
        else:
            print("4. Copy and paste this key into the 'Key' field:")
            print("\n" + pub_key + "\n")
        print("5. Click 'Add SSH key'")
        print("\n6. Back in terminal, verify with:")
        print("   ssh -T git@github.com")
        print("   (You may need to type 'yes' when prompted)")

        print("\n" + "-" * 50)
        ready = input("Have you added the SSH key to GitHub? (y/n): ").lower().strip()
        return ready == "y"

    except (
        subprocess.CalledProcessError,
        subprocess.TimeoutExpired,
        FileNotFoundError,
        OSError,
    ) as e:
        print(f"   ✗ Failed to generate SSH key: {e}")
        return False


async def check_docker() -> bool:
    """Check if Docker is installed and running"""
    try:
        result = subprocess.run(["docker", "--version"], capture_output=True, text=True, timeout=5)
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


async def start_docker_services() -> bool:
    """Start all required Docker services using docker-compose"""
    print("\n🐳 Starting Docker services...")
    print("   (First run may take 5-10 minutes to download images)")

    try:
        # Start services in detached mode (no timeout - image pulls can be slow)
        print("   📦 Pulling and starting containers...")
        process = subprocess.Popen(
            ["docker-compose", "up", "-d"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        # Wait for process with longer timeout for image downloads
        try:
            stdout, stderr = process.communicate(timeout=600)  # 10 minutes for first-time pulls
        except subprocess.TimeoutExpired:
            process.kill()
            print("   ✗ Timeout after 10 minutes (likely network issue)")
            return False

        if process.returncode != 0:
            print(f"   ✗ Failed to start services")
            if stderr:
                print(f"   Error: {stderr}")
            return False

        print("   ✓ Containers started")

        # Wait for services to be healthy with progressive checks
        print("   ⏳ Waiting for services to be ready...")
        print("   (This can take 30-60 seconds on first run)")
        print("   ℹ️  Temporal is optional - setup will continue if it's not ready")

        max_attempts = 10  # 10 attempts x 2 seconds = 20 seconds (reduced for alpha)
        for attempt in range(max_attempts):
            await asyncio.sleep(2)

            services_ok = {
                "PostgreSQL": await check_database(),
                "Redis": await check_redis(),
                "ChromaDB": await check_chromadb(),
                "Temporal": await check_temporal(),
            }

            # Check if core services are ready (Temporal is optional)
            core_services_ready = all(services_ok[s] for s in ["PostgreSQL", "Redis", "ChromaDB"])

            if core_services_ready:
                if services_ok["Temporal"]:
                    print("   ✓ All services ready")
                else:
                    print("   ✓ Core services ready (Temporal still starting)")
                return True

            # Show progress every 10 seconds
            if (attempt + 1) % 5 == 0:
                ready = sum(1 for ok in services_ok.values() if ok)
                print(f"   ⏳ {ready}/4 services ready... (attempt {attempt + 1}/{max_attempts})")

        # Final status after timeout
        print("   ⚠  Timeout waiting for all services:")
        for name, ok in services_ok.items():
            status = "✓" if ok else "✗"
            print(f"      {status} {name}")
        print("   Services may still be starting - you can continue and they might work")
        return False

    except FileNotFoundError:
        print("   ✗ docker-compose command not found")
        print("   Please install Docker Compose: https://docs.docker.com/compose/install/")
        return False
    except (subprocess.CalledProcessError, OSError) as e:
        print(f"   ✗ Error starting services: {e}")
        return False


async def guide_docker_installation() -> bool:
    """Guide user through Docker installation with platform-specific instructions"""
    platform = get_platform()

    print("\n" + "=" * 50)
    print("🐳 Docker Installation Guide")
    print("=" * 50)

    print("\nDocker is required for Piper Morgan's database and services.")
    print("Let's get Docker installed on your system.\n")

    if platform == "macos":
        print("📱 macOS Installation:")
        print("1. Visit: https://docs.docker.com/desktop/mac/install/")
        print("2. Download Docker Desktop for Mac")
        print("3. Open the .dmg file and drag Docker to Applications")
        print("4. Launch Docker Desktop from Applications")
        print("5. Wait for Docker to start (whale icon in menu bar)")

    elif platform == "windows":
        print("🪟 Windows Installation:")
        print("1. Visit: https://docs.docker.com/desktop/windows/install/")
        print("2. Download Docker Desktop for Windows")
        print("3. Run the installer and follow the setup wizard")
        print("4. Restart your computer when prompted")
        print("5. Launch Docker Desktop and wait for it to start")

    elif platform == "linux":
        print("🐧 Linux Installation:")
        print("1. Visit: https://docs.docker.com/engine/install/")
        print("2. Choose your Linux distribution")
        print("3. Follow the installation instructions")
        print("4. Start Docker: sudo systemctl start docker")
        print("5. Enable auto-start: sudo systemctl enable docker")

    else:
        print("❓ Unknown Platform:")
        print("1. Visit: https://docs.docker.com/get-docker/")
        print("2. Choose the appropriate installer for your system")
        print("3. Follow the installation instructions")

    print("\n" + "-" * 50)
    print("After installation:")
    print("• Docker Desktop should show a green 'running' status")
    print("• You can test with: docker --version")
    print("• If you see version info, Docker is working!")

    while True:
        print("\n" + "-" * 50)
        choice = input("Have you installed Docker? (y/n/skip): ").lower().strip()

        if choice in ["y", "yes"]:
            # Test Docker installation
            if await check_docker():
                print("✅ Great! Docker is now working.")
                return True
            else:
                print("❌ Docker doesn't seem to be working yet.")
                print("💡 Try:")
                print("   • Make sure Docker Desktop is running")
                print("   • Restart Docker Desktop")
                print("   • Check Docker Desktop status")
                continue

        elif choice in ["n", "no"]:
            print("📝 No problem! Please install Docker and run setup again.")
            print("   Docker is required for Piper Morgan's database.")
            return False

        elif choice == "skip":
            print("⚠️  WARNING: Skipping Docker installation.")
            print("   Some features may not work without Docker.")
            print("   You can install Docker later and re-run setup.")

            confirm = input("Continue without Docker? (y/n): ").lower().strip()
            if confirm in ["y", "yes"]:
                return True
            else:
                continue
        else:
            print("Please enter 'y' (yes), 'n' (no), or 'skip'")
            continue


async def check_python_version() -> bool:
    """Check Python version >= 3.9 (3.11+ recommended)"""
    version = sys.version_info
    if version >= (3, 11):
        return True
    elif version >= (3, 9):
        # Allow 3.9+ with warning
        print("   ⚠ Python 3.9 detected - works but 3.11+ recommended")
        return True
    else:
        return False


async def check_port_available(port: int = 8001) -> bool:
    """Check if port is available"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # Set SO_REUSEADDR to handle TIME_WAIT state after restart
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind(("", port))
        return True
    except OSError:
        return False


async def check_service_port(host: str, port: int, service_name: str) -> bool:
    """Check if a service is accessible on a specific port"""
    try:
        reader, writer = await asyncio.wait_for(asyncio.open_connection(host, port), timeout=2.0)
        writer.close()
        await writer.wait_closed()
        return True
    except Exception:
        return False


async def check_redis() -> bool:
    """Check Redis connectivity"""
    return await check_service_port("localhost", 6379, "Redis")


async def check_chromadb() -> bool:
    """Check ChromaDB connectivity"""
    return await check_service_port("localhost", 8000, "ChromaDB")


async def check_temporal() -> bool:
    """Check Temporal connectivity"""
    return await check_service_port("localhost", 7233, "Temporal")


async def check_database() -> bool:
    """Check PostgreSQL database connectivity"""
    try:
        from sqlalchemy import text

        from services.database.session_factory import AsyncSessionFactory

        async with AsyncSessionFactory.session_scope_fresh() as session:
            await session.execute(text("SELECT 1"))

        return True
    except Exception as e:
        print(f"   Database check details: {e}")
        return False


async def check_system() -> Dict[str, bool]:
    """Run all system checks (includes all required Docker services)"""
    print("\n1. System Check")

    checks = {
        SERVICE_DOCKER: await check_docker(),
        SERVICE_PYTHON: await check_python_version(),
        SERVICE_PORT: await check_port_available(),
        SERVICE_POSTGRES: await check_database(),
        SERVICE_REDIS: await check_redis(),
        SERVICE_CHROMADB: await check_chromadb(),
        SERVICE_TEMPORAL: await check_temporal(),
    }

    for name, result in checks.items():
        status = "✓" if result else "✗"
        print(f"   {status} {name}")

    return checks


async def check_for_incomplete_setup() -> Any:
    """
    Check if there's an alpha user with no API keys (incomplete setup).

    Returns:
        AlphaUser object if incomplete setup found, None otherwise
    """
    from sqlalchemy import select

    from services.database.models import User as AlphaUser
    from services.database.models import UserAPIKey
    from services.database.session_factory import AsyncSessionFactory

    try:
        async with AsyncSessionFactory.session_scope_fresh() as session:
            # Find alpha users with no API keys (during alpha phase)
            result = await session.execute(
                select(AlphaUser)
                .outerjoin(UserAPIKey, AlphaUser.id == UserAPIKey.user_id)
                .where(UserAPIKey.id.is_(None))
                .order_by(AlphaUser.created_at.desc())
                .limit(1)
            )
            user = result.scalar_one_or_none()
            return user
    except Exception:
        return None


async def create_user_account() -> Any:
    """Create user account with secure password (Issue #297)"""
    from services.auth.password_service import PasswordService
    from services.database.models import User
    from services.database.session_factory import AsyncSessionFactory

    print("\n2. User Account Setup")

    # Check for incomplete setup (Issue #218 - Smart Resume)
    existing_user = await check_for_incomplete_setup()

    if existing_user:
        print(f"   Found incomplete setup for: {existing_user.username}")
        if existing_user.email:
            print(f"   Email: {existing_user.email}")

        resume = input("   Resume this setup? (y/n): ").strip().lower()

        if resume == "y":
            print(f"   ✓ Resuming setup for {existing_user.username}")
            return existing_user
        else:
            # Delete incomplete account so user can reclaim the username
            print(f"   Removing incomplete setup for {existing_user.username}...")
            try:
                from sqlalchemy import delete

                async with AsyncSessionFactory.session_scope_fresh() as session:
                    # Delete the incomplete user account
                    await session.execute(delete(User).where(User.id == existing_user.id))
                    await session.commit()
                print(f"   ✓ Removed incomplete account")
            except Exception as e:
                print(f"   ⚠️  Could not remove incomplete account: {e}")
                print("   Note: You may need to use a different username")

            print("   Starting new setup...")
    else:
        print("   Creating your alpha tester account...")

    # Try to create alpha user, handle duplicates
    max_attempts = 3
    for attempt in range(max_attempts):
        username = input("   Username: ").strip()

        while not username:
            print("   ✗ Username is required")
            username = input("   Username: ").strip()

        email = input("   Email (optional, press Enter to skip): ").strip() or None

        # Prompt for password (Issue #297 - Secure password setup)
        print("\n   Create a secure password:")
        password = getpass("   Password (min 8 characters): ")

        while len(password) < 8:
            print("   ✗ Password must be at least 8 characters")
            password = getpass("   Password (min 8 characters): ")

        # Confirm password
        password_confirm = getpass("   Confirm password: ")

        while password != password_confirm:
            print("   ✗ Passwords don't match, please try again")
            password = getpass("   Password (min 8 characters): ")
            password_confirm = getpass("   Confirm password: ")

        # Hash password with bcrypt
        password_service = PasswordService()
        password_hash = password_service.hash_password(password)
        print("   ✓ Password set securely")

        # Create user account (Issue #262 - UUID migration, #297 - Password setup)
        user = User(
            id=uuid.uuid4(),
            username=username,
            email=email,
            password_hash=password_hash,
            role="user",
            is_active=True,
            is_verified=True,
            is_alpha=True,  # Alpha tester flag
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

        try:
            async with AsyncSessionFactory.session_scope_fresh() as session:
                session.add(user)
                await session.commit()

            print(f"   ✓ Account created: {username}")
            return user

        except Exception as e:
            error_str = str(e).lower()
            if "duplicate" in error_str or "unique" in error_str:
                if "username" in error_str:
                    print(f"   ✗ Username '{username}' already exists")
                elif "email" in error_str:
                    print(f"   ✗ Email '{email}' already exists")
                else:
                    print("   ✗ Account already exists")

                if attempt < max_attempts - 1:
                    print("   Please try a different username or email")
                else:
                    raise ValueError(
                        "Unable to create account after 3 attempts. Username or email may already exist."
                    )
            else:
                # Some other error
                raise


def _check_global_keychain_key(provider: str) -> Optional[str]:
    """
    Check for global keychain key (migration from 0.8.0).

    In 0.8.0, keys were stored globally as '{provider}_api_key'.
    In 0.8.1+, keys are user-scoped as '{user_id}_{provider}_api_key'.
    This function checks for the old global format to support migration.

    Args:
        provider: Provider name (openai, anthropic, github)

    Returns:
        API key if found in global keychain format, None otherwise
    """
    from services.infrastructure.keychain_service import KeychainService

    try:
        keychain = KeychainService()
        # Check without username = global format (0.8.0 style)
        return keychain.get_api_key(provider, username=None)
    except Exception:
        return None


async def _validate_notion_key(api_key: str) -> tuple[bool, Optional[str], Optional[str]]:
    """
    Validate a Notion API key and get workspace name.

    Issue #527: ALPHA-SETUP-NOTION

    Uses the official Notion SDK to test the API key by calling users.me()
    endpoint, which returns workspace information for bot integrations.

    Args:
        api_key: Notion API key (starts with 'secret_' or 'ntn_')

    Returns:
        Tuple of (is_valid, workspace_name, error_message)
        - is_valid: True if key is valid and has workspace access
        - workspace_name: Name of the workspace, or None if invalid
        - error_message: Human-friendly error message, or None if valid
    """
    try:
        from notion_client import Client
        from notion_client.client import ClientOptions
        from notion_client.errors import APIResponseError

        # Create a temporary client with the provided key
        options = ClientOptions(auth=api_key, notion_version="2025-09-03")
        client = Client(options=options)

        # Test the key by calling users.me()
        user_info = client.users.me()

        # Extract workspace name from bot info
        workspace_name = user_info.get("bot", {}).get("workspace", {}).get("name")

        # If no workspace name in bot info, fall back to user name
        if not workspace_name:
            workspace_name = user_info.get("name", "Unknown Workspace")

        return True, workspace_name, None

    except APIResponseError as e:
        # Issue #527: Provide specific error guidance
        error_str = str(e).lower()
        if "unauthorized" in error_str:
            return False, None, "Invalid API key. Check your key at notion.so/my-integrations"
        elif "forbidden" in error_str:
            return (
                False,
                None,
                "Key lacks required permissions. Ensure integration has workspace access",
            )
        elif "rate_limited" in error_str:
            return False, None, "Rate limited by Notion. Wait a moment and try again"
        return False, None, "Invalid API key or insufficient permissions"
    except ImportError:
        return False, None, "Notion SDK not installed"
    except Exception as e:
        error_str = str(e).lower()
        if "connect" in error_str or "network" in error_str or "timeout" in error_str:
            return False, None, "Could not reach Notion API. Check your internet connection"
        return False, None, "Validation failed. Please try again"


async def _collect_notion_api_key(user_id: str, service) -> Optional[str]:
    """
    Collect and validate Notion API key.

    Issue #527: ALPHA-SETUP-NOTION

    Notion uses custom validation (not LLM provider), so we handle it separately
    from _collect_single_api_key.

    Args:
        user_id: User ID for keychain storage
        service: UserAPIKeyService instance

    Returns:
        API key if successful or None if skipped
    """
    from services.database.session_factory import AsyncSessionFactory

    provider = "notion"
    env_var_name = "NOTION_API_KEY"
    api_key = None

    # Step 1: Check keychain for existing key
    print("   Checking keychain for existing key...")
    try:
        async with AsyncSessionFactory.session_scope_fresh() as session:
            existing_key = await service.retrieve_user_key(session, user_id, provider)
            if existing_key:
                print("   ✓ Using existing key from keychain")
                return existing_key
            else:
                print("   ℹ️  No existing key found in keychain")
    except Exception as e:
        print(f"   ℹ️  Keychain check skipped ({type(e).__name__})")

    # Step 2: Check environment variable
    api_key = os.environ.get(env_var_name)
    if api_key:
        print(f"   ℹ️  Using {env_var_name} from environment")
        print("   Validating...")

        is_valid, workspace_name, error_msg = await _validate_notion_key(api_key)
        if is_valid:
            # Store the validated key
            try:
                async with AsyncSessionFactory.session_scope_fresh() as session:
                    await service.store_user_key(
                        user_id=user_id,
                        provider=provider,
                        api_key=api_key,
                        session=session,
                        validate=False,  # Already validated above
                    )
                    await session.commit()
                print(f"   ✓ Valid (Connected to '{workspace_name}')")
                return api_key
            except Exception as e:
                print(f"   ⚠ Storage error: {e}")
                print("   Continuing with manual entry...")
        else:
            print(f"   ✗ {error_msg or 'Invalid API key or insufficient permissions'}")
            print(f"   Key from environment is invalid. Please update {env_var_name}")
        api_key = None  # Force manual entry

    # Step 3: Manual entry loop
    while not api_key:
        prompt = "   Enter key (secret_..., or press Enter to skip): "
        api_key = getpass(prompt)

        if not api_key:
            print("   Skipped (you can add this later)")
            return None

        print("   Validating...")

        is_valid, workspace_name, error_msg = await _validate_notion_key(api_key)
        if is_valid:
            # Store the validated key
            try:
                async with AsyncSessionFactory.session_scope_fresh() as session:
                    await service.store_user_key(
                        user_id=user_id,
                        provider=provider,
                        api_key=api_key,
                        session=session,
                        validate=False,  # Already validated above
                    )
                    await session.commit()
                print(f"   ✓ Valid (Connected to '{workspace_name}')")
                return api_key
            except Exception as e:
                print(f"   ✗ Storage error: {e}")
                api_key = None
        else:
            print(f"   ✗ {error_msg or 'Invalid API key or insufficient permissions'}")
            print("   Please check your key and try again.")
            api_key = None  # Reset to retry

    return api_key


async def _collect_single_api_key(
    user_id: str,
    service,
    provider: str,
    env_var_name: str,
    format_hint: str,
    validation_msg: str,
    is_required: bool = False,
    skip_validation: bool = False,
) -> Optional[str]:
    """
    Generic API key collection with keychain, env var, and manual entry.

    Handles the common pattern for all API key collection:
    1. Check keychain for existing user-scoped key
    2. Check for old global key and migrate if found
    3. Check environment variable
    4. Manual entry with retry loop
    5. Validate and store in keychain

    Args:
        user_id: User ID for keychain storage
        service: UserAPIKeyService instance
        provider: Provider name (openai, anthropic, gemini, github)
        env_var_name: Environment variable name (e.g., OPENAI_API_KEY)
        format_hint: Format hint for manual entry (e.g., sk-...)
        validation_msg: Success message (e.g., "gpt-4 access confirmed")
        is_required: If False, allow skipping by pressing Enter
        skip_validation: Skip validation during store (for GitHub)

    Returns:
        API key if successful or skipped, None otherwise
    """
    from services.database.session_factory import AsyncSessionFactory

    api_key = None

    # Step 1: Check keychain for existing key
    print(f"   Checking keychain for existing key...")
    try:
        async with AsyncSessionFactory.session_scope_fresh() as session:
            existing_key = await service.retrieve_user_key(session, user_id, provider)
            if existing_key:
                print("   ✓ Using existing key from keychain")
                return existing_key
            else:
                print("   ℹ️  No existing key found in keychain")
                # Check for global key (migration from 0.8.0)
                global_key = _check_global_keychain_key(provider)
                if global_key:
                    print("   ✓ Found existing global key (migrating to user-scoped)")
                    api_key = global_key
                    # Migrate: store as user-scoped
                    try:
                        await service.store_user_key(
                            user_id=user_id,
                            provider=provider,
                            api_key=global_key,
                            session=session,
                            validate=not skip_validation,
                        )
                        await session.commit()
                        print("   ✓ Migrated to user-scoped storage")
                        return global_key
                    except Exception as migrate_err:
                        print(f"   ℹ️  Using key (migration skipped: {migrate_err})")
                        return global_key
    except Exception as e:
        print(f"   ℹ️  Keychain check skipped ({type(e).__name__})")
        pass  # Keychain check failed, continue to other methods

    # Step 2: Check for environment variable if not in keychain
    if not api_key:
        api_key = os.environ.get(env_var_name)
    if api_key:
        print(f"   ℹ️  Using {env_var_name} from environment")
        print("   Validating...")

        # Store and validate the key from environment
        try:
            async with AsyncSessionFactory.session_scope_fresh() as session:
                await service.store_user_key(
                    user_id=user_id,
                    provider=provider,
                    api_key=api_key,
                    session=session,
                    validate=not skip_validation,
                )
                await session.commit()

            print(f"   ✓ Valid ({validation_msg})")
            return api_key
        except ValueError as e:
            print(f"   ✗ {str(e)}")
            print(f"   Key from environment is invalid. Please update {env_var_name}")
            api_key = None  # Force manual entry
        except Exception as e:
            print(f"   ✗ Validation error: {e}")
            print("   Continuing with manual entry...")
            api_key = None  # Force manual entry

    # Step 3: Manual entry loop if env var not set or failed
    while not api_key:
        prompt = f"   Enter key ({format_hint}): "
        if not is_required:
            prompt = f"   Enter key ({format_hint}, or press Enter to skip): "

        api_key = getpass(prompt)

        if not api_key:
            if is_required:
                print(f"   ✗ {provider.title()} key is required")
                print(f"   💡 Tip: Set {env_var_name} environment variable to avoid paste issues")
                continue
            else:
                print(f"   Skipped (you can add this later)")
                return None

        print("   Validating...")

        try:
            # Validate with provider API
            async with AsyncSessionFactory.session_scope_fresh() as session:
                # Store the key first
                await service.store_user_key(
                    user_id=user_id,
                    provider=provider,
                    api_key=api_key,
                    session=session,
                    validate=not skip_validation,
                )
                await session.commit()

            # If we got here, validation succeeded
            print(f"   ✓ Valid ({validation_msg})")
            return api_key

        except ValueError as e:
            # Validation failed
            print(f"   ✗ {str(e)}")
            print("   Please check your key and try again.")
            api_key = None  # Reset to retry
        except Exception as e:
            print(f"   ✗ Validation error: {e}")
            print("   Please check your key and try again.")
            api_key = None  # Reset to retry

    return api_key


async def collect_and_validate_api_keys(user_id: str) -> Dict[str, str]:
    """Collect API keys with real-time validation using DRY helper pattern"""
    from services.database.session_factory import AsyncSessionFactory
    from services.security.user_api_key_service import UserAPIKeyService

    print("\n3. API Keys")
    print("   (Keys are stored securely in your system keychain)")

    service = UserAPIKeyService()
    stored_keys = {}

    # OpenAI (required)
    print("\n   OpenAI API key (required):")
    openai_key = await _collect_single_api_key(
        user_id=user_id,
        service=service,
        provider="openai",
        env_var_name="OPENAI_API_KEY",
        format_hint="sk-...",
        validation_msg="gpt-4 access confirmed",
        is_required=True,
        skip_validation=False,
    )
    if openai_key:
        stored_keys["openai"] = openai_key

    # Anthropic (optional)
    print("\n   Anthropic API key (optional, press Enter to skip):")
    anthropic_key = await _collect_single_api_key(
        user_id=user_id,
        service=service,
        provider="anthropic",
        env_var_name="ANTHROPIC_API_KEY",
        format_hint="sk-ant-...",
        validation_msg="claude access confirmed",
        is_required=False,
        skip_validation=False,
    )
    if anthropic_key:
        stored_keys["anthropic"] = anthropic_key

    # Gemini (optional)
    print("\n   Google Gemini API key (optional, press Enter to skip):")
    gemini_key = await _collect_single_api_key(
        user_id=user_id,
        service=service,
        provider="gemini",
        env_var_name="GEMINI_API_KEY",
        format_hint="AIza...",
        validation_msg="gemini-pro access confirmed",
        is_required=False,
        skip_validation=False,
    )
    if gemini_key:
        stored_keys["gemini"] = gemini_key

    # GitHub (optional, no validation)
    print("\n   GitHub token (optional, press Enter to skip):")
    github_token = await _collect_single_api_key(
        user_id=user_id,
        service=service,
        provider="github",
        env_var_name="GITHUB_TOKEN",
        format_hint="ghp_...",
        validation_msg="github token stored",
        is_required=False,
        skip_validation=True,  # GitHub tokens are validated differently
    )
    if github_token:
        stored_keys["github"] = github_token

    # Notion (optional) - Issue #527: ALPHA-SETUP-NOTION
    # Notion uses custom validation (not LLM provider), so we handle it specially
    print("\n   Notion API key (optional, press Enter to skip):")
    print("   Get your key at: https://www.notion.so/my-integrations")
    notion_key = await _collect_notion_api_key(user_id=user_id, service=service)
    if notion_key:
        stored_keys["notion"] = notion_key

    # Slack (optional) - Issue #528: ALPHA-SETUP-SLACK
    # Slack uses OAuth, which requires a browser redirect flow
    print("\n   Slack Integration (optional):")
    print("   Note: Slack requires OAuth authorization via web browser.")
    print("   Run 'python main.py' and visit http://localhost:8001/setup to connect Slack,")
    print("   or set SLACK_BOT_TOKEN environment variable directly.")

    # Check if already configured
    slack_token = os.environ.get("SLACK_BOT_TOKEN")
    if slack_token:
        print("   ✓ Slack already configured (SLACK_BOT_TOKEN found)")
    else:
        print("   ℹ️  Slack not configured (connect via web setup wizard)")

    return stored_keys


async def _wizard_preflight_checks() -> bool:
    """Check Python 3.12, setup venv, SSH key - returns False if critical failure"""
    # Check Python 3.12
    print("\n1️⃣  Checking for Python 3.12...")
    if not check_python312_available():
        print("   ✗ Python 3.12 not found")
        print("   📥 Please install from: https://www.python.org/downloads/release/python-31210/")
        print("   ⏸  Install Python 3.12.10 and run this wizard again.")
        return False
    print("   ✓ Python 3.12 found")

    # Set up virtual environment (only if not already in one)
    in_venv = hasattr(sys, "real_prefix") or (
        hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix
    )

    if not in_venv:
        print("\n2️⃣  Setting up virtual environment...")
        if not setup_virtual_environment():
            print("   ✗ Failed to set up virtual environment")
            return False

        # Restart wizard in the new venv
        print("\n🔄 Restarting wizard in virtual environment...")
        print("   (This ensures all dependencies are available)")
        venv_python = os.path.join(os.getcwd(), "venv", "bin", "python")
        os.execv(venv_python, [venv_python, "main.py", "setup"])
        # execv doesn't return - the process is replaced
    else:
        print("\n2️⃣  Virtual environment: ✓ Active")

    # Set up SSH (optional but recommended)
    print("\n3️⃣  Setting up SSH key...")
    ssh_ready = setup_ssh_key()
    if not ssh_ready:
        print("   ⚠  SSH setup skipped (you can set this up later manually)")

    return True


async def _wizard_system_checks() -> bool:
    """Perform system checks (Docker, PostgreSQL, Redis, etc.) - returns False if critical failure"""
    print("\n" + "=" * 50)
    print("📋 System Checks")
    print("=" * 50)
    checks = await check_system()

    # Handle Docker installation separately with guided setup
    if not checks["Docker installed"]:
        print("\n🐳 Docker is not installed or not running.")
        docker_success = await guide_docker_installation()
        if not docker_success:
            print("\n❌ Setup cannot continue without Docker.")
            return False
        # Re-check Docker after guided installation
        checks[SERVICE_DOCKER] = await check_docker()

    # Check if Docker services need to be started
    services_down = [k for k in CORE_SERVICES if not checks.get(k, False)]
    optional_down = [k for k in OPTIONAL_SERVICES if not checks.get(k, False)]

    if (services_down or optional_down) and checks.get(SERVICE_DOCKER, False):
        all_down = services_down + optional_down
        print(f"\n⚠️  {len(all_down)} service(s) not running:")
        for service in all_down:
            print(f"   ✗ {service}")

        # Try to start services automatically
        services_started = await start_docker_services()

        if services_started:
            # Re-check services after starting
            checks[SERVICE_POSTGRES] = await check_database()
            checks[SERVICE_REDIS] = await check_redis()
            checks[SERVICE_CHROMADB] = await check_chromadb()
            checks[SERVICE_TEMPORAL] = await check_temporal()

            # Update services_down list
            services_down = [k for k in CORE_SERVICES if not checks.get(k, False)]
            optional_down = [k for k in OPTIONAL_SERVICES if not checks.get(k, False)]

            if optional_down:
                print(f"\n   ⚠  Optional service not ready: {', '.join(optional_down)}")
                print("   (This won't prevent setup from continuing)")

    # Check other requirements (exclude optional services from blocking)
    remaining_issues = {
        k: v
        for k, v in checks.items()
        if not v and k != SERVICE_DOCKER and k not in OPTIONAL_SERVICES
    }

    if remaining_issues:
        print("\n❌ Setup cannot continue. Please fix the issues above.")
        print("\nTroubleshooting:")
        if not checks.get(SERVICE_PYTHON, True) is False:
            print("  • Install Python 3.9+: https://www.python.org/downloads/")
            print("  • Recommended: Python 3.11+ for best compatibility")
        if not checks.get(SERVICE_PORT, True) is False:
            print("  • Free up port 8001 or stop other Piper Morgan instances")
            print("  • Run: lsof -i :8001 to see what's using the port")

        if services_down:
            print("  • Docker services not running:")
            print("    1. Launch Docker Desktop application (check menu bar icon)")
            print("    2. Wait for Docker to fully start (icon stops animating)")
            print("    3. Try: docker-compose up -d")
            print("    4. Wait 30 seconds for services to start")
            print("    5. Re-run this wizard")
            print("  • After system restart:")
            print("    - Docker Desktop doesn't auto-start by default")
            print("    - You must manually launch it from Applications")

        return False

    return True


MIGRATION_TIMEOUT_SECONDS = 600


def _run_migrations(project_root: str) -> "subprocess.CompletedProcess[str]":
    """``alembic upgrade head`` with this interpreter (so it does not depend on an
    ``alembic`` executable being on PATH). One seam for the wizard and its tests."""
    return subprocess.run(
        [sys.executable, "-m", "alembic", "upgrade", "head"],
        capture_output=True,
        text=True,
        timeout=MIGRATION_TIMEOUT_SECONDS,
        cwd=project_root,
    )


async def _wizard_database_setup() -> bool:
    """Build or update the database schema with alembic, and only alembic.

    #2372 (Arch 2026-11-14): this used to run ``db.create_tables()``
    (``Base.metadata.create_all``) on an empty database and THEN
    ``alembic upgrade head``. The first migrations then met tables that already
    existed, the failure was printed as a warning, setup continued, and the
    database was left without an ``alembic_version`` stamp, so every later
    ``alembic upgrade head`` (the self-host guide's update step) failed too. Now
    the wizard takes the one path the guide and CI use. A migration failure STOPS
    setup with the error: a half-built schema is not something to continue on.
    """
    print("\n" + "=" * 50)
    print("📊 Database Schema")
    print("=" * 50)
    print("   Running database migrations (this builds the tables on a new database)...")

    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    try:
        migration_result = _run_migrations(project_root)
    except subprocess.TimeoutExpired:
        print(f"   ❌ Migrations did not finish in {MIGRATION_TIMEOUT_SECONDS} seconds.")
        print("   Setup has stopped. Check that PostgreSQL is running, then run the wizard again.")
        return False
    except Exception as e:
        print(f"   ❌ Could not run the migrations: {e}")
        print("   Setup has stopped. Nothing else was changed.")
        return False

    if migration_result.returncode != 0:
        print("   ❌ The database migrations failed. Setup has stopped.")
        if migration_result.stderr:
            print(f"      {migration_result.stderr.strip()}")
        if migration_result.stdout:
            print(f"      {migration_result.stdout.strip()}")
        print("   Fix the error above, then run the wizard again. It is safe to re-run:")
        print("   a migration that already ran is not run twice.")
        return False

    print("   ✓ Database schema up to date")
    return True


async def _wizard_mark_complete(user: object) -> bool:
    """Mark setup as complete and generate CLI token"""
    try:
        from sqlalchemy import text

        from services.database.session_factory import AsyncSessionFactory

        async with AsyncSessionFactory.session_scope_fresh() as session:
            await session.execute(
                text(
                    "UPDATE users SET setup_complete = true, "
                    "setup_completed_at = :now WHERE id = :user_id"
                ),
                {"user_id": str(user.id), "now": datetime.utcnow()},
            )
            await session.commit()
    except Exception as e:
        # Non-fatal: setup succeeded even if flag update fails
        print(f"   ℹ️  Could not update setup flag: {e}")

    # Generate and store CLI session token
    try:
        from services.auth.jwt_service import JWTService
        from services.infrastructure.keychain_service import KeychainService

        jwt_service = JWTService()
        keychain = KeychainService()

        cli_token = jwt_service.generate_cli_token(user_id=user.id, user_email=user.email or "")
        keychain.store_cli_token(str(user.id), cli_token)
        print("   ✓ CLI auto-authentication configured")
    except Exception as e:
        # Non-fatal: CLI auth is optional
        print(f"   ℹ️  CLI auto-auth skipped: {e}")

    return True


async def run_setup_wizard():
    """Main setup wizard entry point - orchestrates all setup phases"""

    print("\n" + "=" * 50)
    print("Welcome to Piper Morgan Alpha!")
    print("=" * 50)
    print("\nLet's get you set up (takes about 5-10 minutes)")
    print()

    try:
        # Phase 0: Pre-flight checks (Python 3.12, venv, SSH)
        print("\n" + "=" * 50)
        print("🚀 Pre-Flight Checks")
        print("=" * 50)

        if not await _wizard_preflight_checks():
            return False

        # Phase 1: System checks
        if not await _wizard_system_checks():
            return False

        # Phase 1.5: Database setup
        if not await _wizard_database_setup():
            return False

        # Phase 2: Create user first (need user_id for API keys)
        user = await create_user_account()

        # Phase 3: API keys
        user_id_str = str(user.id)
        api_keys = await collect_and_validate_api_keys(user_id_str)

        # Phase 4: Mark setup complete and generate CLI token
        await _wizard_mark_complete(user)

        # Success message
        print("\n" + "=" * 50)
        print("✅ Setup Complete!")
        print("=" * 50)

        print(f"\nYour account:")
        print(f"  Username: {user.username}")
        if user.email:
            print(f"  Email: {user.email}")

        print(f"\nConfigured API providers:")
        for provider in api_keys.keys():
            print(f"  ✓ {provider}")

        print("\nNext steps:")
        print("  1. Set your preferences:")
        print("     source venv/bin/activate")
        print("     python main.py preferences")
        print("  2. Start Piper Morgan:")
        print("     python main.py")
        print("  3. Access at: http://localhost:8001")
        print("  4. Check system status:")
        print("     python main.py status")
        print("\n  💡 Tip: All commands work best from within 'venv/bin/activate'")

        print("\nNeed help?")
        print("  • Documentation: https://pmorgan.tech")
        print("  • Report bugs: https://github.com/mediajunkie/piper-morgan/issues")

        return True

    except KeyboardInterrupt:
        print("\n\n❌ Setup cancelled by user")
        return False
    except Exception as e:
        print(f"\n\n❌ Setup failed: {e}")
        import traceback

        traceback.print_exc()
        return False


async def is_setup_complete() -> bool:
    """
    Check if setup has been completed.

    Setup is considered complete when (Issue #389 - explicit flag):
    - Primary: setup_complete flag is True in users table
    - Fallback: Legacy inference (user exists + OpenAI key configured)

    Returns:
        bool: True if setup is complete, False otherwise
    """
    try:
        from sqlalchemy import text

        from services.database.session_factory import AsyncSessionFactory

        async with AsyncSessionFactory.session_scope_fresh() as session:
            # Primary check: explicit setup_complete flag (Issue #389)
            complete_result = await session.execute(
                text("SELECT COUNT(*) FROM users WHERE setup_complete = true")
            )
            complete_count = complete_result.scalar_one()

            if complete_count > 0:
                return True

            # Fallback: legacy inference for backwards compatibility
            # Check if user exists
            user_result = await session.execute(text("SELECT COUNT(*) FROM users"))
            user_count = user_result.scalar_one()

            if user_count == 0:
                return False

            # Check if OpenAI key exists and is active
            key_result = await session.execute(
                text(
                    "SELECT COUNT(*) FROM user_api_keys "
                    "WHERE provider = 'openai' AND is_active = true"
                )
            )
            openai_key_count = key_result.scalar_one()

            if openai_key_count > 0:
                return True

            # Fallback: check global keychain (migration from 0.8.0)
            # User exists but no key in database - maybe key is in global keychain
            global_openai = _check_global_keychain_key("openai")
            if global_openai:
                import logging

                logger = logging.getLogger(__name__)
                logger.debug("Found global OpenAI key in keychain (0.8.0 format)")
                return True

            return False
    except Exception as e:
        # Database might not exist yet (first run)
        # or there might be a connection issue
        import logging

        logger = logging.getLogger(__name__)
        logger.debug(f"Setup check failed (likely first run): {e}")
        return False


if __name__ == "__main__":
    # Allow running directly
    success = asyncio.run(run_setup_wizard())
    sys.exit(0 if success else 1)
