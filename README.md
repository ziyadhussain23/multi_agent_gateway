# 🤖 Multi-Agent Gateway

A unified gateway that hosts multiple AI agents on a single port with path-based routing.

## 📁 Project Structure

```
multi_agent_gateway/
├── gateway.py           # Main gateway app
├── run_gateway.sh       # Start the gateway
├── requirements.txt
│
└── agents/
    ├── a/               # 🔢 Calculator
    │   ├── main.py
    │   ├── run.sh       # Run standalone
    │   ├── README.md
    │   └── frontend/
    │
    ├── b/               # 📝 Todo List  
    │   ├── main.py
    │   ├── run.sh       # Run standalone
    │   ├── README.md
    │   └── frontend/
    │
    └── c/               # 📊 Text Analyzer
        ├── main.py
        ├── run.sh       # Run standalone
        ├── README.md
        └── frontend/
```

## 🚀 Quick Start

### 1. Setup

```bash
cd multi_agent_gateway
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Run the Gateway

```bash
./run_gateway.sh
```

### 3. Open in Browser

**Gateway Homepage:** http://localhost:8000

| Agent | App | API Docs |
|-------|-----|----------|
| Calculator | [/a/](http://localhost:8000/a/) | [/a/docs](http://localhost:8000/a/docs) |
| Todo List | [/b/](http://localhost:8000/b/) | [/b/docs](http://localhost:8000/b/docs) |
| Text Analyzer | [/c/](http://localhost:8000/c/) | [/c/docs](http://localhost:8000/c/docs) |

## 🔧 Running Agents Standalone

Each agent can run independently on its own port:

```bash
cd agents/a && ./run.sh

cd agents/b && ./run.sh

cd agents/c && ./run.sh
```

## ➕ Adding a New Agent

1. Create folder: `agents/d/`
2. Add `main.py` with FastAPI app
3. Add `frontend/index.html` for UI
4. Add `run.sh` for standalone mode
5. Mount in `gateway.py`:

```python
from agents.d.main import app as my_agent
app.mount("/d", my_agent)
```

## 🏗️ Architecture

Uses **FastAPI sub-application mounting**:
- All agents run in one process
- Single port (8000) for everything
- Path-based routing: `/a/`, `/b/`, `/c/`
- Each agent has its own API docs

