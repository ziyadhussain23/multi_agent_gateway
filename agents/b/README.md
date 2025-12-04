# Todo List Agent

A simple task management app with CRUD operations.

## Features
- Create, read, update, delete todos
- Priority levels (low, medium, high)
- Toggle completion status
- Clean web interface

## Run Standalone

```bash
chmod +x run.sh
./run.sh
```

Then open: http://localhost:8002

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Web interface |
| GET | `/api/todos` | Get all todos |
| POST | `/api/todos` | Create a new todo |
| GET | `/api/todos/{id}` | Get a specific todo |
| PUT | `/api/todos/{id}` | Update a todo |
| DELETE | `/api/todos/{id}` | Delete a todo |
| POST | `/api/todos/{id}/toggle` | Toggle completion |

## Example

```bash
# Create a todo
curl -X POST http://localhost:8002/api/todos \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy groceries", "priority": "high"}'

# Get all todos
curl http://localhost:8002/api/todos
```
