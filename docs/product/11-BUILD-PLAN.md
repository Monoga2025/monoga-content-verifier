---
artifact: build-plan
phase: 11
status: approved
reason: ""
last_updated: "2026-10-12"
---

# 11 — Plan de construcción de Agente Generador de Contenido

> Esta es la fase que autoriza escribir código. El plan traduce las fases 1–10 en
> unidades pequeñas y verificables, cada una terminando en valor comprobable. No
> hay tareas tipo "haz el agente".

## Estrategia

**Construir primero el juez, después el escritor.** La unidad más valiosa del
sistema no es la que genera texto: es la que **detecta** una pieza inválida. Si el
verificador funciona, el generador se puede iterar sin miedo y el fallo caro
(R-001 salida genérica, R-005 afirmaciones inventadas) queda contenido por diseño.

Consecuencias de esa estrategia:

1. La Vertical Slice 0 **no incluye generación con modelo**. Incluye validar un
   contexto y validar una pieza escrita a mano. Si eso funciona, la arquitectura
   queda probada de extremo a extremo con una fracción del riesgo.
2. La capa de modelo se añade al final, sobre un verificador que ya funciona.
3. Todo el conocimiento (contexto, AIDA, reglas, checklist) existe como archivos
   antes de que el agente los use, porque el agente que los lee es la última pieza,
   no la primera.

**Sin infraestructura, sin dependencias.** Python 3.14 estándar. Sin `pip install`.
Sin servidor. Sin base de datos (ADR-002, ADR-003).

## Orden de entrega

Adaptado a un producto sin auth, sin layout y sin servidor (los pasos 1–3 del orden
genérico se colapsan):

1. **Setup:** estructura del repositorio y control de versiones.
2. **Verificador de contexto:** la puerta que hace imposible generar sin contexto.
3. **Contexto de marca real:** contenido, no código.
4. **Reglas y checklist:** el conocimiento AIDA escrito.
5. **Verificador de pieza:** las 15 constraints del dominio.
6. **Índice derivado.**
7. **Agente generador:** la única escritura del agente.
8. **Prueba de generación:** primer spike con salida real del modelo.
9. **Ciclo de vida humano:** aprobar, publicar, descartar, medir.
10. **Tests del verificador** y cierre de los constraints no cubiertos.
11. **QA, puesta en uso y handoff.**

## Vertical Slice 0 propuesta

- **Nombre:** `VS-0 — Contexto válido, pieza verificable`
- **Valor:** el operador puede (a) saber si su contexto de marca sirve para generar
  y (b) saber si una pieza cumple las reglas del sistema, **sin haber escrito
  todavía una línea de generación con modelo**. Es el sistema de control de calidad
  funcionando sobre contenido escrito a mano.
- **Riesgo validado:** el spike 1 de la Fase 9 — ¿se pueden verificar de forma
  determinista los constraints del dominio y los ítems mecánicos del checklist, sin
  dependencias externas? Y de paso el riesgo central del proyecto: si el
  verificador detecta una pieza genérica o con una cifra inventada, la mitigación
  de R-001 y R-005 es real y no una promesa del documento.
- **Actor:** Operador (Daniel).
- **Flujo:** UF-001 completo (validar contexto) + la parte de verificación de UF-002
  sobre una pieza escrita a mano.
- **UI:** contratos de texto de `08-UI-SPEC.md`: bloque `RESUMEN` (con checklist),
  bloque `RECHAZO` (contexto incompleto, nombrando los campos).
- **Servidor:** no aplica.
- **Datos:** `marca/contexto-marca.md`, `banco/piezas/<id>-<slug>.md` (escrito a
  mano), `reglas/checklist.md`.
- **Permisos:** el verificador solo lee y reporta; no escribe contenido, solo el
  veredicto del checklist dentro de la pieza.
- **Errores:** contexto incompleto (lista de campos faltantes), pieza con capa
  vacía, pieza sin CTA, pieza con hooks repetidos, pieza con hook de más de 12
  palabras, pieza sin framework declarado.
- **Evidencia:** ejecución real del validador sobre un contexto incompleto (debe
  rechazar nombrando campos) y sobre una pieza inválida fabricada a propósito (debe
  fallar cada constraint por separado), más una pieza válida que pasa las 15
  comprobaciones. Capturas de la salida real, no descripciones.

**Lo que VS-0 deliberadamente no incluye:** generación con modelo, aprobación,
publicación, medición, índice derivado, tests automatizados. Todo eso llega después,
sobre una base verificada.

## Backlog

| ID | Feature | Slice | Dependencias | Prioridad | Estado |
|---|---|---|---|---|---|
| F-001 | Estructura del repositorio y git | VS-0 | — | MUST | Ready |
| F-002 | `validar_contexto.py` | VS-0 | F-001 | MUST | Ready |
| F-003 | Contexto de marca real de Monoga | VS-0 | F-002 | MUST | Ready |
| F-004 | Reglas AIDA, disparadores, reglas de negocio y taxonomía | VS-0 | F-001 | MUST | Ready |
| F-005 | Checklist de 7 ítems con marca de determinista/asistido | VS-0 | F-004 | MUST | Ready |
| F-006 | `validar_pieza.py` (constraints C-01 a C-15) | VS-0 | F-004, F-005 | MUST | Ready |
| F-007 | Piezas de prueba: válida + una inválida por constraint | VS-0 | F-006 | MUST | Ready |
| F-008 | `agente/SKILL.md` + generación de pieza | S1 | F-003, F-006 | MUST | Blocked by F-003 |
| F-009 | Prueba de generación: 3 piezas reales, medir validación a la primera | S1 | F-008 | MUST | Blocked by F-008 |
| F-010 | Índice derivado (`banco/INDICE.md`) | S1 | F-006 | SHOULD | Ready |
| F-011 | Ciclo de vida humano: aprobar, publicar, descartar, medir | S2 | F-008 | MUST | Blocked by F-008 |
| F-012 | Registro de resultado por pieza | S2 | F-011 | SHOULD | Blocked by F-011 |
| F-013 | Tests automatizados del verificador | S2 | F-006 | MUST | Blocked by F-006 |
| F-014 | Verificación asistida de los ítems semánticos | S3 | F-008 | SHOULD | Blocked by F-008 |
| F-015 | Comprobación de tema repetido (UF-007) | S3 | F-010 | COULD | Blocked by F-010 |
| F-016 | Detección de piezas con contexto desactualizado | S3 | F-011 | COULD | Blocked by F-011 |

Sin fechas. La secuencia importa; el calendario no (restricción de la Fase 3: sin
fecha comprometida con terceros).

## Feature F-001 — Estructura del repositorio y git

### Objetivo

Tener el esqueleto de carpetas, el control de versiones y la protección de secretos
antes de escribir cualquier lógica. Protege el activo (R-008) desde el primer
commit.

### Flujo relacionado

Soporte de todos los flujos.

### UI

No aplica.

### Backend

No aplica.

### Datos

Crea `marca/`, `marca/versiones/`, `reglas/`, `agente/`, `banco/`, `banco/piezas/`,
`codigo/`, `codigo/tests/`. Crea `.gitignore` cubriendo `.env`, `*.key`,
`secrets/` y `__pycache__/`.

### Permisos

Ninguno. Solo estructura.

### Edge cases

- El repositorio ya existe con contenido de las fases 1–10: `git init` no debe
  destruirlo.
- Carpetas ya presentes: no sobreescribir.

### Criterios de aceptación

- [ ] Existen todas las carpetas del mapa de `09-TECH-ARCHITECTURE.md`.
- [ ] `git status` muestra el proyecto versionado y sin errores.
- [ ] `.gitignore` impide versionar claves (comprobado creando un `.env` de prueba
      y verificando que git lo ignora).
- [ ] El primer commit contiene los artefactos de las fases 1–10.

### Verificación

- [ ] Typecheck: `python -m py_compile` sobre los scripts (cuando existan).
- [ ] Lint: no aplica (sin herramienta de lint; se usa `py_compile` y revisión).
- [ ] Tests: no aplica en esta unidad.
- [ ] Build: no aplica (sin dependencias, sin artefacto de build).
- [ ] Mobile: no aplica (producto sin UI).
- [ ] Permiso negativo: verificar que el `.env` de prueba no aparece en `git status`.
- [ ] Error states: no aplica.

## Feature F-002 — `validar_contexto.py`

### Objetivo

Hacer **imposible** generar sin contexto de marca válido. Es la implementación de
BR-001 y la mitigación estructural de R-001.

### Flujo relacionado

UF-001 (happy path y errores), UF-004 (rechazo).

### UI

Bloque `RESUMEN` con el veredicto, o bloque `RECHAZO` con la lista numerada de
campos faltantes, según `08-UI-SPEC.md`.

### Backend

Script Python sin dependencias: lee el frontmatter y las secciones obligatorias,
comprueba cada campo, y emite veredicto. No escribe el contexto; solo reporta.

### Datos

Lee `marca/contexto-marca.md`. Campos obligatorios y umbrales según
`10-DATA-AND-PERMISSIONS.md`: 7 campos, ≥3 dolores, ≥3 deseos, ≥3 prohibiciones,
≥3 "lo que nunca decimos", ≥1 oferta con vigencia, ≥2 ejemplos de voz.

### Permisos

Solo lectura del contexto. **No** puede marcar `status: VÁLIDO` por sí mismo: el
humano lo decide con la información del reporte.

### Edge cases

- Archivo inexistente → rechazo con la ruta esperada.
- Frontmatter ausente o malformado → rechazo nombrando el problema de formato.
- Sección presente pero vacía → cuenta como faltante (no basta con que exista el
  título).
- Ejemplos de voz presentes pero con contenido de relleno (`...`, `TBD`) → contarlos
  como faltantes.
- Contradicción entre "lo que nunca decimos" y los ejemplos de voz → aviso, no
  bloqueo en esta unidad (queda como ítem asistido, F-014).

### Criterios de aceptación

- [ ] Con un contexto completo, devuelve `VÁLIDO` y enumera los campos comprobados.
- [ ] Con cada campo obligatorio ausente por separado, lo nombra en la salida.
- [ ] Con dos o más campos ausentes, los enumera todos, no solo el primero.
- [ ] Con el archivo inexistente, informa la ruta esperada y no lanza un traceback.
- [ ] La salida respeta los límites de líneas del contrato de texto.

### Verificación

- [ ] Typecheck: `python -m py_compile codigo/validar_contexto.py`.
- [ ] Lint: no aplica.
- [ ] Tests: manuales en esta unidad; automatizados en F-013.
- [ ] Build: no aplica.
- [ ] Mobile: no aplica.
- [ ] Permiso negativo: comprobar que ejecutarlo **no** modifica el archivo de
      contexto (hash antes y después).
- [ ] Error states: archivo inexistente, frontmatter roto, sección vacía, relleno
      tipo `TBD`.

## Feature F-003 — Contexto de marca real de Monoga

### Objetivo

Que el sistema tenga de verdad su fuente de verdad. Sin este contenido, todo lo
demás es un motor sin combustible, y es el supuesto A-008 ("el contexto no existe
todavía por escrito").

### Flujo relacionado

UF-001.

### UI

No aplica. El archivo sigue la estructura obligatoria de `06-SCREEN-INVENTORY.md`
(SC-002).

### Backend

No aplica.

### Datos

`marca/contexto-marca.md` con posicionamiento, propuesta de valor, audiencia con
dolores y deseos, tono y voz, ofertas vigentes, prohibiciones, vocabulario prohibido
y al menos 2 ejemplos de voz **reales** (texto ya publicado por Monoga, no inventado
para la ocasión).

### Permisos

Escrito por el humano. El agente solo lo lee.

### Edge cases

- **Si Monoga no tiene ejemplos de voz publicados**, hay que decidirlo antes de
  generar: o se escriben dos piezas de referencia a mano y se marcan como ejemplos
  aprobados, o el sistema se queda en `INCOMPLETO`. No se rellena con texto
  inventado por el modelo: eso contaminaría la voz que el sistema debe reproducir.
- Ofertas que ya no están vigentes: no se incluyen.

### Criterios de aceptación

- [ ] `validar_contexto.py` devuelve `VÁLIDO` sobre el contexto real.
- [ ] Los ejemplos de voz son texto real de Monoga, verificables.
- [ ] Cada afirmación del contexto es algo que el negocio puede respaldar.
- [ ] El contexto pasa a `status: VÁLIDO` con `version` y `last_validated`
      registrados.

### Verificación

- [ ] Typecheck: no aplica.
- [ ] Lint: no aplica.
- [ ] Tests: la propia ejecución de `validar_contexto.py` es la prueba.
- [ ] Build: no aplica.
- [ ] Mobile: no aplica.
- [ ] Permiso negativo: no aplica.
- [ ] Error states: probar dejando un campo vacío a propósito y confirmar el rechazo.

**Nota de dependencia:** F-003 necesita información que solo Daniel tiene. Es la
única unidad del plan que no se puede completar sin una entrada humana explícita.

## Feature F-004 — Reglas AIDA, disparadores, reglas de negocio y taxonomía

### Objetivo

Cerrar el supuesto de ADR-003: escribir dentro del repositorio el conocimiento que
se decidió no importar de terceros. Es el activo que sustituye a
`marketingskills`.

### Flujo relacionado

Soporte de UF-002 (elección de framework y estructura).

### UI

SC-004 según `06-SCREEN-INVENTORY.md`.

### Backend

No aplica.

### Datos

- `reglas/aida.md` — definición de las 4 capas con criterio de qué pertenece a cada
  una, errores típicos por capa, y el mapeo explícito de AIDA a
  Hook/Substance/Payoff para video corto.
- `reglas/reglas.md` — las 12 reglas de negocio con ejemplo y excepción.
- `reglas/disparadores.md` — vocabulario cerrado de los 6 disparadores
  (`curiosidad`, `contradicción`, `pérdida`, `prueba social`, `dato`, `pregunta`)
  con un ejemplo de hook por disparador.
- `reglas/taxonomia.md` — frameworks, plataformas (Instagram, TikTok, YouTube
  Shorts, LinkedIn) y formatos válidos por plataforma, con longitudes objetivo.

### Permisos

Escrito por el humano.

### Edge cases

- **Cada capa necesita su criterio negativo:** qué NO es una Atención (por ejemplo,
  un saludo), qué NO es un Deseo (por ejemplo, una característica). Sin el negativo,
  el generador mete cualquier cosa en cualquier capa.
- El mapeo AIDA ↔ Hook/Substance/Payoff debe ser explícito, o el generador declarará
  frameworks alternativos sin justificación.
- La taxonomía no debe admitir plataformas fuera del catálogo (el flujo UF-002 exige
  reportar "no soportada", no improvisar).

### Criterios de aceptación

- [ ] Las 4 capas tienen criterio positivo, criterio negativo y 2 ejemplos cada una.
- [ ] Los 6 disparadores tienen definición y ejemplo de hook.
- [ ] Las 12 reglas de negocio aparecen con ejemplo y excepción.
- [ ] La taxonomía cubre las 4 plataformas con sus formatos y longitudes.
- [ ] Un lector que no conoce AIDA puede aplicar estas reglas sin preguntar nada.

### Verificación

- [ ] Typecheck: no aplica.
- [ ] Lint: no aplica.
- [ ] Tests: revisión contra las reglas BR-001 a BR-012 del modelo de dominio
      (¿alguna regla quedó fuera?).
- [ ] Build: no aplica.
- [ ] Mobile: no aplica.
- [ ] Permiso negativo: no aplica.
- [ ] Error states: no aplica.

## Feature F-005 — Checklist de 7 ítems con marca de determinista/asistido

### Objetivo

Convertir el criterio en verificación, y ser honesto sobre qué se verifica de
verdad. La marca determinista/asistido es lo que impide presentar una opinión del
modelo como una prueba (ADR-004).

### Flujo relacionado

UF-002 (paso 9), UF-003 (validación antes de aprobar).

### UI

Bloque `CHECKLIST` de `08-UI-SPEC.md`.

### Backend

No aplica (definición de datos).

### Datos

`reglas/checklist.md` con los 7 ítems, su regla asociada y su tipo:

| Ítem | Regla | Tipo |
|---|---|---|
| Hook en ≤3 s (≤12 palabras) | BR-006 | Determinista |
| 5 hooks con ángulos distintos | BR-004 | Determinista |
| Las 4 capas escritas | BR-007 | Determinista |
| CTA concreto presente | BR-003 | Determinista |
| Sin afirmaciones fuera del contexto | BR-005 | **Asistido** + verificable parcialmente |
| Framework declarado | BR-002 | Determinista |
| Tono alineado con el contexto | BR-001 | **Asistido** |

### Permisos

Escrito por el humano; leído por el agente y por el verificador.

### Edge cases

- El ítem que exige **3 segundos** no es medible en texto. Se operacionaliza como
  ≤12 palabras más un conteo de sílabas estimado, y se declara esa aproximación en
  el propio checklist. No se finge precisión que no existe.
- BR-005 se verifica parcialmente: se pueden detectar cifras, porcentajes y
  superlativos no presentes en el contexto; no se puede demostrar que una frase
  está respaldada. El checklist debe declarar esa limitación.

### Criterios de aceptación

- [ ] Los 7 ítems están definidos con su regla y su tipo.
- [ ] Cada ítem indica cómo se evalúa y qué no cubre.
- [ ] La aproximación del umbral de 3 segundos está declarada como aproximación.
- [ ] El orden de los ítems es fijo (lo consume `validar_pieza.py`).

### Verificación

- [ ] Typecheck: no aplica.
- [ ] Lint: no aplica.
- [ ] Tests: comprobar que los 7 ítems del archivo coinciden exactamente con los 7
      del bloque `CHECKLIST` de `08-UI-SPEC.md` (orden y texto).
- [ ] Build: no aplica.
- [ ] Mobile: no aplica.
- [ ] Permiso negativo: no aplica.
- [ ] Error states: no aplica.

## Feature F-006 — `validar_pieza.py` (constraints C-01 a C-15)

### Objetivo

Impedir que una pieza incompleta, incoherente o con afirmaciones inventadas llegue
al operador como aprobada. Es el corazón de la estrategia: construir primero el
juez.

### Flujo relacionado

UF-002, UF-003, UF-004.

### UI

Bloque `RESUMEN` con `Checklist: 7/7 APROBADO` o `6/7 CON FALLOS: <ítem>`.

### Backend

Script Python sin dependencias. Parsea el frontmatter y los bloques, aplica las 15
constraints de `10-DATA-AND-PERMISSIONS.md` y emite un veredicto por ítem con la
regla citada.

### Datos

Lee las piezas de `banco/piezas/`, `marca/contexto-marca.md`, `reglas/checklist.md`
y `reglas/taxonomia.md`.

### Permisos

Solo lectura del contenido. Escribe únicamente el veredicto del bloque `CHECKLIST`
en la pieza que se le indique. **No** puede cambiar `estado` (eso es humano).

### Edge cases

- Pieza sin frontmatter → fallo de formato, no traceback.
- Capa duplicada o con nombre mal escrito (`Interes` sin tilde) → fallo de C-01.
- 4 hooks en lugar de 5 **sin** `excepcion_hooks` → fallo de C-02; **con** motivo
  escrito → pasa (BR-004).
- 5 hooks que son la misma frase reformulada → debe fallar C-03. Detectar esto de
  forma determinista es la parte difícil: se resuelve con similitud de tokens
  (solapamiento alto) más igualdad de disparador, y se documenta la limitación.
- `estado: APROBADA` con una capa vacía → fallo de C-06.
- `estado: DESCARTADA` sin motivo → fallo de C-07.
- `contexto_marca: v9` cuando solo existe hasta v3 → fallo de C-09.
- `publicada_el` en el futuro → fallo de C-10.
- Hook de 13 palabras → fallo de C-12 (salvo formato escrito declarado).
- `plataforma: Twitter` fuera de taxonomía → fallo de C-13.

### Criterios de aceptación

- [ ] Las 15 constraints están implementadas y cada una falla de forma aislada.
- [ ] El reporte cita la regla de negocio de cada fallo (por ejemplo, `BR-004`).
- [ ] El reporte distingue ítem determinista de ítem asistido.
- [ ] Una pieza válida pasa las 15 comprobaciones.
- [ ] El script nunca lanza un traceback ante un archivo malformado.

### Verificación

- [ ] Typecheck: `python -m py_compile codigo/validar_pieza.py`.
- [ ] Lint: no aplica.
- [ ] Tests: uno por constraint (15 casos) en F-013; en esta unidad, el set de
      piezas de F-007.
- [ ] Build: no aplica.
- [ ] Mobile: no aplica.
- [ ] Permiso negativo: comprobar que ejecutarlo sobre una pieza `APROBADA` no
      cambia el estado, solo el bloque de checklist.
- [ ] Error states: los 10 edge cases de arriba, uno por uno.

## Feature F-007 — Piezas de prueba: una válida y una inválida por constraint

### Objetivo

Tener la evidencia de que el verificador funciona antes de confiar en él. Un
verificador sin pruebas negativas es una promesa, no una herramienta.

### Flujo relacionado

Soporte de verificación de UF-002 y UF-003.

### UI

No aplica.

### Backend

No aplica.

### Datos

`codigo/tests/fixtures/`: una pieza válida y **una pieza por cada constraint
violada** (15 piezas inválidas, cada una fallando exactamente una cosa). Cada
fixture declara en un comentario qué constraint debe disparar.

### Permisos

Ninguno.

### Edge cases

- Las piezas inválidas deben estar **fuera** de `banco/piezas/` para no contaminar
  el banco real ni el índice. Van en `codigo/tests/fixtures/`.
- Cada fixture debe fallar **una sola** constraint, o la prueba no aísla la causa.

### Criterios de aceptación

- [ ] Existe 1 fixture válido y 15 inválidos, uno por constraint.
- [ ] Cada fixture inválido produce exactamente el fallo esperado y ningún otro.
- [ ] Las piezas de prueba no aparecen en el índice del banco.

### Verificación

- [ ] Typecheck: no aplica.
- [ ] Lint: no aplica.
- [ ] Tests: ejecución de `validar_pieza.py` sobre los 16 fixtures.
- [ ] Build: no aplica.
- [ ] Mobile: no aplica.
- [ ] Permiso negativo: comprobar que el banco real sigue vacío tras las pruebas.
- [ ] Error states: cubiertos por los propios fixtures.

## Feature F-008 — `agente/SKILL.md` y generación de pieza

### Objetivo

La única capacidad de escritura del agente: convertir tema + contexto válido en una
pieza que pase el verificador.

### Flujo relacionado

UF-002 completo.

### UI

Bloque `RESUMEN` y bloque `RECHAZO`.

### Backend

No hay backend. `agente/SKILL.md` declara: capacidades (generar pieza, regenerar
hooks), **no-capacidades explícitas** (aprobar, publicar, descartar, borrar,
reescribir el contexto), el orden de lectura obligatorio (contexto → reglas →
checklist), y la obligación de ejecutar el verificador antes de guardar.

### Datos

Escribe en `banco/piezas/`. Un solo archivo al final: si la generación se
interrumpe, no queda pieza parcial (invariante del dominio).

### Permisos

Según la matriz de la Fase 10: genera `BORRADOR`; no aprueba, no publica, no borra,
no toca el contexto.

### Edge cases

- El modelo devuelve 6 hooks o 4 → el verificador falla y la pieza **no se guarda
  como válida**; se reintenta una vez corrigiendo, y si vuelve a fallar se guarda
  marcada `CON_FALLOS` con el motivo.
- El modelo omite la etiqueta de una capa → fallo de C-01, mismo tratamiento.
- Contexto `INCOMPLETO` → rechazo por BR-001, sin llegar al modelo.
- Tema sensible → la pieza se genera con `tema_sensible: sí`.

### Criterios de aceptación

- [ ] Con contexto válido y un tema, se obtiene una pieza que pasa las 15
      constraints.
- [ ] Con contexto `INCOMPLETO`, el agente se niega y no llama al modelo.
- [ ] El agente no puede mover `estado` a `APROBADA` ni `PUBLICADA`.
- [ ] La pieza se escribe una sola vez, al final, completa.
- [ ] La salida respeta los límites de líneas del contrato de texto.

### Verificación

- [ ] Typecheck: no aplica.
- [ ] Lint: no aplica.
- [ ] Tests: F-009.
- [ ] Build: no aplica.
- [ ] Mobile: no aplica.
- [ ] Permiso negativo: pedir explícitamente al agente que apruebe o publique una
      pieza y comprobar que se niega citando BR-012. **Es la prueba de permiso más
      importante del sistema.**
- [ ] Error states: contexto incompleto, plataforma no soportada, tema vacío,
      interrupción del proveedor.

## Feature F-009 — Prueba de generación: 3 piezas reales

### Objetivo

Cerrar el spike 2 de la Fase 9 y obtener la primera métrica honesta: ¿qué porcentaje
de piezas pasa el verificador a la primera? Determina si hace falta un paso de
normalización.

### Flujo relacionado

UF-002, y la métrica de tiempo del MVP.

### UI

No aplica.

### Backend

No aplica.

### Datos

3 temas reales de Monoga, 3 piezas en el banco, y el registro de: intentos
necesarios, fallos concretos por pieza y tiempo total por pieza.

### Permisos

Humano pide e inspecciona; el agente genera.

### Edge cases

- Si las 3 piezas necesitan más de un reintento, el problema está en las reglas o en
  el formato de salida, no en el modelo. Se documenta y se decide si se normaliza la
  salida o se refuerzan las instrucciones.
- Si las 3 piezas suenan iguales entre sí, se ha disparado R-004 (fatiga de
  plantilla) en la primera prueba: se revisa la variedad de disparadores de hook.

### Criterios de aceptación

- [ ] 3 piezas reales en el banco, todas con checklist completo.
- [ ] Registrado cuántos intentos necesitó cada una.
- [ ] Registrado el tiempo por pieza (insumo de la métrica de ≤15 min del MVP).
- [ ] Las 3 no comparten el mismo disparador de hook dominante.
- [ ] Decisión escrita sobre si hace falta normalización de salida.

### Verificación

- [ ] Typecheck: no aplica.
- [ ] Lint: no aplica.
- [ ] Tests: este bloque **es** la prueba.
- [ ] Build: no aplica.
- [ ] Mobile: no aplica.
- [ ] Permiso negativo: no aplica.
- [ ] Error states: registrar los fallos reales observados, no los previstos.

## Feature F-010 — Índice derivado (`banco/INDICE.md`)

### Objetivo

Saber qué temas y hooks existen sin releer el banco a mano, y alimentar el aviso de
ángulo repetido (R-004).

### Flujo relacionado

UF-007.

### UI

SC-005 según `06-SCREEN-INVENTORY.md`.

### Backend

Script que deriva el índice de los frontmatter de las piezas. Nunca se edita a mano.

### Datos

Escribe `banco/INDICE.md`: ID, Tema, Ángulo, Hook elegido, Estado, Plataforma,
Fecha. Excluye `codigo/tests/fixtures/`.

### Permisos

Solo el verificador escribe este archivo. El humano no lo edita.

### Edge cases

- Banco vacío → `Banco vacío. Genera la primera pieza.`
- Pieza con frontmatter roto → se lista aparte como ilegible, sin romper el índice.
- Piezas descartadas → se incluyen, marcadas; el descarte es información (BR-009).

### Criterios de aceptación

- [ ] El índice se regenera desde cero en cada ejecución.
- [ ] Coincide exactamente con las piezas del banco.
- [ ] Una pieza inválida en fixtures no aparece.
- [ ] Un frontmatter roto no rompe la generación del índice.

### Verificación

- [ ] Typecheck: `python -m py_compile codigo/derivar_indice.py`.
- [ ] Lint: no aplica.
- [ ] Tests: ejecutar dos veces y comprobar que el resultado es idéntico
      (idempotencia).
- [ ] Build: no aplica.
- [ ] Mobile: no aplica.
- [ ] Permiso negativo: comprobar que el índice no contiene contenido de las piezas,
      solo metadatos.
- [ ] Error states: frontmatter roto, banco vacío.

## Feature F-011 — Ciclo de vida humano: aprobar, publicar, descartar, medir

### Objetivo

Que el paso de "generado" a "publicado" sea explícitamente humano y quede trazado.
Es la implementación de BR-012 y BR-009.

### Flujo relacionado

UF-003, UF-005, UF-006.

### UI

Estados en el frontmatter; sin UI.

### Backend

No hay backend. El ciclo se ejecuta editando el frontmatter, con el verificador
comprobando la coherencia estado↔contenido antes de aceptar el cambio (C-06, C-07,
C-08).

### Datos

Transiciones de `estado`, `hook_elegido`, `publicada_el`, `motivo_descarte` y el
bloque `RESULTADO`.

### Permisos

Exclusivamente humano (BR-012). El agente no tiene estas operaciones.

### Edge cases

- Aprobar con capa vacía → C-06 lo impide.
- Aprobar con checklist en fallo → C-06 lo impide.
- Descartar sin motivo → C-07 lo impide.
- Publicar una pieza con `tema_sensible: sí` sin revisión marcada → C-08 lo impide.
- Publicar algo en `BORRADOR` → C-08 lo impide.
- Nueva versión del contexto → se listan las piezas cuya versión ya no es la activa
  (UF-006).

### Criterios de aceptación

- [ ] Las 6 transiciones ilegales se rechazan con la regla citada.
- [ ] Una pieza puede recorrer `BORRADOR → EN_REVISION → APROBADA → PUBLICADA` sin
      obstáculos.
- [ ] El descarte conserva la pieza y el motivo.
- [ ] El cambio de versión de contexto identifica las piezas afectadas.

### Verificación

- [ ] Typecheck: no aplica.
- [ ] Lint: no aplica.
- [ ] Tests: los 6 casos ilegales como pruebas en F-013.
- [ ] Build: no aplica.
- [ ] Mobile: no aplica.
- [ ] Permiso negativo: pedir al agente que apruebe una pieza y confirmar la
      negativa (BR-012).
- [ ] Error states: los 6 de arriba.

## Feature F-012 — Registro de resultado por pieza

### Objetivo

Que el aprendizaje sobre qué hooks funcionan tenga dónde vivir, sin convertirlo en
una integración con plataformas (excluido del MVP).

### Flujo relacionado

UF-005.

### UI

Bloque `RESULTADO` de la pieza.

### Backend

No aplica.

### Datos

Filas de `RESULTADO`: fecha, ventana de observación, métrica, valor. Varias filas por
pieza permitidas.

### Permisos

Humano.

### Edge cases

- Métrica sin ventana de observación → rechazada (el dato no es interpretable).
- Varias mediciones de la misma ventana → permitidas, se conservan ambas.
- Pieza no publicada con resultado → incoherente; se rechaza.

### Criterios de aceptación

- [ ] Se puede registrar más de una medición por pieza.
- [ ] Una medición sin ventana se rechaza con explicación.
- [ ] Los resultados no alteran el estado ni el contenido de la pieza.

### Verificación

- [ ] Typecheck: no aplica.
- [ ] Lint: no aplica.
- [ ] Tests: incluidas en F-013.
- [ ] Build: no aplica.
- [ ] Mobile: no aplica.
- [ ] Permiso negativo: confirmar que registrar un resultado no cambia `estado`.
- [ ] Error states: medición sin ventana, resultado en pieza no publicada.

## Feature F-013 — Tests automatizados del verificador

### Objetivo

Que el juez esté él mismo bajo control: cada constraint con su prueba, para que
cambiar una regla no rompa otra en silencio.

### Flujo relacionado

Soporte de todas las verificaciones.

### UI

No aplica.

### Backend

Sin dependencias externas: un runner simple con `assert`, ejecutable con
`python codigo/tests/run_tests.py`. No se introduce pytest (ADR-003: cero
dependencias) salvo decisión explícita.

### Datos

Pruebas por constraint (15), pruebas de las 6 transiciones ilegales (F-011) y pruebas
del registro de resultado (F-012).

### Permisos

Ninguno.

### Edge cases

- Un fixture que falla por dos constraints a la vez → el test debe detectar el
  acoplamiento, no dar falso verde.
- Cambiar el orden del checklist en `reglas/checklist.md` → el test debe fallar.

### Criterios de aceptación

- [ ] Existe una prueba por constraint (15), por transición ilegal (6) y por edge
      case de resultado (3).
- [ ] El runner devuelve código de salida distinto de cero al fallar.
- [ ] Todas las pruebas pasan sobre el código actual.
- [ ] Ninguna prueba necesita red ni dependencias externas.

### Verificación

- [ ] Typecheck: `python -m py_compile` sobre el runner y los módulos.
- [ ] Lint: no aplica.
- [ ] Tests: `python codigo/tests/run_tests.py` con salida real capturada.
- [ ] Build: no aplica.
- [ ] Mobile: no aplica.
- [ ] Permiso negativo: introducir un fallo deliberado en una constraint y
      comprobar que el test lo detecta.
- [ ] Error states: cubiertos por los fixtures.

## Feature F-014 — Verificación asistida de los ítems semánticos

### Objetivo

Aportar valor donde lo determinista no llega (tono alineado, afirmaciones no
respaldadas), **sin fingir** que es una prueba.

### Flujo relacionado

UF-002, UF-003.

### UI

Bloque `CHECKLIST`, con la marca `ASISTIDO` visible.

### Backend

Una pasada del modelo que compara la pieza contra el contexto de marca y devuelve
hallazgos con la cita del fragmento del contexto que los respalda o su ausencia.

### Datos

Los hallazgos se escriben en la pieza, marcados como asistidos.

### Permisos

El agente puede proponer hallazgos; el humano decide. Un hallazgo asistido **no**
bloquea por sí mismo, pero **sí** bloquea si el humano lo confirma.

### Edge cases

- **Un ítem asistido nunca debe presentarse como aprobado definitivo.** Si el
  reporte no distingue "verificado" de "revisado por el modelo", el sistema miente
  sobre su propia fiabilidad. Es el edge case crítico de esta unidad.
- El modelo puede inventar una cita del contexto para respaldar algo que no está:
  las citas deben ser verificables literalmente contra el archivo.
- Si el ítem asistido y la lectura humana divergen, gana el humano y se registra.

### Criterios de aceptación

- [ ] Los ítems asistidos van marcados como `ASISTIDO` en el reporte.
- [ ] Los ítems deterministas y asistidos no se mezclan sin distinción.
- [ ] Toda cita de respaldo se puede encontrar literalmente en el contexto de marca.
- [ ] Un ítem asistido no puede habilitar por sí solo el estado `APROBADA`.

### Verificación

- [ ] Typecheck: no aplica.
- [ ] Lint: no aplica.
- [ ] Tests: prueba con una afirmación inventada y comprobar que se reporta como
      hallazgo asistido, no como aprobado.
- [ ] Build: no aplica.
- [ ] Mobile: no aplica.
- [ ] Permiso negativo: confirmar que un ítem asistido en `FALLO` no se convierte
      en `APROBADO` por decisión del modelo.
- [ ] Error states: cita de respaldo que no existe en el contexto.

## Feature F-015 — Comprobación de tema repetido (UF-007)

### Objetivo

Evitar publicar el mismo contenido con otro hook, que es una de las formas en que la
fatiga de plantilla (R-004) se manifiesta.

### Flujo relacionado

UF-007.

### UI

Aviso en el bloque `RESUMEN`.

### Backend

Comparación de texto simple contra el índice del banco.

### Datos

Campo `relacionada_con` en el frontmatter.

### Permisos

El agente avisa; el humano decide.

### Edge cases

- Coincidencia alta pero deliberada (segunda parte de una serie) → el aviso no debe
  bloquear.
- Banco ilegible → se avisa y se continúa, sin impedir la generación.

### Criterios de aceptación

- [ ] Un tema idéntico a uno existente produce aviso con la ruta de la pieza previa.
- [ ] El aviso no impide generar.
- [ ] Si se continúa, la relación queda registrada.

### Verificación

- [ ] Typecheck: `python -m py_compile`.
- [ ] Lint: no aplica.
- [ ] Tests: caso con coincidencia, caso sin coincidencia, caso con banco ilegible.
- [ ] Build: no aplica.
- [ ] Mobile: no aplica.
- [ ] Permiso negativo: comprobar que el aviso no modifica el banco.
- [ ] Error states: banco ilegible.

## Feature F-016 — Detección de piezas con contexto desactualizado

### Objetivo

Saber qué piezas antiguas podrían afirmar algo que ya no es cierto, cuando cambia la
oferta o el posicionamiento (UF-006).

### Flujo relacionado

UF-006.

### UI

Aviso con la lista de piezas afectadas.

### Backend

Comparación de `contexto_marca` de cada pieza contra la versión activa.

### Datos

`marca/versiones/` y el campo `contexto_marca` de cada pieza.

### Permisos

Solo lectura y aviso. No reescribe piezas.

### Edge cases

- Cambio solo de estilo → no debería marcar todas las piezas como afectadas.
- Versión histórica ausente en `marca/versiones/` → reportar la ausencia, no fallar.

### Criterios de aceptación

- [ ] Tras subir la versión del contexto, se listan las piezas con versión anterior.
- [ ] El aviso no modifica ninguna pieza.
- [ ] La ausencia de una versión histórica se reporta de forma explícita.

### Verificación

- [ ] Typecheck: `python -m py_compile`.
- [ ] Lint: no aplica.
- [ ] Tests: subir versión y comprobar la lista.
- [ ] Build: no aplica.
- [ ] Mobile: no aplica.
- [ ] Permiso negativo: confirmar que ninguna pieza se modifica.
- [ ] Error states: versión histórica ausente.

## Dependencias y secuencia

```text
F-001 (estructura + git)
  └─▶ F-002 (validar contexto)
        └─▶ F-003 (contexto real)          ← necesita a Daniel
        └─▶ F-004 (reglas)
              └─▶ F-005 (checklist)
                    └─▶ F-006 (validar pieza)
                          ├─▶ F-007 (fixtures)  ──▶ CIERRE DE VS-0
                          ├─▶ F-010 (índice)
                          └─▶ F-013 (tests)
        F-003 + F-006 ─▶ F-008 (agente generador)
                            ├─▶ F-009 (prueba de generación)
                            ├─▶ F-011 (ciclo de vida)
                            │     ├─▶ F-012 (resultado)
                            │     └─▶ F-016 (contexto desactualizado)
                            ├─▶ F-014 (verificación asistida)
                            └─▶ F-010 ─▶ F-015 (tema repetido)
```

Cuello de botella real: **F-003 (contexto de marca real)**. Es lo único que no se
puede resolver con trabajo técnico y bloquea F-008 en adelante. Por eso se puede
completar VS-0 íntegro sin él, salvo esa unidad: F-001, F-002, F-004, F-005, F-006 y
F-007 no dependen de contenido de marca real.

**Decisión de secuencia:** si el contexto real de Monoga no está listo, se ejecuta
VS-0 completo con un contexto de prueba marcado como tal, y se documenta que el
sistema no está listo para piezas reales hasta F-003.

## Riesgos de implementación

| Riesgo | Señal temprana | Respuesta |
|---|---|---|
| C-03 (5 hooks distintos) no es verificable de forma determinista y deja pasar variantes falsas | Las 3 piezas de F-009 pasan con hooks que suenan iguales | Aceptar la limitación, corregir el algoritmo de similitud (solapamiento de tokens) y, si sigue fallando, mover C-03 a verificación asistida marcada como tal |
| El modelo no respeta el formato de salida y falla la validación casi siempre | F-009 necesita más de 2 intentos por pieza | Añadir un paso de normalización de salida antes de validar; no relajar las constraints para que pase |
| El primer ítem del checklist (≤3 s) resulta inaplicable en texto | Falsos positivos y negativos evidentes en F-009 | Documentar la aproximación por palabras y sílabas y **declararla como aproximación**; nunca presentarla como medición real |
| La verificación asistida (F-014) se presenta como prueba | Un reporte dice "tono verificado" sin marca de asistido | Es un fallo de diseño, no un detalle de UI: se corrige antes de cerrar la unidad |
| El contexto de marca se escribe con prisa y el producto sale genérico | Las 3 piezas de F-009 podrían haberlas escrito tres marcas distintas | R-001 es el riesgo central del proyecto: se para la generación y se refuerza el contexto antes de seguir |
| Deriva hacia UI, publicación automática o analítica | Aparece cualquier petición de "ya que estamos…" | `CHANGE_REQUESTS.md` y reevaluación de alcance (R-006) |
| Cero dependencias obliga a escribir cosas que una librería daría | Tentación de hacer `pip install` | ADR-003 es explícito. Si una dependencia se vuelve necesaria, es una decisión, no un atajo |

## Gate

- [x] Las tareas tienen alcance controlado.
- [x] Cada feature termina en valor verificable.
- [x] La Vertical Slice 0 prueba arquitectura real.
- [x] Los criterios son observables.
- [x] Las dependencias están ordenadas.
- [x] QA, deploy y handoff están incluidos.

## Incertidumbres abiertas

- [ ] [REQUIERE DANIEL] **El contexto de marca real (F-003) no existe todavía y
      solo Daniel puede aportarlo:** posicionamiento, audiencia con dolores y
      deseos, tono, ofertas, prohibiciones y **2 ejemplos de voz reales**. No se
      inventa: un contexto escrito por el modelo contaminaría la voz que el sistema
      debe reproducir. No bloquea esta fase ni VS-0 (se puede construir y probar el
      verificador con un contexto de prueba marcado como tal), pero **bloquea F-008
      y todo lo que dependa de él**. El sistema no está listo para piezas reales
      hasta que F-003 esté cerrada.
- [x] [ASSUMPTION] La secuencia "juez antes que escritor" es la correcta: construir
      primero el verificador reduce el riesgo de las fases siguientes en lugar de
      aumentarlo (ADR-004).
- [ ] [ASSUMPTION] Los 15 constraints son implementables sin dependencias externas.
      Se confirma al cerrar VS-0; si alguno no lo es, pasa a verificación asistida y
      se documenta.
- [ ] [ASSUMPTION] Un runner de tests propio con `assert` es suficiente y no hace
      falta pytest. Si escribir el runner cuesta más de una sesión, se reevalúa
      (sería la única dependencia razonable del proyecto).
- [ ] [DEFERRED:Fase 12] Resultado real de los spikes 1 y 2 al ejecutar VS-0.
- [ ] [DEFERRED:Fase 14] Los casos límite del checklist como casos de QA formales.
