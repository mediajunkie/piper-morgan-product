# CORE-USERS-PROD: Production Database Configuration

## Context
Current system uses SQLite for development. Alpha requires production-grade database with multi-user support, proper connection pooling, and migration management.

## Current State
```python
# Current: SQLite with basic AsyncSessionFactory
DATABASE_URL = "sqlite+aiosqlite:///./piper_morgan.db"
```

## Scope

### 1. PostgreSQL Setup
- PostgreSQL as production database
- Connection pooling with asyncpg
- SSL/TLS for connections
- Read replicas support (future)

### 2. Configuration Management
```python
# config/database.py
class DatabaseConfig:
    def get_url(self, env: Environment) -> str:
        """Get database URL for environment"""
        # Development: SQLite
        # Staging: PostgreSQL (local)
        # Production: PostgreSQL (cloud)
```

### 3. Migration System
- Alembic for schema migrations
- Automatic migration on startup (dev)
- Controlled migrations (production)
- Rollback capability
- Data migration scripts

### 4. Connection Management
```python
class ProductionSessionFactory:
    """Production-grade session management"""
    - Connection pooling (min: 5, max: 20)
    - Connection health checks
    - Automatic reconnection
    - Query timeout management
    - Transaction isolation levels
```

### 5. Multi-User Considerations
- User data isolation
- Row-level security where needed
- Audit logging for sensitive operations
- Performance for concurrent users

## Acceptance Criteria
- [ ] PostgreSQL configuration working
- [ ] Connection pooling implemented
- [ ] SSL/TLS enabled
- [ ] Alembic migrations functional
- [ ] SQLite → PostgreSQL migration script
- [ ] Performance benchmarks met
- [ ] Multi-user isolation verified
- [ ] Backup/restore procedures documented

## Performance Targets
- Connection pool: 5-20 connections
- Query timeout: 30 seconds default
- Connection timeout: 10 seconds
- Pool recycle: 1 hour
- Health check: every 30 seconds

## Migration Plan
1. Add PostgreSQL dependencies
2. Create Alembic configuration
3. Generate initial migration from models
4. Create data migration script
5. Test migration with sample data
6. Document rollback procedure

## Time Estimate
2 days

## Priority
High - Required for multi-user Alpha

## Dependencies
- PostgreSQL server (local or cloud)
- Alembic
- asyncpg
- psycopg2-binary (for migrations)

## Notes
Consider cloud providers:
- AWS RDS
- Supabase
- Neon
- Local PostgreSQL for alpha testing
