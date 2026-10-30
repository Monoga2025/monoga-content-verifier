---
artifact: ui-spec
phase: 8
status: approved
reason: ""
last_updated: "2026-10-12"
---

# 08 — UI Spec de Agente Generador de Contenido

> **No hay UI gráfica.** Esta es la especificación de la **superficie de texto**:
> la salida de consola del agente y la estructura de los archivos que produce y
> lee. Aquí se fija el contrato exacto para que un implementador no tenga que
> inventar formato. Es la traducción de `07-UI-DIRECTION.md` (Dirección A) a
> reglas implementables.

## Sistema base

### Sistema de texto

- **Dirección aprobada:** Dirección A — Manual de operador, con frontmatter de
  metadatos y tabla de checklist tomados de la Dirección B.
- **Viewports:** no aplica. La única restricción geométrica es el ancho de
  terminal: el resumen de generación debe renderizar sin scroll a **80 columnas**.
- **Grid:** no aplica.
- **Escala de espaciado:** una línea en blanco entre secciones. Cero líneas en
  blanco dentro de un bloque de datos.
- **Tipografía:** la del terminal y la del editor. El sistema no elige fuentes.
- **Radios / Elevación / Iconografía / Movimiento:** no aplican.
- **Paleta:** no aplica. Ningún significado depende del color (RN-03).
- **Acentos:** ASCII en la medida de lo posible en consola; los archivos markdown
  usan UTF-8 con acentos normales (español correcto en el contenido generado).
- **Accesibilidad:** todo dato lleva etiqueta de texto; los avisos y fallos se
  marcan con `AVISO:` y `FALLO:`; el texto plano copiado sin formato sigue siendo
  comprensible.

### Reglas de anchura y longitud

| Elemento | Límite | Regla |
|---|---:|---|
| Resumen de generación (SC-001) | ≤ 12 líneas, ≤ 80 columnas | Debe caber sin scroll ni corte de línea |
| Reporte de rechazo (SC-006) | ≤ 8 líneas | Una línea por campo faltante |
| Línea de error en consola | 1 línea | Causa + qué hacer, sin salto de línea |
| Archivo de pieza (SC-003) | ≤ 120 líneas | Si excede, sobra contenido |
| Texto de una capa AIDA | 1–3 líneas | Si necesita más, la capa está mal definida |
| Texto de un hook | ≤ 12 palabras | Es el umbral de BR-006 (≤ 3 s al decirlo) |

## Contrato mobile

**No aplica: el producto no tiene interfaz móvil.** No hay viewport, ni grid, ni
hero, ni carruseles, ni safe areas. No se inventa un contrato móvil para cumplir
una casilla.

- **Referencia o viewport de diseño:** no aplica.
- **Densidad visual objetivo:** no aplica.
- **Contenido visible en la primera pantalla:** el resumen de generación completo,
  en terminal de 80×24.
- **Proporción del hero, si aplica:** no aplica.
- **Cantidad visible en carruseles, si aplica:** no aplica.
- **Tokens responsive:** no aplica.
- **Adaptación de 360 a 430 px:** no aplica.
- **Safe areas y unidades de viewport:** no aplica.
- **Desviaciones justificadas frente a la referencia:** no hay referencia; no hay
  desviación. Única concesión de lectura: al abrir una pieza en el móvil, el
  archivo es markdown plano y reflowea solo, sin layout propio que mantenga.

Si en cualquier momento se introduce una interfaz gráfica, este apartado se
reescribe y el contrato de densidad móvil pasa a ser obligatorio.

## Navegación

No hay navegación. Hay tres entradas y ninguna pantalla intermedia:

```text
operador
  ├── pide generar una pieza        → SC-001 (consola) → crea SC-003 (archivo)
  ├── pide validar el contexto      → SC-001 (consola) → actualiza SC-002
  └── abre un archivo directamente  → SC-003 / SC-004 / SC-005
```

Regla: ninguna operación del agente requiere más de **una** invocación y **una**
lectura de resultado.

## Componentes

En un producto sin UI, los "componentes" son los bloques reutilizables de texto.
Sus reglas son obligatorias porque de ellas depende que el checklist sea
verificable de forma automática.

### Bloque `RESUMEN` (SC-001)

- **Variantes:** generación con éxito, generación con fallos de checklist.
- **Tamaños:** 10–12 líneas con éxito; hasta 13 con advertencias (máximo una
  advertencia por línea).
- **Estados:** éxito (`Checklist: 7/7 APROBADO`), con fallos
  (`Checklist: 6/7 CON FALLOS: <ítem>`).
- **Uso:** siempre al final de una generación, siempre con la misma estructura y
  el mismo orden de campos.
- **Evitar:** añadir líneas de cortesía, resúmenes narrados o explicaciones del
  proceso.

```text
PIEZA GENERADA — <tema>
Archivo:        banco/piezas/<id>-<slug>.md
Framework:      AIDA
Plataforma:     <plataforma>/<formato>
Contexto:       v<versión> (<fecha>)
Checklist:      7/7 APROBADO
Hook sugerido:  #2 — <texto del hook 2>
AVISO:          tema sensible — requiere revisión humana antes de publicar
```

### Bloque `RECHAZO` (SC-006)

- **Variantes:** contexto ausente, contexto incompleto, tema vacío, plataforma no
  soportada.
- **Tamaños:** 4–8 líneas.
- **Estados:** siempre termina confirmando que no se creó nada.
- **Uso:** cuando el agente se niega a generar. Es un componente de seguridad, no
  un error de sistema.
- **Evitar:** "lo siento", "error inesperado", cualquier mensaje sin causa
  concreta.

```text
GENERACIÓN RECHAZADA
Causa:     Contexto de marca INCOMPLETO (BR-001)
Faltan:    1. Ofertas vigentes
           2. Prohibiciones
           3. Ejemplos de voz (hay 1, se requieren 2)
Siguiente: completa esos campos en <ruta> y valida el contexto.
No se generó ninguna pieza.
```

### Bloque `CAPAS` (SC-003)

- **Variantes:** AIDA (4 capas) y framework alternativo (3 fases equivalentes,
  declaradas).
- **Tamaños:** 1–3 líneas por capa.
- **Estados:** `ESCRITA` / `VACÍA` (una capa vacía impide aprobar).
- **Uso:** cuerpo central de la pieza.
- **Evitar:** párrafos largos, mezclar capas, capas sin etiqueta.

```markdown
### Atención (0–3 s)
<texto>

### Interés (3–10 s)
<texto>

### Deseo (10–20 s)
<texto>

### Acción (cierre)
<texto>
```

### Bloque `HOOKS` (SC-003)

- **Variantes:** ninguna. Siempre 5 filas.
- **Tamaños:** 5 filas + cabecera.
- **Estados:** `PROPUESTO` / `ELEGIDO` / `DESCARTADO`.
- **Uso:** obligatorio; es el insumo del testeo de hooks.
- **Evitar:** hooks sin disparador declarado; dos filas con el mismo disparador y
  el mismo ángulo.

| # | Hook | Disparador | Palabras | ¿≤3 s? | Estado |
|---|---|---|---:|---|---|
| 1 | | | | | |

Disparadores admitidos (vocabulario cerrado): `curiosidad`, `contradicción`,
`pérdida`, `prueba social`, `dato`, `pregunta`.

### Bloque `CHECKLIST` (SC-003)

- **Variantes:** ninguna. Siempre los mismos 7 ítems, en el mismo orden.
- **Tamaños:** 7 filas + cabecera.
- **Estados:** `APROBADO` / `FALLO`.
- **Uso:** obligatorio en cada pieza; es la evidencia de calidad.
- **Evitar:** añadir ítems ad hoc en una pieza concreta (los ítems se cambian en
  SC-004, no en la pieza); cambiar el orden.

| Ítem | Regla | Resultado |
|---|---|---|
| Hook en ≤3 s | BR-006 | |
| 5 hooks con ángulos distintos | BR-004 | |
| Las 4 capas escritas | BR-007 | |
| CTA concreto presente | BR-003 | |
| Sin afirmaciones fuera del contexto | BR-005 | |
| Framework declarado | BR-002 | |
| Tono alineado con el contexto | BR-001 | |

### Bloque `CONTEXTO` (SC-002)

- **Variantes:** `INCOMPLETO`, `VÁLIDO`, `DESACTUALIZADO`.
- **Tamaños:** sin límite superior; los 7 campos obligatorios no son opcionales.
- **Estados:** el estado vive en el frontmatter y se repite en el reporte de
  validación de consola.
- **Uso:** se valida antes de cualquier generación.
- **Evitar:** dejar campos obligatorios como placeholders vacíos sin que la
  validación los detecte.

### Bloque `INDICE` (SC-005)

- **Variantes:** ninguna. Una fila por pieza.
- **Tamaños:** crece con el banco; sin límite.
- **Estados:** el de cada pieza.
- **Uso:** consulta antes de generar.
- **Evitar:** duplicar el contenido de la pieza aquí; el índice solo orienta.

### Bloque `RESULTADO` (SC-003)

- **Variantes:** ninguna.
- **Tamaños:** una fila por medición.
- **Estados:** `SIN_MEDIR` (tabla vacía) / `MEDIDO`.
- **Uso:** opcional en V1; alimenta el aprendizaje sobre hooks.
- **Evitar:** registrar métricas sin ventana de observación.

## Pantallas clave

### SC-001 — Consola del agente

- **Objetivo:** generar una pieza y recibir un resultado accionable de una
  lectura.
- **Viewport:** terminal 80×24. Sin scroll para el caso feliz.
- **Estructura:** línea de inicio → (proceso) → bloque `RESUMEN`, o bloque
  `RECHAZO`.
- **Contenido realista** (caso de éxito, ejemplo completo y verosímil):

```text
$ generar pieza --tema "por qué perdemos clientes en la primera llamada" --plataforma tiktok --formato video-corto

Generando pieza: por qué perdemos clientes en la primera llamada · tiktok/video-corto

PIEZA GENERADA — por qué perdemos clientes en la primera llamada
Archivo:        banco/piezas/014-primera-llamada.md
Framework:      AIDA
Plataforma:     tiktok/video-corto
Contexto:       v3 (2026-10-10)
Checklist:      7/7 APROBADO
Hook sugerido:  #2 — "Tu cliente no se fue por el precio. Se fue en el minuto 3."
```

- **Jerarquía:** la ruta del archivo primero (es lo que el operador necesita para
  abrirla), después el framework y el contexto (para saber con qué se generó),
  después la calidad, después la recomendación.
- **Acción principal:** generar. Secundaria: validar contexto, regenerar hooks.
- **Estados:**
  - **Loading:** `Generando pieza: <tema> · <plataforma>/<formato>…` — una línea,
    sin spinner falso ni porcentaje inventado.
  - **Empty:** sin tema → bloque `RECHAZO` con causa `Falta el tema`.
  - **Error:** una línea, causa + qué hacer.
  - **Success:** bloque `RESUMEN` completo.
- **Interacción:** el operador lee y abre el archivo. No hay más.
- **Responsive:** no aplica.
- **Accesibilidad:** texto plano, etiquetas en lugar de color, sin emojis.
- **Referencia:** no hay imagen. El contrato de texto de arriba **es** la
  referencia.
- **Prompt visual:** no aplica (ver sección siguiente).

### SC-002 — Documento de contexto de marca

- **Objetivo:** definir la voz y los límites de la marca para que el agente no
  invente.
- **Viewport:** editor de texto.
- **Estructura:** frontmatter (`version`, `last_validated`, `status`) y 7 bloques
  obligatorios más vocabuario prohibido.
- **Contenido realista** (extracto):

```markdown
## Tono y voz
### Registro y ritmo
Directo, sin adornos. Frases cortas. Tuteo. Cero jerga de marketing.

### Lo que nunca decimos
"Revolucionario", "líder del sector", "sin esfuerzo".

## Prohibiciones
- No prometer resultados en euros.
- No comparar por nombre con competidores.
```

- **Jerarquía:** el estado de validación manda; después los campos obligatorios en
  orden fijo.
- **Acción principal:** rellenar y validar.
- **Estados:** `INCOMPLETO` (con la lista de lo que falta), `VÁLIDO` (con versión y
  fecha), `DESACTUALIZADO`.
- **Interacción:** edición manual; la validación se pide explícitamente.
- **Responsive / Accesibilidad:** no aplica más allá de texto plano.
- **Referencia / Prompt visual:** no aplica.

### SC-003 — Archivo de pieza

- **Objetivo:** leer, corregir, aprobar o descartar sin reescribir.
- **Viewport:** editor de texto.
- **Estructura:** frontmatter → Capas → CTA → Variantes de hook → Adaptación →
  Notas de producción → Checklist → Resultado. Orden fijo.
- **Contenido realista:** el especificado en `06-SCREEN-INVENTORY.md` (SC-003),
  con una pieza real de ≤ 120 líneas.
- **Jerarquía:** frontmatter (estado, framework, contexto) → capas → hooks →
  checklist.
- **Acción principal:** elegir hook y mover estado.
- **Estados:** `BORRADOR`, `EN_REVISION`, `APROBADA`, `PUBLICADA`, `DESCARTADA`.
- **Interacción:** edición manual del archivo. El agente solo escribe la versión
  inicial.
- **Responsive / Accesibilidad:** markdown plano; reflowea en móvil sin layout
  propio.
- **Referencia / Prompt visual:** no aplica.

### SC-004 — Reglas del agente

- **Objetivo:** tener el framework y el criterio escritos y auditables, fuera de un
  prompt invisible.
- **Estructura:** definición de las 4 capas de AIDA, mapeo a
  Hook/Substance/Payoff, catálogo de los 6 disparadores de hook, tabla de las 12
  reglas de negocio con ejemplo y excepción, y los 7 ítems del checklist.
- **Estados:** no aplica (documento de consulta).
- **Referencia / Prompt visual:** no aplica.

### SC-005 — Índice del banco

- **Objetivo:** no repetir temas ni ángulos.
- **Estructura:** tabla de 7 columnas: ID, Tema, Ángulo, Hook elegido, Estado,
  Plataforma, Fecha.
- **Estados:** vacío (`Banco vacío. Genera la primera pieza.`) / con filas /
  ilegible (aviso y se continúa sin comprobación de duplicados).
- **Referencia / Prompt visual:** no aplica.

### SC-006 — Reporte de rechazo

- **Objetivo:** convertir un rechazo en una lista de acciones.
- **Estructura:** causa, lista numerada de lo que falta, siguiente paso exacto,
  confirmación de que no se creó nada.
- **Estados:** contexto ausente, contexto incompleto, tema vacío, plataforma no
  soportada, fallo del proveedor.
- **Referencia / Prompt visual:** no aplica.

## Prompts generados

**Ninguno.** No hay herramienta de generación de imágenes en el alcance y no hay
nada visual que generar: el producto no tiene interfaz gráfica. No se generan
prompts visuales para no fabricar referencias de pantallas que no existen.

Cuando la Fase 7 declaró Dirección A, la "referencia" es el propio contrato de
texto de este documento, que es verificable y ejecutable. Se registra como
referencia aprobada en `design-reference/APPROVED.md`.

## Crítica de referencias

No hay imágenes. La crítica se aplica al contrato de texto, contra los mismos
criterios:

| Referencia | Claridad | Jerarquía | Datos reales | Estados | Responsive | Decisión |
|---|---|---|---|---|---|---|
| Contrato `RESUMEN` (SC-001) | Sí: la ruta del archivo está en la primera línea y a 80 columnas | Sí: archivo → framework/contexto → calidad → recomendación | Sí: ejemplo con tema real y hook plausible | Sí: éxito y con fallos | N/A (sin UI) | Aprobado v1 |
| Contrato `RECHAZO` (SC-006) | Sí: causa + lista + siguiente paso | Sí: la causa manda | Sí: campos faltantes concretos | Sí: 4 causas distintas | N/A | Aprobado v1 |
| Estructura de pieza (SC-003) | Sí: ≤ 120 líneas, orden fijo | Sí: frontmatter primero | Sí: ejemplo de TikTok con notas | Sí: 5 estados | N/A | Aprobado v1 |
| Checklist de 7 ítems | Sí: 7 filas, siempre el mismo orden | Sí | Sí: cada ítem referencia su regla BR | Sí: aprobado / fallo | N/A | Aprobado v1 |

## Diferencias permitidas entre imagen y producto

No aplica: no hay imagen de referencia. La única libertad del implementador es el
**orden interno de los campos dentro de una línea** de consola, siempre que
mantenga las etiquetas fijas, el límite de 80 columnas y el límite de líneas.

## Gate

- [x] Las pantallas clave tienen especificación.
- [x] Hay prompts estructurados o referencias generadas.
- [x] Las referencias están registradas en `design-reference/APPROVED.md`.
- [x] Estados y responsive están definidos.
- [x] Mobile conserva densidad visual, proporciones relativas y cantidad de contenido visible.
- [x] La interfaz móvil ocupa todo el ancho y fue especificada para 360, 375, 390, 412 y 430 px.
- [x] Screenshots y mockups se trataron como especificación geométrica cuando aplicaba.
- [x] Los componentes tienen reglas.
- [x] Un desarrollador puede implementar sin inventar el producto.

**Nota sobre las casillas 2, 5, 6 y 7:** se marcan como resueltas por **no
aplicabilidad explícita** (producto sin UI gráfica ni móvil), no por trabajo
realizado. La casilla 2 se cumple porque la referencia aprobada es el contrato de
texto, que está escrito y es verificable; no se declara ninguna imagen generada.
Documentado aquí para no dar por hecho un trabajo que no existe.

## Incertidumbres abiertas

- [x] [ASSUMPTION] El límite de 80 columnas es correcto para el terminal de
      Daniel. Si su terminal tiene otro ancho por defecto, se recalibra.
- [ ] [ASSUMPTION] Los límites de líneas (12 / 8 / 120) se validan con las
      primeras 10 piezas reales; si el resumen no cabe con advertencias, se
      prioriza la advertencia sobre la recomendación de hook.
- [ ] [DEFERRED:Fase 9] Cómo se implementa el checklist (reglas deterministas sobre
      el texto o segunda pasada del modelo). Determina si los 7 ítems son
      verificables automáticamente o solo asistidos.
- [ ] [DEFERRED:Fase 10] Dónde vive el índice del banco: derivado o mantenido.
