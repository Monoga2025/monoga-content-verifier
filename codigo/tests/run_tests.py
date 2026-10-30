"""Runner de pruebas del verificador. Sin dependencias externas.

Uso:
    python codigo/tests/run_tests.py
    python codigo/tests/run_tests.py -v

Devuelve codigo de salida distinto de cero si alguna prueba falla, para que sirva
en una comprobacion automatizada o manual.
"""

from __future__ import annotations

import sys
from pathlib import Path

CODIGO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(CODIGO))

from monoga_core import Hallazgo  # noqa: E402
from validar_contexto import verificar as verificar_contexto  # noqa: E402
from validar_pieza import verificar as verificar_pieza  # noqa: E402

FIXTURES = Path(__file__).resolve().parent / "fixtures"
CONTEXTO_VALIDO = FIXTURES / "contexto_valido.md"
PIEZA_VALIDA = FIXTURES / "pieza_valida.md"
INVALIDAS = FIXTURES / "invalidas"

VERSIONES = {"3"}

# Fixture -> constraint que debe fallar (C-06 exige ademas un fallo de contenido).
ESPERADOS: dict[str, tuple[str, ...]] = {
    "c01-capa-vacia.md": ("C-01",),
    "c02-cuatro-hooks.md": ("C-02",),
    "c03-disparadores-repetidos.md": ("C-03",),
    "c03b-hooks-clonados.md": ("C-03b",),
    "c04-sin-cta.md": ("C-04",),
    "c05-descartada-sin-motivo.md": ("C-05",),
    "c06-aprobada-con-fallo.md": ("C-01", "C-06"),
    "c06b-cifra-no-respaldada.md": ("C-06b",),
    "c06c-superlativo-no-respaldado.md": ("C-06c",),
    "c07b-estado-invalido.md": ("C-07b",),
    "c08-sensible-publicada.md": ("C-08",),
    "c09-version-contexto-inexistente.md": ("C-09",),
    "c10-publicada-sin-fecha.md": ("C-10",),
    "c11-framework-desconocido.md": ("C-11",),
    "c11b-framework-sin-razon.md": ("C-11b",),
    "c13-plataforma-no-soportada.md": ("C-13",),
    "c14-disparador-invalido.md": ("C-14",),
    "c16-frontmatter-incompleto.md": ("C-16",),
}

VERBOSO = "-v" in sys.argv
_pasadas = 0
_falladas: list[str] = []


def comprobar(nombre: str, condicion: bool, detalle: str = "") -> None:
    global _pasadas
    if condicion:
        _pasadas += 1
        if VERBOSO:
            print(f"  ok   {nombre}")
    else:
        _falladas.append(f"{nombre}: {detalle}" if detalle else nombre)
        print(f"  FALLO {nombre} {detalle}")


def codigos(resultado) -> set[str]:
    return {h.codigo for h in resultado.hallazgos if h.severidad == "ERROR"}


def contexto_texto() -> str:
    return CONTEXTO_VALIDO.read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# Pruebas
# ---------------------------------------------------------------------------


def probar_contexto() -> None:
    print("Contexto de marca")
    resultado, _ = verificar_contexto(CONTEXTO_VALIDO)
    comprobar("contexto completo aprueba", resultado.aprobado, str([h.mensaje for h in resultado.bloqueantes]))
    comprobar("contexto completo no tiene errores", not resultado.bloqueantes)
    comprobar(
        "contexto completo no inventa contradicciones",
        not any(h.codigo == "C-12" for h in resultado.hallazgos),
    )

    # Un contexto que si se contradice debe disparar el aviso asistido C-12:
    # "lo que nunca decimos" incluye frases que aparecen en los ejemplos de voz.
    contradictorio = FIXTURES / "contexto_contradictorio.md"
    if contradictorio.exists():
        choca, _ = verificar_contexto(contradictorio)
        comprobar(
            "contexto que se contradice dispara C-12",
            any(h.codigo == "C-12" for h in choca.hallazgos),
        )
        comprobar(
            "la contradiccion no bloquea, es asistida",
            choca.aprobado,
        )
    else:
        comprobar("fixture de contradiccion existe", False, "falta contexto_contradictorio.md")

    incompleto, _ = verificar_contexto(FIXTURES / "contexto_incompleto.md")
    comprobar("contexto incompleto se rechaza", not incompleto.aprobado)
    comprobar("contexto incompleto falla C-01", "C-01" in codigos(incompleto))
    mensaje = " ".join(h.mensaje for h in incompleto.bloqueantes)
    for campo in ("Dolores", "Deseos", "Lo que nunca decimos", "Prohibiciones", "Vocabulario prohibido", "Ejemplos de voz"):
        comprobar(f"contexto incompleto nombra '{campo}'", campo in mensaje)

    inexistente, _ = verificar_contexto(FIXTURES / "no-existe.md")
    comprobar("contexto inexistente se rechaza sin excepcion", not inexistente.aprobado)
    comprobar("contexto inexistente falla C-00", "C-00" in codigos(inexistente))


def probar_pieza_valida() -> None:
    print("Pieza valida")
    resultado, _ = verificar_pieza(PIEZA_VALIDA, contexto_texto(), versiones_disponibles=VERSIONES)
    comprobar("pieza valida aprueba", resultado.aprobado, str([h.mensaje for h in resultado.bloqueantes]))
    comprobar("pieza valida sin fallos bloqueantes", not resultado.bloqueantes)
    comprobar("pieza valida reporta el item asistido", any(h.codigo == "C-15" for h in resultado.hallazgos))
    comprobar("pieza valida comprueba las 4 capas", len(resultado.comprobados) >= 6)


def probar_invalidas() -> None:
    print("Piezas invalidas (una por constraint)")
    for nombre, esperados in ESPERADOS.items():
        archivo = INVALIDAS / nombre
        if not archivo.exists():
            comprobar(f"{nombre} existe", False, "fixture ausente")
            continue
        resultado, _ = verificar_pieza(archivo, contexto_texto(), versiones_disponibles=VERSIONES)
        obtenidos = codigos(resultado)
        comprobar(f"{nombre} se rechaza", not resultado.aprobado, f"aprobo con {sorted(obtenidos)}")
        perdidos = [c for c in esperados if c not in obtenidos]
        comprobar(f"{nombre} falla {'+'.join(esperados)}", not perdidos, f"faltan {perdidos}")
        extra = sorted(obtenidos - set(esperados))
        comprobar(f"{nombre} no falla nada de mas", not extra, f"sobran {extra}")


def probar_coherencia_estado() -> None:
    print("Coherencia estado <-> contenido")
    # Una pieza en BORRADOR con una capa vacia no debe disparar C-06.
    base = (INVALIDAS / "c01-capa-vacia.md").read_text(encoding="utf-8")
    resultado, _ = verificar_pieza(INVALIDAS / "c01-capa-vacia.md", contexto_texto(), versiones_disponibles=VERSIONES)
    comprobar("BORRADOR con capa vacia no falla C-06", "C-06" not in codigos(resultado))

    # ... pero la misma pieza en APROBADA si.
    aprobada = INVALIDAS / "c06-aprobada-con-fallo.md"
    resultado2, _ = verificar_pieza(aprobada, contexto_texto(), versiones_disponibles=VERSIONES)
    comprobar("APROBADA con capa vacia falla C-06", "C-06" in codigos(resultado2))


def probar_reglas() -> None:
    print("Consistencia de reglas")
    import subprocess

    proceso = subprocess.run(
        [sys.executable, str(CODIGO / "verificar_reglas.py")],
        capture_output=True,
        text=True,
    )
    comprobar(
        "verificar_reglas.py aprueba",
        proceso.returncode == 0,
        (proceso.stdout or proceso.stderr).strip().replace("\n", " | ")[:300],
    )


def probar_checklist_escrito() -> None:
    print("Escritura del bloque de checklist")
    import shutil
    import tempfile

    from validar_pieza import bloque_checklist, escribir_checklist

    with tempfile.TemporaryDirectory() as tmp:
        copia = Path(tmp) / "pieza.md"
        shutil.copy2(PIEZA_VALIDA, copia)
        resultado, _ = verificar_pieza(copia, contexto_texto(), versiones_disponibles=VERSIONES)
        cambio = escribir_checklist(copia, resultado)
        texto = copia.read_text(encoding="utf-8")
        comprobar("escribir_checklist modifica el archivo", cambio)
        comprobar("escribir_checklist deja 7 items", texto.count("| BR-") == 7)
        comprobar("escribir_checklist marca APROBADO", "APROBADO" in texto)
        comprobar("escribir_checklist marca el item asistido", "ASISTIDO: revisar" in texto)
        comprobar("escribir_checklist no cambia el estado", "estado: BORRADOR" in texto)
        comprobar("escribir_checklist es idempotente", not escribir_checklist(copia, resultado))

        # Con una pieza invalida, el bloque debe marcar FALLO.
        copia2 = Path(tmp) / "invalida.md"
        shutil.copy2(INVALIDAS / "c01-capa-vacia.md", copia2)
        resultado2, _ = verificar_pieza(copia2, contexto_texto(), versiones_disponibles=VERSIONES)
        escribir_checklist(copia2, resultado2)
        texto2 = copia2.read_text(encoding="utf-8")
        comprobar("escribir_checklist marca FALLO en capa vacia", "FALLO" in texto2)
        comprobar("escribir_checklist no aprueba una pieza invalida", "| APROBADO | APROBADO | APROBADO |" not in texto2)


def probar_indice() -> None:
    print("Indice derivado")
    import tempfile

    from derivar_indice import construir, filas_del_banco

    with tempfile.TemporaryDirectory() as tmp:
        banco = Path(tmp)
        vacio = construir([], [])
        comprobar("banco vacio informa", "Banco vacio" in vacio)

        import shutil

        shutil.copy2(PIEZA_VALIDA, banco / "001-prueba.md")
        filas, ilegibles = filas_del_banco(banco)
        comprobar("indice lee una pieza", len(filas) == 1)
        comprobar("indice sin ilegibles", not ilegibles)
        comprobar("indice no incluye el cuerpo", "Attention" not in construir(filas, ilegibles))

        (banco / "roto.md").write_text("sin frontmatter\n", encoding="utf-8")
        filas2, ilegibles2 = filas_del_banco(banco)
        comprobar("indice tolera frontmatter roto", len(filas2) == 1 and len(ilegibles2) == 1)
        comprobar("indice idempotente", construir(*filas_del_banco(banco)) == construir(filas2, ilegibles2))


def main() -> int:
    probar_contexto()
    probar_pieza_valida()
    probar_invalidas()
    probar_coherencia_estado()
    probar_checklist_escrito()
    probar_indice()
    probar_reglas()

    print()
    total = _pasadas + len(_falladas)
    if _falladas:
        print(f"RESULTADO: {len(_falladas)} de {total} pruebas FALLARON")
        for fallo in _falladas:
            print(f"  - {fallo}")
        return 1
    print(f"RESULTADO: {_pasadas}/{total} pruebas correctas")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
