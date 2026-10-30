# Taxonomía

Vocabulario cerrado de plataformas, formatos y frameworks. Una pieza que use un
valor fuera de esta tabla es un fallo de validación (C-13), no una excepción
creativa. Si falta algo, se amplía este archivo y se registra la decisión.

## Frameworks

| ID | Framework | Capas declaradas | Cuándo aplica |
|---|---|---|---|
| `AIDA` | AIDA | Atención, Interés, Deseo, Acción | Por defecto en todos los formatos |
| `Hook/Substance/Payoff` | Hook / Substance / Payoff | Hook, Substance, Payoff | Video de ≤ 20 s donde Interés y Deseo no caben separados |
| `PAS` | Problema–Agitación–Solución | Problema, Agitación, Solución | Audiencia que ya conoce el problema y necesita ser convencida |
| `BAB` | Before–After–Bridge | Before, After, Bridge | Transformaciones visibles y demostrables |

**Obligación en todos los casos:** `AIDA` no exime de hook ni de CTA. Todo
framework alternativo declara su `razon_framework` (C-11) y mantiene una capa de
Atención y una de Acción explícitas, mapeadas según `reglas/aida.md`.

## Plataformas y formatos

| Plataforma | Formato | Duración / longitud objetivo | Particularidades |
|---|---|---|---|
| `instagram` | `reel` | 15–40 s | El hook compite con el texto en pantalla; el primer frame cuenta como Atención |
| `instagram` | `carrusel` | 5–8 tarjetas | La Atención vive en la tarjeta 1; la Acción, en la última |
| `tiktok` | `video-corto` | 15–60 s | Tolerancia mayor al hook hablado; el ritmo manda sobre la estructura visible |
| `youtube` | `short` | 20–60 s | Retención medida por segundos; el hook puede ser más descriptivo |
| `linkedin` | `post-texto` | 600–1.300 caracteres | Formato escrito: BR-006 no aplica (no hay 3 segundos); el hook es la primera línea visible antes del "ver más" |
| `linkedin` | `video-corto` | 30–90 s | Registro más formal; el hook debe funcionar sin sonido |

Plataformas que **no** están en el catálogo (Twitter/X, Facebook, Threads, YouTube
largo) se reportan como **no soportadas**. El agente no improvisa un formato: lo
dice y se detiene (UF-002).

## Estados de pieza

| Estado | Significado | Quién lo asigna |
|---|---|---|
| `BORRADOR` | Generada por el agente, sin revisar | Agente |
| `EN_REVISION` | El operador la está leyendo | Humano |
| `APROBADA` | Revisada y aceptada; lista para publicar | Humano |
| `PUBLICADA` | Publicada, con fecha | Humano |
| `DESCARTADA` | Rechazada, con motivo | Humano |

El agente **solo** puede crear `BORRADOR` (BR-012).

## Estados del contexto de marca

| Estado | Significado |
|---|---|
| `INCOMPLETO` | Falta al menos un campo obligatorio; la generación está bloqueada (BR-001) |
| `VÁLIDO` | Todos los campos presentes; la generación está habilitada |
| `DESACTUALIZADO` | Cambió una oferta o el posicionamiento; hay piezas que pueden afirmar algo ya falso |

## Métricas de resultado admitidas

| Métrica | Qué mide | Ventana típica |
|---|---|---|
| `retencion_3s` | Porcentaje que supera el segundo 3 | 7 días |
| `retencion_media` | Porcentaje medio de visualización | 7 días |
| `guardados` | Veces guardado | 14 días |
| `comentarios` | Comentarios | 14 días |
| `compartidos` | Veces compartido | 14 días |
| `clics` | Clics en el CTA cuando hay destino | 14 días |

Toda medición exige su ventana de observación: un número sin ventana no es
interpretable.

## Reglas de uso de esta taxonomía

1. Los valores se escriben en minúscula y sin acentos en el frontmatter
   (`instagram`, `video-corto`, `tiktok`) para que sean comparables de forma
   determinista.
2. `duracion_objetivo` usa segundos (`30 s`) o caracteres (`900 caracteres`) según el
   formato.
3. Añadir una plataforma, un formato, un framework o una métrica exige editar este
   archivo y registrar la decisión. No se admite en una pieza concreta.
