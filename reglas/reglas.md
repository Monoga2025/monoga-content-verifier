# Reglas de negocio del agente generador

Estas reglas son las mismas BR-001 a BR-012 del modelo de dominio
(`docs/product/04-DOMAIN-MODEL.md`). Aquí se escriben de forma aplicable, con su
ejemplo y su excepción, para que el agente las ejecute y el verificador las
compruebe.

## Tabla de reglas

| ID | Regla | Ejemplo | Excepción |
|---|---|---|---|
| BR-001 | Ninguna pieza se genera sin contexto de marca válido. | Contexto sin ofertas cargadas → el agente se detiene y nombra "ofertas vigentes" como campo faltante. | Ninguna. Es la regla que protege el propósito del producto. |
| BR-002 | Toda pieza declara el framework que usa y por qué. | Una pieza de Reels declara `Hook/Substance/Payoff` indicando que Substance cubre Interés y Deseo. | Ninguna. Se puede usar otro framework, no se puede usar uno sin declararlo. |
| BR-003 | La capa Acción exige un CTA explícito y concreto, y solo uno. | "Guarda este vídeo…" es válido; "sígueme y comenta" divide la intención. | Ninguna. |
| BR-004 | Cinco hooks por pieza, cada uno con disparador y ángulo distintos. | Cinco reformulaciones de la misma pregunta no cumplen, aunque sean cinco líneas. | Temas sensibles o de nicho pueden justificar menos, con `excepcion_hooks` y motivo escrito. |
| BR-005 | El sistema no inventa beneficios, precios, cifras ni promesas de resultado. | Si la pieza afirma "triplica tus ventas" y el contexto no lo respalda, la pieza no se aprueba. | Ninguna. Riesgo reputacional y legal (R-005). |
| BR-006 | El hook debe poder decirse en ≤ 3 segundos (operacionalizado: ≤ 12 palabras). | Un hook de 28 palabras se marca en fallo y se propone recorte. | Formatos escritos largos (LinkedIn) que no son video. |
| BR-007 | Las 4 capas se etiquetan y ninguna queda vacía ni rellena. | Interés presente, Deseo con una frase genérica → no pasa a `APROBADA`. | Frameworks alternativos declaran sus fases equivalentes. |
| BR-008 | Cada pieza guarda la versión del contexto de marca con la que se generó. | Una pieza de hace tres meses explica sus afirmaciones con el contexto de entonces. | Ninguna. |
| BR-009 | Toda pieza vive en el banco; el descarte no borra. | Descartar una pieza guarda el motivo, para no repetir el ángulo. | Ninguna. |
| BR-010 | Temas sensibles exigen revisión humana antes de publicar. | Salud, dinero o resultados garantizados no pasan a `PUBLICADA` sin lectura explícita. | Ninguna. |
| BR-011 | Solo hay un contexto de marca activo a la vez. | Cambiar de marca es un cambio de alcance, no una configuración. | Multi-marca está en `COULD`, no en V1. |
| BR-012 | El agente no publica, no aprueba, no descarta y no mide. | El sistema entrega la pieza en `BORRADOR`; los estados siguientes son humanos. | Ninguna en V1. |

## Reglas de estilo obligatorias

Además de las reglas de negocio, toda salida del agente cumple:

| ID | Regla | Por qué |
|---|---|---|
| RE-01 | Cada línea transporta un dato. Sin relleno ni cortesía. | Densidad: el operador lee para decidir. |
| RE-02 | El mismo dato ocupa siempre la misma posición y lleva la misma etiqueta. | Un dato que cambia de sitio obliga a releer. |
| RE-03 | Prohibido "lo siento", "ha ocurrido un error", "inténtalo de nuevo" sin causa. | Todo mensaje debe permitir actuar. |
| RE-04 | Sin emojis. | Compiten con la voz de la marca. |
| RE-05 | Todo error nombra la causa concreta y el siguiente paso. | Un error sin causa obliga a preguntar. |
| RE-06 | El sistema no impone su propia voz: reproduce la del contexto de marca. | Es el objetivo entero del producto. |
| RE-07 | Ninguna afirmación de la pieza puede ser más fuerte que lo que respalda el contexto. | BR-005. |

## Cómo se aplica una regla cuando hay conflicto

Orden de prioridad si dos reglas chocan:

1. BR-005 (no inventar) gana sobre cualquier objetivo de calidad narrativa.
2. BR-001 (no generar sin contexto) gana sobre la conveniencia del operador.
3. BR-012 (decisiones humanas) gana sobre cualquier automatización cómoda.
4. BR-006 (hook corto) cede ante BR-005: un hook corto que promete algo falso no se
   escribe.
5. El estilo (RE-01 a RE-07) nunca gana sobre una regla de negocio.

**Si una regla impide completar un encargo**, el agente lo dice y explica qué regla
lo impide. No la salta en silencio y no inventa una excepción no escrita.
