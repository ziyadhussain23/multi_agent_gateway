from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from contextlib import asynccontextmanager
import os

from agents.a.main import app as calculator_app
from agents.b.main import app as todo_app
from agents.c.main import app as text_analyzer_app

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

app.mount("/a", calculator_app)
app.mount("/b", todo_app)
app.mount("/c", text_analyzer_app)


@app.get("/", response_class=HTMLResponse)
async def homepage():
    agent_cards = ""
    for agent_id, agent in AGENTS.items():
        agent_cards += f"""
        <div class="agent-card" style="--accent-color: {agent['color']}">
            <div class="agent-icon">{agent['icon']}</div>
            <h3>{agent['name']}</h3>
            <p>{agent['description']}</p>
            <div class="agent-links">
                <a href="/{agent_id}/" class="btn btn-primary">Open App</a>
                <a href="/{agent_id}/docs" class="btn btn-secondary">API Docs</a>
            </div>
        </div>
        """
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Multi-Agent Gateway</title>
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
                min-height: 100vh;
                color: white;
            }}
            .container {{
                max-width: 1200px;
                margin: 0 auto;
                padding: 40px 20px;
            }}
            header {{
                text-align: center;
                margin-bottom: 50px;
            }}
            h1 {{
                font-size: 3em;
                margin-bottom: 10px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #ee0979 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            }}
            .subtitle {{
                color: #888;
                font-size: 1.2em;
            }}
            .agents-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 30px;
            }}
            .agent-card {{
                background: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 20px;
                padding: 30px;
                transition: all 0.3s ease;
                position: relative;
                overflow: hidden;
            }}
            .agent-card::before {{
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 4px;
                background: var(--accent-color);
            }}
            .agent-card:hover {{
                transform: translateY(-10px);
                box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
                border-color: var(--accent-color);
            }}
            .agent-icon {{
                font-size: 4em;
                margin-bottom: 15px;
            }}
            .agent-card h3 {{
                font-size: 1.5em;
                margin-bottom: 10px;
                color: white;
            }}
            .agent-card p {{
                color: #aaa;
                margin-bottom: 20px;
                line-height: 1.6;
            }}
            .agent-links {{
                display: flex;
                gap: 10px;
            }}
            .btn {{
                padding: 12px 24px;
                border-radius: 8px;
                text-decoration: none;
                font-weight: bold;
                transition: all 0.3s;
                font-size: 0.9em;
            }}
            .btn-primary {{
                background: var(--accent-color);
                color: white;
            }}
            .btn-primary:hover {{
                filter: brightness(1.2);
                transform: scale(1.05);
            }}
            .btn-secondary {{
                background: transparent;
                border: 2px solid var(--accent-color);
                color: var(--accent-color);
            }}
            .btn-secondary:hover {{
                background: var(--accent-color);
                color: white;
            }}
            .status-bar {{
                margin-top: 50px;
                text-align: center;
                padding: 20px;
                background: rgba(255, 255, 255, 0.05);
                border-radius: 10px;
            }}
            .status-indicator {{
                display: inline-block;
                width: 10px;
                height: 10px;
                background: #4CAF50;
                border-radius: 50%;
                margin-right: 8px;
                animation: pulse 2s infinite;
            }}
            @keyframes pulse {{
                0%, 100% {{ opacity: 1; }}
                50% {{ opacity: 0.5; }}
            }}
            footer {{
                text-align: center;
                margin-top: 50px;
                color: #666;
                font-size: 0.9em;
            }}
            footer a {{
                color: #667eea;
                text-decoration: none;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <header>
                <h1>Multi-Agent Gateway</h1>
                <p class="subtitle">Select an agent to get started</p>
            </header>
            
            <div class="agents-grid">
                {agent_cards}
            </div>
            
            <div class="status-bar">
                <span class="status-indicator"></span>
                All agents are running on port 8000
            </div>
            
            <footer>
                <p>
                    Gateway API Docs: <a href="/docs">/docs</a> | 
                    OpenAPI Schema: <a href="/openapi.json">/openapi.json</a>
                </p>
            </footer>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


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
