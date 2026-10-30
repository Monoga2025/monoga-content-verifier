---
artifact: brief
phase: 1
status: approved
reason: ""
last_updated: "2026-10-12"
---

# 01 — Brief de Agente Generador de Contenido

## Identificación

- **Cliente:** Monoga (interno)
- **Modo:** internal
- **Entrega:** prototype
- **Responsable del proyecto:** Daniel (Monoga)
- **Decisor final:** Daniel (Monoga)
- **Fecha del brief:** 2026-10-12

## Problema

### ¿Qué ocurre hoy?

Producir guiones para redes sociales con una estructura que retenga (AIDA u otro
framework) requiere, por pieza: definir el ángulo, escribir y descartar varios
hooks, ordenar el cuerpo, cerrar con CTA y adaptar todo al formato y a la
plataforma. Hoy eso se hace a mano o pidiendo texto suelto a un chat de IA sin
contexto de marca.

El resultado conocido de ese flujo improvisado es contenido genérico: la IA
reproduce la sintaxis del framework (Atención → Interés → Deseo → Acción) sin
aportar posicionamiento, audiencia ni tono propios. Los frameworks aplicados sin
contexto producen fatiga de plantilla y predictibilidad.

La investigación previa del propio Daniel (2026-10-12) confirma el estado del
mercado:

- Existen bundles de skills de marketing open source y gratuitos para agentes de
  IA —el más completo, `coreyhaines31/marketingskills`, 43 sub-skills, con
  `copywriting` (PAS, AIDA, Before-After-Bridge) y `social-content`— que se
  instalan con `npx skills add`.
- Existen skills de conversión y de redes específicas con bibliotecas de hooks
  ("scroll-stopping") y disparadores emocionales, y un framework Hook/Substance/
  Payoff para Reels que es esencialmente AIDA adaptado a video corto.
- Existen SaaS de plantillas AIDA (Jasper, Writesonic, Simplified), de pago,
  con la misma limitación de originalidad.

Conclusión de esa investigación: **la pieza que falta no es el framework ni el
plugin, es el contexto de marca**. Su propia recomendación fue "crea un
documento de contexto con tu marca, audiencia, tono y ofertas — sin esto,
cualquier herramienta producirá guiones genéricos".

### ¿Por qué importa?

Porque sin contexto propio, la salida es indistinguible de la de cualquier
competidor que use la misma herramienta. La ventaja competitiva no está en
generar texto, está en generar texto que suene a una marca concreta dirigido a
una audiencia concreta.

### ¿Cómo se resuelve actualmente?

1. Se busca en repositorios de skills, MCP Market o blogs qué plugin aplicar.
2. Se instala una skill genérica de copywriting o redes sociales.
3. Se le pide texto a un chat de IA sin contexto de marca o con contexto
   improvisado en el mismo mensaje.
4. Se reescribe a mano lo que salió genérico.
5. Se publica sin banco de variantes ni medición del hook.

### Costo observable

- **Tiempo:** una sesión de escritura por pieza; el trabajo real está en
  descartar hooks, no en redactar.
- **Dinero:** entre 0 € (skills gratuitas mal aprovechadas) y la cuota de un SaaS
  de copy (Jasper/Writesonic) que no resuelve el contexto de marca.
- **Errores:** hooks que no retienen los primeros 3 segundos; CTAs ausentes o
  desconectados del cuerpo del guion; mezcla de tonos entre piezas.
- **Riesgo:** dependencia de plugins de terceros que cambian o desaparecen, y
  salida genérica que erosiona diferenciación.
- **Pérdida de confianza:** cada pieza publicada sin contexto refuerza la
  percepción de "contenido de IA" ante la audiencia.

## Usuarios

| Usuario | Objetivo | Frecuencia | Dispositivo | Nivel técnico |
|---|---|---|---|---|
| Operador de contenido (Daniel) | Obtener N variantes de guion AIDA publicables con su marca en minutos | Diaria / por lote semanal | Escritorio (principal), móvil para revisar | Alto: usa terminal, agentes y skills |
| Revisor de marca | Aprobar tono y verificar que no se prometa lo que no se puede cumplir | Semanal | Escritorio, móvil para leer | Medio |

## Proceso actual

```text
Idea/tema → buscar plugin o skill → pedir texto a la IA sin contexto
→ reescribir lo genérico a mano → publicar sin variantes ni medición
```

## Proceso objetivo

```text
Contexto de marca cargado (posicionamiento, audiencia, tono, ofertas, prohibiciones)
→ tema o ángulo → generar N variantes de hook (Atención)
→ guion completo AIDA con CTA y notas de producción
→ checklist automático (hook ≤3 s, promesa verificable, CTA presente, tono)
→ banco de piezas para testear y medir
```

## Dolor principal

La IA entrega estructura sin criterio. El framework AIDA se aplica a la forma y
no al contenido, así que el guion sale correcto y a la vez inservible para esa
marca y esa audiencia.

## Resultado esperado

Un sistema propio que, partiendo de un contexto de marca explícito y reutilizable,
genere guiones de redes sociales con estructura AIDA verificable, en volumen
suficiente para testear varios hooks por idea, con la voz de la marca mantenida
entre piezas.

## Acción principal del usuario

Definir un tema o ángulo y generar un guion (con sus variantes de hook y su CTA)
a partir del contexto de marca ya cargado.

## Valor para administración

- Reutiliza y versiona el contexto de marca en lugar de reescribirlo por pieza.
- Crea un banco de piezas y variantes consultable y medible (qué hook funcionó).
- Sustituye dependencia de plugins de terceros por activos propios dentro del
  repositorio.
- Convierte el criterio de marketing en checklist verificable en vez de
  conocimiento tácito.

## Reglas del negocio conocidas

- AIDA (Atención, Interés, Deseo, Acción) es la columna vertebral estructural de
  todo guion generado.
- El hook ocupa los primeros 3 segundos y debe ser la parte con más variantes
  generadas.
- La "Acción" (CTA) debe ser concreta y aparecer de forma explícita; nunca se
  infiere.
- Toda afirmación sobre el producto u oferta debe ser verificable por el negocio;
  el sistema no inventa beneficios, precios ni resultados.
- Toda pieza respeta un documento de contexto de marca: posicionamiento,
  audiencia, tono, ofertas y prohibiciones.
- Un guion es una pieza de un banco: se genera en variantes para poder testear,
  no de una en una.
- El sistema no sustituye la estrategia: produce ejecución consistente dentro de
  una estrategia definida por el humano.

## Excepciones conocidas

- AIDA no encaja en todo formato: en video corto se admite el equivalente
  Hook/Substance/Payoff y en copy directo se admite PAS o Before-After-Bridge.
  El sistema debe declarar qué framework usó.
- Temas sensibles (salud, dinero, resultados garantizados) requieren revisión
  humana antes de publicar.
- Contexto de marca ausente o desactualizado: el sistema debe negarse a generar
  contenido "de marca" y decirlo, en lugar de inventar el contexto.
- Plataforma sin soporte (por ejemplo un formato que no exista en el catálogo)
  debe reportarse como no soportado, no improvisarse.

## Datos y archivos

- Documento de contexto de marca (posicionamiento, audiencia, tono, ofertas,
  prohibiciones) — fuente de verdad del sistema.
- Banco de piezas generadas (guion, variantes de hook, CTA, metadatos de
  plataforma y formato).
- Checklist de calidad por pieza.
- Candidatos identificados en la investigación: bundle `marketingskills`
  (copywriting, social-content, marketing-psychology), skills de hooks y de
  Instagram, y la propia estructura de skills del runtime.
- Ningún dato personal de terceros. No hay PII en el alcance actual.

## Integraciones

- Runtime de agente/skills ya disponible en el entorno de Daniel (candidato, no
  decidido).
- Proveedor de modelo de lenguaje con API (candidato, no decidido): implica
  coste y por tanto decisión Type 1 en Fase 9.
- Plataformas destino de publicación (Instagram, TikTok, YouTube Shorts,
  LinkedIn) — inicialmente solo como formato de salida, sin publicación
  automática.

## Restricciones

- **Presupuesto:** por definir; el coste de API es una decisión Type 1 diferida a
  Fase 9. Las alternativas open source y gratuitas deben preferirse cuando la
  calidad no se degrade.
- **Tiempo:** trabajo interno, sin fecha contractual externa.
- **Plataforma:** Windows; entorno de trabajo en escritorio.
- **Privacidad:** no se procesan datos personales de terceros; el contexto de
  marca es información propia del negocio.
- **Operación:** una sola persona operando; cualquier pieza que exija
  mantenimiento diario manual contradice el objetivo.
- **Otras:** el sistema no puede superar a una agencia en estrategia, conocimiento
  de mercado, producción audiovisual ni medición. El alcance es ejecución y
  volumen, no estrategia.

## Riesgos iniciales

- **R-001 — Salida genérica.** Si el contexto de marca es pobre, el sistema
  produce exactamente el contenido de plantilla que se quiere evitar. Es el
  riesgo central del proyecto.
- **R-002 — Expectativa sobredimensionada.** Esperar "mejores resultados que una
  agencia" cuando la brecha real es velocidad, volumen y coste.
- **R-003 — Dependencia de plugins de terceros.** Instalar skills externas
  introduce dependencia de repositorios ajenos, licencias y cambios de esquema.
- **R-004 — Fatiga de plantilla.** El uso mecánico de AIDA genera predictibilidad
  y la audiencia lo detecta.
- **R-005 — Afirmaciones no verificables.** El modelo puede inventar beneficios,
  cifras o promesas de resultado con consecuencias legales o reputacionales.
- **R-006 — Alcance elástico.** "Entrenar el agente" puede crecer sin límite
  hacia estrategia, publicación automática o analítica.

## Definición en cinco líneas

1. **Para quién:** para el operador de contenido de Monoga, que hoy escribe cada
   guion a mano o lo pide a una IA sin contexto.
2. **Problema:** la IA aplica AIDA a la forma y no al fondo, y produce guiones
   correctos pero genéricos, porque el contexto de marca no está sistematizado.
3. **Acción principal:** definir un tema y generar un guion AIDA con variantes de
   hook, CTA y checklist de calidad desde el contexto de marca cargado.
4. **Valor administrativo:** contexto de marca reutilizable y versionado, banco de
   piezas y variantes medible, y criterio de marketing convertido en checklist
   verificable, sin depender de plugins de terceros.
5. **Resultado de negocio:** reducir el tiempo por pieza publicable y aumentar el
   número de variantes testeables manteniendo una voz de marca consistente.

## Evidencia clasificada

- [FACT] El repositorio `coreyhaines31/marketingskills` existe, es open source y
  gratuito, agrupa 43 sub-skills e incluye `copywriting` (PAS, AIDA,
  Before-After-Bridge) y `social-content`. Fuente: investigación de Daniel,
  2026-10-12.
- [FACT] La instalación de esas skills se realiza con
  `npx skills add coreyhaines31/marketingskills` (o filtrando con `--skill`).
  Fuente: misma investigación.
- [FACT] Existen skills de redes con bibliotecas de hooks y un framework
  Hook/Substance/Payoff para Reels descrito como AIDA adaptado a video corto.
  Fuente: misma investigación.
- [FACT] Existen SaaS de plantillas AIDA de pago (Jasper, Writesonic,
  Simplified). Fuente: misma investigación.
- [FACT] La arquitectura de skills del runtime de Daniel permite cargar
  instrucciones de tarea por nombre. Fuente: catálogo de skills de la sesión.
- [FACT] El propio sistema de Daniel ya dispone de un método de proyecto por fases
  (Monoga Project OS) reutilizable para este producto. Fuente: skill
  `monoga-project-os` y `.monoga/state.json`.
- [INFERENCE] El cuello de botella real no es el framework sino el contexto de
  marca. Cálculo: la investigación identifica el framework como commodity
  (múltiples fuentes gratuitas equivalentes) y el contexto como el factor que
  todas las fuentes señalan como determinante de calidad; por tanto el factor
  escaso es el contexto. Fuente: conclusión explícita de la investigación de
  Daniel.
- [INFERENCE] El usuario principal es una sola persona con perfil técnico alto,
  porque el proyecto es interno, sin cliente externo ni mención de equipo.
  Fuente: nombre y ubicación del proyecto más la ausencia de terceros en el
  encargo.
- [INFERENCE] AIDA aplicado a video corto se traduce en Hook (Atención) +
  Substance (Interés/Deseo) + Payoff (Acción), lo que hace que las skills de
  redes de la investigación sean complementarias y no competidoras del enfoque
  AIDA. Fuente: descripción de la skill Instagram Content Strategy en la
  investigación.
- [ASSUMPTION] El sistema se usa para las marcas propias de Monoga, no como
  servicio multi-cliente. Si es falso, se necesita contexto de marca múltiple y
  aislamiento por cliente en Fases 4 y 10.
- [ASSUMPTION] "Entrenar el agente" significa dotarlo de contexto de marca,
  reglas, ejemplos y checklist, no reentrenar pesos de un modelo. Si es falso, el
  proyecto cambia de naturaleza, de coste y de fase.
- [ASSUMPTION] Las plataformas iniciales son Instagram (Reels), TikTok y YouTube
  Shorts, con LinkedIn como extensión barata. Si es falso, cambia el catálogo de
  formatos y longitudes en Fases 4 y 6.
- [ASSUMPTION] El formato de salida principal es texto estructurado (guion +
  hook + CTA + notas), sin generación de audio o video en el MVP. Si es falso,
  aparece una dependencia de proveedor audiovisual de coste alto.

## Incertidumbres abiertas

- [x] [BLOCKING] Qué es el agente y a qué se dedica — resuelto: generador de
  guiones de redes sociales con estructura AIDA y contexto de marca.
- [ ] [DEFERRED:Fase 2] Cuántas variantes de hook por pieza entran en el MVP y
  cuál es el mínimo de piezas para considerar el sistema útil.
- [ ] [DEFERRED:Fase 4] Catálogo exacto de frameworks alternativos (PAS,
  Before-After-Bridge, Hook/Substance/Payoff) y cuándo aplica cada uno.
- [ ] [DEFERRED:Fase 6] Formatos y longitudes por plataforma, y campos exactos de
  cada pieza del banco.
- [ ] [DEFERRED:Fase 9] Verificar licencia y esquema vigente de
  `marketingskills` antes de reutilizarlo.
- [ ] [DEFERRED:Fase 9] Proveedor de modelo (API propia, suscripción o runtime
  local), su coste y su política de uso de datos.
- [ ] [DEFERRED:Fase 9] Si se instalan skills de terceros o se escribe el
  conocimiento AIDA dentro del repositorio. Decisión Type 1 por dependencia y
  licencias.
- [ ] [DEFERRED:Fase 10] Si el contexto de marca y el banco de piezas viven en
  archivos del repositorio o en una base de datos.

## Gate

- [x] El problema está descrito sin usar "necesitamos una app" como explicación.
- [x] Existe usuario principal.
- [x] El proceso actual está documentado.
- [x] La acción principal está definida.
- [x] El valor administrativo está definido.
- [x] El resultado de negocio es verificable.
- [x] Las incertidumbres están clasificadas y no queda ningún `BLOCKING` abierto.
