from fastmcp import FastMCP

# 1. Inicializamos el servidor FastMCP con un nombre descriptivo
server = FastMCP("MiServidorPython")

# 2. Definimos una herramienta (Tool) usando el decorador @mcp.tool()
@server.tool()
def saludar(nombre: str) -> str:
    """Devuelve un saludo personalizado."""
    return f"Hola {nombre}!"

# 3. Punto de entrada para ejecutar el servidor MCP
if __name__ == "__main__":
    server.run(transport="stdio")