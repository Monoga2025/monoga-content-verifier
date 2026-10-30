"""Verifica que los siete items del checklist son consistentes entre artefactos.

El orden y el texto de los items se consumen en tres sitios:
  - reglas/checklist.md            (definicion y aproximaciones declaradas)
  - codigo/validar_pieza.py        (ITEMS_CHECKLIST, lo que se evalua)
  - docs/product/08-UI-SPEC.md     (bloque CHECKLIST, el contrato de UI)

Si divergen, el reporte de calidad miente. Esta comprobacion lo detecta.

Uso:
    python codigo/verificar_reglas.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from monoga_core import (  # noqa: E402
    Resultado,
    imprimir_resultado,
    normalizar,
    salir,
    secciones,
    tabla_con_cabecera,
)
from validar_pieza import DISPARADORES, FRAMEWORKS_CONOCIDOS, ITEMS_CHECKLIST  # noqa: E402

RAIZ = Path(__file__).resolve().parent.parent
CHECKLIST = RAIZ / "reglas" / "checklist.md"
UI_SPEC = RAIZ / "docs" / "product" / "08-UI-SPEC.md"
DISPARADORES_DOC = RAIZ / "reglas" / "disparadores.md"
TAXONOMIA = RAIZ / "reglas" / "taxonomia.md"


def _normalizar_item(texto: str) -> str:
    """Normaliza un item para compararlo entre artefactos.

    Los documentos usan el simbolo tipografico `≤` y el codigo usa `<=`. Sin esta
    equivalencia, la comprobacion daria un fallo falso.
    """
    return (
        normalizar(texto)
        .replace("≤", "<=")
        .replace("≥", ">=")
        .replace("  ", " ")
        .strip()
    )


def _items_de_tabla(tabla: list[list[str]] | None, columna: int = 1) -> list[str]:
    if not tabla:
        return []
    return [_normalizar_item(fila[columna]) for fila in tabla if len(fila) > columna]


def main() -> int:
    resultado = Resultado(sujeto="reglas del agente")

    # 1. checklist.md frente a ITEMS_CHECKLIST del codigo
    texto_checklist = CHECKLIST.read_text(encoding="utf-8") if CHECKLIST.exists() else ""
    if not texto_checklist:
        resultado.error("R-01", f"No existe {CHECKLIST}", "BR-007", "Crea el archivo de checklist.")
    else:
        tabla = tabla_con_cabecera(secciones(texto_checklist).get("los siete items", ""), ("#", "item"))
        if tabla is None:
            tabla = tabla_con_cabecera(texto_checklist, ("#", "item"))
        items_doc = _items_de_tabla(tabla)
        items_codigo = [_normalizar_item(t) for t, _, _ in ITEMS_CHECKLIST]
        if len(items_doc) != 7:
            resultado.error(
                "R-01",
                f"reglas/checklist.md define {len(items_doc)} items; se requieren 7.",
                "BR-007",
                "Corrige el archivo de checklist.",
            )
        elif items_doc != items_codigo:
            resultado.error(
                "R-01",
                "Los items de reglas/checklist.md no coinciden (texto u orden) con ITEMS_CHECKLIST de validar_pieza.py.",
                "BR-007",
                "Alinea ambos: el orden del checklist es un contrato.",
            )
        else:
            resultado.ok("checklist.md coincide con ITEMS_CHECKLIST (7 items, mismo orden)")

        # 2. cada item cita su regla BR
        if tabla:
            for fila in tabla:
                if len(fila) < 3 or not fila[2].startswith("BR-"):
                    resultado.error(
                        "R-02",
                        f"El item '{fila[1] if len(fila) > 1 else '?'}' no cita su regla BR.",
                        "BR-007",
                        "Anade la regla de negocio a la que responde el item.",
                    )
            if not any(h.codigo == "R-02" for h in resultado.hallazgos):
                resultado.ok("cada item cita su regla de negocio")

    # 3. ui-spec.md contiene los mismos 7 items
    texto_ui = UI_SPEC.read_text(encoding="utf-8") if UI_SPEC.exists() else ""
    if not texto_ui:
        resultado.error("R-03", f"No existe {UI_SPEC}", "BR-007", "Crea el artefacto de UI spec.")
    else:
        tabla_ui = tabla_con_cabecera(texto_ui, ("item", "regla", "resultado"))
        # La tabla del contrato no lleva columna '#': el item esta en la columna 0.
        items_ui = _items_de_tabla(tabla_ui, columna=0)
        items_codigo = [_normalizar_item(t) for t, _, _ in ITEMS_CHECKLIST]
        if len(items_ui) != 7:
            resultado.error(
                "R-03",
                f"El bloque CHECKLIST de 08-UI-SPEC.md tiene {len(items_ui)} items; se requieren 7.",
                "BR-007",
                "Alinea el bloque CHECKLIST con reglas/checklist.md.",
            )
        elif items_ui != items_codigo:
            resultado.error(
                "R-03",
                "El bloque CHECKLIST de 08-UI-SPEC.md no coincide con reglas/checklist.md (texto u orden).",
                "BR-007",
                "Alinea ambos: el contrato de salida debe describir el checklist real.",
            )
        else:
            resultado.ok("08-UI-SPEC.md declara los mismos 7 items, en el mismo orden")

    # 4. disparadores del codigo frente al documento
    texto_disparadores = DISPARADORES_DOC.read_text(encoding="utf-8") if DISPARADORES_DOC.exists() else ""
    faltan = [
        d for d in sorted(DISPARADORES) if d.replace("_", " ") not in normalizar(texto_disparadores)
        and d not in normalizar(texto_disparadores)
    ]
    if faltan:
        resultado.error(
            "R-04",
            "Disparadores del codigo sin documentar en reglas/disparadores.md: " + ", ".join(faltan),
            "BR-004",
            "Documenta cada disparador o retiralo del vocabulario.",
        )
    else:
        resultado.ok("los 6 disparadores del codigo estan documentados")

    # 5. frameworks del codigo frente a la taxonomia
    texto_taxonomia = TAXONOMIA.read_text(encoding="utf-8") if TAXONOMIA.exists() else ""
    faltan_fw = [
        fw
        for fw in sorted(FRAMEWORKS_CONOCIDOS)
        if fw not in normalizar(texto_taxonomia)
    ]
    if faltan_fw:
        resultado.error(
            "R-05",
            "Frameworks del codigo sin documentar en reglas/taxonomia.md: " + ", ".join(faltan_fw),
            "BR-002",
            "Documenta cada framework admitido.",
        )
    else:
        resultado.ok("los frameworks del codigo estan en la taxonomia")

    return salir(resultado)


if __name__ == "__main__":
    raise SystemExit(main())
