# RippleMap AI - Deployment Guide

Complete guide to deploying RippleMap AI to production.

## Prerequisites

- Docker & Docker Compose installed
- PostgreSQL 12+ with PostGIS
- Node.js 16+
- Python 3.9+
- AWS account (S3 bucket for reports)
- SSL certificate (HTTPS required)

## Quick Start with Docker

### 1. Clone Repository

```bash
git clone https://github.com/ripplemap-ai/ripplemap-ai.git
cd ripplemap-ai
```

### 2. Environment Setup

Create `.env` file:

```env
# App
DEBUG=False
APP_NAME=RippleMap AI
APP_VERSION=1.0.0

# Database
DATABASE_URL=postgresql+asyncpg://ripplemap:secure_password_here@db:5432/ripplemap_db

# Security
SECRET_KEY=your-super-secret-key-change-this
JWT_SECRET=your-jwt-secret-key

# Frontend
NEXT_PUBLIC_API_URL=https://api.ripplemap.ai

# AWS
AWS_ACCESS_KEY_ID=your-aws-key
AWS_SECRET_ACCESS_KEY=your-aws-secret
AWS_S3_BUCKET=ripplemap-ai-reports
AWS_REGION=us-east-1

# CORS
CORS_ORIGINS=["https://ripplemap.ai","https://www.ripplemap.ai"]
```

### 3. Docker Compose

Start all services:

```bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

Services start in this order:
1. PostgreSQL + PostGIS database
2. Redis cache
3. Backend API
4. Frontend
5. Nginx reverse proxy

### 4. Database Migrations

```bash
docker exec ripplemap-backend python -m alembic upgrade head
```

### 5. Verify Deployment

```bash
# Health check
curl https://api.ripplemap.ai/health

# Frontend
open https://ripplemap.ai
```

---

## Production Architecture

```
                    ┌──────────────┐
                    │   CloudFlare │
                    │     (DNS)    │
                    └──────┬───────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
        ▼                  ▼                  ▼
    ┌────────┐      ┌──────────┐      ┌──────────┐
    │ Vercel │      │ Render   │      │ Netlify  │
    │Frontend│      │  Backend │      │ CDN      │
    └────────┘      └──────────┘      └──────────┘
        │                  │                  │
        └──────────────────┼──────────────────┘
                          │
                    ┌─────▼──────┐
                    │   Nginx    │
                    │(Load Bal.) │
                    └─────┬──────┘
                          │
            ┌─────────────┼─────────────┐
            ▼             ▼             ▼
        ┌───────┐    ┌───────┐    ┌───────┐
        │Backend│    │Backend│    │Backend│
        │ API 1 │    │ API 2 │    │ API 3 │
        └───┬───┘    └───┬───┘    └───┬───┘
            │            │            │
            └────────────┼────────────┘
                         │
                ┌────────▼────────┐
                │  PostgreSQL +   │
                │     PostGIS     │
                │   (Primary)     │
                └────────────────┘
                         │
                ┌────────▼────────┐
                │   PostgreSQL    │
                │   (Standby)     │
                │  (Read Replica) │
                └────────────────┘
```

---

## Hosting Options

### **Frontend**

| Provider | Cost | Features | Recommended |
|----------|------|----------|-------------|
| **Vercel** | ~$20/mo | Git deploy, Edge functions, SSL | ✅ Yes |
| **Netlify** | ~$19/mo | Continuous deploy, Lambda | Yes |
| **AWS CloudFront** | Pay-per-use | Scalable, S3 integration | Yes |

```bash
# Deploy to Vercel
vercel --prod
```

### **Backend**

| Provider | Cost | Features | Recommended |
|----------|------|----------|-------------|
| **Render** | ~$12/mo | Docker container, PostgreSQL | ✅ Yes |
| **Railway** | Pay-per-use | Easy scaling, PostgreSQL | Yes |
| **AWS ECS** | ~$30+/mo | Full control, Fargate | Yes |
| **DigitalOcean App Platform** | ~$12/mo | Simple, PostgreSQL included | Yes |

```bash
# Deploy to Render
render deploy
```

### **Database**

| Provider | Cost | Features | Recommended |
|----------|------|----------|-------------|
| **AWS RDS** | ~$50/mo | Managed, PostGIS support | ✅ Yes |
| **Railway PostgreSQL** | ~$10/mo | Simple, automatic backups | Yes |
| **Managed PostgreSQL** | ~$40/mo | Dedicated, PostGIS | Yes |

```bash
# Create PostgreSQL with PostGIS
CREATE EXTENSION postgis;
```

### **Storage (Reports)**

| Provider | Cost | Features | Recommended |
|----------|------|----------|-------------|
| **AWS S3** | ~$1/GB | Scalable, Glacier archive | ✅ Yes |
| **Backblaze B2** | ~$0.01/GB | Low cost alternative | Yes |
| **CloudFlare R2** | ~$0.015/GB | No egress charges | Yes |

---

## SSL/TLS Configuration

### Let's Encrypt (Free)

```bash
# Using Certbot
sudo certbot certonly --standalone \
  -d ripplemap.ai \
  -d api.ripplemap.ai

# Certificate paths
/etc/letsencrypt/live/ripplemap.ai/fullchain.pem
/etc/letsencrypt/live/ripplemap.ai/privkey.pem

# Auto-renewal
sudo certbot renew --dry-run
```

### Nginx Configuration

```nginx
server {
    listen 443 ssl http2;
    server_name api.ripplemap.ai;

    ssl_certificate /etc/letsencrypt/live/ripplemap.ai/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/ripplemap.ai/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    location / {
        proxy_pass http://backend:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

---

## Database Backup & Recovery

### Automated Backups

```bash
# Daily backup script
#!/bin/bash
BACKUP_DIR="/backups/postgresql"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

pg_dump -h localhost -U ripplemap ripplemap_db | gzip > $BACKUP_DIR/ripplemap_$TIMESTAMP.sql.gz

# Upload to S3
aws s3 cp $BACKUP_DIR/ripplemap_$TIMESTAMP.sql.gz s3://ripplemap-backups/
```

### Recovery

```bash
# Restore from backup
gunzip < ripplemap_20240115_100000.sql.gz | psql -h localhost -U ripplemap ripplemap_db
```

---

## Monitoring & Logging

### Application Monitoring

```bash
# Health check endpoint
GET https://api.ripplemap.ai/health

# Response should be:
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### Log Aggregation

```bash
# Using ELK Stack
docker run -d \
  --name elasticsearch \
  -e "discovery.type=single-node" \
  docker.elastic.co/elasticsearch/elasticsearch:8.11.0

# Filebeat for log shipping
filebeat -e -c filebeat.yml
```

### Performance Metrics

Monitor with Prometheus:

```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'backend'
    static_configs:
      - targets: ['backend:8000']
        metrics_path: '/metrics'
```

---

## Security Checklist

- [ ] SSL/TLS certificate installed
- [ ] CORS properly configured
- [ ] Database password hashed (bcrypt)
- [ ] Environment secrets not in git
- [ ] API rate limiting enabled
- [ ] Input validation on all endpoints
- [ ] SQL injection prevention (SQLAlchemy ORM)
- [ ] CSRF protection enabled
- [ ] Audit logging configured
- [ ] Backups tested and working
- [ ] WAF rules configured
- [ ] DDoS protection enabled

---

## Scaling Considerations

### Horizontal Scaling (Multiple Backends)

```bash
# Docker Compose - scale backend
docker-compose up -d --scale backend=3
```

Load balancer automatically distributes requests across instances.

### Database Scaling

```sql
-- Create read replica
SELECT pg_create_physical_replication_slot('replica1');

-- Connect read-only instance
PRIMARY_CONNINFO='host=primary user=replica password=xxx' \
pg_basebackup -D /var/lib/postgresql/data -v -P
```

### Caching Layer (Redis)

```python
# FastAPI + Redis
from fastapi_cache2 import FastAPICache2
from fastapi_cache2.backends.redis import RedisBackend

@app.get("/study-areas")
@cached(expire=3600)
async def list_study_areas():
    # Cached for 1 hour
    pass
```

---

## Troubleshooting

### Backend won't start

```bash
# Check logs
docker logs ripplemap-backend

# Common issues:
# 1. Database connection
# 2. Missing environment variables
# 3. Port already in use
```

### Database connection errors

```bash
# Test connection
psql -h db.example.com -U ripplemap -d ripplemap_db

# Check PostGIS
SELECT PostGIS_version();
```

### Performance issues

```bash
# Profile API endpoints
from pyinstrument import Profiler

profiler = Profiler()
profiler.start()
# ... run code ...
profiler.stop()
print(profiler.output_text())
```

---

## Post-Deployment Checklist

- [ ] All health checks passing
- [ ] Domain DNS resolved correctly
- [ ] SSL certificate valid (no warnings)
- [ ] Monitoring alerts configured
- [ ] Backup system tested
- [ ] Auto-scaling policies set
- [ ] Documentation updated
- [ ] User access provisioned
- [ ] Support channels established
- [ ] Performance baseline recorded

---

**For additional support**: deployment-help@ripplemap.ai
