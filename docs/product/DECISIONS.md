# Decisiones de Agente Generador de Contenido

## ADR-001 — AIDA como columna vertebral y el contexto de marca como fuente de verdad

- **Estado:** Accepted
- **Fecha:** 2026-10-12
- **Fase:** 1

### Contexto

La investigación de mercado identificó múltiples skills, plugins y SaaS que ya
aplican AIDA, PAS y otros frameworks, varias de ellas gratuitas y abiertas. La
misma investigación señala que el resultado sigue siendo genérico cuando falta el
contexto de marca y que la aplicación mecánica de AIDA produce fatiga de
plantilla. El proyecto no puede justificar su existencia por "aplicar AIDA",
porque eso ya es commodity.

### Opciones

1. **Construir el proyecto alrededor de un plugin o skill de terceros**, con el
   contexto de marca como entrada opcional.
2. **Construir el proyecto alrededor de un contexto de marca propio y
   versionado**, con AIDA como estructura obligatoria y el conocimiento del
   framework escrito dentro del repositorio, admitiendo adaptadores externos como
   complemento.
3. **Adoptar un SaaS de copy con plantillas AIDA** y estandarizar el proceso
   sobre esa herramienta.

### Decisión

Opción 2. El contexto de marca es artefacto obligatorio y fuente de verdad; AIDA
es la estructura obligatoria y declarada de cada guion; el conocimiento del
framework y el checklist de calidad son activos propios del repositorio. La
reutilización de skills de terceros queda como decisión explícita y diferida a
Fase 9, no como cimiento.

### Razón

Es la única opción que ataca el factor escaso (contexto y criterio) en lugar del
factor abundante (plantillas de framework). También elimina la dependencia
estructural de repositorios ajenos, que es el riesgo R-003, y permite que el
sistema se niegue a generar cuando no hay contexto, que es la mitigación central
de R-001.

### Consecuencias

- Construir el documento de contexto de marca pasa a ser parte del alcance
  obligatorio, no un extra (supuesto A-008).
- El producto no se define por una herramienta externa, así que sobrevive a que
  un plugin desaparezca.
- Hay que escribir y mantener el conocimiento AIDA y el checklist dentro del
  repositorio (coste de mantenimiento asumido).
- La evaluación de licencias de terceros deja de bloquear el diseño, pero sigue
  pendiente antes de instalar cualquier cosa (Fase 9).

### Artefactos afectados

- `docs/product/01-BRIEF.md` (reglas del negocio y alcance)
- `docs/product/02-MVP-SCOPE.md` (el contexto de marca entra en el MVP)
- `docs/product/09-TECH-ARCHITECTURE.md` (adaptadores externos opcionales)
- `docs/product/ASSUMPTIONS.md` (A-004, A-008, A-011)

## ADR-002 — Almacenamiento en archivos versionados, sin base de datos

- **Estado:** Accepted
- **Fecha:** 2026-10-12
- **Fase:** 9

### Contexto

El dominio (Fase 4) define entidades con estados, versiones y relaciones:
ContextoDeMarca, Pieza, Hook, Capa, CTA, Checklist, Taxonomía y Resultado. El
volumen esperado es de decenas a cientos de piezas, con un solo usuario local. La
arquitectura debe permitir explicar por qué una pieza antigua dice lo que dice
(BR-008) y no perder el descarte (BR-009).

### Opciones

1. **SQLite o Postgres** con tablas, constraints e índices.
2. **Archivos markdown versionados en git**, con la estructura del dominio
   reflejada en el frontmatter.
3. Servicio externo de contenido (CMS headless o similar).

### Decisión

Opción 2. El banco de piezas, el contexto de marca y las reglas viven como
archivos de texto en el repositorio, versionados con git.

### Razón

El producto se define por el criterio escrito y auditable (ADR-001). Un archivo de
texto es revisable, diffeable y recuperable sin herramientas; una base de datos
esconde esas decisiones en filas que nadie lee. El volumen no justifica
infraestructura, y la regla de simplicidad del método prohíbe añadir
infraestructura sin evidencia. Además, el modelo de lenguaje lee archivos de
contexto de forma directa, no consulta SQL.

### Consecuencias

- No hay migraciones, ni servidor, ni cadena de conexión, ni copia de seguridad
  separada: el repo *es* la base de datos.
- Las consultas agregadas (índice del banco) se derivan con un script, no con SQL.
- Los invariantes del dominio (4 capas, 5 hooks, 1 CTA, checklist sin fallos) deben
  protegerse con código de verificación, porque no hay constraints de base de datos
  que los impongan.
- La calidad depende de que la edición manual del contexto de marca se valide.

### Artefactos afectados

- `docs/product/09-TECH-ARCHITECTURE.md`
- `docs/product/10-DATA-AND-PERMISSIONS.md`
- `docs/product/04-DOMAIN-MODEL.md` (los invariantes pasan a verificarse en código)

## ADR-003 — Cero dependencias de terceros en V1

- **Estado:** Accepted
- **Fecha:** 2026-10-12
- **Fase:** 9

### Contexto

La investigación de Fase 1 identificó bundles de skills open source que ya aplican
AIDA, PAS y frameworks de copy (`coreyhaines31/marketingskills` con 43 sub-skills,
entre otros). Instalarlas por `npx skills add` es inmediato y gratuito. El riesgo
R-003 señala la dependencia de repositorios ajenos, sus licencias y sus cambios de
esquema.

### Opciones

1. **Instalar y depender de `marketingskills`** (o similar) como base del
   framework y del copywriting.
2. **Escribir el conocimiento AIDA, los disparadores y el checklist dentro del
   repositorio**, sin instalar nada.
3. Instalar las skills como complemento opcional y escribir igualmente lo propio.

### Decisión

Opción 2 en V1. La opción 3 queda abierta como mejora futura, con licencia
verificada y aislada tras un adaptador.

### Razón

El framework AIDA es commodity: la propia investigación concluyó que el factor
escaso es el contexto de marca, no la plantilla del framework. Depender de un
repositorio de terceros para lo que ya es abundante introduce un riesgo
permanente a cambio de un ahorro de una sola sesión de trabajo. El checklist
propio, además, debe reflejar reglas de negocio específicas (BR-005, BR-006) que
ninguna skill genérica implementa.

### Consecuencias

- Coste asumido: escribir `reglas/aida.md`, `reglas/reglas.md`,
  `reglas/disparadores.md` y `reglas/checklist.md` (estimado: 1 sesión).
- El sistema no se rompe si un repositorio externo cambia o desaparece.
- Si más adelante se reutiliza una skill, debe verificarse su licencia y quedar
  tras un adaptador, sin convertirse en cimiento.
- Se cierra la incertidumbre A-011 y se mitiga R-003.

### Artefactos afectados

- `docs/product/09-TECH-ARCHITECTURE.md`
- `docs/product/ASSUMPTIONS.md` (A-011 pasa a resuelto)
- `docs/product/03-COMMERCIAL-SCOPE.md` (dependencias externas)
- `docs/product/RISKS.md` (R-003)

## ADR-004 — Verificación determinista en Python para lo verificable

- **Estado:** Accepted
- **Fecha:** 2026-10-12
- **Fase:** 9

### Contexto

El checklist tiene 7 ítems. Algunos son mecánicos (existen 4 capas, hay 5 hooks,
hay 1 CTA, el frontmatter declara framework, el hook tiene ≤ 12 palabras). Otros
son semánticos (el tono está alineado, ninguna afirmación sale del contexto de
marca). La calidad del producto depende de que un fallo se detecte **antes** de
que la pieza llegue al operador como aprobada.

### Opciones

1. **Segunda pasada del modelo** evaluando su propia salida.
2. **Script Python determinista** sobre el texto generado, sin dependencias.
3. Verificación manual del operador en cada pieza.

### Decisión

Opción 2 para lo mecánico, obligatoria antes de guardar. Los ítems semánticos
quedan como verificación asistida por modelo, **marcados explícitamente en el
reporte como asistidos y no deterministas**, y siempre sujetos a la lectura del
operador.

### Razón

El mismo modelo que inventó una cifra no es una fuente fiable para detectar que la
inventó (mitigación de R-005). Un script determinista es reproducible, auditable y
gratuito, y protege los invariantes del dominio que ya no protege una base de datos
(ADR-002). La verificación manual no escala al volumen que el producto busca
(5 variantes por pieza, varias piezas por sesión).

### Consecuencias

- Se escriben `codigo/validar_contexto.py` y `codigo/validar_pieza.py`, sin
  dependencias externas.
- El reporte de checklist debe distinguir ítem determinista de ítem asistido: no se
  puede presentar una verificación asistida como prueba.
- Una pieza con fallo determinista no se guarda como válida; el fallo es visible y
  bloquea la aprobación (BR-007, invariante del dominio).
- El spike 1 y el spike 2 de la Fase 12 verifican si esta decisión se sostiene en
  la práctica; si no, se revisa antes de construir.

### Artefactos afectados

- `docs/product/09-TECH-ARCHITECTURE.md`
- `docs/product/11-BUILD-PLAN.md` (la verificación es parte de la Vertical Slice 0)
- `docs/product/14-QA-REPORT.md` (los ítems deterministas son casos de prueba)
- `docs/product/08-UI-SPEC.md` (el bloque `CHECKLIST` debe distinguir ambos tipos)
