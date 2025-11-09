#!/bin/bash

# Deployment script for Py-Agentic AI
# Usage: ./deploy.sh [environment]

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Configuration
ENVIRONMENT=${1:-production}
APP_NAME="py-agenticai"

echo -e "${GREEN}🚀 Deploying Py-Agentic AI to ${ENVIRONMENT}${NC}"
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker is not installed${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Docker is installed${NC}"

# Check if .env file exists
if [ ! -f .env ]; then
    echo -e "${YELLOW}⚠️  .env file not found. Creating from .env.example${NC}"
    if [ -f .env.example ]; then
        cp .env.example .env
        echo -e "${YELLOW}⚠️  Please update .env with your configuration${NC}"
        exit 1
    else
        echo -e "${RED}❌ .env.example not found${NC}"
        exit 1
    fi
fi

echo -e "${GREEN}✅ .env file found${NC}"

# Pull latest changes (if in git repo)
if [ -d .git ]; then
    echo ""
    echo -e "${GREEN}📥 Pulling latest changes...${NC}"
    git pull origin main || echo -e "${YELLOW}⚠️  Could not pull latest changes${NC}"
fi

# Build Docker image
echo ""
echo -e "${GREEN}🔨 Building Docker image...${NC}"
docker build -t ${APP_NAME}:latest . || {
    echo -e "${RED}❌ Docker build failed${NC}"
    exit 1
}

echo -e "${GREEN}✅ Docker image built successfully${NC}"

# Stop existing containers
echo ""
echo -e "${GREEN}🛑 Stopping existing containers...${NC}"
docker compose down || echo -e "${YELLOW}⚠️  No containers to stop${NC}"

# Start new containers
echo ""
echo -e "${GREEN}🚀 Starting containers...${NC}"
docker compose up -d || {
    echo -e "${RED}❌ Failed to start containers${NC}"
    exit 1
}

# Wait for application to start
echo ""
echo -e "${GREEN}⏳ Waiting for application to start...${NC}"
sleep 5

# Health check
echo ""
echo -e "${GREEN}🏥 Performing health check...${NC}"
HEALTH_CHECK=$(curl -s http://localhost:8000/health | grep -o "healthy" || echo "failed")

if [ "$HEALTH_CHECK" == "healthy" ]; then
    echo -e "${GREEN}✅ Health check passed${NC}"
else
    echo -e "${RED}❌ Health check failed${NC}"
    echo ""
    echo "Container logs:"
    docker compose logs --tail=50
    exit 1
fi

# Show running containers
echo ""
echo -e "${GREEN}📊 Running containers:${NC}"
docker compose ps

# Show logs
echo ""
echo -e "${GREEN}📝 Recent logs:${NC}"
docker compose logs --tail=20

echo ""
echo -e "${GREEN}✅ Deployment completed successfully!${NC}"
echo ""
echo "Application is running at:"
echo "  - API: http://localhost:8000/agenticai/api/v1"
echo "  - Docs: http://localhost:8000/agenticai/docs"
echo "  - Health: http://localhost:8000/health"
echo ""
echo "To view logs: docker compose logs -f"
echo "To stop: docker compose down"
