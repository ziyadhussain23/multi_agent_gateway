"""
Agent B: Todo List Service
A simple todo list API with CRUD operations
"""
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import os
import uuid

app = FastAPI(
    title="Todo Agent",
    description="A todo list service with CRUD operations",
    version="1.0.0"
)

# Get the directory where this script is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Mount static files
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "frontend")), name="static")

# In-memory todo storage
todos = {}


class TodoCreate(BaseModel):
    title: str
    description: Optional[str] = ""
    priority: Optional[str] = "medium"  # low, medium, high


class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    priority: Optional[str] = None


class Todo(BaseModel):
    id: str
    title: str
    description: str
    completed: bool
    priority: str
    created_at: str


@app.get("/")
async def serve_frontend():
    """Serve the todo frontend"""
    return FileResponse(os.path.join(BASE_DIR, "frontend", "index.html"))


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "agent": "todo", "total_todos": len(todos)}


@app.get("/api/todos", response_model=List[Todo])
async def get_todos():
    """Get all todos"""
    return list(todos.values())


@app.post("/api/todos", response_model=Todo)
async def create_todo(todo: TodoCreate):
    """Create a new todo"""
    todo_id = str(uuid.uuid4())[:8]
    new_todo = Todo(
        id=todo_id,
        title=todo.title,
        description=todo.description or "",
        completed=False,
        priority=todo.priority or "medium",
        created_at=datetime.now().isoformat()
    )
    todos[todo_id] = new_todo
    return new_todo


@app.get("/api/todos/{todo_id}", response_model=Todo)
async def get_todo(todo_id: str):
    """Get a specific todo"""
    if todo_id not in todos:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todos[todo_id]


@app.put("/api/todos/{todo_id}", response_model=Todo)
async def update_todo(todo_id: str, update: TodoUpdate):
    """Update a todo"""
    if todo_id not in todos:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    todo = todos[todo_id]
    if update.title is not None:
        todo.title = update.title
    if update.description is not None:
        todo.description = update.description
    if update.completed is not None:
        todo.completed = update.completed
    if update.priority is not None:
        todo.priority = update.priority
    
    todos[todo_id] = todo
    return todo


@app.delete("/api/todos/{todo_id}")
async def delete_todo(todo_id: str):
    """Delete a todo"""
    if todo_id not in todos:
        raise HTTPException(status_code=404, detail="Todo not found")
    del todos[todo_id]
    return {"message": "Todo deleted", "id": todo_id}


@app.post("/api/todos/{todo_id}/toggle")
async def toggle_todo(todo_id: str):
    """Toggle todo completion status"""
    if todo_id not in todos:
        raise HTTPException(status_code=404, detail="Todo not found")
    todos[todo_id].completed = not todos[todo_id].completed
    return todos[todo_id]


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
