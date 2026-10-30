"""Utilidades comunes del verificador. Sin dependencias externas.

Todo el sistema de verificacion comparte este modulo: normalizacion de texto,
lectura de archivos, frontmatter, tablas markdown y el contrato de salida de
consola definido en docs/product/08-UI-SPEC.md.
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path

# ---------------------------------------------------------------------------
# Normalizacion de texto
# ---------------------------------------------------------------------------

# Marcadores de relleno: un campo con esto NO cuenta como relleno valido.
RELLENO = (
    "...",
    "…",
    "tbd",
    "todo",
    "pendiente",
    "por definir",
    "por rellenar",
    "xxx",
    "<texto>",
    "n/a",
    "na",
)

_TILDES = str.maketrans(
    "áéíóúüñÁÉÍÓÚÜÑ", "aeiouunAEIOUUN"
)


def sin_acentos(texto: str) -> str:
    """Quita acentos conservando el resto del texto."""
    return texto.translate(_TILDES)


def normalizar(texto: str) -> str:
    """Normaliza para comparaciones: minusculas, sin acentos, espacios simples."""
    texto = unicodedata.normalize("NFKC", texto)
    texto = sin_acentos(texto)
    return re.sub(r"\s+", " ", texto).strip().lower()


def a_ascii(texto: str) -> str:
    """Salida de consola en ASCII (evita problemas de codepage en Windows)."""
    return unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode("ascii")


def es_relleno(texto: object) -> bool:
    """True si el valor es vacio, None o solo un marcador de relleno."""
    if texto is None:
        return True
    limpio = normalizar(str(texto))
    limpio = re.sub(r"^[-*>\s]+", "", limpio)
    if not limpio:
        return True
    if limpio in RELLENO:
        return True
    # Solo signos de puntuacion
    if not re.search(r"[a-z0-9]", limpio):
        return True
    return False


PALABRAS_VACIAS = frozenset(
    """
    para como cuando donde porque pero este esta estos estas ese esa esos esas
    que quien cuales cual todo toda todos todas con sin por los las del una uno
    unos unas mas menos muy solo cada entre sobre bajo ante desde hasta hacia
    segun contra segun tambien ademas aunque entonces siempre nunca nada algo
    alguien nadie mismo misma siendo sido esta estan estaba fueron sera seran
    tiene tienen hacer hace pueden puede debe deben
    """.split()
)


def es_palabra_significativa(palabra: str) -> bool:
    return len(palabra) > 3 and palabra not in PALABRAS_VACIAS


def palabras(texto: str) -> list[str]:
    """Palabras significativas normalizadas de un texto."""
    return [
        p
        for p in re.findall(r"[a-z0-9]+", normalizar(texto))
        if es_palabra_significativa(p)
    ]


def solapamiento(a: str, b: str) -> float:
    """Coeficiente de solapamiento de Jaccard sobre palabras significativas."""
    wa, wb = set(palabras(a)), set(palabras(b))
    if not wa or not wb:
        return 0.0
    return len(wa & wb) / len(wa | wb)


# ---------------------------------------------------------------------------
# Hallazgos y resultado
# ---------------------------------------------------------------------------

ERROR = "ERROR"
AVISO = "AVISO"
ASISTIDO = "ASISTIDO"

_ETIQUETA = {ERROR: "FALLO", AVISO: "AVISO", ASISTIDO: "ASISTIDO"}


@dataclass(frozen=True)
class Hallazgo:
    """Un hallazgo de verificacion. `regla` permite citar la regla de negocio."""

    severidad: str
    codigo: str
    mensaje: str
    regla: str = ""
    recuperacion: str = ""

    @property
    def es_error(self) -> bool:
        return self.severidad == ERROR


@dataclass
class Resultado:
    """Resultado de una verificacion, con su evidencia y sus conteos."""

    sujeto: str
    hallazgos: list[Hallazgo] = field(default_factory=list)
    comprobados: list[str] = field(default_factory=list)

    def error(self, codigo: str, mensaje: str, regla: str = "", recuperacion: str = "") -> None:
        self.hallazgos.append(Hallazgo(ERROR, codigo, mensaje, regla, recuperacion))

    def aviso(self, codigo: str, mensaje: str, regla: str = "", recuperacion: str = "") -> None:
        self.hallazgos.append(Hallazgo(AVISO, codigo, mensaje, regla, recuperacion))

    def asistido(self, codigo: str, mensaje: str, regla: str = "") -> None:
        self.hallazgos.append(Hallazgo(ASISTIDO, codigo, mensaje, regla))

    def ok(self, descripcion: str) -> None:
        self.comprobados.append(descripcion)

    @property
    def aprobado(self) -> bool:
        return not any(h.es_error for h in self.hallazgos)

    @property
    def bloqueantes(self) -> list[Hallazgo]:
        return [h for h in self.hallazgos if h.es_error]

    def ordenados(self) -> list[Hallazgo]:
        return sorted(self.hallazgos, key=lambda h: (h.codigo, h.mensaje))


# ---------------------------------------------------------------------------
# Lectura de archivos
# ---------------------------------------------------------------------------


def leer(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def leer_si_existe(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except (FileNotFoundError, IsADirectoryError, PermissionError, UnicodeDecodeError):
        return None


def parsear_frontmatter(texto: str) -> dict[str, str]:
    """Frontmatter YAML simple (clave: valor). Ignora listas y anidamiento."""
    if not texto.startswith("---"):
        return {}
    fin = texto.find("\n---", 3)
    if fin == -1:
        return {}
    datos: dict[str, str] = {}
    for linea in texto[3:fin].splitlines():
        linea = linea.strip()
        if not linea or linea.startswith("#") or linea.startswith("-"):
            continue
        if ":" not in linea:
            continue
        clave, valor = linea.split(":", 1)
        valor = valor.strip()
        if len(valor) >= 2 and valor[0] == valor[-1] and valor[0] in {'"', "'"}:
            valor = valor[1:-1]
        datos[clave.strip().lower()] = valor
    return datos


def cuerpo_sin_frontmatter(texto: str) -> str:
    if not texto.startswith("---"):
        return texto
    fin = texto.find("\n---", 3)
    if fin == -1:
        return texto
    return texto[fin + 4 :]


def secciones(texto: str) -> dict[str, str]:
    """Devuelve {titulo: contenido} para encabezados de nivel 2 a 4.

    La clave usa el camino completo con puntos (`audiencia.dolores`) y, ademas,
    se registra el ultimo titulo por separado (`dolores`) para busquedas simples.
    Una misma clave repetida concatena.
    """
    resultado: dict[str, str] = {}
    pila: dict[int, str] = {}
    buffers: dict[str, list[str]] = {}
    orden: list[str] = []

    def claves_activas() -> list[str]:
        claves: list[str] = []
        niveles = sorted(pila)
        if niveles:
            camino = ".".join(pila[n] for n in niveles)
            claves.append(camino)
            ultimo = pila[niveles[-1]]
            if ultimo not in claves:
                claves.append(ultimo)
        return claves

    def registrar(linea: str) -> None:
        for clave in claves_activas():
            if clave not in buffers:
                buffers[clave] = []
                orden.append(clave)
            buffers[clave].append(linea)

    for linea in texto.splitlines():
        m = re.match(r"^(#{2,4})\s+(.*)$", linea)
        if m:
            nivel = len(m.group(1))
            for existente in [n for n in pila if n >= nivel]:
                del pila[existente]
            pila[nivel] = normalizar(m.group(2))
            continue
        if pila:
            registrar(linea)

    for clave in orden:
        contenido = "\n".join(buffers[clave]).strip()
        if contenido:
            resultado[clave] = contenido
        else:
            resultado.setdefault(clave, "")
    return resultado


def lineas_utiles(contenido: str) -> list[str]:
    """Lineas con contenido real (ni vacias, ni relleno, ni encabezados)."""
    utiles: list[str] = []
    for linea in contenido.splitlines():
        limpia = linea.strip()
        if not limpia or limpia.startswith("#"):
            continue
        if es_relleno(limpia):
            continue
        utiles.append(limpia)
    return utiles


def _coincide_clave(k: str, clave: str) -> bool:
    """True si la seccion `k` es la pedida, una subseccion suya, o un camino que
    termina en ella.

    Cubre los tres casos reales: `audiencia.dolores`, `ejemplos de voz
    aprobados.ejemplo 1` y `capas aida.atencion (0-3 s)` cuando se pide `atencion`.
    """
    if k == clave or k.startswith(clave + ".") or k.endswith("." + clave):
        return True
    for segmento in k.split("."):
        if segmento == clave or segmento.startswith(clave + " ") or segmento.startswith(clave + " ("):
            return True
    return False


def contenido_completo(secciones_doc: dict[str, str], clave: str) -> str:
    """Contenido de una seccion mas el de todas sus subsecciones.

    `ejemplos de voz aprobados` incluye `ejemplos de voz aprobados.ejemplo 1`.
    `atencion` incluye `atencion (0-3 s)`.
    Necesario porque un bloque con subencabezados deja el padre sin lineas propias.
    """
    clave = normalizar(clave)
    partes: list[str] = []
    for k, v in secciones_doc.items():
        if v and _coincide_clave(k, clave):
            partes.append(v)
    return "\n".join(partes).strip()


def tablas(texto: str) -> list[list[list[str]]]:
    """Extrae todas las tablas markdown como lista de filas de celdas."""
    tablas_encontradas: list[list[list[str]]] = []
    filas: list[list[str]] = []

    def cerrar() -> None:
        nonlocal filas
        if len(filas) >= 2:
            tablas_encontradas.append(filas)
        filas = []

    for linea in texto.splitlines():
        limpia = linea.strip()
        if limpia.startswith("|") and limpia.endswith("|") and len(limpia) > 2:
            celdas = [c.strip() for c in limpia.strip("|").split("|")]
            if all(re.fullmatch(r":?-{2,}:?", c) for c in celdas if c):
                continue  # separador de cabecera
            filas.append(celdas)
        else:
            cerrar()
    cerrar()
    return tablas_encontradas


def tabla_con_cabecera(texto: str, primeras_celdas: tuple[str, ...]) -> list[list[str]] | None:
    """Primera tabla cuya cabecera empiece por las celdas indicadas."""
    objetivo = tuple(normalizar(c) for c in primeras_celdas)
    for tabla in tablas(texto):
        if not tabla:
            continue
        cabecera = tuple(normalizar(c) for c in tabla[0])
        if cabecera[: len(objetivo)] == objetivo:
            return tabla[1:]
    return None


# ---------------------------------------------------------------------------
# Contrato de salida (docs/product/08-UI-SPEC.md)
# ---------------------------------------------------------------------------


def imprimir_resultado(resultado: Resultado, extra: list[str] | None = None) -> None:
    """Imprime segun el contrato de texto: ASCII, etiquetas fijas, sin emojis."""
    lineas: list[str] = []
    if resultado.aprobado and not resultado.hallazgos:
        lineas.append(f"VERIFICACION OK - {resultado.sujeto}")
    else:
        lineas.append(f"VERIFICACION - {resultado.sujeto}")

    for hallazgo in resultado.ordenados():
        etiqueta = _ETIQUETA.get(hallazgo.severidad, "AVISO")
        regla = f" ({hallazgo.regla})" if hallazgo.regla else ""
        lineas.append(f"{etiqueta}: [{hallazgo.codigo}]{regla} {hallazgo.mensaje}")
        if hallazgo.recuperacion:
            lineas.append(f"        -> {hallazgo.recuperacion}")

    if extra:
        lineas.extend(extra)

    errores = len(resultado.bloqueantes)
    if resultado.aprobado:
        lineas.append(f"Resultado: APROBADO ({len(resultado.comprobados)} comprobaciones)")
    else:
        lineas.append(f"Resultado: RECHAZADO ({errores} fallo(s) bloqueante(s))")

    for linea in lineas:
        print(a_ascii(linea))


def salir(resultado: Resultado, extra: list[str] | None = None, codigo_ok: int = 0, codigo_fallo: int = 1) -> int:
    imprimir_resultado(resultado, extra)
    return codigo_ok if resultado.aprobado else codigo_fallo
