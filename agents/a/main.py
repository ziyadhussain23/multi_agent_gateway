from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
import os

app = FastAPI(
    title="Calculator Agent",
    description="A simple calculator service with basic arithmetic operations",
    version="1.0.0"
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "frontend")), name="static")


class CalculationRequest(BaseModel):
    a: float
    b: float
    operation: str  # add, subtract, multiply, divide


class CalculationResponse(BaseModel):
    result: float
    operation: str
    expression: str


@app.get("/")
async def serve_frontend():
    return FileResponse(os.path.join(BASE_DIR, "frontend", "index.html"))


@app.get("/health")
async def health_check():
    return {"status": "healthy", "agent": "calculator"}


@app.post("/calculate", response_model=CalculationResponse)
async def calculate(request: CalculationRequest):
    a, b, op = request.a, request.b, request.operation.lower()
    
    operations = {
        "add": (a + b, f"{a} + {b}"),
        "subtract": (a - b, f"{a} - {b}"),
        "multiply": (a * b, f"{a} × {b}"),
        "divide": (a / b if b != 0 else float('inf'), f"{a} ÷ {b}"),
    }
    
    if op not in operations:
        return {"result": 0, "operation": op, "expression": "Invalid operation"}
    
    result, expression = operations[op]
    return CalculationResponse(result=result, operation=op, expression=expression)


@app.get("/api/add")
async def add(a: float, b: float):
    """Add two numbers"""
    return {"result": a + b, "expression": f"{a} + {b}"}


@app.get("/api/subtract")
async def subtract(a: float, b: float):
    """Subtract two numbers"""
    return {"result": a - b, "expression": f"{a} - {b}"}


@app.get("/api/multiply")
async def multiply(a: float, b: float):
    """Multiply two numbers"""
    return {"result": a * b, "expression": f"{a} × {b}"}


@app.get("/api/divide")
async def divide(a: float, b: float):
    """Divide two numbers"""
    if b == 0:
        return {"error": "Division by zero", "result": None}
    return {"result": a / b, "expression": f"{a} ÷ {b}"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
