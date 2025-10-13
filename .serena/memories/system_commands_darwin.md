# Piper Morgan - System Commands (macOS/Darwin)

## Essential Unix Commands
```bash
# File operations
ls -la                     # List files with details
find . -name "*.py"        # Find Python files
grep -r "pattern" .        # Search in files
cd /path/to/directory      # Change directory

# Process management
ps aux | grep python       # Find Python processes
kill -9 <pid>             # Force kill process
lsof -i :8001             # Check what's using port 8001

# System information
uname -a                  # System information
df -h                     # Disk usage
top                       # Process monitor
```

## Docker Commands (macOS)
```bash
# Docker Desktop management
docker info               # Check Docker status
docker-compose up -d      # Start services in background
docker-compose down       # Stop services
docker ps                 # List running containers
docker logs <container>   # View container logs

# Cleanup
docker system prune       # Clean up unused resources
```

## Python Environment (macOS)
```bash
# Virtual environment
python3 -m venv venv      # Create virtual environment
source venv/bin/activate  # Activate (bash/zsh)
deactivate               # Deactivate

# Package management
pip install -r requirements.txt
pip freeze > requirements.txt
pip list                 # Show installed packages
```

## Git Commands
```bash
# Basic operations
git status               # Check repository status
git add .                # Stage all changes
git commit -m "message"  # Commit changes
git push origin main     # Push to remote

# Branch management
git branch               # List branches
git checkout -b feature  # Create and switch to branch
git merge feature        # Merge branch
```

## Network & Ports (macOS)
```bash
# Port checking
lsof -i :8001           # Check port 8001
netstat -an | grep 8001 # Alternative port check
curl http://localhost:8001/health  # Test endpoint

# Network diagnostics
ping google.com         # Test connectivity
nslookup domain.com     # DNS lookup
```

## File Permissions (macOS)
```bash
chmod +x script.sh      # Make executable
chmod 755 file          # Set permissions
chown user:group file   # Change ownership
```