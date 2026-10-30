---
artifact: mvp-scope
phase: 2
status: approved
reason: ""
last_updated: "2026-10-12"
---

# 02 — MVP Scope de Agente Generador de Contenido

## Objetivo de V1

Dado un **documento de contexto de marca** versionado en el repositorio y un
**tema o ángulo**, producir un **guion AIDA completo** con **5 variantes de hook**
y **CTA explícito**, validado contra un **checklist de calidad**, y guardarlo como
una pieza en un **banco de contenido** en markdown.

V1 no es una app. Es un agente con conocimiento propio (contexto de marca, reglas
AIDA, checklist) que se ejecuta sobre el repositorio. La interfaz es el propio
agente invocado desde el runtime de trabajo.

## Flujo principal

```text
Contexto de marca válido (o se detiene con error claro)
→ tema o ángulo
→ generación: 1 guion AIDA + 5 variantes de hook + CTA + notas
→ validación contra checklist (hook ≤3 s, promesa verificable, CTA presente, tono)
→ pieza guardada en el banco de contenido + resumen en consola
```

## Usuarios incluidos

- **Operador de contenido (Daniel).** Único usuario incluido en V1. Genera y
  revisa; es quien decide qué se publica.

Fuera de V1: revisor de marca con rol separado, clientes externos, cualquier
usuario no técnico.

## MUST

| Capacidad | Problema que resuelve | Evidencia de éxito |
|---|---|---|
| Documento de contexto de marca como fuente de verdad (posicionamiento, audiencia, tono, ofertas, prohibiciones, ejemplos de voz) | Sin contexto propio la salida es genérica e indistinguible (R-001) | Existe el archivo y el agente lo cita al generar; dos piezas de la misma marca comparten voz reconocible |
| Generación de guion con estructura AIDA en 4 capas etiquetadas (Atención, Interés, Deseo, Acción) | La IA aplica el framework a la forma y no al fondo | Cada pieza declara y separa sus 4 capas; ninguna capa queda vacía |
| 5 variantes de hook para la capa de Atención | El trabajo real está en descartar hooks; el hook decide los primeros 3 segundos | 5 hooks distintos por pieza (no 5 reformulaciones del mismo), con ángulo declarado |
| CTA explícito y concreto en la capa de Acción | CTAs ausentes o desconectados del cuerpo del guion | Toda pieza tiene 1 CTA con acción concreta; ninguna pieza sale sin CTA |
| Checklist de calidad aplicado por pieza | El criterio de marketing hoy es tácito y se aplica a mano | El reporte de la pieza muestra el checklist evaluado, con aprobado/fallo por ítem |
| Banco de contenido: 1 archivo markdown por pieza, con guion, hooks, CTA, metadatos y checklist | Sin banco no hay variantes testeables ni aprendizaje | Tras 3 temas distintos hay 3 piezas recuperables en disco |
| Rechazo explícito cuando falta o está incompleto el contexto de marca | Generar sin contexto produce exactamente lo que se quiere evitar | Con contexto ausente o con campos vacíos, el agente se detiene y nombra los campos faltantes |
| Regla dura: no inventar beneficios, precios, cifras ni promesas de resultado | Riesgo reputacional y legal (R-005) | El checklist marca fallo si aparece una afirmación no presente en el contexto de marca |

## SHOULD

- Adaptación de longitud y tono por plataforma (Reels, TikTok, YouTube Shorts).
- Selección declarada de framework alternativo cuando AIDA no encaje
  (PAS, Before-After-Bridge, Hook/Substance/Payoff), siempre declarando cuál se usó.
- Notas de producción por escena (qué se ve mientras se dice cada capa).
- Banco indexado con una vista resumen (qué temas y qué hooks ya existen) para no
  repetir ángulos.

## COULD

- Registro de resultado por pieza (retención, guardados, comentarios) para saber
  qué hooks funcionan, con la medición aportada a mano.
- Biblioteca de hooks por tipo de disparador (curiosidad, contradicción, pérdida,
  prueba social).
- Multi-marca con varios documentos de contexto.
- Adaptador opcional que reutilice skills de terceros, si en Fase 9 se aprueba su
  licencia.

## NOT NOW

- Publicación automática en redes.
- Generación de audio, voz o video.
- Analítica automática conectada a las plataformas.
- Multiusuario, permisos, roles o multi-cliente.
- Reentrenamiento de pesos de un modelo.
- Estrategia de contenido, calendario editorial o investigación de mercado
  asistida.

## Exclusiones explícitas

- **No es una aplicación web.** No hay interfaz gráfica en V1; la interfaz es el
  agente sobre el repositorio. Si en Fase 6 se detecta necesidad real de UI, se
  registra como cambio de alcance.
- **No publica.** El sistema entrega texto; publicar es humano.
- **No mide.** V1 no promete mejores resultados que una agencia; promete velocidad,
  volumen y consistencia (R-002).
- **No reemplaza la estrategia.** El ángulo y el tema los aporta el humano.
- **No garantiza resultados de negocio.** Es una herramienta de ejecución.

## Definición de éxito

| Métrica | Estado actual | Meta V1 | Cómo se mide |
|---|---:|---:|---|
| Tiempo por pieza publicable | ~60–90 min (estimado de sesión de escritura con descarte manual de hooks) | ≤ 15 min | Cronometrar 5 piezas reales de principio a fin, incluida la revisión humana |
| Piezas publicables sin reescritura | No medido | ≥ 7 de 10 | Sobre las primeras 10 piezas: publicable con edición ligera = sí; reescritura de fondo = no |
| Variantes de hook por pieza | 1–3 improvisadas | 5 distintas | Recuento por pieza en el banco |
| Prueba de indistinguibilidad de voz | No existe | 2 de 3 evaluadores no aciertan el origen | 5 piezas del sistema + 5 escritas a mano sin contexto, presentadas sin etiqueta a alguien que conozca la marca |
| Generaciones sin contexto que producen contenido | N/A (no aplica hoy) | 0 | Probar a propósito con contexto vacío: el agente debe fallar y decirlo |

## Restricciones de V1

- **Límite de coste:** máximo 5 variantes de hook por pieza y 1 guion por
  generación, para acotar el consumo de API (mitiga R-007).
- **Sin instalaciones nuevas** hasta que Fase 9 resuelva licencias y proveedor
  (ADR-001).
- **Una marca** en V1 (marca propia de Monoga); el modelo de datos no se diseña
  multi-marca todavía.
- **Todo el conocimiento vive en el repositorio**, versionado y revisable: el
  contexto de marca, las reglas AIDA y el checklist.
- **Plataforma:** Windows, trabajo de escritorio.

## Riesgos que pueden invalidar el MVP

- **R-001 (salida genérica).** Si tras aplicar contexto de marca la prueba de
  indistinguibilidad falla, el MVP no resuelve el problema y hay que volver a
  Fase 1. Es el riesgo que puede matar el MVP.
- **R-002 (expectativa).** Si la expectativa real es "superar a una agencia", el
  MVP se percibirá como fracaso aunque funcione. Requiere validación explícita de
  Daniel.
- **R-004 (fatiga de plantilla).** Si las 5 variantes de hook son reformulaciones
  del mismo ángulo, el volumen es falso y la métrica de variantes se cumple en
  vano.
- **R-005 (afirmaciones no verificables).** Si el checklist no detecta promesas
  inventadas, el daño es reputacional y legal, no técnico.
- **R-007 (coste).** Si el uso real multiplica las generaciones, el coste se
  descontrola antes de llegar a Fase 9.

## Criterios generales de aceptación

- [ ] Existe un documento de contexto de marca con todos los campos obligatorios
      (posicionamiento, audiencia, tono, ofertas, prohibiciones, ejemplos de voz).
- [ ] Con contexto completo y un tema, se obtiene una pieza con 4 capas AIDA
      separadas, 5 variantes de hook distintas y 1 CTA concreto.
- [ ] La pieza se guarda como archivo en el banco y se puede volver a leer.
- [ ] El reporte de la pieza incluye el checklist evaluado ítem por ítem.
- [ ] Con el contexto de marca vacío o incompleto, el agente se detiene y nombra
      los campos que faltan, sin generar contenido de marca.
- [ ] Ninguna pieza contiene beneficios, precios, cifras ni resultados que no
      estén en el contexto de marca.
- [ ] Una segunda pieza sobre otro tema mantiene la misma voz de marca que la
      primera.

## Gate

- [x] Existe un único flujo principal.
- [x] Cada MUST es indispensable.
- [x] Las exclusiones están escritas.
- [x] El éxito puede medirse.
- [x] El MVP no mezcla varios productos.
- [x] Los riesgos críticos tienen respuesta o bloqueo.

## Incertidumbres abiertas

- [x] [ASSUMPTION] El número de variantes de hook del MVP es 5 y el mínimo de
      piezas para considerar el sistema útil es 3 temas distintos en el banco.
      Resuelto aquí como decisión de alcance (A-009).
- [ ] [ASSUMPTION] El tiempo actual por pieza (60–90 min) es una estimación, no
      una medición. Debe medirse con una pieza real antes de Fase 14 para que la
      métrica de éxito sea honesta.
- [ ] [DEFERRED:Fase 4] Reglas exactas del contexto de marca: campos obligatorios,
      validaciones y qué se considera "contexto incompleto".
- [ ] [DEFERRED:Fase 5] Qué ocurre cuando el tema es sensible o el contexto está
      desactualizado, y cómo se recupera el flujo tras un rechazo.
- [ ] [DEFERRED:Fase 6] Campos exactos de la pieza del banco y estructura del
      archivo de guion.
- [ ] [DEFERRED:Fase 9] Si el checklist se evalúa con reglas deterministas o con
      una segunda pasada del modelo.
