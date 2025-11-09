# Quick Start Guide

Get up and running with Py-Agentic AI in 5 minutes!

## Prerequisites
- Python 3.10 or higher
- OpenAI API key

## Installation Steps

### 1. Clone and Setup
```bash
# Navigate to project directory
cd py-agenticai

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment
```bash
# Copy example environment file
cp .env.example .env

# Edit .env and add your OpenAI API key
# OPENAI_API_KEY=your_actual_api_key_here
```

### 4. Run the Application
```bash
# Development mode (with auto-reload)
make dev

# Or using uvicorn directly
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### 5. Test the API

Open your browser and visit:
- **API Documentation**: http://localhost:8000/agenticai/docs
- **Health Check**: http://localhost:8000/health

Or use curl:
```bash
# Health check
curl http://localhost:8000/health

# Basic chat
curl http://localhost:8000/agenticai/api/v1/mainchat/basic

# Custom chat
curl -X POST http://localhost:8000/agenticai/api/v1/mainchat/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, AI!"}'
```

## Common Commands

```bash
# Install dependencies
make install

# Run in development mode
make dev

# Run tests
make test

# Clean cache files
make clean
```

## Troubleshooting

### "OPENAI_API_KEY environment variable is not set"
- Make sure you created `.env` file
- Add your OpenAI API key to `.env`
- Restart the application

### "Module not found" errors
- Activate your virtual environment
- Run `pip install -r requirements.txt`

### Port already in use
- Change the port: `uvicorn src.main:app --reload --port 8001`
- Or kill the process using port 8000

## Next Steps

1. Read the [README.md](README.md) for detailed documentation
2. Check [API_EXAMPLES.md](API_EXAMPLES.md) for usage examples
3. Review [IMPROVEMENTS.md](IMPROVEMENTS.md) to understand the architecture
4. Start building your features!

## Project Structure Overview

```
src/
├── main.py              # Application entry point
├── config.py            # Configuration management
├── routes/              # API endpoints
├── controller/          # Business logic
├── services/            # External API integration
└── models/              # Request/response models
```

## Key Features

✅ OpenAI integration  
✅ Modular architecture  
✅ Type-safe with Pydantic  
✅ Auto-generated API docs  
✅ Proper error handling  
✅ Environment-based config  

Happy coding! 🚀
