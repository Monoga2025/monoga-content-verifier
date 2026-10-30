---
artifact: approved-design-references
phase: 8
status: approved
reason: ""
last_updated: "2026-10-12"
---

# Referencias visuales aprobadas — Agente Generador de Contenido

> **No existen referencias visuales, y eso es correcto.** El producto no tiene
> interfaz gráfica (decisión de MVP, `02-MVP-SCOPE.md`). No hay imágenes,
> mockups ni screenshots que aprobar. Este archivo registra la referencia real:
> el **contrato de texto** de `08-UI-SPEC.md`, que es verificable y ejecutable.

## Sistema aprobado

- **Dirección:** Dirección A — Manual de operador (texto plano, etiquetas fijas,
  densidad alta), de `07-UI-DIRECTION.md`.
- **Versión:** v1
- **Aprobado por:** Daniel (Monoga)
- **Fecha:** 2026-10-12
- **Naturaleza de la referencia:** contrato de texto, no imagen.

## Referencias

| ID | Archivo o enlace | Superficie | Versión | Estado | Notas |
|---|---|---|---|---|---|
| TXT-001 | `docs/product/08-UI-SPEC.md` → bloque `RESUMEN` | SC-001 consola | v1 | Approved | ≤ 12 líneas, 80 columnas, orden de campos fijo |
| TXT-002 | `docs/product/08-UI-SPEC.md` → bloque `RECHAZO` | SC-006 reporte | v1 | Approved | ≤ 8 líneas, causa + faltantes + siguiente paso |
| TXT-003 | `docs/product/08-UI-SPEC.md` → estructura de pieza | SC-003 pieza | v1 | Approved | ≤ 120 líneas, orden fijo de bloques |
| TXT-004 | `docs/product/08-UI-SPEC.md` → bloques `HOOKS` y `CHECKLIST` | SC-003 pieza | v1 | Approved | 5 filas siempre; 7 ítems siempre, mismo orden |
| TXT-005 | `docs/product/08-UI-SPEC.md` → bloque `CONTEXTO` | SC-002 contexto | v1 | Approved | 7 campos obligatorios + vocabulario prohibido |

No hay filas de tipo imagen y no se añadirán mientras no exista interfaz gráfica.

## Reglas extraídas

Reglas implementables y verificables que salen de la referencia aprobada:

1. Etiquetas fijas en consola: `PIEZA GENERADA`, `GENERACIÓN RECHAZADA`,
   `Archivo`, `Framework`, `Plataforma`, `Contexto`, `Checklist`,
   `Hook sugerido`, `AVISO`, `FALLO`.
2. El resumen de generación siempre presenta los campos en el mismo orden.
3. Todo mensaje de error tiene una sola línea con causa + acción.
4. Prohibido "lo siento", "ha ocurrido un error", "inténtalo de nuevo" sin causa.
5. Sin emojis en ninguna salida del agente.
6. Cinco hooks por pieza, siempre; cada uno con disparador del vocabulario
   cerrado (`curiosidad`, `contradicción`, `pérdida`, `prueba social`, `dato`,
   `pregunta`).
7. Siete ítems de checklist, siempre, en el mismo orden, cada uno ligado a su
   regla de negocio.
8. Un hook ocupa como máximo 12 palabras (umbral de BR-006).
9. Una capa AIDA ocupa entre 1 y 3 líneas.
10. Ningún elemento comunica significado solo por color o símbolo.
11. El reporte de rechazo siempre confirma explícitamente que no se creó ninguna
    pieza.
12. La ruta del archivo creado aparece siempre en la primera línea del resumen.

## Geometría móvil extraída

**No aplica.** No hay superficie móvil, ni viewport, ni proporciones que extraer.
No se registra geometría inventada para cumplir la casilla.

- **Viewport de referencia:** no aplica.
- **Márgenes relativos:** no aplica.
- **Proporción del hero:** no aplica.
- **Alturas relativas de cards y controles:** no aplica.
- **Cantidad de elementos visibles horizontalmente:** no aplica.
- **Densidad vertical:** no aplica.
- **Nivel aparente de zoom tipográfico:** no aplica.

Única restricción de "geometría" aplicable, y es de texto, no de layout: el
resumen cabe en **80 columnas × 12 líneas**.

## Elementos que NO deben copiarse

No hay referencia de la que copiar. Lo que **no** debe aparecer en el producto,
por decisión explícita:

- Cualquier interfaz gráfica, dashboard o pantalla. No está en V1.
- Emojis, iconos o decoración en la salida del agente (RN-05, RN-09).
- Lenguaje de asistente ("¡Claro!", "Aquí tienes…", "Lo siento").
- Relleno narrativo que explique lo que el agente está haciendo paso a paso.
- Colores o símbolos como único portador de significado.
- Hooks, capas o ítems de checklist añadidos ad hoc en una pieza concreta fuera de
  los bloques especificados.
- Cualquier afirmación de beneficio, cifra o promesa que no esté en el contexto de
  marca (BR-005).

## Gate

- [x] Existe al menos una referencia o prompt aprobado.
- [x] Cada referencia tiene pantalla y versión.
- [x] Las reglas implementables están escritas.
- [x] Las referencias móviles registran geometría, densidad y cantidad de contenido visible.
- [x] Los errores visuales que no deben copiarse están identificados.

**Nota sobre las casillas 1 y 4:** la casilla 1 se cumple con referencias de
texto aprobadas (TXT-001 a TXT-005), que son las que este producto puede tener.
La casilla 4 se cumple como **no aplicable** (sin superficie móvil), declarado de
forma explícita y no simulado.

## Incertidumbres abiertas

- [ ] [ASSUMPTION] Los cinco contratos de texto (TXT-001 a TXT-005) se mantienen
      v1 hasta que las primeras 10 piezas reales revelen que un límite de líneas no
      se sostiene. Entonces se versionan a v2 aquí, no dentro de una pieza.
- [ ] [DEFERRED:Fase 14] Verificación de que las 12 reglas extraídas se cumplen en
      la práctica, como parte de los criterios de aceptación de QA.
