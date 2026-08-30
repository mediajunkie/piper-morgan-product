# Piper Morgan Operational Guide

**Document Status**: Operational Procedures
**Last Updated**: September 30, 2025
**Audience**: Developers and Operations Teams

## Overview

This guide provides operational procedures for running, managing, and troubleshooting Piper Morgan. Covers server management, spatial systems, feature flags, security configuration, and common issues.

---

## Server Management

### Architecture

**Components**:
- **Backend**: FastAPI application on port 8001
- **Frontend**: Next.js application on port 3000
- **Database**: PostgreSQL on port 5433 (note: not default 5432)

**Process Management**:
- PID files stored in project root
- Stop script cleans up PIDs automatically
- Health checks verify service availability

---

### Starting Services

**Method 1: Start Script (Recommended)**

```bash
# Start both backend and frontend
./start-piper.sh

# Script performs:
# 1. Starts backend on port 8001 (uvicorn)
# 2. Waits for backend health check
# 3. Starts frontend on port 3000 (Next.js dev server)
# 4. Waits for frontend health check
# 5. Displays status of both services
```

**Method 2: Manual Start (Development)**

```bash
# Terminal 1: Start backend
cd /path/to/piper-morgan
source venv/bin/activate  # If using virtual environment
PYTHONPATH=. uvicorn main:app --host 0.0.0.0 --port 8001 --reload

# Terminal 2: Start frontend
cd web
npm run dev
```

**Expected Output**:
```
Backend: http://localhost:8001 ✅
Frontend: http://localhost:3000 ✅
API Docs: http://localhost:8001/docs
Health: http://localhost:8001/health
```

---

### Stopping Services

**Method 1: Stop Script (Recommended)**

```bash
# Stop both services cleanly
./stop-piper.sh

# Script performs:
# 1. Reads PID files (backend.pid, frontend.pid)
# 2. Sends SIGTERM to processes
# 3. Waits for graceful shutdown (5s timeout)
# 4. Removes PID files
# 5. Verifies processes stopped
```

**Method 2: Manual Stop**

```bash
# Find and kill processes
lsof -ti :8001 | xargs kill -9  # Backend
lsof -ti :3000 | xargs kill -9  # Frontend

# Clean up PID files
rm -f backend.pid frontend.pid
```

**Verification**:
```bash
# Check ports are freed
lsof -i :8001  # Should return nothing
lsof -i :3000  # Should return nothing
```

---

### Health Monitoring

**Backend Health Check**:
```bash
# Check backend health
curl http://localhost:8001/health

# Expected response:
{
  "status": "healthy",
  "timestamp": "2025-09-30T12:00:00Z",
  "version": "1.0.0"
}
```

**Frontend Health Check**:
```bash
# Check frontend is responding
curl http://localhost:3000

# Expected: HTML response (Next.js app)
```

**Database Health Check**:
```bash
# Connect to database
docker exec -it piper-postgres psql -U piper -d piper_morgan

# Or using psql directly (if installed)
PGPASSWORD=your_password psql -h localhost -p 5433 -U piper -d piper_morgan

# Check database status
\l  # List databases
\dt  # List tables
```

---

## Spatial System Management

### Feature Flag Control

Piper Morgan uses environment variables to control spatial intelligence systems.

**Available Flags**:
- `USE_SPATIAL_SLACK` - Controls Slack spatial system (default: `true`)
- `USE_SPATIAL_NOTION` - Controls Notion spatial system (default: `true`)
- `USE_SPATIAL_CALENDAR` - Controls Calendar spatial system (default: `true`)
- `USE_SPATIAL_GITHUB` - Controls GitHub spatial system (default: `true`)

**Enable Spatial Systems** (Default):
```bash
# Enable Slack spatial intelligence
export USE_SPATIAL_SLACK=true

# Enable Notion spatial intelligence
export USE_SPATIAL_NOTION=true

# Restart server to activate
./stop-piper.sh && ./start-piper.sh
```

**Disable Spatial Systems** (Legacy Mode):
```bash
# Disable for legacy/basic mode
export USE_SPATIAL_SLACK=false
export USE_SPATIAL_NOTION=false

# Restart server to activate
./stop-piper.sh && ./start-piper.sh
```

**Persistent Configuration**:
```bash
# Add to .env file (recommended)
cat >> .env << 'EOF'
USE_SPATIAL_SLACK=true
USE_SPATIAL_NOTION=true
USE_SPATIAL_CALENDAR=true
USE_SPATIAL_GITHUB=true
EOF

# Or add to shell profile (~/.bashrc, ~/.zshrc)
echo 'export USE_SPATIAL_SLACK=true' >> ~/.bashrc
source ~/.bashrc
```

---

### Spatial System Verification

**Test Slack Spatial System**:
```python
# Python REPL or script
from services.integrations.slack.slack_integration_router import SlackIntegrationRouter

router = SlackIntegrationRouter()
adapter = router.get_spatial_adapter()

if adapter:
    print(f"✅ Slack spatial system operational")
    print(f"   Adapter type: {type(adapter).__name__}")

    # List available methods
    methods = [m for m in dir(adapter) if not m.startswith('_')]
    print(f"   Methods: {len(methods)} available")
    print(f"   Methods: {', '.join(methods[:5])}...")
else:
    print(f"❌ Slack spatial system not available")
```

**Test Notion Spatial System**:

> ⚠️ **Removed 2026-08-29**: `NotionSpatialIntelligence`
> (`services/intelligence/spatial/notion_spatial.py`) was disposed of in the PM-ruled spatial
> cold-island disposal — it was the superseded direct-API predecessor of the live Notion path
> and had zero importers. The live Notion integration is `NotionMCPAdapter`
> (`services/integrations/mcp/notion_adapter.py`) via the Notion plugin router; verify that
> instead. Prior art: commit-hash references in the 2026-08-29 spatial-disposal entry of
> `docs/internal/architecture/decisions/decisions.log`.

**Quick Verification Script**:
```bash
# Create verification script
cat > verify_spatial.py << 'EOF'
#!/usr/bin/env python3
import sys
import os

print("=== SPATIAL SYSTEM VERIFICATION ===\n")

# Check environment variables
slack_flag = os.environ.get('USE_SPATIAL_SLACK', 'true')
notion_flag = os.environ.get('USE_SPATIAL_NOTION', 'true')

print(f"USE_SPATIAL_SLACK={slack_flag}")
print(f"USE_SPATIAL_NOTION={notion_flag}\n")

# Test Slack
try:
    from services.integrations.slack.slack_integration_router import SlackIntegrationRouter
    router = SlackIntegrationRouter()
    adapter = router.get_spatial_adapter()
    print(f"✅ Slack spatial: {'enabled' if adapter else 'disabled'}")
except Exception as e:
    print(f"❌ Slack spatial error: {e}")

# Notion spatial check removed 2026-08-29: NotionSpatialIntelligence was disposed of
# (spatial cold-island disposal); the live Notion path is NotionMCPAdapter via the plugin router.

print("\n=== VERIFICATION COMPLETE ===")
EOF

chmod +x verify_spatial.py

# Run verification
PYTHONPATH=. python3 verify_spatial.py
```

---

## Security Configuration

### Webhook Security

Piper Morgan implements graceful degradation for webhook security.

**Development Mode** (Default - No Configuration):
- Webhook endpoints accept all requests
- No signing secrets required
- Suitable for local development
- Warning logged: "No Slack signing secret configured"

**Production Mode** (Signing Secret Configured):
- Full HMAC-SHA256 signature verification
- Invalid signatures return 401 Unauthorized
- Replay attack protection (5-minute window)
- Production-ready security

**Configure for Production**:
```bash
# Get signing secret from Slack App settings
# 1. Open Slack App > Basic Information
# 2. Scroll to "App Credentials"
# 3. Copy "Signing Secret"

# Set environment variable
export SLACK_SIGNING_SECRET=your_secret_here

# Or in .env file
echo "SLACK_SIGNING_SECRET=your_secret_here" >> .env

# Restart server to activate
./stop-piper.sh && ./start-piper.sh
```

**Verify Security Mode**:
```bash
# Check logs after server start
# Development mode shows:
# WARNING: No Slack signing secret configured, skipping signature verification

# Production mode shows:
# (no warning - signature verification active)

# Test with curl
curl -X POST http://localhost:8001/slack/webhooks/events \
  -H "Content-Type: application/json" \
  -d '{"test": "data"}'

# Development: Returns 200 OK
# Production (no signature): Returns 401 Unauthorized
```

---

### Database Configuration

**Connection Settings**:
```bash
# PostgreSQL connection (note port 5433, not 5432)
DATABASE_URL=postgresql://piper:password@localhost:5433/piper_morgan

# Or individual settings
DB_HOST=localhost
DB_PORT=5433
DB_NAME=piper_morgan
DB_USER=piper
DB_PASSWORD=your_password
```

**Common Operations**:
```bash
# Connect to database
docker exec -it piper-postgres psql -U piper -d piper_morgan

# Backup database
pg_dump -h localhost -p 5433 -U piper piper_morgan > backup.sql

# Restore database
psql -h localhost -p 5433 -U piper piper_morgan < backup.sql

# Check database size
psql -h localhost -p 5433 -U piper -d piper_morgan -c "SELECT pg_size_pretty(pg_database_size('piper_morgan'));"
```

---

## Troubleshooting

### Spatial Systems

**Issue: Spatial system not working**

**Symptoms**:
- `get_spatial_adapter()` returns `None`
- Spatial methods not available
- Feature not working as expected

**Solutions**:
1. Check feature flag is set correctly:
   ```bash
   echo $USE_SPATIAL_SLACK
   echo $USE_SPATIAL_NOTION
   ```

2. Verify router imports successfully:
   ```bash
   PYTHONPATH=. python3 -c "from services.integrations.slack.slack_integration_router import SlackIntegrationRouter; print('✅ Import successful')"
   ```

3. Check logs for import errors:
   ```bash
   tail -f logs/app.log | grep -i spatial
   ```

4. Restart server after changing flags:
   ```bash
   ./stop-piper.sh && ./start-piper.sh
   ```

---

### Webhook Security

**Issue: Webhooks rejected in production (401 Unauthorized)**

**Symptoms**:
- Slack events not processing
- Webhooks return 401 status
- Signature verification failing

**Solutions**:
1. Verify signing secret is set:
   ```bash
   echo $SLACK_SIGNING_SECRET
   # Should output your signing secret (not empty)
   ```

2. Check signing secret matches Slack workspace:
   - Open Slack App > Basic Information
   - Compare "Signing Secret" with environment variable
   - Update if different

3. Check server logs for specific error:
   ```bash
   tail -f logs/app.log | grep -i signature
   ```

4. Verify timestamp is current (clock sync):
   ```bash
   date  # Check server time
   ntpq -p  # Check NTP sync (if available)
   ```

**Issue: Webhooks accepted when they shouldn't be**

**Symptoms**:
- Production receiving unsigned requests
- Security warning in logs

**Solutions**:
1. Set signing secret:
   ```bash
   export SLACK_SIGNING_SECRET=your_secret_here
   ```

2. Restart server:
   ```bash
   ./stop-piper.sh && ./start-piper.sh
   ```

3. Verify no warning in logs:
   ```bash
   tail -f logs/app.log | grep "skipping signature verification"
   # Should not appear after restart
   ```

---

### Server Issues

**Issue: Server won't start (port already in use)**

**Symptoms**:
```
Error: Address already in use (port 8001)
Error: Address already in use (port 3000)
```

**Solutions**:
1. Check if processes are running:
   ```bash
   lsof -i :8001
   lsof -i :3000
   ```

2. Kill existing processes:
   ```bash
   ./stop-piper.sh

   # Or manual kill
   lsof -ti :8001 | xargs kill -9
   lsof -ti :3000 | xargs kill -9
   ```

3. Clean up PID files:
   ```bash
   rm -f backend.pid frontend.pid
   ```

4. Start server again:
   ```bash
   ./start-piper.sh
   ```

**Issue: Server starts but immediately crashes**

**Symptoms**:
- Server starts then stops
- Process not found in `ps` output
- Health check fails

**Solutions**:
1. Check logs for errors:
   ```bash
   tail -f logs/app.log
   ```

2. Check for missing dependencies:
   ```bash
   pip list | grep -E "(fastapi|uvicorn|pydantic)"
   ```

3. Check database connectivity:
   ```bash
   psql -h localhost -p 5433 -U piper -d piper_morgan -c "SELECT 1;"
   ```

4. Run server in foreground for debugging:
   ```bash
   PYTHONPATH=. uvicorn main:app --host 0.0.0.0 --port 8001
   ```

**Issue: Database connection errors**

**Symptoms**:
```
psycopg2.OperationalError: could not connect to server
Connection refused (port 5433)
```

**Solutions**:
1. Check database is running:
   ```bash
   docker ps | grep postgres
   # Should show piper-postgres container
   ```

2. Start database if needed:
   ```bash
   docker start piper-postgres
   ```

3. Check port 5433 is correct (not 5432):
   ```bash
   # Correct
   psql -h localhost -p 5433 -U piper -d piper_morgan

   # Wrong (default PostgreSQL port)
   psql -h localhost -p 5432 -U piper -d piper_morgan
   ```

4. Verify DATABASE_URL environment variable:
   ```bash
   echo $DATABASE_URL
   # Should contain :5433 not :5432
   ```

---

## Common Operations

### Running Tests

**All Tests**:
```bash
# Run full test suite
PYTHONPATH=. pytest tests/ -v

# With coverage
PYTHONPATH=. pytest tests/ --cov=services --cov-report=html
```

**Specific Test Categories**:
```bash
# Integration tests
PYTHONPATH=. pytest tests/integration/ -v

# Unit tests
PYTHONPATH=. pytest tests/unit/ -v

# Spatial tests
PYTHONPATH=. pytest tests/integration/test_slack_spatial* -v
PYTHONPATH=. pytest tests/features/test_notion_spatial* -v

# Specific test file
PYTHONPATH=. pytest tests/integration/test_slack_spatial_adapter_integration.py -v
```

**Feature Flag Testing**:
```bash
# Test with spatial enabled
USE_SPATIAL_SLACK=true PYTHONPATH=. pytest tests/integration/test_slack* -v

# Test with spatial disabled
USE_SPATIAL_SLACK=false PYTHONPATH=. pytest tests/integration/test_slack* -v
```

---

### Viewing Logs

**Application Logs**:
```bash
# Follow application logs
tail -f logs/app.log

# Last 100 lines
tail -100 logs/app.log

# Filter for errors
tail -f logs/app.log | grep ERROR

# Filter for specific feature
tail -f logs/app.log | grep -i spatial
tail -f logs/app.log | grep -i webhook
```

**Server Access Logs**:
```bash
# Follow access logs
tail -f logs/access.log

# Show recent requests
tail -100 logs/access.log
```

---

### Database Maintenance

**Common Tasks**:
```bash
# Vacuum database
psql -h localhost -p 5433 -U piper -d piper_morgan -c "VACUUM ANALYZE;"

# Check table sizes
psql -h localhost -p 5433 -U piper -d piper_morgan -c "
  SELECT schemaname, tablename,
         pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
  FROM pg_tables
  WHERE schemaname NOT IN ('pg_catalog', 'information_schema')
  ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;"

# Check for slow queries
psql -h localhost -p 5433 -U piper -d piper_morgan -c "
  SELECT query, calls, total_time, mean_time
  FROM pg_stat_statements
  ORDER BY total_time DESC
  LIMIT 10;"
```

---

## Best Practices

### Development

1. **Use Stop/Start Scripts**: More reliable than manual process management
2. **Check Health Endpoints**: Verify services are truly ready before use
3. **Enable Spatial by Default**: Most development benefits from spatial features
4. **Monitor Logs**: Watch for warnings and errors during development

### Production

1. **Set Signing Secrets**: Always configure webhook security
2. **Monitor Health**: Set up automated health checks
3. **Review Logs Regularly**: Check for security warnings
4. **Use Environment Variables**: Don't hardcode secrets in code
5. **Backup Database**: Regular automated backups

### Operations

1. **Document Configuration**: Keep track of environment variables
2. **Test Feature Flags**: Verify flags work before deploying
3. **Plan Restarts**: Use graceful shutdown (stop script)
4. **Monitor Performance**: Watch for slow queries, high CPU

---

## Quick Reference

**Ports**:
- Backend: 8001
- Frontend: 3000
- Database: 5433 (not default 5432!)

**Scripts**:
- Start: `./start-piper.sh`
- Stop: `./stop-piper.sh`

**Health Checks**:
- Backend: `http://localhost:8001/health`
- Frontend: `http://localhost:3000`

**Feature Flags**:
- Spatial Slack: `USE_SPATIAL_SLACK=true/false`
- Spatial Notion: `USE_SPATIAL_NOTION=true/false`

**Security**:
- Webhook Secret: `SLACK_SIGNING_SECRET=your_secret`

**Key Paths**:
- Logs: `logs/app.log`, `logs/access.log`
- PID Files: `backend.pid`, `frontend.pid`
- Config: `.env`, environment variables

---

## Getting Help

**Resources**:
- Architecture Docs: `docs/architecture/`
- API Docs: `http://localhost:8001/docs`
- GitHub Issues: Create issue with label `operations`

**Common Issue Labels**:
- `spatial-systems` - Spatial intelligence issues
- `security` - Webhook security, authentication
- `operations` - Server management, deployment

---

**See Also**:
- Spatial Intelligence Patterns *(proposed; doc TBD)* - Spatial system architecture
- Webhook Security Design *(proposed; doc TBD)* - Security architecture
- [Troubleshooting Guide](../troubleshooting.md) - General troubleshooting

**Maintained by**: Piper Morgan Core Team
**Last Verified**: September 30, 2025 (CORE-GREAT-2C)
