# 🎯 Feedback Analysis System

Intelligent multi-agent system for automated user feedback processing and ticket generation.

## 🚀 Quick Start

### 1. Start the Server

```bash
python3 -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Run the Test Client

```bash
python3 test_feedback_client.py
```

## 📡 API Endpoints

### Base URL
```
http://localhost:8000/agenticai/api/v1/feedback
```

### Available Endpoints

#### 1. Health Check
```bash
GET /feedback/health
```
Check if the feedback system is operational.

#### 2. Process Feedback
```bash
POST /feedback/process
```
Process feedback from default CSV files.

**Example:**
```bash
curl -X POST http://localhost:8000/agenticai/api/v1/feedback/process
```

#### 3. Get Summary
```bash
GET /feedback/summary
```
Get processing summary with metrics.

**Example:**
```bash
curl http://localhost:8000/agenticai/api/v1/feedback/summary
```

#### 4. Get Tickets
```bash
GET /feedback/tickets?category=Bug&priority=Critical
```
Get generated tickets with optional filters.

**Query Parameters:**
- `category`: Bug, Feature Request, Praise, Complaint
- `priority`: Critical, High, Medium, Low

**Example:**
```bash
# Get all tickets
curl http://localhost:8000/agenticai/api/v1/feedback/tickets

# Get only bugs
curl http://localhost:8000/agenticai/api/v1/feedback/tickets?category=Bug

# Get critical priority
curl http://localhost:8000/agenticai/api/v1/feedback/tickets?priority=Critical
```

#### 5. Export Tickets
```bash
POST /feedback/tickets/export?output_path=output/tickets.csv
```
Export tickets to CSV file.

**Example:**
```bash
curl -X POST "http://localhost:8000/agenticai/api/v1/feedback/tickets/export"
```

## 📊 Sample Data

The system includes sample data in `data/` directory:
- `app_store_reviews.csv` - 20 app store reviews
- `support_emails.csv` - 10 support emails

### Categories Detected:
- 🐛 **Bugs** - Crashes, errors, performance issues
- ✨ **Feature Requests** - New feature suggestions
- 👍 **Praise** - Positive feedback
- 😞 **Complaints** - Pricing, service issues
- 🚫 **Spam** - Irrelevant content

## 🏗️ Architecture

```
Routes (HTTP) → Controllers (Logic) → Services (Processing)
```

### Components:

1. **Routes** (`src/routes/feedback_router.py`)
   - Define API endpoints
   - Handle HTTP requests/responses

2. **Controllers** (`src/controller/feedback_controller.py`)
   - Business logic
   - Validation
   - Error handling

3. **Services** (`src/services/feedback_service.py`)
   - Feedback processing
   - Classification
   - Ticket generation

4. **Models** (`src/models/feedback_models.py`)
   - Request/response schemas
   - Data validation

## 📈 Output

Generated tickets include:
- Ticket ID
- Category & Priority
- Title & Description
- Technical details (for bugs)
- Assigned team
- Source information

## 🧪 Testing

### Using Python Client
```bash
python3 test_feedback_client.py
```

### Using cURL
```bash
# Health check
curl http://localhost:8000/agenticai/api/v1/feedback/health

# Process feedback
curl -X POST http://localhost:8000/agenticai/api/v1/feedback/process

# Get summary
curl http://localhost:8000/agenticai/api/v1/feedback/summary
```

### Using Browser
Visit: `http://localhost:8000/agenticai/docs`

Interactive API documentation with Swagger UI.

## 📝 Example Response

```json
{
  "tickets": [
    {
      "ticket_id": "TICK-1001",
      "category": "Bug",
      "title": "[BUG] Application issue on Android",
      "priority": "Critical",
      "status": "Open",
      "assigned_to": "Engineering Team"
    }
  ],
  "metrics": {
    "total_feedback": 30,
    "tickets_created": 28,
    "bugs": 10,
    "features": 8,
    "processing_time": 2.5
  }
}
```

## 🎯 Features

✅ Automated classification  
✅ Priority assignment  
✅ Technical detail extraction  
✅ Team assignment  
✅ CSV export  
✅ REST API  
✅ Filtering & search  

## 🔧 Configuration

Edit `src/services/feedback_service.py` to customize:
- Classification keywords
- Priority rules
- Team assignments

## 📦 Dependencies

- FastAPI - Web framework
- Pandas - Data processing
- Pydantic - Data validation

Install:
```bash
pip install fastapi pandas pydantic uvicorn
```

## 🎓 Use Cases

- SaaS companies processing user feedback
- App developers managing reviews
- Support teams triaging tickets
- Product teams prioritizing features

---

**Built with ❤️ using FastAPI and best practices**
