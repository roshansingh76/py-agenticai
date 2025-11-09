# Best Practices: Separation of Concerns

## Layer Responsibilities

### ✅ Routes Layer (HTTP Only)

**What Routes SHOULD Do:**
- Define HTTP endpoints (path, method)
- Declare request/response models
- Inject dependencies (controllers)
- Handle HTTP status codes
- Generate API documentation
- Pass data to controllers

**What Routes SHOULD NOT Do:**
- ❌ Business logic
- ❌ Data validation (beyond Pydantic)
- ❌ Database calls
- ❌ External API calls
- ❌ Data transformation
- ❌ Error handling logic

**Example - CORRECT:**
```python
@router.post("/chat", response_model=ChatResponse)
async def post_chat_message(
    request: ChatRequest,
    controller: ChatController = Depends(get_chat_controller)
) -> ChatResponse:
    """Route only handles HTTP concerns"""
    return await controller.handle_chat_message(request)
```

**Example - WRONG:**
```python
@router.post("/chat")
async def post_chat_message(request: ChatRequest):
    """❌ Route contains business logic - BAD!"""
    if not request.message:  # ❌ Business validation
        raise HTTPException(400, "Message required")
    
    client = OpenAI()  # ❌ External API call
    response = client.chat.create(...)  # ❌ Service logic
    return {"response": response}  # ❌ Data transformation
```

---

### ✅ Controllers Layer (Business Logic)

**What Controllers SHOULD Do:**
- Coordinate between routes and services
- Implement business logic
- Validate business rules
- Transform data between layers
- Handle application errors
- Log operations
- Manage transactions

**What Controllers SHOULD NOT Do:**
- ❌ HTTP-specific concerns (status codes in routes)
- ❌ Direct database queries (use services)
- ❌ Direct external API calls (use services)

**Example - CORRECT:**
```python
class ChatController:
    async def handle_chat_message(self, request: ChatRequest) -> ChatResponse:
        """Controller contains ALL business logic"""
        
        # Business validation
        if not request.message.strip():
            raise HTTPException(400, "Message cannot be empty")
        
        # Business logic
        logger.info(f"Processing message: {request.message[:50]}")
        
        # Call service
        response_text = await self.chat_service.get_chat_response(request.message)
        
        # Transform to response model
        return ChatResponse(response=response_text)
```

**Example - WRONG:**
```python
class ChatController:
    async def handle_chat_message(self, request: ChatRequest):
        """❌ Controller doing service work - BAD!"""
        
        # ❌ Direct API call - should be in service
        client = OpenAI(api_key=settings.api_key)
        response = await client.chat.create(...)
        
        return response
```

---

### ✅ Services Layer (External Integration)

**What Services SHOULD Do:**
- Make external API calls
- Execute database queries
- Handle connection management
- Return raw data
- Handle service-specific errors

**What Services SHOULD NOT Do:**
- ❌ Business logic
- ❌ Business validation
- ❌ HTTP exceptions
- ❌ Data transformation for API responses

**Example - CORRECT:**
```python
class ChatService:
    async def get_chat_response(self, message: str) -> str:
        """Service only handles external API"""
        
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": message}]
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"API error: {e}")
            raise  # Let controller handle it
```

**Example - WRONG:**
```python
class ChatService:
    async def get_chat_response(self, message: str):
        """❌ Service contains business logic - BAD!"""
        
        # ❌ Business validation - should be in controller
        if not message.strip():
            raise HTTPException(400, "Message required")
        
        # ❌ Business logic - should be in controller
        logger.info(f"User sent: {message}")
        
        response = await self.client.chat.create(...)
        
        # ❌ Response transformation - should be in controller
        return ChatResponse(response=response)
```

---

## Request Flow

```
1. Client sends HTTP request
   ↓
2. Route receives request
   - Validates request model (Pydantic)
   - Injects controller dependency
   ↓
3. Route calls controller method
   - Passes validated request data
   ↓
4. Controller processes request
   - Validates business rules
   - Logs operation
   - Calls service(s)
   ↓
5. Service executes external operation
   - Makes API call / DB query
   - Returns raw data
   ↓
6. Controller receives service response
   - Transforms to response model
   - Handles errors
   ↓
7. Route receives response model
   - FastAPI validates response
   - Returns HTTP response
   ↓
8. Client receives JSON response
```

---

## Naming Conventions

### Routes
- Use HTTP verb prefix: `get_`, `post_`, `put_`, `delete_`
- Describe the resource: `get_current_user`, `post_chat_message`
- Keep names short and clear

### Controllers
- Use `handle_` prefix: `handle_chat_message`, `handle_user_login`
- Describe the action: `handle_get_current_user`
- Match route purpose

### Services
- Use action verbs: `get_`, `create_`, `update_`, `delete_`
- Describe the operation: `get_chat_response`, `create_user`
- Focus on data operations

---

## Code Examples

### ✅ CORRECT Implementation

**Route:**
```python
@router.post("/chat", response_model=ChatResponse)
async def post_chat_message(
    request: ChatRequest,
    controller: ChatController = Depends(get_chat_controller)
) -> ChatResponse:
    """HTTP concerns only"""
    return await controller.handle_chat_message(request)
```

**Controller:**
```python
async def handle_chat_message(self, request: ChatRequest) -> ChatResponse:
    """Business logic here"""
    # Validate
    if not request.message.strip():
        raise HTTPException(400, "Empty message")
    
    # Log
    logger.info(f"Processing: {request.message[:50]}")
    
    # Call service
    response = await self.chat_service.get_chat_response(request.message)
    
    # Transform
    return ChatResponse(response=response)
```

**Service:**
```python
async def get_chat_response(self, message: str) -> str:
    """External API only"""
    response = await self.client.chat.completions.create(
        model=self.model,
        messages=[{"role": "user", "content": message}]
    )
    return response.choices[0].message.content
```

---

### ❌ WRONG Implementation

**Route with business logic:**
```python
@router.post("/chat")
async def post_chat_message(request: ChatRequest):
    """❌ BAD - Route has business logic"""
    if not request.message.strip():  # ❌ Business validation
        raise HTTPException(400, "Empty")
    
    logger.info(f"Processing: {request.message}")  # ❌ Business logging
    
    service = ChatService()  # ❌ Direct service instantiation
    response = await service.get_chat_response(request.message)
    
    return {"response": response}  # ❌ Manual response building
```

---

## Checklist

### Routes
- [ ] Only HTTP concerns (path, method, status)
- [ ] Uses dependency injection for controllers
- [ ] Declares request/response models
- [ ] No business logic
- [ ] No service calls
- [ ] No data transformation

### Controllers
- [ ] Contains all business logic
- [ ] Validates business rules
- [ ] Coordinates service calls
- [ ] Transforms data between layers
- [ ] Handles application errors
- [ ] Logs operations
- [ ] No HTTP concerns
- [ ] No direct external calls

### Services
- [ ] Only external integrations
- [ ] Makes API/database calls
- [ ] Returns raw data
- [ ] No business logic
- [ ] No business validation
- [ ] No HTTP exceptions
- [ ] No response transformation

---

## Benefits

### Testability
- Routes: Test HTTP concerns only
- Controllers: Mock services, test business logic
- Services: Mock external APIs, test integration

### Maintainability
- Clear responsibilities
- Easy to find code
- Changes isolated to one layer

### Scalability
- Services can be replaced
- Controllers can be reused
- Routes stay simple

### Reusability
- Services can be used by multiple controllers
- Controllers can be used by multiple routes
- Business logic centralized

---

## Common Mistakes

### ❌ Mistake 1: Business Logic in Routes
```python
@router.post("/chat")
async def chat(request: ChatRequest):
    if len(request.message) < 5:  # ❌ Business rule in route
        raise HTTPException(400, "Too short")
```

**✅ Fix:** Move to controller
```python
# Route
@router.post("/chat")
async def chat(request: ChatRequest, controller = Depends(...)):
    return await controller.handle_chat(request)

# Controller
async def handle_chat(self, request):
    if len(request.message) < 5:  # ✅ Business rule in controller
        raise HTTPException(400, "Too short")
```

### ❌ Mistake 2: Service Calls in Routes
```python
@router.post("/chat")
async def chat(request: ChatRequest):
    service = ChatService()  # ❌ Direct service call
    return await service.get_response(request.message)
```

**✅ Fix:** Use controller
```python
@router.post("/chat")
async def chat(request: ChatRequest, controller = Depends(...)):
    return await controller.handle_chat(request)  # ✅ Via controller
```

### ❌ Mistake 3: Business Logic in Services
```python
class ChatService:
    async def get_response(self, message):
        if not message.strip():  # ❌ Business validation
            raise HTTPException(400, "Empty")
        return await self.api_call(message)
```

**✅ Fix:** Move to controller
```python
# Service - only API call
class ChatService:
    async def get_response(self, message):
        return await self.api_call(message)  # ✅ Just API call

# Controller - business logic
async def handle_chat(self, request):
    if not request.message.strip():  # ✅ Validation here
        raise HTTPException(400, "Empty")
    return await self.service.get_response(request.message)
```

---

## Summary

**Remember:**
- **Routes** = HTTP only
- **Controllers** = Business logic
- **Services** = External integration

**Golden Rule:**
> If you're not sure where code belongs, ask:
> - Is it HTTP-related? → Route
> - Is it business logic? → Controller
> - Is it external API/DB? → Service
