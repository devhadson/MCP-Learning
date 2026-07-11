# Guía de instalación y uso para los servicios MCP

## Requisitos

- Python 3.9 o superior
- Entorno virtual recomendando para aislar dependencias
- Node.Js 24+ (para MCP Inspector)

## Instalación de librerías

1. Abrir PowerShell y navegar al proyecto:

```powershell
cd ..\MCP-Learning
```

2. Crear y activar un entorno virtual:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. Instalar dependencias:

```powershell
pip install -r requirements.txt
```

## Archivos generados

- `requirements.txt`
- `src/my_server_hello.py.py`
- `src/calculator_service.py`

## Cómo ejecutar los servicios creados

### Modo HTTP

Ejecuta el servidor MCP creada:

```powershell
python src/my_server_hello.py --mode=http --host=127.0.0.1 --port=8000
```
Ejecuta el inspector (de otra terminal) apuntando a la URL de tu servidor:

```powershell
npx @modelcontextprotocol/inspector
```
> [!Note]
> En proceso de elaboración