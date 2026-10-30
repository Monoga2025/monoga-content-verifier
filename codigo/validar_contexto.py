"""Verificador del contexto de marca (BR-001, UF-001).

Hace imposible generar contenido de marca sin un contexto valido: comprueba los
campos obligatorios definidos en docs/product/10-DATA-AND-PERMISSIONS.md y
reporta exactamente que falta.

Uso:
    python codigo/validar_contexto.py
    python codigo/validar_contexto.py --archivo marca/contexto-marca.md
    python codigo/validar_contexto.py --json

No escribe nada: solo lee y reporta. Marcar el contexto como VALIDO es decision
humana.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from monoga_core import (  # noqa: E402
    Resultado,
    contenido_completo,
    es_relleno,
    leer_si_existe,
    lineas_utiles,
    normalizar,
    parsear_frontmatter,
    salir,
    secciones,
)

RAIZ = Path(__file__).resolve().parent.parent
CONTEXTO_POR_DEFECTO = RAIZ / "marca" / "contexto-marca.md"

ESTADOS = {"incompleto", "valido", "desactualizado"}


@dataclass(frozen=True)
class Campo:
    """Un campo obligatorio del contexto de marca."""

    clave: str  # clave normalizada de seccion, o nombre del campo de frontmatter
    etiqueta: str  # como se nombra al operador
    minimo: int  # numero minimo de lineas utiles (0 = solo no vacio)
    regla: str
    es_frontmatter: bool = False


# Campos obligatorios: docs/product/10-DATA-AND-PERMISSIONS.md, esquema de
# marca/contexto-marca.md.
CAMPOS: tuple[Campo, ...] = (
    Campo("marca", "marca (frontmatter)", 0, "C-01", es_frontmatter=True),
    Campo("posicionamiento", "Posicionamiento", 0, "C-02"),
    Campo("propuesta de valor", "Propuesta de valor", 0, "C-03"),
    Campo("audiencia.dolores", "Audiencia > Dolores", 3, "C-04"),
    Campo("audiencia.deseos", "Audiencia > Deseos", 3, "C-05"),
    Campo("tono y voz.registro y ritmo", "Tono y voz > Registro y ritmo", 0, "C-06"),
    Campo("tono y voz.lo que nunca decimos", "Tono y voz > Lo que nunca decimos", 3, "C-07"),
    Campo("ofertas vigentes", "Ofertas vigentes", 1, "C-08"),
    Campo("prohibiciones", "Prohibiciones", 3, "C-09"),
    Campo("vocabulario prohibido", "Vocabulario prohibido", 0, "C-10"),
    Campo("ejemplos de voz aprobados", "Ejemplos de voz aprobados", 2, "C-11"),
)


def _buscar_seccion(secciones_doc: dict[str, str], clave: str) -> str | None:
    """Busca por camino completo (`audiencia.dolores`), titulo suelto y subsecciones."""
    clave = normalizar(clave)
    contenido = contenido_completo(secciones_doc, clave)
    if contenido:
        return contenido
    suelto = clave.split(".")[-1]
    contenido = contenido_completo(secciones_doc, suelto)
    return contenido or None


def _termino_vetado(linea: str) -> str:
    """Extrae el termino concreto de una linea de 'lo que nunca decimos'.

    'No decimos "revolucionario".' -> 'revolucionario'. Sin esto, la comparacion
    contra los ejemplos de voz nunca coincidia: se buscaba la frase entera
    ('no decimos revolucionario') en lugar del termino vetado.
    """
    limpio = normalizar(linea)
    limpio = re.sub(r"^[-*>\s]+", "", limpio)
    for marcador in ("no decimos", "nunca decimos", "no usamos", "nunca usamos", "no dir", "no decir"):
        if limpio.startswith(marcador):
            limpio = limpio[len(marcador) :]
            break
    limpio = limpio.replace('"', "").replace("'", "").replace("\u201c", "").replace("\u201d", "")
    limpio = re.sub(r"[.;,]+$", "", limpio).strip()
    return limpio


def verificar(archivo: Path) -> tuple[Resultado, str | None]:
    resultado = Resultado(sujeto=f"contexto de marca ({archivo.name})")

    texto = leer_si_existe(archivo)
    if texto is None:
        resultado.error(
            "C-00",
            f"No se pudo leer el contexto de marca: {archivo}",
            "BR-001",
            f"Crea el archivo en {archivo} con la estructura de docs/product/06-SCREEN-INVENTORY.md (SC-002).",
        )
        return resultado, None

    frontmatter = parsear_frontmatter(texto)
    if not frontmatter:
        resultado.error(
            "C-00b",
            "El contexto no tiene frontmatter legible (falta el bloque --- del inicio).",
            "BR-001",
            "Anade frontmatter con: version, last_validated, status, marca.",
        )

    estado = normalizar(frontmatter.get("status", ""))
    if estado not in ESTADOS:
        resultado.error(
            "C-00c",
            f"El campo status es '{frontmatter.get('status', 'vacio')}'; se espera INCOMPLETO, VALIDO o DESACTUALIZADO.",
            "BR-001",
            "Corrige el campo status del frontmatter.",
        )

    if not normalizar(frontmatter.get("version", "")).isdigit():
        resultado.error(
            "C-00d",
            "Falta el campo version (numero entero) en el frontmatter.",
            "C-09",
            "Anade version: 1 al frontmatter.",
        )

    if not normalizar(frontmatter.get("last_validated", "")):
        resultado.aviso(
            "C-00e",
            "Falta last_validated; sin fecha no se sabe cuando se reviso el contexto por ultima vez.",
            "BR-008",
            "Anade last_validated con la fecha de la ultima revision.",
        )

    cuerpo = texto
    if texto.startswith("---"):
        fin = texto.find("\n---", 3)
        if fin != -1:
            cuerpo = texto[fin + 4 :]
    secciones_doc = secciones(cuerpo)

    faltantes: list[str] = []

    for campo in CAMPOS:
        if campo.es_frontmatter:
            valor = frontmatter.get(campo.clave, "")
            if es_relleno(valor):
                faltantes.append(f"{campo.etiqueta} [{campo.regla}]")
            else:
                resultado.ok(campo.etiqueta)
            continue

        contenido = _buscar_seccion(secciones_doc, normalizar(campo.clave))
        if contenido is None:
            faltantes.append(f"{campo.etiqueta} (seccion ausente) [{campo.regla}]")
            continue
        utiles = lineas_utiles(contenido)
        if len(utiles) < max(campo.minimo, 1):
            necesita = (
                f"requiere al menos {campo.minimo} elementos"
                if campo.minimo > 1
                else "no puede estar vacia"
            )
            faltantes.append(
                f"{campo.etiqueta} (tiene {len(utiles)}; {necesita}) [{campo.regla}]"
            )
            continue
        resultado.ok(f"{campo.etiqueta} ({len(utiles)} elementos)")

    if faltantes:
        detalle = "\n".join(f"  {i}. {f}" for i, f in enumerate(faltantes, 1))
        resultado.error(
            "C-01",
            f"Contexto INCOMPLETO. Faltan {len(faltantes)} campo(s):\n{detalle}",
            "BR-001",
            "Completa esos campos y vuelve a validar. El agente no genera contenido de marca sin contexto valido.",
        )
    else:
        # Coherencia: ejemplos de voz frente a "lo que nunca decimos".
        nunca = _buscar_seccion(secciones_doc, "tono y voz.lo que nunca decimos") or ""
        ejemplos = _buscar_seccion(secciones_doc, "ejemplos de voz aprobados") or ""
        frases_prohibidas = [
            _termino_vetado(l) for l in lineas_utiles(nunca) if not es_relleno(l)
        ]
        texto_ejemplos = normalizar(ejemplos)
        choques = [
            f for f in frases_prohibidas if len(f) > 8 and f in texto_ejemplos
        ]
        if choques:
            resultado.asistido(
                "C-12",
                "Posible contradiccion: 'lo que nunca decimos' incluye frases que aparecen en los ejemplos de voz: "
                + "; ".join(choques[:3]),
                "BR-001",
            )

    return resultado, frontmatter.get("status")


def main() -> int:
    parser = argparse.ArgumentParser(description="Valida el contexto de marca (BR-001).")
    parser.add_argument("--archivo", default=str(CONTEXTO_POR_DEFECTO))
    parser.add_argument("--json", action="store_true", help="Salida en JSON para uso programatico.")
    args = parser.parse_args()

    archivo = Path(args.archivo)
    if not archivo.is_absolute():
        archivo = (RAIZ / archivo).resolve()

    resultado, estado = verificar(archivo)

    if args.json:
        print(
            json.dumps(
                {
                    "aprobado": resultado.aprobado,
                    "sujeto": resultado.sujeto,
                    "comprobados": resultado.comprobados,
                    "hallazgos": [
                        {
                            "severidad": h.severidad,
                            "codigo": h.codigo,
                            "regla": h.regla,
                            "mensaje": h.mensaje,
                            "recuperacion": h.recuperacion,
                        }
                        for h in resultado.ordenados()
                    ],
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0 if resultado.aprobado else 1

    extra: list[str] = []
    if resultado.aprobado:
        extra.append(f"Contexto listo para generar. status declarado: {estado or 'vacio'}")
    else:
        extra.append("No se puede generar ninguna pieza. No se creo nada.")
    return salir(resultado, extra)


if __name__ == "__main__":
    raise SystemExit(main())
