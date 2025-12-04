#!/bin/bash
# Run Todo Agent standalone on port 8002

echo "📝 Todo List Agent"
echo "=================="
echo ""
echo "Starting on: http://localhost:8002"
echo "API Docs:    http://localhost:8002/docs"
echo ""

cd "$(dirname "$0")"
source ../../venv/bin/activate 2>/dev/null || source ../../../venv/bin/activate 2>/dev/null || true
uvicorn main:app --host 0.0.0.0 --port 8002 --reload
