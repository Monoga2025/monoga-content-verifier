---
artifact: ui-direction
phase: 7
status: approved
reason: ""
last_updated: "2026-10-12"
---

# 07 — Dirección visual de Agente Generador de Contenido

> **Este producto no tiene interfaz gráfica.** No hay web, ni app, ni pantallas.
> Sus únicas superficies son archivos markdown y mensajes de consola (ver
> `06-SCREEN-INVENTORY.md`). Por tanto la "dirección visual" aquí no es color ni
> tipografía: es **la forma del texto**. Decide cómo se lee, se escanea y se
> diferencia el contenido generado, tanto por el operador como por el modelo que
> lo produce.
>
> El contrato `Mobile Visual Density & Responsive Scaling` **no aplica**: no hay
> viewport, ni UI móvil, ni layout que escalar. Se declara la no aplicación de
> forma explícita en lugar de inventar una pantalla móvil que no existe.

## Contexto de uso

- **Usuario:** una sola persona, perfil técnico alto, trabaja en terminal y
  editor de texto.
- **Dispositivo:** escritorio con Windows, terminal y editor. Móvil solo para
  leer una pieza ya escrita, no para operar el sistema.
- **Frecuencia:** varias piezas por sesión de trabajo; consulta del banco antes
  de generar.
- **Entorno:** repositorio local, trabajo concentrado, sin interrupciones de
  terceros.
- **Densidad:** alta. El operador quiere ver las cuatro capas, los cinco hooks y
  el checklist **en una sola lectura**, sin scroll ni navegación.
- **Marca:** la marca afectada es la del contenido generado, no la del sistema.
  El sistema debe ser neutro para no contaminar la voz de la marca.
- **Accesibilidad:** el significado nunca depende del color ni de un símbolo;
  siempre hay etiqueta de texto. Los mensajes deben ser legibles por lector de
  pantalla sin contexto visual.

## Dirección A — Manual de operador (texto plano, etiquetas fijas, densidad alta)

- **Carácter:** herramienta, no producto. Se parece a leer la salida de un
  compilador: sobrio, predecible, sin adornos.
- **Jerarquía:** por encabezado de sección y por etiqueta en mayúsculas. La
  jerarquía es estable: el mismo dato ocupa siempre la misma posición.
- **Navegación:** ninguna. Todo lo importante de una pieza cabe en un archivo y
  el resultado cabe en una pantalla de terminal.
- **Layout:** bloques de sección con encabezados `##`; tablas solo cuando el dato
  es genuinamente tabular (los 5 hooks, el checklist, los resultados).
- **Densidad:** máxima. Cero texto decorativo. Cada línea existe porque un dato
  vive en ella.
- **Densidad visual móvil objetivo:** no aplica (sin UI móvil).
- **Cantidad de contenido visible objetivo:** el resumen de generación ≤ 12
  líneas; el reporte de rechazo ≤ 8 líneas; una pieza completa ≤ 120 líneas.
- **Proporciones móviles clave:** no aplica.
- **Tipografía:** la del terminal y la del editor. Sin elección tipográfica
  propia: el sistema no impone estética, impone estructura.
- **Espaciado:** una línea en blanco entre secciones; ninguna línea en blanco
  dentro de una lista de datos.
- **Cards:** no existen.
- **Formularios:** no existen; la "entrada" es el mensaje del operador y el
  documento de contexto de marca.
- **Iconografía:** ninguna. `AVISO:` y `FALLO:` son las marcas de atención.
- **Imágenes:** ninguna.
- **Responsive:** no aplica. El único ajuste tolerado es el ancho de línea del
  archivo markdown en el editor.
- **Fortalezas:** máxima velocidad de lectura, diffs limpios en git (cada pieza
  es un archivo de texto), verificable de forma determinista, sin mantenimiento
  visual, imposible que la estética tape un fallo de contenido.
- **Riesgos:** puede resultar árido para revisar; exige disciplina para que el
  checklist no se convierta en un formulario que nadie lee.

## Dirección B — Ficha modular (bloques cerrados, metadatos en cabecera)

- **Carácter:** ficha técnica. Cada pieza es una unidad autocontenida con su
  cabecera de metadatos bien visible y sus bloques etiquetados.
- **Jerarquía:** la cabecera de metadatos (frontmatter) manda; después las capas,
  después los hooks, después el checklist.
- **Navegación:** por bloques; el operador salta de "Hooks" a "Checklist" sin
  releer el guion.
- **Layout:** frontmatter + bloques con encabezado + tablas.
- **Densidad:** alta, algo menor que A por el coste de los encabezados.
- **Densidad visual móvil objetivo:** no aplica.
- **Cantidad de contenido visible objetivo:** una pieza completa ≤ 160 líneas.
- **Proporciones móviles clave:** no aplica.
- **Tipografía:** no aplica.
- **Espaciado:** bloque separado por línea en blanco; encabezado siempre presente
  aunque el bloque tenga una sola línea.
- **Cards:** los bloques de sección actúan como cards.
- **Formularios:** no existen.
- **Iconografía:** ninguna.
- **Imágenes:** ninguna.
- **Responsive:** no aplica.
- **Fortalezas:** los metadatos son imposibles de perder de vista; el checklist y
  el estado quedan siempre visibles arriba; facilita filtrar piezas por estado.
- **Riesgos:** más líneas para la misma información; el encabezado repetido
  empuja el contenido útil fuera de la primera pantalla de terminal.

## Dirección C — Cuaderno narrado (contexto antes del dato, prosa)

- **Carácter:** documento explicativo. Cada pieza se explica a sí misma: por qué
  ese ángulo, por qué ese framework, qué se buscaba.
- **Jerarquía:** narrativa; el dato aparece dentro de la explicación.
- **Navegación:** lectura lineal.
- **Layout:** prosa con datos incrustados.
- **Densidad:** baja.
- **Densidad visual móvil objetivo:** no aplica.
- **Cantidad de contenido visible objetivo:** sin límite definido.
- **Proporciones móviles clave:** no aplica.
- **Tipografía:** no aplica.
- **Espaciado:** el de la prosa.
- **Cards / Formularios / Iconografía / Imágenes:** no aplican.
- **Responsive:** no aplica.
- **Fortalezas:** útil para explicar decisiones a otra persona; deja el criterio
  escrito.
- **Riesgos:** contradice directamente el objetivo del producto. Fragmenta los
  datos, hace imposible escanear 5 hooks de un vistazo, llena el archivo de
  narración que compite con la voz de la marca y hace que el checklist se pierda
  en el texto. Además, el output del modelo pierde verificabilidad determinista.

## Matriz de decisión

Pesos sobre 5, puntuación de 1 a 5 (5 = mejor).

| Criterio | Peso | A — Manual de operador | B — Ficha modular | C — Cuaderno narrado |
|---|---:|---:|---:|---:|
| Claridad para decidir en 3 segundos | 5 | 5 | 4 | 1 |
| Velocidad de uso y generación | 5 | 5 | 4 | 1 |
| Confianza y verificabilidad | 5 | 5 | 5 | 2 |
| Densidad de información útil | 4 | 5 | 4 | 1 |
| Mantenibilidad y diffs en git | 4 | 5 | 4 | 3 |
| Coherencia con "el sistema no impone marca" | 4 | 5 | 5 | 2 |
| Bajo coste de tokens por pieza | 3 | 5 | 4 | 1 |
| **Total ponderado** | | **121** | **104** | **31** |

## Dirección elegida

**Dirección A — Manual de operador**, con dos préstamos concretos de la
Dirección B: el frontmatter de metadatos en la cabecera de cada pieza (necesario
para el contrato de salida de `06-SCREEN-INVENTORY.md`) y la tabla del checklist.

## Razón funcional

1. El objetivo declarado del producto es velocidad y volumen de variantes, no
   presentación. La Dirección C contradice el objetivo por diseño.
2. El usuario es una sola persona con perfil técnico alto y trabaja en terminal:
   la densidad máxima es una ventaja, no un coste.
3. Una pieza es un artefacto versionado en git. El texto plano produce diffs
   útiles; la prosa narrada contamina esos diffs con explicaciones irrelevantes.
4. El sistema no debe imponer estética propia, porque todo lo que escribe compite
   con la voz de la marca que está intentando reproducir.
5. El checklist debe leerse de un vistazo. Un checklist dentro de prosa no se
   revisa, y un checklist que no se revisa equivale a no tenerlo.

## Reglas no negociables

- **RN-01 — Cada línea transporta un dato.** Cero relleno, cero frases de
  cortesía, cero introducciones explicativas.
- **RN-02 — El mismo dato siempre en la misma posición.** Un dato que cambia de
  sitio obliga a releer.
- **RN-03 — Ninguna etiqueta depende del color.** Las advertencias se marcan con
  `AVISO:` y los fallos con `FALLO:`.
- **RN-04 — Mensajes sin disculpas ni vaguedades.** Prohibido "lo siento", "ha
  ocurrido un error", "inténtalo de nuevo". Siempre causa concreta + qué hacer.
- **RN-05 — Sin emojis en la salida del agente.** Compiten con la voz de la marca
  y rompen la parsabilidad.
- **RN-06 — El resumen de generación cabe en una pantalla de terminal** (≤ 12
  líneas) sin scroll.
- **RN-07 — Una pieza completa ≤ 120 líneas.** Si no cabe, sobra contenido.
- **RN-08 — Tablas solo para datos genuinamente tabulares** (hooks, checklist,
  resultados). Nunca para prosa.
- **RN-09 — El sistema no se decora.** No hay logo, ni cabecera de marca, ni
  firma en las piezas.
- **RN-10 — El estado y el framework se declaran siempre** en la cabecera: no se
  infieren por contexto.
- **RN-11 — El reporte de rechazo nunca es un texto genérico.** Enumera los campos
  que faltan y el siguiente paso exacto.
- **RN-12 — Legible sin color y sin formato.** Si se copia como texto plano, sigue
  siendo comprensible. Esto cubre la accesibilidad en un producto sin UI.

## Gate

- [x] Las tres direcciones son realmente distintas.
- [x] La elección se basa en contexto, no solo gusto.
- [x] Jerarquía y densidad están definidas.
- [x] Mobile y desktop están resueltos sin convertir mobile en una versión ampliada o reducida accidental de desktop.
- [x] La dirección móvil define densidad visual, proporciones y cantidad de contenido visible.
- [x] La solución móvil ocupa el viewport edge-to-edge sin bloquearse a un único teléfono.
- [x] Existen reglas de accesibilidad y contenido.

**Sobre las tres casillas de mobile:** se marcan como resueltas porque la decisión
es **no aplica por inexistencia de UI móvil**, y así consta por escrito arriba.
No se declara una solución móvil inventada. Si el alcance incorporara una interfaz
gráfica, este artefacto se reabre y el contrato de densidad móvil pasa a ser
obligatorio.

## Incertidumbres abiertas

- [x] [ASSUMPTION] Los límites de densidad (≤ 12 líneas de resumen, ≤ 120 líneas
      por pieza, ≤ 160 en la variante B) son decisiones de producto sin medir. Se
      recalibran con las primeras 10 piezas reales.
- [ ] [DEFERRED:Fase 8] Especificación final del formato de salida y del archivo
      de referencia aprobado.
- [ ] [ASSUMPTION] La ausencia de UI gráfica se mantiene durante todo el proyecto.
      Si Daniel pide una interfaz, se reabre la Fase 6 antes de continuar.
