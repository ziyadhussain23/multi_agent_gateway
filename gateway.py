from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager
import os

from agents.a.main import app as calculator_app
from agents.b.main import app as todo_app
from agents.c.main import app as text_analyzer_app

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

AGENTS = {
    "a": {
        "name": "Calculator",
        "description": "Perform basic arithmetic operations",
        "icon": "#",
        "color": "#667eea"
    },
    "b": {
        "name": "Todo List",
        "description": "Manage your tasks and todos",
        "icon": "T",
        "color": "#11998e"
    },
    "c": {
        "name": "Text Analyzer",
        "description": "Analyze text for statistics and sentiment",
        "icon": "A",
        "color": "#ee0979"
    }
}


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Multi-Agent Gateway starting...")
    print(f"Available agents: {', '.join(AGENTS.keys())}")
    yield
    print("Multi-Agent Gateway shutting down...")


app = FastAPI(
    title="Multi-Agent Gateway",
    description="A unified gateway for multiple AI agents",
    version="1.0.0",
    lifespan=lifespan
)

app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "frontend")), name="static")
app.mount("/a", calculator_app)
app.mount("/b", todo_app)
app.mount("/c", text_analyzer_app)


@app.get("/")
async def homepage():
    return FileResponse(os.path.join(BASE_DIR, "frontend", "index.html"))


@app.get("/health")
async def gateway_health():
    return {
        "status": "healthy",
        "gateway": "multi-agent-gateway",
        "agents": list(AGENTS.keys()),
        "agent_count": len(AGENTS)
    }


@app.get("/api/agents")
async def list_agents():
    return {"agents": AGENTS}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
