"""Deriva el indice del banco (SC-005, F-010).

Nunca se edita a mano: un indice manual se desincroniza el primer dia.

Uso:
    python codigo/derivar_indice.py
    python codigo/derivar_indice.py --banco banco/piezas --salida banco/INDICE.md
    python codigo/derivar_indice.py --comprobar   (no escribe; falla si esta desactualizado)
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from monoga_core import leer_si_existe, parsear_frontmatter  # noqa: E402

RAIZ = Path(__file__).resolve().parent.parent
BANCO = RAIZ / "banco" / "piezas"
SALIDA = RAIZ / "banco" / "INDICE.md"

CABECERA = """---
generated: true
source: codigo/derivar_indice.py
---

# Indice del banco de contenido

> Archivo generado. No editar a mano: se regenera desde las piezas del banco.
> Solo metadatos de orientacion; el contenido vive en cada pieza.

"""

COLUMNAS = ("ID", "Tema", "Angulo", "Hook elegido", "Estado", "Plataforma", "Fecha")


def filas_del_banco(banco: Path) -> tuple[list[list[str]], list[str]]:
    filas: list[list[str]] = []
    ilegibles: list[str] = []
    for pieza in sorted(banco.glob("*.md")):
        texto = leer_si_existe(pieza)
        if texto is None:
            ilegibles.append(f"{pieza.name} (no se pudo leer)")
            continue
        frontmatter = parsear_frontmatter(texto)
        if not frontmatter:
            ilegibles.append(f"{pieza.name} (sin frontmatter legible)")
            continue
        filas.append(
            [
                frontmatter.get("pieza", "—"),
                frontmatter.get("tema", "—"),
                frontmatter.get("angulo", frontmatter.get("tema", "—")),
                frontmatter.get("hook_elegido", "sin elegir"),
                frontmatter.get("estado", "—"),
                frontmatter.get("plataforma", "—"),
                frontmatter.get("fecha", "—"),
            ]
        )
    return filas, ilegibles


def construir(filas: list[list[str]], ilegibles: list[str]) -> str:
    if not filas:
        return CABECERA + "Banco vacio. Genera la primera pieza.\n"

    partes = [CABECERA]
    partes.append("| " + " | ".join(COLUMNAS) + " |")
    partes.append("|" + "---|" * len(COLUMNAS))
    for fila in filas:
        partes.append("| " + " | ".join(fila) + " |")
    if ilegibles:
        partes.append("")
        partes.append("## Ilegibles")
        partes.append("")
        for item in ilegibles:
            partes.append(f"- {item}")
    return "\n".join(partes) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Deriva banco/INDICE.md desde las piezas.")
    parser.add_argument("--banco", default=str(BANCO))
    parser.add_argument("--salida", default=str(SALIDA))
    parser.add_argument(
        "--comprobar",
        action="store_true",
        help="No escribe: falla si el indice en disco no coincide con el banco.",
    )
    args = parser.parse_args()

    banco = Path(args.banco)
    if not banco.is_absolute():
        banco = (RAIZ / banco).resolve()
    salida = Path(args.salida)
    if not salida.is_absolute():
        salida = (RAIZ / salida).resolve()

    if not banco.exists():
        print(f"El banco no existe: {banco}")
        return 1

    filas, ilegibles = filas_del_banco(banco)
    contenido = construir(filas, ilegibles)

    if args.comprobar:
        actual = leer_si_existe(salida)
        if actual is None:
            print(f"Indice ausente: {salida}")
            return 1
        if actual != contenido:
            print("Indice desactualizado. Ejecuta: python codigo/derivar_indice.py")
            return 1
        print(f"Indice actualizado ({len(filas)} pieza(s)).")
        return 0

    salida.parent.mkdir(parents=True, exist_ok=True)
    salida.write_text(contenido, encoding="utf-8", newline="\n")
    print(f"Indice generado: {salida}")
    print(f"Piezas indexadas: {len(filas)}")
    if ilegibles:
        print(f"Ilegibles: {len(ilegibles)}")
        for item in ilegibles:
            print(f"  - {item}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
