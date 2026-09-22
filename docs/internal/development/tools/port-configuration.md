# Port Configuration - Piper Morgan

## Development Ports
**Critical**: These ports are fixed and must be used correctly in all documentation

### Port 8001 - API Backend
- **Service**: FastAPI backend server
- **Purpose**: All API endpoints including personality enhancement
- **URL**: `http://localhost:8001`
- **API Base**: `http://localhost:8001/api/`
- **Examples**:
  - Personality profile: `http://localhost:8001/api/v1/personality/profile` (auth required; no user-id segment)
  - Standup with personality: `http://localhost:8001/api/standup?personality=true`

### Port 8081 - Web UI Frontend
- **Service**: Frontend web interface
- **Purpose**: User interface for chat, standup, personality preferences
- **URL**: `http://localhost:8081`
- **Key Pages**:
  - Main chat: `http://localhost:8081/`
  - Standup interface: `http://localhost:8081/standup`
  - Personality preferences: `http://localhost:8081/personality-preferences`

## Common Agent Mistakes to Avoid
- ❌ Assuming web UI on port 8001 (it's 8081)
- ❌ Assuming API on port 8080 or other ports (it's 8001)
- ❌ Using placeholder ports in documentation
- ❌ Not specifying ports in testing procedures

## Testing URL Examples
```bash
# API Testing (authenticate first — form-encoded, not JSON)
curl -s -c /tmp/piper-cookies.txt -X POST http://localhost:8001/api/v1/auth/login \
  -d "username=YOUR_USERNAME&password=YOUR_PASSWORD"
curl -b /tmp/piper-cookies.txt -X GET "http://localhost:8001/api/v1/personality/profile" | jq '.'

# Web UI Testing (browser)
open http://localhost:8081/personality-preferences
```

## Development Setup
Both services must run simultaneously:
1. Backend API on 8001
2. Frontend UI on 8081
