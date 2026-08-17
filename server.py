import httpx
from fastmcp import FastMCP

# 1. Inicializamos el servidor FastMCP con un nombre descriptivo
mcp = FastMCP("Servidor Clima Externo")

# 2. Definimos una herramienta (Tool) usando el decorador @mcp.tool()
@mcp.tool()
async def obtener_clima(ciudad: str) -> str:
    """Obtiene la temperatura y condiciones meteorológicas actuales de una ciudad en tiempo real.

    Args:
        ciudad: Nombre de la ciudad a consultar (ej. 'Lima', 'Madrid', 'Mexico City').
    """
    async with httpx.AsyncClient() as client:
        # Paso A: Obtener las coordenadas geográficas de la ciudad
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={ciudad}&count=1&language=es&format=json"
        geo_response = await client.get(geo_url)
        geo_data = geo_response.json()

        if not geo_data.get("results"):
            return f"Error: No se encontraron coordenadas para la ciudad '{ciudad}'."

        lugar = geo_data["results"][0]
        lat, lon = lugar["latitude"], lugar["longitude"]
        nombre_completo = (
            f"{lugar.get('name')}, {lugar.get('country', 'Desconocido')}"
        )

        # Paso B: Consultar la API de clima usando las coordenadas
        clima_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        clima_response = await client.get(clima_url)
        clima_data = clima_response.json()

        if "current_weather" not in clima_data:
            return f"Error: No se pudo obtener el clima para {nombre_completo}."

        actual = clima_data["current_weather"]
        temp = actual.get("temperature")
        viento = actual.get("windspeed")

        return f"El clima actual en {nombre_completo} es de {temp}°C con un viento de {viento} km/h."


# 3. Punto de entrada para ejecutar el servidor MCP
if __name__ == "__main__":
    mcp.run()