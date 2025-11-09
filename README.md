# Py-Agentic AI

A FastAPI-based AI application with modular routing, proper separation of concerns, and best practices.

## Features

- ✅ Modular architecture (Routes → Controllers → Services)
- ✅ Pydantic models for request/response validation
- ✅ Environment-based configuration
- ✅ Proper error handling and logging
- ✅ OpenAPI documentation
- ✅ CORS support
- ✅ Health check endpoint
- ✅ Dependency injection

## Project Structure

```
src/
├── controller/          # Business logic layer
│   ├── chat_controller.py
│   └── user_controller.py
├── models/             # Pydantic models
│   ├── chat_models.py
│   └── user_models.py
├── routes/             # API endpoints
│   ├── chat_router.py
│   ├── user_router.py
│   └── main_router.py
├── services/           # External API and data layer
│   └── chat_service.py
├── config.py           # Configuration management
└── main.py            # Application entry point
```

## Setup

### Prerequisites

- Python 3.10+
- pip or poetry

### Installation

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create `.env` file from example:
   ```bash
   cp .env.example .env
   ```

5. Add your OpenAI API key to `.env`:
   ```
   OPENAI_API_KEY=your_actual_api_key_here
   ```

## Running the Application

### Development

```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### Production

```bash
uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## API Endpoints

### Health Check
- `GET /health` - Check application health

### Chat Endpoints
- `GET /api/v1/mainchat/basic` - Get basic chat response
- `POST /api/v1/mainchat/chat` - Send custom message to AI

### User Endpoints
- `GET /api/v1/user/me` - Get current user information
- `POST /api/v1/user/login` - User login

## API Documentation

Once running, visit:
- Swagger UI: `http://localhost:8000/agenticai/docs`
- ReDoc: `http://localhost:8000/agenticai/redoc`

## Configuration

All configuration is managed through environment variables. See `.env.example` for available options.

### Key Configuration Options

- `OPENAI_API_KEY` - Your OpenAI API key (required)
- `MODEL_NAME` - OpenAI model to use (default: gpt-4o-mini)
- `LOG_LEVEL` - Logging level (default: INFO)
- `CORS_ORIGINS` - Allowed CORS origins

## Best Practices Implemented

### 1. Separation of Concerns
- **Routes**: Define HTTP endpoints and handle routing
- **Controllers**: Process requests, validate data, coordinate services
- **Services**: Handle external APIs and business logic
- **Models**: Define data structures and validation

### 2. Configuration Management
- Centralized configuration using Pydantic Settings
- Environment-based configuration
- Type-safe settings with validation

### 3. Error Handling
- Proper HTTP status codes
- Structured error responses
- Comprehensive logging with context

### 4. API Documentation
- OpenAPI/Swagger documentation
- Response models for all endpoints
- Clear endpoint descriptions

### 5. Dependency Injection
- FastAPI's dependency injection system
- Testable controller and service layers

### 6. Security
- No hardcoded credentials
- Environment variable management
- CORS configuration

## Testing

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html
```

## Development Guidelines

### Adding a New Endpoint

1. Create Pydantic models in `src/models/`
2. Create service logic in `src/services/`
3. Create controller in `src/controller/`
4. Create route in `src/routes/`
5. Include router in `main_router.py`

### Code Style

- Follow PEP 8
- Use type hints
- Add docstrings to all functions
- Keep functions focused and small

## License

MIT
