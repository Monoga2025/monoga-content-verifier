---
artifact: screen-inventory
phase: 6
status: approved
reason: ""
last_updated: "2026-10-12"
---

# 06 — Inventario de pantallas de Agente Generador de Contenido

> **No hay pantallas.** V1 es un agente sobre el repositorio (decisión del MVP).
> Las "superficies" de este producto son **artefactos en disco** y **mensajes en
> consola**. Este documento es, por tanto, la especificación de la estructura de
> esos artefactos: es el contrato de salida del agente y lo que hace posible
> validarlo de forma reproducible.
>
> Nota de alcance: si en el futuro se quisiera interfaz gráfica, este inventario
> sería el punto de partida, pero no está en V1.

## Navegación general

```text
Repositorio
├── contexto de marca            ← fuente de verdad, se valida antes de generar
│     └── versión + estado (INCOMPLETO / VÁLIDO / DESACTUALIZADO)
├── reglas del agente            ← conocimiento AIDA, reglas de estructura, checklist
├── banco de contenido
│     ├── índice                 ← qué temas y ángulos existen ya
│     └── piezas/                ← 1 archivo por pieza
└── consola                      ← feedback de cada operación
```

## Pantallas (superficies)

| ID | Superficie | Usuario | Objetivo | Acción principal | Flujo |
|---|---|---|---|---|---|
| SC-001 | Consola del agente | Operador | Ejecutar generación o validación y recibir el resultado | Indicar tema, plataforma y formato | UF-001, UF-002, UF-004 |
| SC-002 | Documento de contexto de marca | Operador | Definir la voz, la audiencia y los límites de la marca | Rellenar los campos obligatorios y validar | UF-001, UF-006 |
| SC-003 | Archivo de pieza | Operador | Leer, corregir, aprobar o descartar una pieza | Elegir hook y mover el estado | UF-003 |
| SC-004 | Reglas del agente | Operador | Consultar y ajustar el framework, las reglas y el checklist | Editar una regla | — (mantenimiento) |
| SC-005 | Índice del banco | Operador | Saber qué temas y hooks ya existen para no repetir | Consultar antes de generar | UF-007 |
| SC-006 | Reporte de rechazo | Operador | Saber exactamente qué falta para poder generar | Completar lo que falta | UF-004 |

## Detalle por superficie

### SC-001 — Consola del agente

- **Usuario:** Operador.
- **Objetivo:** ejecutar la generación de una pieza y recibir un resultado
  accionable en una sola lectura.
- **Entrada:** tema o ángulo (texto libre), plataforma (una del catálogo),
  formato (uno del catálogo de la plataforma). Opcional: marco de tiempo o
  duración objetivo.
- **Acción primaria:** generar la pieza.
- **Acciones secundarias:** validar el contexto de marca; regenerar solo los
  hooks; consultar el índice del banco.
- **Datos:** tema, plataforma, formato, contexto de marca activo y su versión.
- **Componentes:** mensaje de inicio, resumen final, advertencias, ruta del
  archivo creado.
- **Loading:** `Generando pieza: <tema> · <plataforma>/<formato>…` (una línea, sin
  barra de progreso falsa).
- **Empty:** sin tema indicado → `Indica un tema o ángulo concreto.` Sin contexto
  → deriva a SC-006.
- **Error:** ver tabla de errores de UF-002. Todo error nombra la causa concreta.
- **Success:** resumen con ruta del archivo, framework usado, hook recomendado,
  resultado del checklist y advertencias.
- **Responsive:** no aplica; se lee en escritorio. Debe caber en una pantalla de
  terminal sin scroll para el caso feliz.
- **Accesibilidad:** texto plano, sin color como único portador de significado
  (las advertencias se etiquetan con la palabra `AVISO`, no solo con color).
- **Salida:** archivo de pieza (SC-003) y resumen en consola.

**Estructura del resumen final (contrato de salida):**

```text
PIEZA GENERADA — <tema>
Archivo:        banco/piezas/<id>-<slug>.md
Framework:      AIDA (o el declarado, con su razón)
Plataforma:     <plataforma>/<formato>
Contexto:       v<versión> (<fecha de validación>)
Checklist:      7/7 APROBADO   (o "6/7 CON FALLOS: <ítem>")
Hook sugerido:  #2 — <texto>
AVISO:          tema sensible → requiere revisión humana antes de publicar
AVISO:          ángulo parecido a <ruta de pieza existente>
```

### SC-002 — Documento de contexto de marca

- **Usuario:** Operador.
- **Objetivo:** que la marca esté definida de forma que el agente pueda escribir
  con su voz y no pueda inventar.
- **Entrada:** escritura manual.
- **Acción primaria:** rellenar los campos obligatorios y validar.
- **Acciones secundarias:** añadir ejemplos de voz; versionar.
- **Datos:** campos obligatorios declarados en el dominio (posicionamiento,
  propuesta de valor, audiencia con dolores y deseos, tono y voz, ofertas
  vigentes, prohibiciones, 2+ ejemplos de voz) más la versión y la fecha.
- **Componentes:** un bloque por campo, y un bloque de **vocabulario prohibido**
  (palabras y promesas que la marca no usa nunca).
- **Loading:** no aplica.
- **Empty:** el documento existe con los campos vacíos y la validación falla
  nombrando cada campo que falta.
- **Error:** contradicción entre tono declarado y ejemplos de voz.
- **Success:** estado `VÁLIDO` con versión y fecha registradas.
- **Responsive:** no aplica.
- **Accesibilidad:** no aplica (archivo de texto).
- **Salida:** contexto `VÁLIDO` que habilita la generación.

**Estructura obligatoria (contrato de entrada del agente):**

```markdown
# Contexto de marca — <marca>
version: <n>
last_validated: <fecha>
status: INCOMPLETO | VÁLIDO | DESACTUALIZADO

## Posicionamiento
## Propuesta de valor
## Audiencia
### Dolores
### Deseos
## Tono y voz
### Registro y ritmo
### Lo que nunca decimos
## Ofertas vigentes
| Oferta | Qué incluye | Vigente desde | Vigente hasta |
## Prohibiciones
- ...
## Vocabulario prohibido
- ...
## Ejemplos de voz aprobados
### Ejemplo 1
### Ejemplo 2
```

### SC-003 — Archivo de pieza

- **Usuario:** Operador.
- **Objetivo:** leer, corregir, aprobar o descartar una pieza sin reescribirla.
- **Entrada:** generada por el agente; editada a mano por el operador.
- **Acción primaria:** elegir el hook y mover el estado.
- **Acciones secundarias:** corregir una capa; corregir o quitar el CTA; anotar el
  motivo de descarte.
- **Datos:** todos los del dominio de Pieza.
- **Componentes:** los bloques siguientes.
- **Loading:** no aplica.
- **Empty:** una pieza nunca se guarda vacía; si la generación falla, no hay
  archivo.
- **Error:** intento de aprobar con capa vacía, sin CTA o con checklist con fallos.
- **Success:** pieza en `APROBADA` con checklist completo.
- **Responsive:** no aplica; legible en móvil ocasionalmente (texto plano).
- **Accesibilidad:** no aplica.
- **Salida:** pieza aprobada, publicada o descartada.

**Estructura obligatoria del archivo de pieza:**

```markdown
---
pieza: <id>
tema: <tema o ángulo>
fecha: <fecha>
contexto_marca: v<versión>
framework: AIDA | PAS | BAB | Hook/Substance/Payoff
razon_framework: <por qué ese y no AIDA>
plataforma: <plataforma>
formato: <formato>
duracion_objetivo: <segundos o "n/a">
estado: BORRADOR | EN_REVISION | APROBADA | PUBLICADA | DESCARTADA
hook_elegido: <n o "sin elegir">
tema_sensible: sí | no
relacionada_con: <ruta o "—">
publicada_el: <fecha o "—">
motivo_descarte: <texto o "—">
---

# Pieza — <tema>

## Capas AIDA
### Atención (0–3 s)
<texto>
### Interés (3–10 s)
<texto>
### Deseo (10–20 s)
<texto>
### Acción (cierre)
<texto>

## CTA
- **Acción:** <verbo + objeto>
- **Destino o siguiente paso:** <...>
- **Alcanzable por la audiencia:** sí | no

## Variantes de hook
| # | Hook | Disparador | Palabras | ¿≤3 s? | Estado |
|---|---|---|---|---|---|
| 1 | | curiosidad / contradicción / pérdida / prueba social / dato / pregunta | | | |
| 2 | | | | | |
| 3 | | | | | |
| 4 | | | | | |
| 5 | | | | | |

## Adaptación
- **Plataforma y formato:** <...>
- **Longitud objetivo:** <...>
- **Ritmo:** <...>
- **Ajustes respecto a la versión base:** <...>

## Notas de producción
| Capa | Qué se ve | Recurso necesario |
|---|---|---|
| Atención | | |
| Interés | | |
| Deseo | | |
| Acción | | |

## Checklist
| Ítem | Regla | Resultado |
|---|---|---|
| Hook en ≤3 s | BR-006 | |
| 5 hooks con ángulos distintos | BR-004 | |
| Las 4 capas escritas | BR-007 | |
| CTA concreto presente | BR-003 | |
| Sin afirmaciones fuera del contexto | BR-005 | |
| Framework declarado | BR-002 | |
| Tono alineado con el contexto | BR-001 | |

## Resultado
| Fecha | Ventana | Métrica | Valor |
|---|---|---|---|
```

### SC-004 — Reglas del agente

- **Usuario:** Operador.
- **Objetivo:** tener el framework y el criterio de calidad escritos, versionados
  y auditables en lugar de dentro de un prompt invisible.
- **Entrada:** escritura manual.
- **Acción primaria:** editar una regla.
- **Acciones secundarias:** añadir un disparador de hook; añadir un ítem al
  checklist.
- **Datos:** definición de las 4 capas de AIDA, mapeo de AIDA a
  Hook/Substance/Payoff, catálogo de disparadores de hook, las 12 reglas de
  negocio y los 7 ítems del checklist.
- **Componentes:** un bloque por framework, un bloque por disparador, la tabla de
  reglas con ejemplo y excepción.
- **Loading / Empty / Error / Success:** no aplican (documento de consulta).
- **Responsive:** no aplica.
- **Accesibilidad:** no aplica.
- **Salida:** reglas que el agente aplica en cada generación.

### SC-005 — Índice del banco

- **Usuario:** Operador.
- **Objetivo:** saber de un vistazo qué temas, ángulos y hooks ya existen, para no
  repetirse (R-004).
- **Entrada:** derivado de las piezas existentes.
- **Acción primaria:** consultar.
- **Acciones secundarias:** ir a una pieza concreta.
- **Datos:** por pieza: id, tema, ángulo, hook elegido, estado, plataforma y fecha.
- **Componentes:** una tabla; agrupación por estado.
- **Loading:** no aplica.
- **Empty:** `Banco vacío. Genera la primera pieza.`
- **Error:** banco ilegible → aviso y la generación continúa sin comprobación de
  duplicados (UF-007).
- **Success:** no aplica.
- **Responsive:** no aplica.
- **Accesibilidad:** no aplica.
- **Salida:** evidencia de cobertura y de no repetición.

```markdown
| ID | Tema | Ángulo | Hook elegido | Estado | Plataforma | Fecha |
```

### SC-006 — Reporte de rechazo

- **Usuario:** Operador.
- **Objetivo:** convertir un "no se pudo" en una lista concreta de acciones.
- **Entrada:** el intento de generación fallido.
- **Acción primaria:** completar lo que falta.
- **Acciones secundarias:** ninguna.
- **Datos:** causa del rechazo; campos faltantes del contexto; plataformas
  soportadas; temas sensibles detectados.
- **Componentes:** causa, lista numerada de lo que falta, siguiente paso exacto.
- **Loading:** no aplica.
- **Empty:** no aplica.
- **Error:** no aplica (este artefacto *es* el error).
- **Success:** no aplica.
- **Responsive:** no aplica.
- **Accesibilidad:** no aplica.
- **Salida:** operador que sabe exactamente qué hacer a continuación.

```text
GENERACIÓN RECHAZADA
Causa:     Contexto de marca INCOMPLETO (BR-001)
Faltan:    1. Ofertas vigentes
           2. Prohibiciones
           3. Ejemplos de voz (hay 1, se requieren 2)
Siguiente: completa esos campos en <ruta> y valida el contexto.
No se generó ninguna pieza.
```

## Modales, drawers y componentes

| ID | Tipo | Propósito | Disparador |
|---|---|---|---|
| C-001 | Confirmación | Confirmar el descarte de una pieza, que exige motivo | Intento de pasar a `DESCARTADA` |
| C-002 | Aviso | Señalar tema sensible con revisión humana obligatoria | Generación de tema sensible |
| C-003 | Aviso | Señalar ángulo ya existente en el banco | Coincidencia con una pieza previa |
| C-004 | Aviso | Señalar piezas afectadas por una nueva versión del contexto | Revalidación del contexto (UF-006) |

En V1 estos "modales" son mensajes en consola o bloques dentro del archivo. No
hay UI.

## Mensajes externos

| Canal | Trigger | Contenido | Destinatario |
|---|---|---|---|
| Ninguno | — | V1 no envía correos, notificaciones ni mensajes externos | — |

La publicación en redes es una acción humana fuera del sistema.

## Copy funcional

Elementos cuya redacción ya está fijada y debe respetarse en la implementación:

- **Labels (consola):** `PIEZA GENERADA`, `GENERACIÓN RECHAZADA`, `Checklist`,
  `Framework`, `Contexto`, `Hook sugerido`, `AVISO`.
- **Ayudas:** al pedir el tema → `Indica un tema o ángulo concreto (por ejemplo:
  "por qué perdemos clientes en la primera llamada").`
- **Validaciones:** toda validación nombra el campo o la regla, nunca "datos
  inválidos". Ejemplo: `Falló BR-005: "triplica tus ventas" no está respaldado por
  el contexto.`
- **Confirmaciones:** el descarte exige motivo → `Indica el motivo del descarte.`
- **Errores:** ver UF-002, UF-003 y UF-004. Regla de estilo: **causa concreta +
  qué hacer**, sin disculpas ni relleno.
- **Prohibido en los mensajes:** "Lo siento", "Ha ocurrido un error inesperado",
  "Por favor, inténtalo de nuevo" sin causa. Cada mensaje debe permitir actuar sin
  preguntar nada a nadie.

## Gate

- [x] Cada flujo tiene superficies suficientes.
- [x] No hay pantallas sin objetivo.
- [x] Cada pantalla tiene acción principal.
- [x] Loading, empty, error y success están definidos.
- [x] Navegación funciona para el dispositivo principal.
- [x] El inventario incluye administración.

## Incertidumbres abiertas

- [x] [ASSUMPTION] No hay pantallas gráficas en V1; las superficies son archivos y
      consola. Confirmado por la exclusión explícita del MVP.
- [ ] [ASSUMPTION] La estructura del archivo de pieza (SC-003) es completa para
      video corto, pero puede sobrar o faltar para LinkedIn. Se ajusta cuando se
      genere la primera pieza de LinkedIn.
- [ ] [DEFERRED:Fase 8] Si el reporte de checklist se muestra como tabla o como
      lista dentro del archivo, y su formato visual definitivo.
- [ ] [DEFERRED:Fase 9] Cómo se evalúa el checklist técnicamente (reglas
      deterministas sobre el texto o segunda pasada del modelo), que determina si
      los 7 ítems son verificables de forma automática.
- [ ] [DEFERRED:Fase 10] Dónde vive el índice del banco y si se mantiene a mano o
      se deriva de las piezas.
