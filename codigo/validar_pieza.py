"""Verificador de piezas (constraints C-01 a C-15, BR-002 a BR-012).

Es el juez del sistema: impide que una pieza incompleta, incoherente o con
afirmaciones no respaldadas llegue al operador como aprobada.

Uso:
    python codigo/validar_pieza.py banco/piezas/001-mi-tema.md
    python codigo/validar_pieza.py --todas
    python codigo/validar_pieza.py --todas --json
    python codigo/validar_pieza.py pieza.md --escribir-checklist

Solo lee el contenido. Con --escribir-checklist escribe UNICAMENTE el bloque
## Checklist con el veredicto; nunca cambia `estado` (BR-012, eso es humano).
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from monoga_core import (  # noqa: E402
    Resultado,
    contenido_completo,
    cuerpo_sin_frontmatter,
    es_relleno,
    imprimir_resultado,
    leer,
    lineas_utiles,
    normalizar,
    parsear_frontmatter,
    secciones,
    solapamiento,
    tabla_con_cabecera,
)

RAIZ = Path(__file__).resolve().parent.parent
BANCO = RAIZ / "banco" / "piezas"
CONTEXTO = RAIZ / "marca" / "contexto-marca.md"
VERSIONES = RAIZ / "marca" / "versiones"
TAXONOMIA = RAIZ / "reglas" / "taxonomia.md"

# ---------------------------------------------------------------------------
# Vocabularios (reglas/taxonomia.md y reglas/disparadores.md)
# ---------------------------------------------------------------------------

FRAMEWORKS_CONOCIDOS = {
    "aida",
    "hook/substance/payoff",
    "pas",
    "bab",
}

DISPARADORES = {
    "curiosidad",
    "contradiccion",
    "perdida",
    "prueba_social",
    "dato",
    "pregunta",
}

PLATAFORMAS = {"instagram", "tiktok", "youtube", "linkedin"}

FORMATOS_POR_PLATAFORMA = {
    "instagram": {"reel", "carrusel"},
    "tiktok": {"video-corto"},
    "youtube": {"short"},
    "linkedin": {"post-texto", "video-corto"},
}

ESTADOS = {"borrador", "en_revision", "aprobada", "publicada", "descartada"}

CAPAS_AIDA = ("atencion", "interes", "deseo", "accion")

# Mapeo de frameworks alternativos a las capas de AIDA (reglas/aida.md).
MAPEO_CAPAS = {
    "hook/substance/payoff": {
        "hook": ("atencion",),
        "substance": ("interes", "deseo"),
        "payoff": ("accion",),
    },
    "pas": {
        "problema": ("interes",),
        "agitacion": ("deseo",),
        "solucion": ("accion",),
    },
    "bab": {
        "before": ("interes",),
        "after": ("deseo",),
        "bridge": ("accion",),
    },
}

VERBOS_ACCION = {
    "guarda", "guardar", "comenta", "comentar", "escribe", "escribir", "descarga",
    "descargar", "apunta", "apuntar", "prueba", "probar", "empieza", "empezar",
    "pide", "pedir", "reserva", "reservar", "solicita", "solicitar", "entra",
    "entrar", "visita", "visitar", "sigue", "seguir", "suscribete", "unete",
    "unir", "contacta", "contactar", "agenda", "agendar", "mira", "mirar",
    "lee", "leer", "comparte", "compartir", "etiqueta", "etiquetar", "responde",
    "responder", "envia", "enviar", "abre", "abrir", "aplica", "aplicar",
}

SUPERLATIVOS = (
    "revolucionario", "lider", "garantizado", "garantizada", "infalible",
    "unico en el mercado", "mejor del mercado", "sin esfuerzo", "resultados garantizados",
    "numero uno", "el mejor", "la mejor", "increible", "espectacular",
    "milagroso", "definitivo", "insuperable",
)

# Item del checklist -> (texto, regla, tipo, funcion que lo evalua)
ITEMS_CHECKLIST: tuple[tuple[str, str, str], ...] = (
    ("Hook en <=3 s", "BR-006", "Determinista"),
    ("5 hooks con angulos distintos", "BR-004", "Determinista"),
    ("Las 4 capas escritas", "BR-007", "Determinista"),
    ("CTA concreto presente", "BR-003", "Determinista"),
    ("Sin afirmaciones fuera del contexto", "BR-005", "Determinista + asistido"),
    ("Framework declarado", "BR-002", "Determinista"),
    ("Tono alineado con el contexto", "BR-001", "Asistido"),
)

MARCAS_FALLO = ("C-01", "C-02", "C-03", "C-04", "C-06", "C-07", "C-08", "C-11", "C-12", "C-13")
MARCAS_HOOKS = ("C-02", "C-03", "C-14")
MARCAS_CAPAS = ("C-01",)
MARCAS_CTA = ("C-04",)
MARCAS_AFIRMACIONES = ("C-06", "C-07", "C-08", "C-11", "C-12", "C-13")
MARCAS_CONTENIDO = MARCAS_FALLO + MARCAS_CAPAS + MARCAS_CTA


def _enmascarar_justificaciones(texto: str) -> str:
    """Sustituye spans entre comillas por espacios: dentro de una cita se declara
    una excepcion, no se afirma nada."""
    return re.sub(r'"[^"]*"', lambda m: " " * len(m.group(0)), texto)


def _numeros(texto: str) -> set[str]:
    return {
        n.replace(",", ".").rstrip("0").rstrip(".") if "." in n else n
        for n in re.findall(r"\d+(?:[.,]\d+)?", texto)
    }


def _contexto_que_respalda(contexto: str) -> str:
    """Solo el contenido del contexto que puede respaldar una afirmacion.

    Dos exclusiones deliberadas, ambas por fallos reales detectados por fixtures:

    1. 'Prohibiciones' y 'Vocabulario prohibido' son listas de lo que la marca NO
       dice. Tomarlas como respaldo permitiria que un superlativo prohibido pasara
       la verificacion (fallo detectado por C-06c).
    2. Dentro de cualquier seccion se descartan las lineas que *enuncian* una
       prohibicion ("no decimos X", "nunca usamos X"): nombran el termino para
       vetarlo, no para respaldarlo.
    """
    if not contexto:
        return ""
    secciones_doc = secciones(cuerpo_sin_frontmatter(contexto))
    respaldo: list[str] = []
    for clave in (
        "posicionamiento",
        "propuesta de valor",
        "audiencia",
        "tono y voz",
        "ofertas vigentes",
        "ejemplos de voz aprobados",
    ):
        contenido = contenido_completo(secciones_doc, clave)
        if not contenido:
            continue
        for linea in contenido.splitlines():
            if _enuncia_prohibicion(linea):
                continue
            respaldo.append(linea)
    return "\n".join(respaldo)


def _prosa_afirmativa(cuerpo: str) -> str:
    """Solo el contenido que *afirma* algo: excluye encabezados y notas.

    Las lineas que empiezan por `>` son notas del archivo (por ejemplo, la
    cabecera que declara que un fixture es invalido a proposito) y no son
    contenido publicable. Sin esta exclusion, la propia nota que describe una
    cifra inventada contaba como afirmacion y generaba un falso positivo.
    """
    lineas: list[str] = []
    dentro_de_comentario = False
    for linea in cuerpo.splitlines():
        if "<!--" in linea and "-->" not in linea:
            dentro_de_comentario = True
        if dentro_de_comentario:
            if "-->" in linea:
                dentro_de_comentario = False
            continue
        limpia = linea.lstrip()
        if limpia.startswith((">", "#")):
            continue
        lineas.append(linea)
    return "\n".join(lineas)


def _enuncia_prohibicion(linea: str) -> bool:
    """True si la linea nombra un termino para vetarlo, no para respaldarlo."""
    normalizada = normalizar(linea)
    return any(
        marcador in normalizada
        for marcador in (
            "no decimos",
            "nunca decimos",
            "no usamos",
            "nunca usamos",
            "no dir",
            "no decir",
            "prohib",
            "evitar",
            "vetad",
            "sin usar",
        )
    )


def verificar(
    archivo: Path,
    contexto: str | None = None,
    taxonomia: str | None = None,
    versiones_disponibles: set[str] | None = None,
) -> tuple[Resultado, str | None]:
    resultado = Resultado(sujeto=f"pieza ({archivo.name})")
    texto = leer(archivo)
    frontmatter = parsear_frontmatter(texto)
    cuerpo = cuerpo_sin_frontmatter(texto)
    secciones_doc = secciones(cuerpo)

    if not frontmatter:
        resultado.error(
            "C-00",
            "La pieza no tiene frontmatter legible.",
            "BR-002",
            "Anade el frontmatter de docs/product/06-SCREEN-INVENTORY.md (SC-003).",
        )
        return resultado, None

    if contexto is None:
        contexto = ""
    if taxonomia is None:
        taxonomia = ""

    # ---------------- Frontmatter: campos obligatorios ----------------
    obligatorios = {
        "pieza": "identificador",
        "tema": "tema",
        "fecha": "fecha",
        "contexto_marca": "version de contexto",
        "framework": "framework",
        "plataforma": "plataforma",
        "formato": "formato",
        "estado": "estado",
    }
    faltan = [
        etiqueta
        for clave, etiqueta in obligatorios.items()
        if es_relleno(frontmatter.get(clave, ""))
    ]
    if faltan:
        resultado.error(
            "C-16",
            "Frontmatter incompleto. Faltan: " + ", ".join(faltan),
            "BR-002",
            "Completa el frontmatter de la pieza.",
        )

    estado = normalizar(frontmatter.get("estado", ""))
    if estado and estado not in ESTADOS:
        resultado.error(
            "C-07b",
            f"Estado '{frontmatter.get('estado')}' no valido. Admitidos: BORRADOR, EN_REVISION, APROBADA, PUBLICADA, DESCARTADA.",
            "BR-012",
            "Corrige el estado en el frontmatter.",
        )

    # ---------------- C-11: framework declarado ----------------
    framework = normalizar(frontmatter.get("framework", ""))
    razon = frontmatter.get("razon_framework", "").strip()
    if framework not in FRAMEWORKS_CONOCIDOS:
        resultado.error(
            "C-11",
            f"Framework '{frontmatter.get('framework', 'vacio')}' fuera de la taxonomia. Admitidos: AIDA, Hook/Substance/Payoff, PAS, BAB.",
            "BR-002",
            "Declara un framework del catalogo de reglas/taxonomia.md.",
        )
    elif framework != "aida" and es_relleno(razon):
        resultado.error(
            "C-11b",
            f"El framework '{frontmatter.get('framework')}' exige razon_framework no vacia.",
            "BR-002",
            "Explica en razon_framework por que no se usa AIDA en esta pieza.",
        )
    else:
        resultado.ok("framework declarado y admitido")

    # ---------------- C-13: plataforma y formato ----------------
    plataforma = normalizar(frontmatter.get("plataforma", ""))
    formato = normalizar(frontmatter.get("formato", ""))
    if plataforma and plataforma not in PLATAFORMAS:
        resultado.error(
            "C-13",
            f"Plataforma '{frontmatter.get('plataforma')}' no soportada. Soportadas: Instagram, TikTok, YouTube, LinkedIn.",
            "BR-002",
            "Usa una plataforma del catalogo o amplia reglas/taxonomia.md con una decision registrada.",
        )
    elif plataforma and formato and formato not in FORMATOS_POR_PLATAFORMA.get(plataforma, set()):
        admitidos = ", ".join(sorted(FORMATOS_POR_PLATAFORMA.get(plataforma, set())))
        resultado.error(
            "C-13b",
            f"Formato '{frontmatter.get('formato')}' no valido para '{plataforma}'. Admitidos: {admitidos}.",
            "BR-002",
            "Corrige el formato o usa la plataforma correcta.",
        )
    elif plataforma:
        resultado.ok(f"plataforma y formato ({plataforma}/{formato})")

    # ---------------- C-09: la version de contexto referenciada debe existir ----------------
    version_pieza = normalizar(frontmatter.get("contexto_marca", "")).lstrip("v")
    version_contexto = ""
    if contexto:
        version_contexto = normalizar(parsear_frontmatter(contexto).get("version", ""))
    disponibles = set(versiones_disponibles or set())
    if version_contexto:
        disponibles.add(version_contexto)
    if not version_pieza:
        pass  # C-16 ya lo reporta
    elif version_pieza not in disponibles:
        disponible_txt = ", ".join(f"v{v}" for v in sorted(disponibles)) or "ninguna"
        resultado.error(
            "C-09",
            f"La pieza referencia el contexto v{version_pieza}, que no existe. Versiones disponibles: {disponible_txt}.",
            "BR-008",
            "Corrige contexto_marca o crea la version historica en marca/versiones/.",
        )
    elif version_contexto and version_pieza != version_contexto:
        resultado.aviso(
            "C-17",
            f"La pieza referencia el contexto v{version_pieza} y el contexto activo es v{version_contexto}.",
            "BR-008",
            "Revisa la pieza: puede afirmar algo que ya no es cierto (UF-006).",
        )
    else:
        resultado.ok(f"version de contexto referenciada (v{version_pieza})")

    # ---------------- C-01: las cuatro capas ----------------
    capas_requeridas: tuple[str, ...] = CAPAS_AIDA
    if framework in MAPEO_CAPAS:
        # El framework alternativo conserva las 4 capas etiquetadas (reglas/aida.md).
        capas_requeridas = CAPAS_AIDA
    capas_vacias: list[str] = []
    for capa in capas_requeridas:
        # El encabezado puede llevar sufijo de tiempo: "Atencion (0-3 s)".
        contenido = contenido_completo(secciones_doc, capa)
        if not lineas_utiles(contenido):
            capas_vacias.append(capa)
    if capas_vacias:
        nombres = ", ".join(c.capitalize() for c in capas_vacias)
        resultado.error(
            "C-01",
            f"Las 4 capas AIDA no estan completas. Vacias o ausentes: {nombres}.",
            "BR-007",
            "Escribe el contenido de cada capa. Una capa con relleno cuenta como vacia.",
        )
    else:
        resultado.ok("las 4 capas AIDA escritas")

    # ---------------- C-02 y C-03: hooks ----------------
    filas_hooks = tabla_con_cabecera(cuerpo, ("#", "hook", "disparador"))
    num_hooks = len(filas_hooks) if filas_hooks else 0
    excepcion = frontmatter.get("excepcion_hooks", "").strip()
    if filas_hooks is None:
        resultado.error(
            "C-02",
            "No se encontro la tabla de variantes de hook.",
            "BR-004",
            "Anade el bloque 'Variantes de hook' con 5 filas.",
        )
    else:
        if num_hooks != 5:
            if excepcion and not es_relleno(excepcion):
                resultado.aviso(
                    "C-02",
                    f"La pieza tiene {num_hooks} hooks en lugar de 5; se acepta por excepcion declarada: {excepcion}",
                    "BR-004",
                    "Excepcion registrada. Revisa que el motivo sea real.",
                )
            else:
                resultado.error(
                    "C-02",
                    f"La pieza tiene {num_hooks} hooks; se requieren 5. Sin excepcion_hooks con motivo, cualquier otro numero es un fallo.",
                    "BR-004",
                    "Anade las variantes que faltan o declara excepcion_hooks con su motivo.",
                )
        else:
            resultado.ok("5 variantes de hook")

        # Disparadores validos
        disparadores_usados: list[str] = []
        hooks_texto: list[str] = []
        for fila in filas_hooks:
            if len(fila) < 3:
                continue
            hook_texto = fila[1].strip()
            disparador = normalizar(fila[2])
            disparador = re.sub(r"[^a-z_/]", "", disparador.replace(" ", "_"))
            hooks_texto.append(hook_texto)
            if disparador:
                disparadores_usados.append(disparador)
            if disparador and disparador not in DISPARADORES:
                resultado.error(
                    "C-14",
                    f"Disparador '{fila[2]}' fuera del vocabulario cerrado. Admitidos: curiosidad, contradiccion, perdida, prueba_social, dato, pregunta.",
                    "BR-004",
                    "Usa un disparador de reglas/disparadores.md.",
                )
            if es_relleno(hook_texto):
                resultado.error(
                    "C-02b",
                    "Hay una fila de hook sin texto.",
                    "BR-004",
                    "Escribe las 5 variantes completas.",
                )

        distintos = len(set(disparadores_usados))
        if disparadores_usados and distintos < 3:
            resultado.error(
                "C-03",
                f"Solo {distintos} disparador(es) distinto(s) entre {len(disparadores_usados)} hooks. Se requieren al menos 3.",
                "BR-004",
                "Varía el angulo: usa disparadores distintos en al menos 3 de los 5 hooks.",
            )

        # Angulos repetidos: mismo disparador + solapamiento alto
        for i in range(len(hooks_texto)):
            for j in range(i + 1, len(hooks_texto)):
                if not hooks_texto[i] or not hooks_texto[j]:
                    continue
                mismo_disparador = (
                    i < len(disparadores_usados)
                    and j < len(disparadores_usados)
                    and disparadores_usados[i] == disparadores_usados[j]
                )
                similitud = solapamiento(hooks_texto[i], hooks_texto[j])
                if mismo_disparador and similitud >= 0.6:
                    resultado.error(
                        "C-03b",
                        f"Los hooks {i + 1} y {j + 1} comparten disparador y angulo (similitud {similitud:.0%}): son variantes falsas.",
                        "BR-004",
                        "Reescribe uno de los dos con otro angulo.",
                    )

    # ---------------- C-04: CTA ----------------
    cta = secciones_doc.get("cta")
    if cta is None or not lineas_utiles(cta):
        resultado.error(
            "C-04",
            "No hay CTA. La capa Accion exige un CTA explicito y concreto.",
            "BR-003",
            "Anade el bloque 'CTA' con accion, destino y alcanzabilidad.",
        )
    else:
        texto_cta_normalizado = normalizar(cta)
        if "accion:" not in texto_cta_normalizado:
            resultado.error(
                "C-04b",
                "El CTA no declara su 'Accion'.",
                "BR-003",
                "Anade '- **Accion:** <verbo + objeto>'.",
            )
        if "destino" not in texto_cta_normalizado and "siguiente paso" not in texto_cta_normalizado:
            resultado.error(
                "C-04c",
                "El CTA no declara destino ni siguiente paso.",
                "BR-003",
                "Anade el destino o siguiente paso concreto.",
            )
        elif "—" in cta or " - " in cta:
            pasos = [
                l
                for l in lineas_utiles(cta)
                if normalizar(l).startswith("-") and "accion" not in normalizar(l)
            ]
            if len(pasos) > 2:
                # Heuristica suave: no bloquea, avisa.
                resultado.aviso(
                    "C-04d",
                    f"El CTA parece contener {len(pasos)} elementos. Un CTA con varias acciones divide la intencion.",
                    "BR-003",
                    "Deja una sola accion concreta.",
                )
        partes = re.split(r"accion:", texto_cta_normalizado, maxsplit=1)
        cola = partes[1] if len(partes) > 1 else ""
        tiene_verbo = any(v in cola for v in VERBOS_ACCION) or any(
            v in texto_cta_normalizado for v in VERBOS_ACCION
        )
        if not tiene_verbo:
            resultado.aviso(
                "C-04e",
                "El CTA no usa un verbo de accion reconocible.",
                "BR-003",
                "Empieza el CTA con un verbo: guarda, comenta, descarga, escribe...",
            )
        if not any(h.es_error for h in resultado.hallazgos if h.codigo.startswith("C-04")):
            resultado.ok("CTA concreto presente")

    # ---------------- C-06: coherencia estado <-> contenido ----------------
    error_contenido = any(
        h.es_error and h.codigo in MARCAS_CONTENIDO for h in resultado.hallazgos
    )
    if estado in {"aprobada", "publicada"} and error_contenido:
        resultado.error(
            "C-06",
            f"La pieza esta en estado {frontmatter.get('estado')} pero su contenido no cumple: no puede aprobarse con fallos.",
            "BR-007",
            "Corrige los fallos antes de aprobar, o devuelve la pieza a BORRADOR.",
        )

    # ---------------- C-05: motivo de descarte ----------------
    if estado == "descartada" and es_relleno(frontmatter.get("motivo_descarte", "")):
        resultado.error(
            "C-05",
            "Una pieza descartada exige motivo_descarte no vacio (el descarte es informacion).",
            "BR-009",
            "Escribe el motivo del descarte en el frontmatter.",
        )
    elif estado == "descartada":
        resultado.ok("motivo de descarte registrado")

    # ---------------- C-10: fecha de publicacion ----------------
    if estado == "publicada":
        publicada_el = frontmatter.get("publicada_el", "").strip()
        if es_relleno(publicada_el):
            resultado.error(
                "C-10",
                "Una pieza publicada exige publicada_el.",
                "BR-012",
                "Anade la fecha de publicacion.",
            )
        elif normalizar(publicada_el) > normalizar(frontmatter.get("fecha", "")) and re.match(
            r"^\d{4}-\d{2}-\d{2}$", publicada_el
        ):
            resultado.ok(f"fecha de publicacion ({publicada_el})")
    if es_relleno(frontmatter.get("publicada_el", "")) and estado != "publicada":
        pass

    # ---------------- C-08: tema sensible ----------------
    sensible = normalizar(frontmatter.get("tema_sensible", "no"))
    if sensible in {"si", "sí", "true", "yes"}:
        if estado == "publicada":
            resultado.error(
                "C-08",
                "La pieza esta marcada como tema sensible y no puede publicarse sin revision humana explicita registrada.",
                "BR-010",
                "Registra la revision humana antes de publicar.",
            )
        else:
            resultado.aviso(
                "C-08",
                "Tema sensible: requiere revision humana antes de publicar.",
                "BR-010",
                "Revisa la pieza a mano antes de publicarla.",
            )

    # ---------------- BR-005: afirmaciones fuera del contexto ----------------
    prosa = _enmascarar_justificaciones(_prosa_afirmativa(cuerpo))
    contexto_norm = normalizar(_contexto_que_respalda(contexto))
    numeros_contexto = _numeros(contexto_norm)
    # Solo las lineas con unidad explicita cuentan como afirmacion cuantificable.
    patron_cifra = re.compile(
        r"(\d+(?:[.,]\d+)?)\s*(%|por ciento|euros|euro|€|x\b|veces)", re.IGNORECASE
    )
    for linea in prosa.splitlines():
        for coincidencia in patron_cifra.finditer(linea):
            numero = coincidencia.group(1).replace(",", ".")
            if numero in numeros_contexto or numero.rstrip("0").rstrip(".") in numeros_contexto:
                continue
            resultado.error(
                "C-06b",
                f"Afirmacion no respaldada por el contexto: '{coincidencia.group(0).strip()}' no aparece en marca/contexto-marca.md.",
                "BR-005",
                "Quita la cifra o anadela al contexto de marca si el negocio puede respaldarla.",
            )
    for superlativo in SUPERLATIVOS:
        if superlativo in normalizar(prosa) and superlativo not in contexto_norm:
            resultado.error(
                "C-06c",
                f"Afirmacion no respaldada por el contexto: '{superlativo}'.",
                "BR-005",
                "Quita el superlativo o anadelo al contexto si es cierto y demostrable.",
            )
    if not any(h.es_error and h.codigo in MARCAS_AFIRMACIONES for h in resultado.hallazgos):
        resultado.ok("sin afirmaciones cuantificables fuera del contexto (comprobacion determinista)")

    # ---------------- C-15 / 07: tono (asistido) ----------------
    tono = secciones_doc.get("tono y voz") or ""
    ejemplos = secciones_doc.get("ejemplos de voz aprobados") or ""
    if tono and ejemplos:
        resultado.ok("tono y ejemplos de voz disponibles en el contexto")
    resultado.asistido(
        "C-15",
        "Tono alineado con el contexto: comparacion asistida por modelo, no verificada de forma determinista. Requiere lectura humana.",
        "BR-001",
    )

    return resultado, frontmatter.get("estado")


def bloque_checklist(resultado: Resultado) -> str:
    """Genera el bloque ## Checklist con el veredicto, en el orden fijo."""
    codigos_error = {h.codigo for h in resultado.hallazgos if h.es_error}

    def grupo_ok(codigos: tuple[str, ...]) -> bool:
        return not any(c in codigos_error for c in codigos)

    estados = [
        ("APROBADO" if grupo_ok(MARCAS_HOOKS) else "FALLO"),
        ("APROBADO" if grupo_ok(MARCAS_HOOKS) else "FALLO"),
        ("APROBADO" if grupo_ok(MARCAS_CAPAS) else "FALLO"),
        ("APROBADO" if grupo_ok(MARCAS_CTA) else "FALLO"),
        ("APROBADO" if grupo_ok(MARCAS_AFIRMACIONES) else "FALLO"),
        ("APROBADO" if grupo_ok(("C-11", "C-11b", "C-16")) else "FALLO"),
        "ASISTIDO: revisar",
    ]

    lineas = [
        "## Checklist",
        "| # | Item | Regla | Tipo | Resultado |",
        "|---:|---|---|---|---|",
    ]
    for i, ((texto, regla, tipo), estado) in enumerate(zip(ITEMS_CHECKLIST, estados), 1):
        lineas.append(f"| {i} | {texto} | {regla} | {tipo} | {estado} |")
    return "\n".join(lineas)


def escribir_checklist(archivo: Path, resultado: Resultado) -> bool:
    """Reescribe SOLO el bloque ## Checklist. No toca el estado ni el contenido."""
    texto = leer(archivo)
    nuevo = bloque_checklist(resultado)
    patron = re.compile(r"^##\s+Checklist\s*$.*?(?=^##\s|\Z)", re.MULTILINE | re.DOTALL)
    if patron.search(texto):
        actualizado = patron.sub(nuevo + "\n\n", texto)
    else:
        actualizado = texto.rstrip() + "\n\n" + nuevo + "\n"
    if actualizado == texto:
        return False
    archivo.write_text(actualizado, encoding="utf-8")
    return True


def piezas_del_banco() -> list[Path]:
    if not BANCO.exists():
        return []
    return sorted(p for p in BANCO.glob("*.md") if p.is_file())


def main() -> int:
    parser = argparse.ArgumentParser(description="Valida piezas del banco (BR-002 a BR-012).")
    parser.add_argument("archivo", nargs="?", help="Ruta de la pieza a validar.")
    parser.add_argument("--todas", action="store_true", help="Valida todas las piezas del banco.")
    parser.add_argument("--json", action="store_true", help="Salida en JSON.")
    parser.add_argument(
        "--contexto",
        default=None,
        help="Ruta del contexto de marca a usar. Por defecto se resuelve automaticamente.",
    )
    parser.add_argument(
        "--escribir-checklist",
        action="store_true",
        help="Reescribe el bloque ## Checklist con el veredicto (no cambia el estado).",
    )
    args = parser.parse_args()

    contexto = ""
    ruta_contexto: Path | None = None
    if args.contexto:
        ruta_contexto = Path(args.contexto)
        if not ruta_contexto.is_absolute():
            ruta_contexto = (RAIZ / ruta_contexto).resolve()
    elif CONTEXTO.exists():
        ruta_contexto = CONTEXTO
    if ruta_contexto and ruta_contexto.exists():
        contexto = ruta_contexto.read_text(encoding="utf-8")
    taxonomia = TAXONOMIA.read_text(encoding="utf-8") if TAXONOMIA.exists() else ""

    # Version de contexto del fixture (si se valida un fixture) mas las versiones
    # historicas reales. Permite que C-09 distinga "no existe" de "esta anticuada".
    versiones: set[str] = set()
    if VERSIONES.exists():
        for ruta_version in VERSIONES.glob("v*.md"):
            numero = normalizar(ruta_version.stem).lstrip("v")
            if numero:
                versiones.add(numero)
    if ruta_contexto and ruta_contexto.exists():
        numero = normalizar(parsear_frontmatter(contexto).get("version", ""))
        if numero:
            versiones.add(numero)

    if args.todas:
        archivos = piezas_del_banco()
        if not archivos:
            print("Banco vacio. Genera la primera pieza.")
            return 0
    elif args.archivo:
        archivos = [Path(args.archivo)]
    else:
        parser.error("Indica una pieza o usa --todas.")

    resultados: list[tuple[Path, Resultado]] = []
    for archivo in archivos:
        if not archivo.is_absolute():
            archivo = (RAIZ / archivo).resolve()
        if not archivo.exists():
            resultado = Resultado(sujeto=f"pieza ({archivo.name})")
            resultado.error("C-00", f"No existe: {archivo}", "BR-002", "Revisa la ruta.")
            resultados.append((archivo, resultado))
            continue
        resultado, _ = verificar(archivo, contexto, taxonomia, versiones)
        resultados.append((archivo, resultado))
        if args.escribir_checklist:
            escribir_checklist(archivo, resultado)

    if args.json:
        print(
            json.dumps(
                [
                    {
                        "archivo": str(a),
                        "aprobado": r.aprobado,
                        "comprobados": r.comprobados,
                        "hallazgos": [
                            {
                                "severidad": h.severidad,
                                "codigo": h.codigo,
                                "regla": h.regla,
                                "mensaje": h.mensaje,
                                "recuperacion": h.recuperacion,
                            }
                            for h in r.ordenados()
                        ],
                    }
                    for a, r in resultados
                ],
                ensure_ascii=False,
                indent=2,
            )
        )
    else:
        for i, (_, resultado) in enumerate(resultados):
            if i:
                print()
            imprimir_resultado(resultado)

    return 0 if all(r.aprobado for _, r in resultados) else 1


if __name__ == "__main__":
    raise SystemExit(main())
