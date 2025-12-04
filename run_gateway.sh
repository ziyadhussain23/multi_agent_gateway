#!/bin/bash
# Run the Multi-Agent Gateway
# All agents are accessible via path routing on port 8000

echo "🚀 Starting Multi-Agent Gateway..."
echo ""
echo "Gateway will be available at: http://localhost:8000"
echo ""
echo "Agent endpoints:"
echo "  📊 Calculator:    http://localhost:8000/a/"
echo "  📝 Todo List:     http://localhost:8000/b/"
echo "  📈 Text Analyzer: http://localhost:8000/c/"
echo ""
echo "API Documentation:"
echo "  🔧 Gateway:       http://localhost:8000/docs"
echo "  🔧 Calculator:    http://localhost:8000/a/docs"
echo "  🔧 Todo List:     http://localhost:8000/b/docs"
echo "  🔧 Text Analyzer: http://localhost:8000/c/docs"
echo ""

cd "$(dirname "$0")"
uvicorn gateway:app --host 0.0.0.0 --port 8000 --reload
