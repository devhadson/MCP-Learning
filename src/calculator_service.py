from argparse import ArgumentParser
from typing import Literal

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from mcp.server.fastmcp import FastMCP

app = FastAPI(
    title="Servicio de Calculadora MCP",
    description="API REST para operaciones básicas y servidor MCP compatible con STDIO.",
    version="1.0.0",
)

mcp = FastMCP("Calculadora MCP")


class OperationRequest(BaseModel):
    a: float
    b: float
    operation: Literal["add", "subtract", "multiply", "divide"]


@app.get("/add")
def add_numbers(a: float, b: float) -> float:
    """Suma los dos valores proporcionados."""
    return a + b


@app.get("/subtract")
def subtract_numbers(a: float, b: float) -> float:
    """Resta `b` de `a`."""
    return a - b


@app.get("/multiply")
def multiply_numbers(a: float, b: float) -> float:
    """Multiplica los dos valores proporcionados."""
    return a * b


@app.get("/divide")
def divide_numbers(a: float, b: float) -> float:
    """Divide `a` entre `b` y maneja el divisor cero."""
    if b == 0:
        raise HTTPException(status_code=400, detail="No se puede dividir entre cero")
    return a / b


@app.post("/calculate")
def calculate(request: OperationRequest) -> float:
    """Ejecuta una operación básica basada en el cuerpo JSON."""
    if request.operation == "add":
        return request.a + request.b
    if request.operation == "subtract":
        return request.a - request.b
    if request.operation == "multiply":
        return request.a * request.b
    if request.operation == "divide":
        if request.b == 0:
            raise HTTPException(status_code=400, detail="No se puede dividir entre cero")
        return request.a / request.b
    raise HTTPException(status_code=400, detail="Operación no válida")


@mcp.tool()
def sumar(a: float, b: float) -> float:
    """Suma dos valores y devuelve el resultado."""
    return a + b


@mcp.tool()
def restar(a: float, b: float) -> float:
    """Resta el segundo valor del primero."""
    return a - b


@mcp.tool()
def multiplicar(a: float, b: float) -> float:
    """Multiplica dos valores y devuelve el producto."""
    return a * b


@mcp.tool()
def dividir(a: float, b: float) -> float:
    """Divide el primer valor entre el segundo y valida divisor cero."""
    if b == 0:
        raise ValueError("No se puede dividir entre cero")
    return a / b


def main() -> None:
    parser = ArgumentParser(description="Servicio de calculadora con FastAPI y MCP STDIO")
    parser.add_argument(
        "--mode",
        choices=["http", "stdio"],
        default="http",
        help="Selecciona el modo de ejecución: http o stdio",
    )
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="Host para el servidor HTTP",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Puerto para el servidor HTTP",
    )
    args = parser.parse_args()

    if args.mode == "http":
        import uvicorn

        uvicorn.run(app, host=args.host, port=args.port, log_level="info")
    else:
        mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
