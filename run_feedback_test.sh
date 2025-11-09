#!/bin/bash

echo "🎯 Feedback Analysis System - Quick Test"
echo "========================================"
echo ""

# Check if server is running
echo "📡 Checking if server is running..."
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Server is running!"
else
    echo "❌ Server is not running!"
    echo ""
    echo "Please start the server first:"
    echo "  python3 -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000"
    echo ""
    exit 1
fi

echo ""
echo "🧪 Running feedback system tests..."
echo ""

# Run the test client
python3 test_feedback_client.py

echo ""
echo "✅ Test complete!"
echo ""
echo "📚 View API docs at: http://localhost:8000/agenticai/docs"
echo "📁 Check output files in: output/"
