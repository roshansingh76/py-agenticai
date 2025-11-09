# Architecture Documentation

## System Architecture

### High-Level Overview

```
┌─────────────────────────────────────────────────────────────┐
│                         Client Layer                         │
│  (Browser, Mobile App, API Consumer)                        │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP/HTTPS
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                      FastAPI Application                     │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │                    Middleware Layer                     │ │
│  │  • CORS                                                 │ │
│  │  • Logging                                              │ │
│  │  • Error Handling                                       │ │
│  └────────────────────────────────────────────────────────┘ │
│                         │                                    │
│  ┌────────────────────────────────────────────────────────┐ │
│  │                     Routes Layer                        │ │
│  │  • main_router.py                                       │ │
│  │  • user_router.py                                       │ │
│  │  • chat_router.py                                       │ │
│  └────────────────────────────────────────────────────────┘ │
│                         │                                    │
│  ┌────────────────────────────────────────────────────────┐ │
│  │                  Controllers Layer                      │ │
│  │  • UserController                                       │ │
│  │  • ChatController                                       │ │
│  └────────────────────────────────────────────────────────┘ │
│                         │                                    │
│  ┌────────────────────────────────────────────────────────┐ │
│  │                   Services Layer                        │ │
│  │  • ChatService (OpenAI)                                 │ │
│  │  • UserService (Future)                                 │ │
│  └────────────────────────────────────────────────────────┘ │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    External Services                         │
│  • OpenAI API                                               │
│  • Database (Future)                                        │
└─────────────────────────────────────────────────────────────┘
```

## Layer Responsibilities

### 1. Routes Layer
**Purpose**: Define HTTP endpoints and handle routing

**Responsibilities**:
- Define URL paths and HTTP methods
- Declare request/response models
- Inject dependencies (controllers)
- Handle HTTP-specific concerns
- Generate OpenAPI documentation

**Example**:
```python
@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    controller: ChatController = Depends(get_chat_controller)
) -> ChatResponse:
    return await controller.basic_chat(request)
```

### 2. Controllers Layer
**Purpose**: Process requests and coordinate business logic

**Responsibilities**:
- Validate business rules
- Coordinate service calls
- Transform data between layers
- Handle application-level errors
- Log operations

**Example**:
```python
class ChatController:
    async def basic_chat(self, request: ChatRequest) -> ChatResponse:
        try:
            response = await self.chat_service.get_basic_response(request.message)
            return ChatResponse(response=response)
        except Exception as e:
            logger.error(f"Error: {e}")
            raise HTTPException(status_code=500, detail="Error")
```

### 3. Services Layer
**Purpose**: Handle external integrations and data operations

**Responsibilities**:
- Call external APIs
- Manage database operations
- Handle data transformation
- Implement business logic
- Manage connections

**Example**:
```python
class ChatService:
    async def get_basic_response(self, message: str) -> str:
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": message}]
        )
        return response.choices[0].message.content
```

## Request Flow

### Example: Chat Request

```
1. Client sends POST request
   ↓
2. FastAPI receives request at /api/v1/mainchat/chat
   ↓
3. CORS middleware validates origin
   ↓
4. Route handler validates request body against ChatRequest model
   ↓
5. Dependency injection creates ChatController instance
   ↓
6. Controller.basic_chat() is called with validated request
   ↓
7. Controller calls ChatService.get_basic_response()
   ↓
8. Service makes API call to OpenAI
   ↓
9. Service returns response string to Controller
   ↓
10. Controller creates ChatResponse model
   ↓
11. FastAPI validates response against ChatResponse model
   ↓
12. Response is serialized to JSON and sent to client
```

## Data Flow

```
┌──────────────┐
│   Client     │
└──────┬───────┘
       │ ChatRequest JSON
       ▼
┌──────────────────┐
│  Pydantic Model  │ ← Validation
│  ChatRequest     │
└──────┬───────────┘
       │ ChatRequest object
       ▼
┌──────────────────┐
│   Controller     │ ← Business Logic
└──────┬───────────┘
       │ message: str
       ▼
┌──────────────────┐
│    Service       │ ← External API
└──────┬───────────┘
       │ response: str
       ▼
┌──────────────────┐
│   Controller     │ ← Transform
└──────┬───────────┘
       │ ChatResponse object
       ▼
┌──────────────────┐
│  Pydantic Model  │ ← Validation
│  ChatResponse    │
└──────┬───────────┘
       │ ChatResponse JSON
       ▼
┌──────────────┐
│   Client     │
└──────────────┘
```

## Configuration Management

```
┌─────────────┐
│   .env      │ ← Environment variables
└──────┬──────┘
       │
       ▼
┌─────────────────────┐
│  pydantic-settings  │ ← Type-safe loading
│     Settings        │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│   Application       │ ← Global settings instance
│   Components        │
└─────────────────────┘
```

## Dependency Injection

```
Route Handler
    │
    ├─ Depends(get_chat_controller)
    │     │
    │     └─ Creates ChatController
    │           │
    │           └─ Creates ChatService
    │                 │
    │                 └─ Uses settings.openai_api_key
    │
    └─ Calls controller.basic_chat()
```

## Error Handling Flow

```
Service Layer Error
    │
    ├─ Logs error with context
    │
    └─ Raises exception
          │
          ▼
Controller catches exception
    │
    ├─ Logs error
    │
    └─ Raises HTTPException with appropriate status code
          │
          ▼
FastAPI exception handler
    │
    └─ Returns JSON error response to client
```

## Security Layers

```
┌─────────────────────────────────────┐
│  1. CORS Middleware                 │ ← Origin validation
├─────────────────────────────────────┤
│  2. Request Validation              │ ← Pydantic models
├─────────────────────────────────────┤
│  3. Authentication (Future)         │ ← JWT validation
├─────────────────────────────────────┤
│  4. Authorization (Future)          │ ← Permission checks
├─────────────────────────────────────┤
│  5. Rate Limiting (Future)          │ ← Request throttling
└─────────────────────────────────────┘
```

## Module Dependencies

```
main.py
  ├─ config.py
  ├─ routes/
  │   ├─ main_router.py
  │   ├─ user_router.py
  │   │   ├─ controller/user_controller.py
  │   │   └─ models/user_models.py
  │   └─ chat_router.py
  │       ├─ controller/chat_controller.py
  │       │   └─ services/chat_service.py
  │       │       └─ config.py
  │       └─ models/chat_models.py
  └─ middleware (CORS, etc.)
```

## Scalability Considerations

### Horizontal Scaling
- Stateless design allows multiple instances
- No session storage in application
- Configuration via environment variables

### Vertical Scaling
- Async/await for I/O operations
- Connection pooling ready
- Efficient dependency injection

### Future Enhancements
- Add caching layer (Redis)
- Implement message queue (RabbitMQ/Celery)
- Add database connection pooling
- Implement API gateway pattern

## Testing Strategy

```
┌─────────────────────────────────────┐
│         Integration Tests           │
│  (Test full request/response flow)  │
└─────────────────┬───────────────────┘
                  │
    ┌─────────────┼─────────────┐
    │             │             │
    ▼             ▼             ▼
┌─────────┐  ┌─────────┐  ┌─────────┐
│ Route   │  │Controller│  │ Service │
│ Tests   │  │  Tests   │  │  Tests  │
└─────────┘  └─────────┘  └─────────┘
    │             │             │
    └─────────────┼─────────────┘
                  │
                  ▼
         ┌────────────────┐
         │   Unit Tests   │
         │ (Test models)  │
         └────────────────┘
```

## Deployment Architecture

```
┌─────────────────────────────────────┐
│         Load Balancer               │
└────────────┬────────────────────────┘
             │
    ┌────────┼────────┐
    │        │        │
    ▼        ▼        ▼
┌────────┐ ┌────────┐ ┌────────┐
│ App    │ │ App    │ │ App    │
│Instance│ │Instance│ │Instance│
└────┬───┘ └────┬───┘ └────┬───┘
     │          │          │
     └──────────┼──────────┘
                │
                ▼
    ┌───────────────────────┐
    │   External Services   │
    │  • OpenAI API         │
    │  • Database           │
    └───────────────────────┘
```

## Best Practices Applied

1. **Separation of Concerns**: Each layer has a single responsibility
2. **Dependency Injection**: Loose coupling between components
3. **Type Safety**: Pydantic models for validation
4. **Error Handling**: Consistent error responses
5. **Configuration**: Environment-based settings
6. **Documentation**: OpenAPI/Swagger auto-generation
7. **Logging**: Structured logging throughout
8. **Testing**: Testable architecture with DI
9. **Security**: No hardcoded secrets
10. **Scalability**: Stateless, async design
