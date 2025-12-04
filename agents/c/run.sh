#!/bin/bash
# Run Text Analyzer Agent standalone on port 8003

echo "📊 Text Analyzer Agent"
echo "======================"
echo ""
echo "Starting on: http://localhost:8003"
echo "API Docs:    http://localhost:8003/docs"
echo ""

cd "$(dirname "$0")"
source ../../venv/bin/activate 2>/dev/null || source ../../../venv/bin/activate 2>/dev/null || true
uvicorn main:app --host 0.0.0.0 --port 8003 --reload
