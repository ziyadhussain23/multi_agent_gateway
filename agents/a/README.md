# Calculator Agent

A simple calculator with basic arithmetic operations.

## Features
- Addition, Subtraction, Multiplication, Division
- Clean web interface
- REST API

## Run Standalone

```bash
chmod +x run.sh
./run.sh
```

Then open: http://localhost:8001

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Web interface |
| POST | `/calculate` | Calculate with JSON body |
| GET | `/api/add?a=1&b=2` | Add two numbers |
| GET | `/api/subtract?a=5&b=3` | Subtract |
| GET | `/api/multiply?a=4&b=5` | Multiply |
| GET | `/api/divide?a=10&b=2` | Divide |

## Example

```bash
curl -X POST http://localhost:8001/calculate \
  -H "Content-Type: application/json" \
  -d '{"a": 10, "b": 5, "operation": "add"}'
```
