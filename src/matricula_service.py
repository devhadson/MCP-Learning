from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Matricula Service")

STORAGE_FILE = Path(__file__).resolve().parent.parent / "dataset" / "matricula_alumnos.csv"
CSV_FIELDS = ["id", "dni", "nombres", "apellidos", "ciclo", "carrera", "fecha", "costo"]


def ensure_storage() -> None:
    STORAGE_FILE.parent.mkdir(parents=True, exist_ok=True)
    if not STORAGE_FILE.exists():
        with STORAGE_FILE.open("w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(CSV_FIELDS)


def load_students() -> list[dict[str, Any]]:
    ensure_storage()
    with STORAGE_FILE.open("r", newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        return [
            {
                "id": int(row["id"]),
                "dni": row["dni"],
                "nombres": row["nombres"],
                "apellidos": row["apellidos"],
                "ciclo": int(row["ciclo"]),
                "carrera": row["carrera"],
                "fecha": row["fecha"],
                "costo": float(row["costo"]),
            }
            for row in reader
            if row["id"]
        ]


def save_student(student: dict[str, Any]) -> None:
    ensure_storage()
    with STORAGE_FILE.open("a", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=CSV_FIELDS)
        writer.writerow({
            "id": student["id"],
            "dni": student["dni"],
            "nombres": student["nombres"],
            "apellidos": student["apellidos"],
            "ciclo": student["ciclo"],
            "carrera": student["carrera"],
            "fecha": student["fecha"],
            "costo": student["costo"],
        })


def next_student_id() -> int:
    students = load_students()
    if not students:
        return 1
    return max(student["id"] for student in students) + 1


def find_student(student_id: str) -> dict[str, Any] | None:
    students = load_students()
    for student in students:
        if str(student["id"]) == str(student_id):
            return student
    return None


@mcp.tool()
def agregar_estudiante(
    dni: str,
    nombres: str,
    apellidos: str,
    ciclo: int,
    carrera: str,
    fecha: str,
    costo: float,
) -> dict[str, Any]:
    """Agrega un nuevo estudiante al archivo de matrícula."""
    estudiante = {
        "id": next_student_id(),
        "dni": dni,
        "nombres": nombres,
        "apellidos": apellidos,
        "ciclo": ciclo,
        "carrera": carrera,
        "fecha": fecha,
        "costo": costo,
    }
    save_student(estudiante)
    return estudiante


@mcp.tool()
def listar_estudiantes() -> list[dict[str, Any]]:
    """Lista todos los estudiantes registrados en el CSV de matrícula."""
    return load_students()


@mcp.tool()
def obtener_estudiante_por_id(student_id: str) -> dict[str, Any]:
    """Devuelve los datos de un estudiante por su ID."""
    estudiante = find_student(student_id)
    if estudiante is None:
        raise ValueError(f"Estudiante con id {student_id} no encontrado")
    return estudiante


@mcp.resource("resource://estudiantes/{student_id}")
def get_student(student_id: str) -> dict[str, Any] | None:
    """Recurso MCP para recuperar la información de un estudiante."""
    return find_student(student_id)


@mcp.prompt()
def prompt_student_info() -> str:
    """Devuelve un prompt para solicitar los datos de matrícula de un estudiante."""
    return (
        "Por favor, proporciona los datos del estudiante en formato JSON con los campos: "
        "dni, nombres, apellidos, ciclo, carrera, fecha, costo."
    )


if __name__ == "__main__":
    # Ejecutar por STDIO para integrarse con MCP Inspector
    mcp.run(transport="stdio")
