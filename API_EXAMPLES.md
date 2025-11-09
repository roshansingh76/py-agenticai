# API Usage Examples

## Base URL
```
http://localhost:8000/agenticai
```

## Health Check

### Check Application Health
```bash
curl -X GET "http://localhost:8000/health"
```

**Response:**
```json
{
  "status": "healthy",
  "app": "Py-Agentic AI",
  "version": "1.0.0"
}
```

## Chat Endpoints

### Basic Chat (GET)
Get a default chat response from the AI.

```bash
curl -X GET "http://localhost:8000/agenticai/api/v1/mainchat/basic"
```

**Response:**
```json
{
  "response": "Hello! I'm Py-Agentic AI..."
}
```

### Custom Chat (POST)
Send a custom message to the AI.

```bash
curl -X POST "http://localhost:8000/agenticai/api/v1/mainchat/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What can you help me with?"
  }'
```

**Request Body:**
```json
{
  "message": "What can you help me with?"
}
```

**Response:**
```json
{
  "response": "I can help you with..."
}
```

## User Endpoints

### Get Current User
Get information about the currently authenticated user.

```bash
curl -X GET "http://localhost:8000/agenticai/api/v1/user/me" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Response:**
```json
{
  "user_id": "test_user_123",
  "email": "user@example.com",
  "username": "testuser"
}
```

### User Login
Authenticate and receive an access token.

```bash
curl -X POST "http://localhost:8000/agenticai/api/v1/user/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "your_password"
  }'
```

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "your_password"
}
```

**Response:**
```json
{
  "user_id": "test_user_123",
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Invalid request: message is required"
}
```

### 401 Unauthorized
```json
{
  "detail": "Invalid credentials"
}
```

### 500 Internal Server Error
```json
{
  "detail": "An error occurred processing your request"
}
```

## Using with Python Requests

```python
import requests

# Base URL
BASE_URL = "http://localhost:8000/agenticai/api/v1"

# Chat example
response = requests.post(
    f"{BASE_URL}/mainchat/chat",
    json={"message": "Hello, AI!"}
)
print(response.json())

# Login example
response = requests.post(
    f"{BASE_URL}/user/login",
    json={
        "email": "user@example.com",
        "password": "password123"
    }
)
token = response.json()["access_token"]

# Get user with token
response = requests.get(
    f"{BASE_URL}/user/me",
    headers={"Authorization": f"Bearer {token}"}
)
print(response.json())
```

## Using with JavaScript/Fetch

```javascript
// Chat example
const chatResponse = await fetch('http://localhost:8000/agenticai/api/v1/mainchat/chat', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    message: 'Hello, AI!'
  })
});
const chatData = await chatResponse.json();
console.log(chatData);

// Login example
const loginResponse = await fetch('http://localhost:8000/agenticai/api/v1/user/login', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    email: 'user@example.com',
    password: 'password123'
  })
});
const loginData = await loginResponse.json();
const token = loginData.access_token;

// Get user with token
const userResponse = await fetch('http://localhost:8000/agenticai/api/v1/user/me', {
  headers: {
    'Authorization': `Bearer ${token}`
  }
});
const userData = await userResponse.json();
console.log(userData);
```
