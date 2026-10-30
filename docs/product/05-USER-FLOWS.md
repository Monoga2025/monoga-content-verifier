---
artifact: user-flows
phase: 5
status: approved
reason: ""
last_updated: "2026-10-12"
---

# 05 — User flows de Agente Generador de Contenido

> La interfaz de V1 es el agente sobre el repositorio, así que "feedback" y
> "persistencia" son mensajes en consola y archivos en disco. Los flujos se
> escriben igual porque el comportamiento debe estar resuelto antes de elegir
> cualquier superficie (Fase 6).

## Índice de flujos

| ID | Flujo | Actor | Prioridad | Estado |
|---|---|---|---|---|
| UF-001 | Preparar y validar el contexto de marca | Operador | MUST | Draft |
| UF-002 | Generar una pieza desde un tema | Operador + Agente | MUST | Draft |
| UF-003 | Revisar, aprobar o descartar una pieza | Operador | MUST | Draft |
| UF-004 | Recuperarse de un rechazo de generación | Operador + Agente | MUST | Draft |
| UF-005 | Publicar y registrar resultado | Operador | SHOULD | Draft |
| UF-006 | Actualizar el contexto de marca | Operador | SHOULD | Draft |
| UF-007 | Evitar repetir un ángulo ya publicado | Operador + Agente | COULD | Draft |

---

## UF-001 — Preparar y validar el contexto de marca

### Actor

Operador de contenido (Daniel), único actor del flujo.

### Trigger

Inicio del proyecto, o cambio de oferta, posicionamiento o audiencia.

### Precondiciones

- Existe el repositorio del proyecto.
- El operador conoce el negocio (es su propia marca).

### Happy path

1. El operador abre el documento de contexto de marca.
2. Rellena los campos obligatorios: posicionamiento, propuesta de valor,
   audiencia con dolores y deseos, tono y voz, ofertas vigentes, prohibiciones y
   al menos 2 ejemplos de voz aprobados.
3. Ejecuta la validación del contexto.
4. El sistema comprueba campo por campo y marca el contexto como `VÁLIDO`.
5. El sistema registra la versión del contexto y la fecha.

### Decisiones

- Si falta un campo obligatorio → el contexto queda `INCOMPLETO` y la generación
  se bloquea (BR-001).
- Si hay ejemplos de voz contradictorios con el tono declarado → se señala la
  contradicción y no se marca `VÁLIDO` hasta resolverla.
- Si el contexto ya era `VÁLIDO` y se edita → pasa a `INCOMPLETO` hasta revalidar.

### Validaciones

- Todos los campos obligatorios presentes y no vacíos.
- Al menos 2 ejemplos de voz.
- Coherencia entre tono declarado y ejemplos de voz.
- Las ofertas tienen vigencia declarada (no quedan ofertas muertas).

### Persistencia

- El documento de contexto de marca y su versión.
- La fecha de última revisión y el resultado de la validación.

### Permisos

- Solo el operador escribe el contexto. El agente solo lee.

### Errores y recuperación

| Error | Mensaje | Recuperación |
|---|---|---|
| Campo obligatorio vacío | `Contexto INCOMPLETO. Faltan: ofertas vigentes, prohibiciones.` | Rellenar los campos nombrados y revalidar |
| Menos de 2 ejemplos de voz | `Contexto INCOMPLETO. Se requieren al menos 2 ejemplos de voz aprobados.` | Añadir ejemplos reales ya publicados |
| Tono contradice los ejemplos | `Contradicción: el tono declarado es "cercano" y los ejemplos son formales.` | Corregir tono o reemplazar ejemplos |
| Documento ilegible o con formato roto | `No se pudo leer el contexto de marca: <ruta>.` | Corregir el archivo |

### Cancelación / timeout

No aplica: no hay operación remota. Guardar a medias deja el contexto en
`INCOMPLETO`, que es un estado válido y seguro.

### Notificaciones

Ninguna automática. El resultado de la validación se muestra al ejecutarla.

### Resultado y evidencia

- Contexto de marca en estado `VÁLIDO` con versión registrada.
- Evidencia: el reporte de validación con los campos comprobados.

---

## UF-002 — Generar una pieza desde un tema

Flujo principal del producto.

### Actor

Operador (aporta el tema) + Agente (genera).

### Trigger

El operador decide un tema o ángulo y pide una pieza.

### Precondiciones

- Contexto de marca en estado `VÁLIDO`.
- Tema o ángulo indicado (texto libre).
- Plataforma y formato destino indicados (o un valor por defecto declarado).

### Happy path

1. El operador indica tema, plataforma y formato.
2. El agente lee el contexto de marca `VÁLIDO` y su versión.
3. El agente comprueba que el tema no esté ya cubierto en el banco (UF-007 si
   existe; aviso, no bloqueo).
4. El agente elige el framework: AIDA por defecto; otro si el formato lo exige, y
   lo declara con su razón (BR-002).
5. El agente genera 5 hooks con ángulos distintos (BR-004).
6. El agente desarrolla las 4 capas etiquetadas y con contenido (BR-007).
7. El agente escribe 1 CTA concreto dentro de la capa Acción (BR-003).
8. El agente añade notas de producción por capa.
9. El agente ejecuta el checklist sobre el resultado.
10. Si el checklist pasa, guarda la pieza en el banco con estado `BORRADOR` y
    muestra un resumen con la ruta del archivo.
11. Si el checklist falla, reintenta una vez corrigiendo los ítems fallidos; si
    vuelve a fallar, guarda la pieza marcada `CON_FALLOS` y explica qué falló.

### Decisiones

- Contexto no `VÁLIDO` → se detiene en UF-004.
- Formato que exige otro framework → se usa y se declara.
- Tema sensible (salud, dinero, resultados garantizados) → la pieza se genera,
  pero queda marcada para revisión humana obligatoria antes de publicar (BR-010).
- Checklist con fallos tras un reintento → se guarda igual, con el fallo visible.
  Nunca se presenta como aprobada.
- Tema ya existente en el banco → se avisa y se ofrece continuar con otro ángulo.

### Validaciones

- Contexto `VÁLIDO` (BR-001).
- 5 hooks, cada uno con ángulo declarado y distinto entre sí.
- 4 capas no vacías.
- 1 CTA concreto y alcanzable.
- Hook pronunciable en ≤ 3 segundos (BR-006), salvo formato escrito largo.
- Ninguna afirmación de beneficio, precio, cifra o resultado fuera del contexto
  (BR-005).

### Persistencia

- Un archivo de pieza en el banco, con: tema, framework declarado, 4 capas, 5
  hooks, CTA, adaptación, notas, checklist evaluado y versión del contexto usada
  (BR-008).

### Permisos

- El agente crea piezas. No las aprueba, no las publica, no las borra.

### Errores y recuperación

| Error | Mensaje | Recuperación |
|---|---|---|
| Contexto de marca ausente | `No hay contexto de marca. Genera primero el contexto (UF-001).` | Ir a UF-001 |
| Contexto incompleto | `Contexto INCOMPLETO. Faltan: <campos>.` | Completar y revalidar |
| Tema vacío o ininteligible | `Indica un tema o ángulo concreto.` | Reformular el tema |
| Plataforma no soportada | `Plataforma no soportada: <nombre>. Soportadas: Instagram, TikTok, YouTube Shorts, LinkedIn.` | Elegir una soportada |
| Checklist falla tras reintento | `Pieza guardada con fallos: 5 hooks no son distintos (BR-004).` | Corregir a mano o regenerar con otro ángulo |
| Afirmación no verificable detectada | `Falló BR-005: "triplica tus ventas" no está respaldado por el contexto.` | Quitar la afirmación o respaldarla en el contexto |
| Fallo del proveedor de modelo a mitad | `Generación interrumpida. No se guardó ninguna pieza.` | Reintentar; no queda pieza parcial en el banco |
| Salida con formato inválido | `La pieza generada no tiene 4 capas. No se guardó.` | Reintentar |

### Cancelación / timeout

- El operador puede cancelar antes de que se guarde: no se escribe ninguna pieza
  parcial (invariante del dominio).
- Timeout del proveedor: se trata como fallo de generación; se reintenta o se
  aborta sin residuo.

### Notificaciones

Resumen en consola al terminar: ruta de la pieza, framework usado, hook elegido
propuesto, resultado del checklist y advertencias (tema sensible, tema repetido,
contexto desactualizado).

### Resultado y evidencia

- 1 archivo de pieza en el banco, recuperable, con checklist evaluado.
- Evidencia para la métrica del MVP: tiempo desde que se indica el tema hasta que
  la pieza queda en disco.

---

## UF-003 — Revisar, aprobar o descartar una pieza

### Actor

Operador (y, en fase posterior, revisor de marca).

### Trigger

La pieza existe en estado `BORRADOR`.

### Precondiciones

- Existe al menos una pieza en el banco.

### Happy path

1. El operador abre la pieza.
2. Lee los 5 hooks y elige uno (o pide uno nuevo).
3. Lee las 4 capas y el CTA.
4. Revisa el checklist y las advertencias.
5. Corrige a mano lo que haga falta directamente en el archivo.
6. Mueve la pieza a `EN_REVISIÓN`.
7. Si el tono y las afirmaciones son correctos, la mueve a `APROBADA`.
8. Si no, la mueve a `DESCARTADA` con el motivo escrito.

### Decisiones

- Ningún hook convence → se regeneran solo los hooks, sin rehacer la pieza.
- Capa vacía o CTA ausente → no puede pasar a `APROBADA` (invariante).
- Checklist `CON_FALLOS` → no puede pasar a `APROBADA` hasta corregir.
- Tema sensible → se exige marcar la revisión humana explícita antes de publicar
  (BR-010).
- Pieza descartada → se conserva con motivo (BR-009).

### Validaciones

- Las 4 capas escritas.
- 1 CTA presente.
- Checklist sin fallos.
- Revisión humana marcada si el tema es sensible.

### Persistencia

- El estado de la pieza, el hook elegido y el motivo de descarte si aplica.

### Permisos

- El agente no puede aprobar ni descartar. Solo el operador.

### Errores y recuperación

| Error | Mensaje | Recuperación |
|---|---|---|
| Intento de aprobar con capa vacía | `No se puede aprobar: la capa "Deseo" está vacía.` | Completar la capa |
| Intento de aprobar con checklist con fallos | `No se puede aprobar: 1 ítem del checklist falló (BR-005).` | Corregir y reevaluar |
| Intento de aprobar sin CTA | `No se puede aprobar: falta el CTA.` | Añadir CTA concreto |
| Descarte sin motivo | `Indica el motivo del descarte.` | Escribir el motivo |

### Cancelación / timeout

No aplica.

### Notificaciones

Ninguna. El estado de la pieza es la notificación.

### Resultado y evidencia

- Pieza en `APROBADA` o `DESCARTADA` con motivo.
- Evidencia: el propio archivo con su estado y su checklist.

---

## UF-004 — Recuperarse de un rechazo de generación

Flujo de recuperación del flujo principal.

### Actor

Operador + Agente.

### Trigger

El agente rechaza generar por contexto inválido, tema vacío o plataforma no
soportada.

### Precondiciones

- Existe una intención de generar una pieza.

### Happy path

1. El agente se detiene sin crear pieza.
2. El agente nombra exactamente qué falta y qué puede hacer el operador.
3. El operador completa el contexto o corrige el tema.
4. Revalida el contexto.
5. Vuelve a UF-002 con el estado corregido.

### Decisiones

- ¿El rechazo es por contexto o por entrada? Determina si el operador edita el
  contexto o la petición.
- Si el operador insiste en generar sin contexto → el agente se niega y explica
  que el resultado sería genérico por diseño, que es el problema que el proyecto
  existe para resolver.

### Validaciones

- El rechazo nunca genera contenido de marca parcial.
- El mensaje siempre nombra los campos faltantes concretos, no "falta
  información".

### Persistencia

- Ninguna pieza. El rechazo no deja residuo.

### Permisos

- El agente puede rechazar. No puede omitir la regla.

### Errores y recuperación

| Error | Mensaje | Recuperación |
|---|---|---|
| El operador insiste sin contexto | `No genero contenido de marca sin contexto: saldría genérico, que es el problema a resolver (BR-001).` | Completar el contexto (UF-001) |
| Contexto corregido pero sigue inválido | `Contexto INCOMPLETO. Sigue faltando: <campos>.` | Iterar hasta `VÁLIDO` |
| Rechazo repetido por la misma causa | Se registra la causa repetida para revisar si la regla está mal calibrada | Revisar el checklist o el contexto |

### Cancelación / timeout

No aplica.

### Notificaciones

El mensaje de rechazo es la notificación. Debe ser accionable, no un genérico.

### Resultado y evidencia

- Contexto en `VÁLIDO` o petición corregida.
- Evidencia: el mensaje de rechazo con los campos faltantes (sirve como prueba del
  criterio de aceptación "rechazo seguro verificado").

---

## UF-005 — Publicar y registrar resultado

### Actor

Operador.

### Trigger

La pieza está `APROBADA` y el operador decide publicarla.

### Precondiciones

- Pieza en `APROBADA`.
- Revisión humana hecha si el tema es sensible.

### Happy path

1. El operador publica manualmente en la plataforma.
2. Marca la pieza como `PUBLICADA` con la fecha.
3. Días después, registra el resultado observado (retención, guardados,
   comentarios) con su ventana de observación.
4. El sistema guarda el resultado asociado a la pieza y al hook elegido.

### Decisiones

- Sin medición → la pieza queda `SIN_MEDIR`; no es un fallo, es el estado por
  defecto.
- Varias ventanas de medición → se guardan varias lecturas.

### Validaciones

- Solo se publica lo `APROBADA`.
- La fecha de publicación no puede ser futura.

### Persistencia

- Estado `PUBLICADA`, fecha, y el Resultado si se registra.

### Permisos

- Exclusivamente humano (BR-012).

### Errores y recuperación

| Error | Mensaje | Recuperación |
|---|---|---|
| Publicar algo no aprobado | `No se puede publicar: la pieza está en BORRADOR.` | Aprobar primero (UF-003) |
| Resultado sin ventana de observación | `Indica la ventana (por ejemplo, 7 días desde la publicación).` | Añadir la ventana |

### Cancelación / timeout

No aplica.

### Notificaciones

Ninguna.

### Resultado y evidencia

- Pieza `PUBLICADA`, con o sin Resultado.
- Evidencia: el histórico de piezas publicadas y sus resultados, base del
  aprendizaje sobre hooks.

---

## UF-006 — Actualizar el contexto de marca

### Actor

Operador.

### Trigger

Cambia una oferta, el posicionamiento o la audiencia.

### Precondiciones

- Existe un contexto `VÁLIDO`.

### Happy path

1. El operador edita el contexto (nueva versión).
2. Revalida.
3. El contexto pasa a `VÁLIDO` como nueva versión.
4. Las piezas anteriores conservan la referencia a la versión anterior (BR-008).
5. El sistema señala las piezas cuya versión de contexto ya no es la activa, para
   revisión.

### Decisiones

- Si el cambio invalida afirmaciones de piezas publicadas → se listan para
  revisión humana.
- Si el cambio es solo de estilo → las piezas antiguas no se marcan.

### Validaciones

- La nueva versión cumple los mismos campos obligatorios que UF-001.

### Persistencia

- Nueva versión del contexto, fecha, y la lista de piezas afectadas.

### Permisos

- Solo el operador.

### Errores y recuperación

| Error | Mensaje | Recuperación |
|---|---|---|
| Nueva versión incompleta | `Contexto INCOMPLETO. Faltan: <campos>.` | Completar |
| Se intenta borrar la versión anterior | `Las versiones anteriores se conservan: hay piezas que dependen de ellas.` | No borrar; versionar |

### Cancelación / timeout

No aplica.

### Notificaciones

Lista de piezas afectadas por el cambio.

### Resultado y evidencia

- Contexto `VÁLIDO` en nueva versión, con las piezas afectadas identificadas.
- Evidencia: histórico de versiones del contexto.

---

## UF-007 — Evitar repetir un ángulo ya publicado

### Actor

Operador + Agente.

### Trigger

El operador pide una pieza sobre un tema parecido a uno existente.

### Precondiciones

- El banco contiene piezas.

### Happy path

1. El agente compara el tema nuevo con los temas y ángulos del banco.
2. Si hay coincidencia alta, lo avisa antes de generar.
3. El operador decide: continuar con otro ángulo, o descartar la idea.
4. Si continúa, la pieza se marca como relacionada con la anterior.

### Decisiones

- Coincidencia alta → aviso, no bloqueo: repetir un tema con otro ángulo puede
  ser deliberado.
- Sin coincidencias → se genera con normalidad.

### Validaciones

- La comparación usa tema y ángulo declarados, no solo el título.

### Persistencia

- Relación entre la pieza nueva y la existente, si el operador continúa.

### Permisos

- Solo lectura del banco por parte del agente.

### Errores y recuperación

| Error | Mensaje | Recuperación |
|---|---|---|
| Banco ilegible | `No se pudo leer el banco de piezas; se omite la comprobación de duplicados.` | Corregir el banco o continuar aceptando el riesgo de repetición |

### Cancelación / timeout

No aplica.

### Notificaciones

Aviso de posible repetición con la ruta de la pieza existente.

### Resultado y evidencia

- Pieza nueva con o sin relación declarada a una anterior.
- Evidencia: el aviso mostrado y la decisión del operador.

---

## Gate

- [x] Todos los MUST tienen happy path.
- [x] Todos los MUST tienen errores y recuperación.
- [x] Cada acción sensible tiene actor y permiso.
- [x] Se sabe qué datos cambian.
- [x] Existen cancelación y duplicados cuando aplican.
- [x] Los mensajes de feedback están definidos.

## Incertidumbres abiertas

- [ ] [ASSUMPTION] El umbral de "coincidencia alta" de UF-007 se resuelve con
      comparación de texto simple; si genera ruido, se descarta el flujo (está en
      `COULD`).
- [ ] [ASSUMPTION] El reintento único del checklist en UF-002 es suficiente. Se
      valida con piezas reales; si la mayoría necesita más reintentos, el problema
      está en las reglas, no en el número de intentos.
- [ ] [DEFERRED:Fase 6] Dónde vive cada mensaje (consola, archivo de reporte) y su
      copy definitivo.
- [ ] [DEFERRED:Fase 10] Cómo se versiona el contexto de marca y cómo se registra
      la relación entre piezas y versiones.
