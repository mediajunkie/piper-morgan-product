# Production Deployment Guide

This guide covers everything you need to deploy Piper Morgan in production environments, from infrastructure requirements to monitoring and maintenance.

## Infrastructure Requirements

### Minimum System Requirements
- **CPU**: 4 cores, 2.4GHz
- **RAM**: 8GB minimum, 16GB recommended
- **Storage**: 100GB SSD
- **Network**: 1Gbps connection

### Recommended Production Setup
- **CPU**: 8+ cores, 3.0GHz
- **RAM**: 32GB+
- **Storage**: 500GB+ SSD with backup
- **Network**: Multi-zone deployment with load balancing

### Dependencies
- **PostgreSQL**: 14+ (managed service recommended)
- **Redis**: 6+ (for caching and queues)
- **Docker**: 24+ with Docker Compose
- **Load Balancer**: Nginx, HAProxy, or cloud provider solution

## Deployment Options

### Docker Compose (Simple)

For single-server deployments:

```yaml
version: '3.8'
services:
  api:
    image: piper-morgan:latest
    environment:
      - DATABASE_URL=postgresql://user:pass@postgres:5432/piper_morgan
      - REDIS_URL=redis://redis:6379
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - ENVIRONMENT=production
    ports:
      - "8001:8001"
    depends_on:
      - postgres
      - redis

  postgres:
    image: postgres:14
    environment:
      POSTGRES_DB: piper_morgan
      POSTGRES_USER: piper
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:6-alpine
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

### Kubernetes (Scalable)

For container orchestration:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: piper-morgan-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: piper-morgan-api
  template:
    metadata:
      labels:
        app: piper-morgan-api
    spec:
      containers:
      - name: api
        image: piper-morgan:latest
        ports:
        - containerPort: 8001
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: piper-morgan-secrets
              key: database-url
```

### Cloud Deployments

#### AWS
- **Compute**: ECS Fargate or EKS
- **Database**: RDS PostgreSQL
- **Cache**: ElastiCache Redis
- **Load Balancer**: Application Load Balancer
- **Storage**: EFS for shared files

#### Google Cloud
- **Compute**: Cloud Run or GKE
- **Database**: Cloud SQL PostgreSQL
- **Cache**: Memorystore Redis
- **Load Balancer**: Cloud Load Balancing
- **Storage**: Cloud Storage

#### Azure
- **Compute**: Container Instances or AKS
- **Database**: Azure Database for PostgreSQL
- **Cache**: Azure Cache for Redis
- **Load Balancer**: Azure Load Balancer
- **Storage**: Azure Blob Storage

## Environment Configuration

### Production Environment Variables

```bash
# Application
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=INFO

# API Keys
ANTHROPIC_API_KEY=your-production-key
OPENAI_API_KEY=your-production-key
GITHUB_TOKEN=your-production-token

# Database
DATABASE_URL=postgresql://user:pass@prod-db:5432/piper_morgan
DATABASE_POOL_SIZE=20
DATABASE_MAX_OVERFLOW=30

# Redis
REDIS_URL=redis://prod-redis:6379
REDIS_MAX_CONNECTIONS=100

# Security
JWT_SECRET_KEY=your-secure-random-key
ALLOWED_HOSTS=yourdomain.com,api.yourdomain.com
CORS_ORIGINS=https://yourdomain.com

# Monitoring
SENTRY_DSN=your-sentry-dsn
DATADOG_API_KEY=your-datadog-key
```

### Security Configuration

#### SSL/TLS Setup

```nginx
server {
    listen 443 ssl http2;
    server_name api.yourdomain.com;

    ssl_certificate /path/to/certificate.crt;
    ssl_certificate_key /path/to/private.key;
    ssl_protocols TLSv1.2 TLSv1.3;

    location / {
        proxy_pass http://piper-morgan-api:8001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

#### Firewall Rules

```bash
# Allow HTTP/HTTPS
ufw allow 80
ufw allow 443

# Allow SSH (restrict by IP)
ufw allow from YOUR_IP_ADDRESS to any port 22

# Database access (internal only)
ufw deny 5432
```

## Database Setup

### Production PostgreSQL Configuration

```sql
-- Create production database
CREATE DATABASE piper_morgan_prod;
CREATE USER piper_prod WITH ENCRYPTED PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE piper_morgan_prod TO piper_prod;

-- Performance tuning
ALTER SYSTEM SET shared_buffers = '256MB';
ALTER SYSTEM SET effective_cache_size = '1GB';
ALTER SYSTEM SET maintenance_work_mem = '64MB';
ALTER SYSTEM SET checkpoint_completion_target = 0.9;
ALTER SYSTEM SET wal_buffers = '16MB';
```

### Backup Strategy

```bash
#!/bin/bash
# Automated database backup script
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups/postgres"
DB_NAME="piper_morgan_prod"

# Create backup
pg_dump -h localhost -U piper_prod -d $DB_NAME -f $BACKUP_DIR/backup_$DATE.sql

# Upload to cloud storage
aws s3 cp $BACKUP_DIR/backup_$DATE.sql s3://your-backup-bucket/postgres/

# Cleanup old backups (keep 30 days)
find $BACKUP_DIR -name "backup_*.sql" -mtime +30 -delete
```

## Monitoring and Observability

### Health Checks

```python
# Health check endpoint
@app.get("/health")
async def health_check():
    checks = {
        "database": await check_database_connection(),
        "redis": await check_redis_connection(),
        "external_apis": await check_external_apis()
    }

    if all(checks.values()):
        return {"status": "healthy", "checks": checks}
    else:
        raise HTTPException(status_code=503, detail="Service unavailable")
```

### Logging Configuration

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'production': {
            'format': '%(asctime)s %(name)s %(levelname)s %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        }
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/piper-morgan/app.log',
            'maxBytes': 1024*1024*100,  # 100MB
            'backupCount': 5,
            'formatter': 'production'
        }
    },
    'root': {
        'level': 'INFO',
        'handlers': ['file']
    }
}
```

### Metrics and Alerting

```yaml
# Prometheus configuration
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'piper-morgan'
    static_configs:
      - targets: ['api:8001']
    metrics_path: '/metrics'

rule_files:
  - "alert_rules.yml"

alerting:
  alertmanagers:
    - static_configs:
        - targets:
          - alertmanager:9093
```

## Performance Optimization

### Application Performance

```python
# Connection pooling
DATABASE_CONFIG = {
    'pool_size': 20,
    'max_overflow': 30,
    'pool_pre_ping': True,
    'pool_recycle': 300
}

# Caching strategy
@cache(expire=3600)  # 1 hour cache
async def get_repository_stats(repo_id: str):
    # Expensive computation
    pass
```

### Database Optimization

```sql
-- Add appropriate indexes
CREATE INDEX CONCURRENTLY idx_issues_created_at ON issues(created_at);
CREATE INDEX CONCURRENTLY idx_issues_repository_id ON issues(repository_id);
CREATE INDEX CONCURRENTLY idx_issues_status ON issues(status);

-- Analyze and vacuum regularly
ANALYZE;
VACUUM ANALYZE;
```

## Scaling Considerations

### Horizontal Scaling

- **API Servers**: Multiple instances behind load balancer
- **Background Workers**: Separate worker processes for async tasks
- **Database**: Read replicas for queries, master for writes
- **Caching**: Distributed Redis cluster

### Auto-scaling Configuration

```yaml
# Kubernetes HPA
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: piper-morgan-api-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: piper-morgan-api
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

## Maintenance and Updates

### Rolling Updates

```bash
# Zero-downtime deployment script
#!/bin/bash
docker pull piper-morgan:latest
docker-compose up -d --no-deps api
docker system prune -f
```

### Database Migrations

```bash
# Production migration workflow
python manage.py migrate --check
python manage.py migrate --dry-run
python manage.py migrate
```

## Troubleshooting

### Common Issues

1. **High CPU Usage**: Check for inefficient queries, add database indexes
2. **Memory Leaks**: Monitor connection pools, implement proper cleanup
3. **Slow Response Times**: Enable caching, optimize database queries
4. **Database Locks**: Review long-running transactions

### Emergency Procedures

```bash
# Quick service restart
docker-compose restart api

# Database emergency recovery
pg_restore -h localhost -U piper_prod -d piper_morgan_prod latest_backup.sql

# Scale up immediately (Kubernetes)
kubectl scale deployment piper-morgan-api --replicas=10
```

## Support and Documentation

- **Architecture Guide**: [Architecture Documentation](../architecture/)
- **API Reference**: [API Documentation](../../../internal/architecture/current/api-reference.md)
- **Monitoring Guide**: [Operations Documentation](../operations/)
- **Security Guide**: [Security Documentation](../architecture/)

---

*For development environment setup, see [Developer Quick Start](developers.md). For API integration patterns, see [API Integration](api-integration.md).*
