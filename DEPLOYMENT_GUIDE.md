# 🚀 Deployment Guide - Py-Agentic AI

## 📋 Table of Contents
- [Prerequisites](#prerequisites)
- [Local Development](#local-development)
- [Docker Deployment](#docker-deployment)
- [Production Deployment](#production-deployment)
- [Testing](#testing)
- [Monitoring](#monitoring)

## Prerequisites

### Required
- Python 3.10+
- Docker & Docker Compose
- OpenAI API Key

### Optional
- PostgreSQL (for production)
- Redis (for caching)
- Nginx (for reverse proxy)

## Local Development

### 1. Setup Environment

```bash
# Clone repository
git clone <repository-url>
cd py-agenticai

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment Variables

```bash
# Copy example env file
cp .env.example .env

# Edit .env and add your keys
nano .env
```

Required variables:
```env
OPENAI_API_KEY=your_openai_api_key_here
MODEL_NAME=gpt-4o-mini
LOG_LEVEL=INFO
```

### 3. Run Application

```bash
# Development mode (with auto-reload)
python3 -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# Production mode
python3 -m uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### 4. Access Application

- API: `http://localhost:8000/agenticai/api/v1`
- Docs: `http://localhost:8000/agenticai/docs`
- Health: `http://localhost:8000/health`

## Docker Deployment

### 1. Build Docker Image

```bash
# Build image
docker build -t py-agenticai:latest .

# Check image size
docker images py-agenticai:latest
```

### 2. Run with Docker

```bash
# Run container
docker run -d \
  --name py-agenticai \
  -p 8000:8000 \
  -e OPENAI_API_KEY=your_key_here \
  -v $(pwd)/data:/app/data:ro \
  -v $(pwd)/output:/app/output \
  py-agenticai:latest

# View logs
docker logs -f py-agenticai

# Stop container
docker stop py-agenticai
docker rm py-agenticai
```

### 3. Run with Docker Compose

```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild and restart
docker-compose up -d --build
```

### 4. Test Docker Deployment

```bash
# Run automated tests
./docker-test.sh

# Manual health check
curl http://localhost:8000/health
```

## Production Deployment

### 1. AWS EC2 Deployment

```bash
# SSH into EC2 instance
ssh -i your-key.pem ubuntu@your-ec2-ip

# Install Docker
sudo apt-get update
sudo apt-get install -y docker.io docker-compose

# Clone repository
git clone <repository-url>
cd py-agenticai

# Setup environment
cp .env.example .env
nano .env  # Add production keys

# Deploy with Docker Compose
docker-compose up -d

# Setup Nginx reverse proxy (optional)
sudo apt-get install -y nginx
sudo nano /etc/nginx/sites-available/py-agenticai
```

Nginx configuration:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 2. Kubernetes Deployment

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: py-agenticai
spec:
  replicas: 3
  selector:
    matchLabels:
      app: py-agenticai
  template:
    metadata:
      labels:
        app: py-agenticai
    spec:
      containers:
      - name: py-agenticai
        image: py-agenticai:latest
        ports:
        - containerPort: 8000
        env:
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: api-secrets
              key: openai-key
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: py-agenticai-service
spec:
  selector:
    app: py-agenticai
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
  type: LoadBalancer
```

Deploy:
```bash
kubectl apply -f deployment.yaml
kubectl get pods
kubectl get services
```

### 3. Environment-Specific Configurations

#### Development
```env
LOG_LEVEL=DEBUG
WORKERS=1
```

#### Staging
```env
LOG_LEVEL=INFO
WORKERS=2
```

#### Production
```env
LOG_LEVEL=WARNING
WORKERS=4
```

## Testing

### 1. Unit Tests

```bash
# Run all tests
python3 -m pytest tests/ -v

# Run with coverage
python3 -m pytest tests/ --cov=src --cov-report=html

# View coverage report
open htmlcov/index.html
```

### 2. Integration Tests

```bash
# Test feedback system
python3 test_feedback_direct.py

# Test API endpoints
python3 test_feedback_client.py
```

### 3. Load Testing

```bash
# Install locust
pip install locust

# Create locustfile.py
cat > locustfile.py << 'EOF'
from locust import HttpUser, task, between

class APIUser(HttpUser):
    wait_time = between(1, 3)
    
    @task
    def health_check(self):
        self.client.get("/health")
    
    @task(3)
    def process_feedback(self):
        self.client.post("/agenticai/api/v1/feedback/process")
EOF

# Run load test
locust -f locustfile.py --host=http://localhost:8000
```

## Monitoring

### 1. Application Logs

```bash
# Docker logs
docker-compose logs -f app

# Tail logs
tail -f logs/app.log
```

### 2. Health Monitoring

```bash
# Health check script
cat > health_check.sh << 'EOF'
#!/bin/bash
HEALTH=$(curl -s http://localhost:8000/health | jq -r '.status')
if [ "$HEALTH" != "healthy" ]; then
    echo "Application unhealthy!"
    # Send alert
fi
EOF

# Add to crontab
crontab -e
# */5 * * * * /path/to/health_check.sh
```

### 3. Metrics Collection

```bash
# Install Prometheus exporter
pip install prometheus-fastapi-instrumentator

# Add to src/main.py
from prometheus_fastapi_instrumentator import Instrumentator

Instrumentator().instrument(app).expose(app)
```

## Performance Optimization

### 1. Enable Caching

```python
# Add Redis caching
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

@app.on_event("startup")
async def startup():
    redis = aioredis.from_url("redis://localhost")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
```

### 2. Database Connection Pooling

```python
# Add connection pooling for PostgreSQL
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

engine = create_async_engine(
    "postgresql+asyncpg://user:pass@localhost/db",
    pool_size=20,
    max_overflow=0
)
```

### 3. Worker Configuration

```bash
# Optimal workers = (2 x CPU cores) + 1
# For 4 cores:
uvicorn src.main:app --workers 9 --host 0.0.0.0 --port 8000
```

## Security Best Practices

### 1. Environment Variables

```bash
# Never commit .env files
echo ".env" >> .gitignore

# Use secrets management
# AWS: AWS Secrets Manager
# GCP: Secret Manager
# Azure: Key Vault
```

### 2. HTTPS Configuration

```bash
# Generate SSL certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal
sudo certbot renew --dry-run
```

### 3. Rate Limiting

```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.get("/api/v1/feedback/process")
@limiter.limit("10/minute")
async def process_feedback(request: Request):
    ...
```

## Troubleshooting

### Common Issues

1. **Port already in use**
```bash
lsof -ti:8000 | xargs kill -9
```

2. **Docker build fails**
```bash
docker system prune -a
docker build --no-cache -t py-agenticai:latest .
```

3. **Permission denied**
```bash
sudo chown -R $USER:$USER /app
```

4. **Out of memory**
```bash
# Increase Docker memory limit
docker run -m 2g py-agenticai:latest
```

## Backup & Recovery

### 1. Backup Data

```bash
# Backup output files
tar -czf backup-$(date +%Y%m%d).tar.gz output/

# Backup to S3
aws s3 cp backup-$(date +%Y%m%d).tar.gz s3://your-bucket/backups/
```

### 2. Database Backup

```bash
# PostgreSQL backup
pg_dump -U user -d database > backup.sql

# Restore
psql -U user -d database < backup.sql
```

## Scaling

### Horizontal Scaling

```bash
# Docker Compose scaling
docker-compose up -d --scale app=3

# Kubernetes scaling
kubectl scale deployment py-agenticai --replicas=5
```

### Vertical Scaling

```yaml
# Increase resources
resources:
  requests:
    memory: "512Mi"
    cpu: "500m"
  limits:
    memory: "1Gi"
    cpu: "1000m"
```

## Support

- Documentation: `/docs`
- Issues: GitHub Issues
- Email: support@example.com

---

**Last Updated**: November 2025  
**Version**: 1.0.0  
**Status**: Production Ready ✅
