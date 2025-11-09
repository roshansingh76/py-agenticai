#!/bin/bash

echo "🐳 Docker Build & Test Script"
echo "=============================="
echo ""

# Colors
GREEN='\033[0.32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker is not installed${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Docker is installed${NC}"

# Check if docker-compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo -e "${YELLOW}⚠️  docker-compose not found, using 'docker compose'${NC}"
    DOCKER_COMPOSE="docker compose"
else
    DOCKER_COMPOSE="docker-compose"
fi

# Build Docker image
echo ""
echo "📦 Building Docker image..."
docker build -t py-agenticai:latest . || {
    echo -e "${RED}❌ Docker build failed${NC}"
    exit 1
}

echo -e "${GREEN}✅ Docker image built successfully${NC}"

# Check image size
echo ""
echo "📊 Image size:"
docker images py-agenticai:latest --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}"

# Run tests in Docker
echo ""
echo "🧪 Running tests in Docker container..."
docker run --rm py-agenticai:latest python3 -m pytest tests/test_feedback_system.py -v || {
    echo -e "${RED}❌ Tests failed${NC}"
    exit 1
}

echo -e "${GREEN}✅ All tests passed${NC}"

# Test health endpoint
echo ""
echo "🏥 Testing health endpoint..."
docker run -d --name py-agenticai-test -p 8001:8000 py-agenticai:latest
sleep 5

HEALTH_CHECK=$(curl -s http://localhost:8001/health | grep -o "healthy" || echo "failed")

if [ "$HEALTH_CHECK" == "healthy" ]; then
    echo -e "${GREEN}✅ Health check passed${NC}"
else
    echo -e "${RED}❌ Health check failed${NC}"
fi

# Cleanup
docker stop py-agenticai-test
docker rm py-agenticai-test

echo ""
echo -e "${GREEN}🎉 Docker build and test completed successfully!${NC}"
echo ""
echo "To run the application:"
echo "  docker-compose up -d"
echo ""
echo "To view logs:"
echo "  docker-compose logs -f"
echo ""
echo "To stop:"
echo "  docker-compose down"
