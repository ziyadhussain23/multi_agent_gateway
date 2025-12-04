#!/bin/bash
# Run Calculator Agent standalone on port 8001

echo "🔢 Calculator Agent"
echo "==================="
echo ""
echo "Starting on: http://localhost:8001"
echo "API Docs:    http://localhost:8001/docs"
echo ""

cd "$(dirname "$0")"
source ../../venv/bin/activate 2>/dev/null || source ../../../venv/bin/activate 2>/dev/null || true
uvicorn main:app --host 0.0.0.0 --port 8001 --reload
