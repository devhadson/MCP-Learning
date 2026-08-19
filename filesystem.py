import sys
from pathlib import Path

from fastmcp import FastMCP

# ---------------------------------------------------------------------------
# 1. Configuración de la ruta raíz (sandbox)
# ---------------------------------------------------------------------------
BASE_DIR = Path(r"C:\Users\User\archivos-mcp").resolve()

# Nos aseguramos de que la carpeta raíz exista antes de aceptar operaciones.
BASE_DIR.mkdir(parents=True, exist_ok=True)

server = FastMCP("filesystem")


def _resolver_ruta_segura(nombre_relativo: str) -> Path:
    """
    Convierte una ruta relativa proporcionada por el modelo en una ruta
    absoluta, verificando que el resultado permanezca dentro de BASE_DIR.

    Lanza ValueError si la ruta intenta escapar del directorio raíz
    (ej. mediante '..' o rutas absolutas ajenas).
    """
    ruta_solicitada = (BASE_DIR / nombre_relativo).resolve()

    if not ruta_solicitada.is_relative_to(BASE_DIR):
        raise ValueError(
            f"Acceso denegado: '{nombre_relativo}' está fuera del "
            f"directorio permitido ({BASE_DIR})."
        )

    return ruta_solicitada


# ---------------------------------------------------------------------------
# 2. Herramienta: listar archivos y carpetas
# ---------------------------------------------------------------------------
@server.tool()
def listar_archivos(subcarpeta: str = "") -> list[str]:
    """
    Lista los archivos y carpetas dentro de C:\\Users\\User\\archivos-mcp.
    Si se especifica 'subcarpeta', lista el contenido de esa subcarpeta
    relativa al directorio raíz. Devuelve rutas relativas al directorio raíz.
    """
    directorio = _resolver_ruta_segura(subcarpeta)

    if not directorio.exists():
        raise FileNotFoundError(f"La ruta '{subcarpeta}' no existe.")
    if not directorio.is_dir():
        raise NotADirectoryError(f"'{subcarpeta}' no es un directorio.")

    elementos = []
    for item in sorted(directorio.iterdir()):
        etiqueta = "[DIR]" if item.is_dir() else "[FILE]"
        ruta_relativa = item.relative_to(BASE_DIR)
        elementos.append(f"{etiqueta} {ruta_relativa}")

    return elementos


# ---------------------------------------------------------------------------
# 3. Herramienta: leer contenido de un archivo
# ---------------------------------------------------------------------------
@server.tool()
def leer_archivo(nombre_archivo: str) -> str:
    """
    Lee y devuelve el contenido de texto de un archivo ubicado dentro de
    C:\\Users\\User\\archivos-mcp. La ruta debe ser relativa al directorio raíz.
    """
    ruta = _resolver_ruta_segura(nombre_archivo)

    if not ruta.exists():
        raise FileNotFoundError(f"El archivo '{nombre_archivo}' no existe.")
    if not ruta.is_file():
        raise IsADirectoryError(f"'{nombre_archivo}' es un directorio, no un archivo.")

    try:
        return ruta.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        raise ValueError(
            f"'{nombre_archivo}' no parece ser un archivo de texto legible en UTF-8."
        )


# ---------------------------------------------------------------------------
# 4. Herramienta: crear un archivo Markdown
# ---------------------------------------------------------------------------
@server.tool()
def crear_archivo_markdown(nombre_archivo: str, contenido: str) -> str:
    """
    Crea un nuevo archivo Markdown (.md) dentro de C:\\Users\\User\\archivos-mcp
    con el contenido proporcionado. Si 'nombre_archivo' no termina en '.md',
    la extensión se agrega automáticamente. No sobrescribe archivos existentes.
    """
    if not nombre_archivo.endswith(".md"):
        nombre_archivo = f"{nombre_archivo}.md"

    ruta = _resolver_ruta_segura(nombre_archivo)

    if ruta.exists():
        raise FileExistsError(
            f"El archivo '{nombre_archivo}' ya existe. Elige otro nombre."
        )

    # Aseguramos que existan las subcarpetas intermedias, si las hubiera.
    ruta.parent.mkdir(parents=True, exist_ok=True)
    ruta.write_text(contenido, encoding="utf-8")

    return f"Archivo creado correctamente en: {ruta.relative_to(BASE_DIR)}"


# ---------------------------------------------------------------------------
# 5. Punto de entrada
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print(f"Servidor 'filesystem' operando sobre: {BASE_DIR}", file=sys.stderr)
    server.run(transport="stdio")