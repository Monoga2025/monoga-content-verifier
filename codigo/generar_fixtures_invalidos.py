"""Genera las piezas de prueba invalidas: una por constraint.

Cada fixture viola exactamente una cosa (salvo C-06, que por definicion exige un
contenido invalido para que el estado APROBADA sea incoherente). Se generan desde
el fixture valido aplicando una mutacion concreta.

Uso:
    python codigo/generar_fixtures_invalidos.py
"""

from __future__ import annotations

from pathlib import Path

RAIZ = Path(__file__).resolve().parent
FIXTURES = RAIZ / "tests" / "fixtures" / "invalidas"
VALIDA = RAIZ / "tests" / "fixtures" / "pieza_valida.md"

AVISO_VALIDA = (
    "> FIXTURE DE PRUEBA. Pieza correcta usada para demostrar que el verificador\n"
    "> aprueba una pieza completa. No es contenido real de publicacion.\n"
)

CABECERA_AVISO = """> FIXTURE DE PRUEBA INVALIDO A PROPOSITO. Debe fallar {codigo}: {desc}
> No es contenido real y no debe copiarse a banco/piezas/.
"""

# Texto que sustituye a la capa de Deseo para el fixture de superlativo.
DESEO_CON_SUPERLATIVO = "Es un metodo revolucionario que cambia por completo como vendes."


def reemplazar(texto: str, viejo: str, nuevo: str) -> str:
    if viejo not in texto:
        raise SystemExit(f"ERROR: no se encontro el fragmento esperado:\n{viejo[:100]}")
    return texto.replace(viejo, nuevo, 1)


def reemplazar_linea(texto: str, prefijo: str, nuevo: str) -> str:
    """Sustituye la primera linea que empieza por `prefijo`."""
    lineas = texto.split("\n")
    for i, linea in enumerate(lineas):
        if linea.startswith(prefijo):
            lineas[i] = nuevo
            return "\n".join(lineas)
    raise SystemExit(f"ERROR: no se encontro ninguna linea que empiece por: {prefijo}")


def vaciar_capa(texto: str, titulo: str) -> str:
    """Deja el encabezado de la capa y vacia su contenido."""
    lineas = texto.split("\n")
    inicio = lineas.index(titulo)
    fin = inicio + 1
    while fin < len(lineas) and not lineas[fin].startswith("###"):
        fin += 1
    return "\n".join(lineas[: inicio + 1] + [""] + lineas[fin:])


def borrar_seccion(texto: str, titulo: str) -> str:
    lineas = texto.split("\n")
    inicio = lineas.index(titulo)
    fin = inicio + 1
    while fin < len(lineas) and not lineas[fin].startswith("## "):
        fin += 1
    return "\n".join(lineas[:inicio] + lineas[fin:])


MUTACIONES: tuple[tuple[str, str, str, str], ...] = (
    ("C-01", "c01-capa-vacia.md", "C-01", "La capa Interes queda vacia."),
    ("C-02", "c02-cuatro-hooks.md", "C-02", "Solo 4 hooks y sin excepcion_hooks declarada."),
    ("C-03", "c03-disparadores-repetidos.md", "C-03", "Los 5 hooks usan el mismo disparador."),
    ("C-03b", "c03b-hooks-clonados.md", "C-03b", "Dos hooks con el mismo disparador y el mismo angulo."),
    ("C-04", "c04-sin-cta.md", "C-04", "No existe el bloque CTA."),
    ("C-06", "c06-aprobada-con-fallo.md", "C-06", "Estado APROBADA con una capa vacia (falla C-01 y C-06)."),
    ("C-07b", "c07b-estado-invalido.md", "C-07b", "Estado REVISADA, fuera del vocabulario."),
    ("C-05", "c05-descartada-sin-motivo.md", "C-05", "Estado DESCARTADA sin motivo_descarte."),
    ("C-09", "c09-version-contexto-inexistente.md", "C-09", "Referencia al contexto v99, que no existe."),
    ("C-10", "c10-publicada-sin-fecha.md", "C-10", "Estado PUBLICADA sin publicada_el."),
    ("C-11", "c11-framework-desconocido.md", "C-11", "Framework StoryBrand, fuera de la taxonomia."),
    ("C-11b", "c11b-framework-sin-razon.md", "C-11b", "Framework PAS sin razon_framework."),
    ("C-13", "c13-plataforma-no-soportada.md", "C-13", "Plataforma Twitter, no soportada."),
    ("C-14", "c14-disparador-invalido.md", "C-14", "Disparador miedo, fuera del vocabulario cerrado."),
    ("C-06b", "c06b-cifra-no-respaldada.md", "C-06b", "Afirma 2000 euros y un multiplicador que no estan en el contexto."),
    ("C-06c", "c06c-superlativo-no-respaldado.md", "C-06c", "Usa revolucionario, no respaldado por el contexto."),
    ("C-08", "c08-sensible-publicada.md", "C-08", "Tema sensible marcado como publicado."),
    ("C-16", "c16-frontmatter-incompleto.md", "C-16", "Falta el campo tema en el frontmatter."),
)


def aplicar(codigo: str, texto: str) -> str:
    if codigo == "C-01":
        return vaciar_capa(texto, "### Interes (3-10 s)")
    if codigo == "C-02":
        return reemplazar_linea(
            texto,
            "| 5 | Cuanto tardas",
            "",
        ).replace("\n\n\n", "\n\n")
    if codigo == "C-03":
        return (
            texto.replace("| contradiccion |", "| pregunta |")
            .replace("| curiosidad |", "| pregunta |")
            .replace("| perdida |", "| pregunta |")
        )
    if codigo == "C-03b":
        return reemplazar(
            texto,
            "| 3 | Hay un minuto exacto en el que pierdes la venta. | curiosidad | 10 | si | PROPUESTO |",
            "| 3 | La venta se decide mucho antes de que hables de dinero. | curiosidad | 10 | si | PROPUESTO |",
        )
    if codigo == "C-04":
        return borrar_seccion(texto, "## CTA")
    if codigo == "C-06":
        return reemplazar(
            vaciar_capa(texto, "### Deseo (10-20 s)"),
            "estado: BORRADOR",
            "estado: APROBADA",
        )
    if codigo == "C-07b":
        return reemplazar_linea(texto, "estado: ", "estado: REVISADA")
    if codigo == "C-05":
        return reemplazar_linea(texto, "estado: ", "estado: DESCARTADA")
    if codigo == "C-09":
        return reemplazar_linea(texto, "contexto_marca: ", "contexto_marca: v99")
    if codigo == "C-10":
        return reemplazar_linea(texto, "estado: ", "estado: PUBLICADA")
    if codigo == "C-11":
        return reemplazar_linea(texto, "framework: ", "framework: StoryBrand")
    if codigo == "C-11b":
        return reemplazar_linea(texto, "framework: ", "framework: PAS")
    if codigo == "C-13":
        return reemplazar_linea(texto, "plataforma: ", "plataforma: Twitter")
    if codigo == "C-14":
        return reemplazar(
            texto,
            "| perdida | 9 | si | PROPUESTO |",
            "| miedo | 9 | si | PROPUESTO |",
        )
    if codigo == "C-06b":
        return reemplazar(
            texto,
            "La proxima vez sabras en el minuto 3 si la conversacion va a avanzar, sin esperar tres dias para descubrirlo.",
            "Con este metodo ahorras 2000 euros al mes y multiplicas por 3 las llamadas que cierras.",
        )
    if codigo == "C-06c":
        return reemplazar(
            texto,
            "La proxima vez sabras en el minuto 3 si la conversacion va a avanzar, sin esperar tres dias para descubrirlo.",
            DESEO_CON_SUPERLATIVO,
        )
    if codigo == "C-08":
        return reemplazar(
            reemplazar_linea(
                reemplazar_linea(texto, "tema_sensible: ", "tema_sensible: si"),
                "estado: ",
                "estado: PUBLICADA",
            ),
            "publicada_el: —",
            "publicada_el: 2026-10-12",
        )
    if codigo == "C-16":
        return reemplazar_linea(texto, "tema: ", "")
    raise SystemExit(f"ERROR: mutacion no implementada para {codigo}")


def main() -> int:
    FIXTURES.mkdir(parents=True, exist_ok=True)
    base = VALIDA.read_text(encoding="utf-8").replace(AVISO_VALIDA, "")
    base = base.replace("\r\n", "\n")
    # Une parrafos partidos por el wrap del editor para que las mutaciones casen.
    base = reemplazar(
        base,
        "La proxima vez sabras en el minuto 3 si la conversacion va a avanzar, sin esperar\ntres dias para descubrirlo.",
        "La proxima vez sabras en el minuto 3 si la conversacion va a avanzar, sin esperar tres dias para descubrirlo.",
    )

    for codigo, nombre, constraint, descripcion in MUTACIONES:
        cuerpo = aplicar(codigo, base)
        aviso = CABECERA_AVISO.format(codigo=constraint, desc=descripcion)
        texto = cuerpo.replace(
            "# Pieza — por que se pierden clientes en la primera llamada\n",
            "# Pieza — por que se pierden clientes en la primera llamada\n\n" + aviso,
            1,
        )
        (FIXTURES / nombre).write_text(texto, encoding="utf-8", newline="\n")

    print(f"Fixtures invalidos generados: {len(MUTACIONES)} en {FIXTURES}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
