---
artifact: domain-model
phase: 4
status: approved
reason: ""
last_updated: "2026-10-12"
---

# 04 — Modelo de dominio de Agente Generador de Contenido

> Dominio, no base de datos. Todavía no se eligen tablas, índices ni ORM
> (Fase 10). Aquí se decide qué cosas existen, cómo se llaman y qué reglas las
> gobiernan aunque cambie la herramienta.

## Entidad principal

**Pieza (Script).** Es lo que el negocio produce y lo que sobrevive a cualquier
cambio de herramienta, proveedor de modelo o formato de plataforma. Una pieza
existe desde que se genera hasta que se publica o se descarta, y permanece como
historial de qué se dijo, con qué ángulo y con qué resultado.

La pieza **no** es el guion de una plataforma concreta: es la unidad de contenido
de la marca, que declara para qué plataforma y formato se adaptó.

## Mapa conceptual

```text
CONTEXTO DE MARCA (1, fuente de verdad)
  ├── POSICIONAMIENTO
  ├── AUDIENCIA
  ├── TONO Y VOZ
  ├── OFERTAS
  ├── PROHIBICIONES
  ├── EJEMPLOS DE VOZ
  └── TAXONOMÍA (frameworks admitidos, plataformas, formatos)
        │
        └── PIEZA ────────────────────────────────┐
              ├── FRAMEWORK APLICADO (AIDA por defecto)
              ├── CAPAS  (Atención / Interés / Deseo / Acción)
              │     └── CTA (1, obligatorio, vive en la capa Acción)
              ├── HOOKS (5 variantes, alimentan la capa Atención)
              ├── ADAPTACIÓN (plataforma + formato + longitud)
              ├── CHECKLIST (resultado por ítem)
              ├── ESTADO (borrador → revisión → aprobada → publicada/descartada)
              └── RESULTADO (medición manual, opcional, fase posterior)
```

## Entidades

### ContextoDeMarca

- **Representa:** la fuente de verdad de quién es la marca, a quién le habla y
  qué puede y no puede decir. Es el activo que convierte texto genérico en texto
  de marca.
- **Persiste aunque:** cambie el proveedor de modelo, el formato de plataforma o
  el agente con el que se genere.
- **Atributos conceptuales:** posicionamiento, propuesta de valor, audiencia
  (dolores y deseos), tono y voz, ofertas vigentes, prohibiciones, ejemplos de
  voz aprobados, y la fecha de última revisión.
- **Relaciones:** tiene muchas Piezas. Es referenciado por cada Checklist.
- **Dueño:** Daniel (Monoga). Es información propia del negocio.
- **Creación:** manual, por el operador, al inicio del proyecto y en cada cambio
  de oferta o posicionamiento.
- **Estados:** `INCOMPLETO` → `VÁLIDO` → `DESACTUALIZADO`.
- **Cierre/eliminación:** no se elimina; se versiona. Un contexto no se borra
  porque las piezas antiguas deben seguir siendo explicables.
- **Historial requerido:** qué versión del contexto se usó al generar cada pieza.
  Sin esto no se puede saber por qué una pieza antigua dice lo que dice.

### Pieza

- **Representa:** una unidad de contenido de la marca, generada y todavía no
  descartada.
- **Persiste aunque:** cambie el hook ganador, el estado de publicación o el
  resultado medido.
- **Atributos conceptuales:** tema o ángulo de origen, framework aplicado, las
  cuatro capas con su texto, el CTA, la adaptación de plataforma y formato,
  versión del contexto de marca usada, fecha de creación y notas de producción.
- **Relaciones:** pertenece a un ContextoDeMarca (versión concreta); tiene
  exactamente 5 Hooks; tiene exactamente 1 CTA; tiene 1 Checklist; puede tener un
  Resultado medido.
- **Dueño:** Daniel.
- **Creación:** por generación del agente a partir de un tema y un contexto
  válido.
- **Estados:** `BORRADOR` → `EN_REVISIÓN` → `APROBADA` → `PUBLICADA`;
  desde cualquier estado anterior a publicación puede pasar a `DESCARTADA`.
- **Cierre/eliminación:** `DESCARTADA` conserva la pieza y el motivo del descarte;
  no se borra, porque el descarte también es información (qué ángulos no
  funcionan).
- **Historial requerido:** estado, motivo de descarte si aplica, y resultado
  medido cuando exista.

### Hook

- **Representa:** una variante concreta de la capa de Atención de una pieza. Es
  la parte con más impacto en los primeros 3 segundos y por eso es la que más
  variantes genera.
- **Persiste aunque:** cambie la plataforma o el formato.
- **Atributos conceptuales:** texto del hook, ángulo o disparador que usa
  (curiosidad, contradicción, pérdida, prueba social, dato, pregunta), y si fue
  el elegido.
- **Relaciones:** pertenece a una Pieza. Exactamente 5 por pieza.
- **Dueño:** Daniel.
- **Creación:** generado junto con la pieza.
- **Estados:** `PROPUESTO` → `ELEGIDO` o `DESCARTADO`.
- **Cierre/eliminación:** se conserva aunque se descarte: es el insumo del
  aprendizaje sobre qué hooks funcionan.
- **Historial requerido:** cuál se eligió por pieza.

### Layer (Capa)

- **Representa:** cada una de las cuatro etapas de AIDA dentro de una pieza. Es
  una parte estructurada de la pieza, no una entidad independiente con vida
  propia.
- **Persiste aunque:** cambie el formato o la plataforma.
- **Atributos conceptuales:** tipo de capa (Atención, Interés, Deseo, Acción),
  contenido textual, nota de producción (qué se ve mientras se dice).
- **Relaciones:** cuatro por pieza; la capa Acción contiene el CTA.
- **Dueño:** Daniel.
- **Creación:** generada junto con la pieza.
- **Estados:** `VACÍA` → `ESCRITA` → `APROBADA`. Una pieza no puede estar
  aprobada con una capa vacía.
- **Cierre/eliminación:** se elimina solo si se descarta la pieza completa.
- **Historial requerido:** ninguno propio; el de la pieza lo cubre.

### CTA

- **Representa:** la acción concreta que la audiencia debe ejecutar. Es una
  entidad separada de la capa Acción porque debe ser verificable
  individualmente: el checklist falla si no existe.
- **Persiste aunque:** cambie el copy del resto de la pieza.
- **Atributos conceptuales:** verbo de acción, destino o siguiente paso, y si la
  acción es alcanzable por la audiencia real.
- **Relaciones:** uno por pieza, vive dentro de la capa Acción.
- **Dueño:** Daniel.
- **Creación:** generado junto con la pieza.
- **Estados:** `PROPUESTO` → `VALIDADO`.
- **Cierre/eliminación:** no se elimina sin descartar la pieza.
- **Historial requerido:** ninguno propio.

### Checklist

- **Representa:** el criterio de marketing convertido en verificación por pieza.
  Es la diferencia entre "el modelo dijo algo" y "el modelo cumplió las reglas".
- **Persiste aunque:** cambie el modelo o el prompt.
- **Atributos conceptuales:** ítems evaluados (hook ≤3 segundos, 5 hooks
  distintos, CTA presente y concreto, las 4 capas escritas, promesa verificable
  contra el contexto, tono alineado, framework declarado) y el resultado
  aprobado/fallo de cada uno.
- **Relaciones:** uno por pieza; referencia la versión de ContextoDeMarca contra
  la que se verificó.
- **Dueño:** Daniel.
- **Creación:** generado al generar la pieza, no después.
- **Estados:** `PENDIENTE` → `APROBADO` / `CON_FALLOS`.
- **Cierre/eliminación:** permanente con la pieza.
- **Historial requerido:** el resultado completo, porque es la evidencia de
  calidad de la pieza.

### Taxonomía

- **Representa:** los vocabularios controlados del sistema: frameworks admitidos
  (AIDA por defecto; PAS, Before-After-Bridge, Hook/Substance/Payoff como
  alternativas declarables), plataformas (Instagram, TikTok, YouTube Shorts,
  LinkedIn) y formatos.
- **Persiste aunque:** cambien las modas o las plataformas: se amplía, no se
  reescribe.
- **Atributos conceptuales:** nombre, cuándo aplica, y su restricción de formato.
- **Relaciones:** usada por Piezas y por la adaptación de cada pieza.
- **Dueño:** Daniel.
- **Creación:** definida en Fase 6 para plataformas y formatos.
- **Estados:** `ACTIVO` / `RETIRADO`.
- **Cierre/eliminación:** se retira, no se borra: hay piezas históricas que lo
  usan.
- **Historial requerido:** no.

### Resultado

- **Representa:** el rendimiento observado de una pieza publicada. Existe como
  entidad porque es la única forma de saber qué hooks funcionan, pero en V1 se
  alimenta a mano y es opcional.
- **Persiste aunque:** cambie la plataforma.
- **Atributos conceptuales:** métrica observada, valor, fecha de medición y
  ventana de observación.
- **Relaciones:** opcional, pertenece a una Pieza publicada.
- **Dueño:** Daniel.
- **Creación:** manual.
- **Estados:** `SIN_MEDIR` → `MEDIDO`.
- **Cierre/eliminación:** no se elimina.
- **Historial requerido:** sí; una pieza puede medirse en ventanas distintas.

## Actores

| Actor | Responsabilidad | Entidades que controla |
|---|---|---|
| Operador de contenido (Daniel) | Definir tema y ángulo, revisar, aprobar, publicar, medir | ContextoDeMarca, Pieza, Checklist, Resultado |
| Agente generador (sistema) | Generar pieza, hooks, capas, CTA y checklist; rechazar generación sin contexto válido | Crea Pieza, Hook, Capa, CTA, Checklist. No aprueba ni publica |
| Revisor de marca (fase posterior) | Aprobar tono y detectar promesas no verificables | Pieza (a `APROBADA`) |

El agente **nunca** mueve una pieza a `PUBLICADA`. Publicar es una acción humana
irreversible hacia el exterior.

## Eventos del negocio

- `ContextoDeMarca validado` — el contexto pasa a `VÁLIDO` y habilita la generación.
- `Pieza generada` — se crean pieza, 4 capas, 5 hooks, 1 CTA y 1 checklist.
- `Generación rechazada` — el contexto es inválido; no se crea ninguna pieza.
- `Hook elegido` — uno de los 5 pasa a `ELEGIDO`.
- `Pieza aprobada` — el operador acepta la pieza para uso.
- `Pieza publicada` — acción humana; habilita la medición.
- `Pieza descartada` — con motivo registrado.
- `Pieza medida` — se registra un Resultado.
- `Contexto de marca actualizado` — nueva versión; las piezas anteriores
  conservan la referencia a la versión con la que se generaron.

## Reglas

| ID | Regla | Ejemplo | Excepción |
|---|---|---|---|
| BR-001 | Ninguna pieza se genera sin contexto de marca válido. | Contexto sin ofertas cargadas → el agente se detiene y nombra "ofertas" como campo faltante. | Ninguna. Es la regla que protege el propósito del producto. |
| BR-002 | Toda pieza declara el framework que usa y por qué. | Una pieza de Reels declara Hook/Substance/Payoff indicando que AIDA se mapea a esas tres fases. | Ninguna. Se puede usar otro framework, no se puede usar uno sin declararlo. |
| BR-003 | La capa Acción exige un CTA explícito y concreto. | "Guarda este video para tu próxima campaña" es válido; "sígueme" sin más contexto se marca como débil. | Ninguna. |
| BR-004 | Exactamente 5 hooks por pieza, cada uno con ángulo distinto. | Cinco reformulaciones de la misma pregunta no cumplen: falla el checklist. | Temas sensibles o de nicho pueden justificar menos, siempre registrando el motivo. |
| BR-005 | El sistema no inventa beneficios, precios, cifras ni promesas de resultado. | Si la pieza afirma "triplica tus ventas", el checklist falla salvo que el contexto de marca lo respalde. | Ninguna. Es riesgo reputacional y legal (R-005). |
| BR-006 | El hook debe poder decirse en ≤ 3 segundos. | Un hook de 28 palabras se marca como fallo y se propone recorte. | Formatos escritos largos (LinkedIn) que no son video. |
| BR-007 | Las 4 capas de AIDA se etiquetan y ninguna queda vacía. | Interés presente pero Deseo vacío → la pieza no puede pasar a `APROBADA`. | Frameworks alternativos declaran sus propias fases equivalentes. |
| BR-008 | Cada pieza guarda la versión del contexto de marca con la que se generó. | Una pieza de hace 3 meses explica sus afirmaciones con el contexto de entonces. | Ninguna. |
| BR-009 | Toda pieza vive en el banco; el descarte no borra. | Descartar una pieza guarda el motivo, para no repetir el ángulo. | Ninguna. |
| BR-010 | Temas sensibles exigen revisión humana antes de publicar. | Salud, dinero o resultados garantizados no se publican desde el estado `APROBADA` sin lectura explícita. | Ninguna. |
| BR-011 | Solo hay un contexto de marca activo a la vez en V1. | Cambiar de marca es un cambio de alcance, no una configuración. | Multi-marca está en `COULD`, no en V1. |
| BR-012 | El agente no publica ni mide: no tiene permiso sobre esos estados. | El sistema entrega la pieza `APROBADA`; el paso a `PUBLICADA` es humano. | Ninguna en V1. |

## Estados y transiciones

```text
CONTEXTO:  INCOMPLETO → VÁLIDO → DESACTUALIZADO → (revisión) → VÁLIDO

PIEZA:     BORRADOR → EN_REVISIÓN → APROBADA → PUBLICADA
               └──────────┴─────────────┴──→ DESCARTADA (con motivo)

HOOK:      PROPUESTO → ELEGIDO
                    └→ DESCARTADO (se conserva)

CAPA:      VACÍA → ESCRITA → APROBADA

CHECKLIST: PENDIENTE → APROBADO
                    └→ CON_FALLOS (impide APROBADA)

RESULTADO: SIN_MEDIR → MEDIDO
```

Ninguna transición salta de `BORRADOR` a `PUBLICADA`: publicar exige aprobación
humana previa.

## Invariantes

- Ninguna pieza existe sin una versión de contexto de marca asociada.
- Ninguna pieza aprobada tiene capas vacías, checklist con fallos ni CTA ausente.
- El número de hooks propuestos por pieza es 5, salvo excepción justificada.
- Una pieza no puede tener dos CTAs.
- El agente no puede mover una pieza a `PUBLICADA` ni marcar un Resultado.
- El contexto de marca activo es único.

## Casos límite

- **Contexto de marca parcialmente cargado.** El agente no genera "lo que pueda":
  se detiene y enumera los campos faltantes (BR-001).
- **Contexto desactualizado** (oferta que ya no existe). Una pieza puede afirmar
  algo válido en su momento y falso hoy. El sistema marca las piezas cuya versión
  de contexto ya no es la activa, para revisión.
- **Los 5 hooks son el mismo ángulo.** El checklist debe detectarlo; si no lo
  detecta, el volumen de variantes es falso y la métrica del MVP se cumple en
  vano (R-004).
- **Tema sensible.** La pieza puede generarse y aprobarse, pero publicarla exige
  revisión humana explícita (BR-010).
- **Plataforma fuera del catálogo.** Se reporta como no soportada; no se
  improvisa un formato.
- **Afirmación que suena a dato pero no está en el contexto.** Falla el checklist
  y la pieza no puede aprobarse hasta corregirla o respaldarla.
- **Tema repetido.** Ya existe una pieza con ese ángulo: el banco debe
  señalizarlo para no publicar el mismo contenido con otro hook.
- **Fallo del proveedor de modelo a mitad de generación.** No se guarda una pieza
  incompleta: o se guarda completa con checklist, o no se guarda.

## Términos del negocio

| Término | Significado exacto |
|---|---|
| Pieza | Unidad de contenido de la marca: tema + framework + 4 capas + 5 hooks + CTA + adaptación. No es "un post". |
| Hook | Variante de la capa de Atención; lo primero que se dice, con objetivo de retener los primeros 3 segundos. |
| Capa | Cada fase de AIDA dentro de una pieza (Atención, Interés, Deseo, Acción). |
| CTA | Acción concreta y verificable que se pide en la capa Acción. |
| Contexto de marca | Documento fuente de verdad sobre posicionamiento, audiencia, tono, ofertas y prohibiciones. Sin él no se genera. |
| Framework | Estructura narrativa declarada: AIDA por defecto; PAS, Before-After-Bridge y Hook/Substance/Payoff como alternativas. |
| Banco de contenido | Conjunto versionado de piezas generadas, aprobadas y descartadas. |
| Adaptación | Ajuste de la pieza a una plataforma y formato concretos (longitud, ritmo, registro). |
| Entrenar el agente | Dotarlo de contexto, reglas y ejemplos. **No** significa reentrenar pesos de un modelo (A-005). |
| Pieza publicable | Pieza aprobada que el operador considera lista para publicar con edición ligera, no reescritura de fondo. |

## Gate

- [x] La entidad persistente principal está identificada.
- [x] Cada entidad tiene ciclo de vida.
- [x] Las relaciones importantes están claras.
- [x] Estados y transiciones no se contradicen.
- [x] Las reglas críticas tienen ejemplo.
- [x] El historial necesario está definido.
- [x] Todavía no se confundió dominio con tablas.

## Incertidumbres abiertas

- [x] [ASSUMPTION] Campos obligatorios del contexto de marca: posicionamiento,
      propuesta de valor, audiencia con dolores y deseos, tono y voz, ofertas
      vigentes, prohibiciones y al menos 2 ejemplos de voz. Un contexto sin
      cualquiera de ellos queda `INCOMPLETO` y bloquea la generación (BR-001).
- [ ] [ASSUMPTION] El número de hooks por pieza (5) y el umbral del hook (3
      segundos) son decisiones de producto, no medidas. Se validan con piezas
      reales en Fase 14.
- [ ] [DEFERRED:Fase 6] Lista cerrada de disparadores de hook (curiosidad,
      contradicción, pérdida, prueba social, dato, pregunta) y cuáles son
      obligatorios.
- [ ] [DEFERRED:Fase 6] Valores de plataforma y formato, y límites de longitud.
- [ ] [DEFERRED:Fase 9] Cómo se verifica BR-005 (no inventar beneficios): por
      reglas deterministas contra el contexto o por segunda pasada del modelo.
- [ ] [DEFERRED:Fase 10] Cómo se materializa la versión del contexto de marca por
      pieza (BR-008) en archivos o base de datos.
