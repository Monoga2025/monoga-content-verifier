# Checklist de calidad

**Siete ítems, orden fijo.** El orden lo consume `codigo/validar_pieza.py` y
escribirlo distinto rompe la verificación. Cada ítem cita su regla de negocio y
declara su **tipo de verificación**, porque presentar una opinión del modelo como
una prueba sería mentir sobre la fiabilidad del sistema (ADR-004).

## Los siete ítems

| # | Ítem | Regla | Tipo | Cómo se evalúa |
|---:|---|---|---|---|
| 1 | Hook en ≤3 s | BR-006 | **Determinista** | Recuento de palabras del hook elegido: ≤ 12. En formatos escritos declarados, no aplica |
| 2 | 5 hooks con ángulos distintos | BR-004 | **Determinista** | Recuento de hooks = 5 (o `excepcion_hooks` con motivo) + disparadores del catálogo + solapamiento de palabras entre hooks por debajo del umbral |
| 3 | Las 4 capas escritas | BR-007 | **Determinista** | Existencia de las 4 capas requeridas, con contenido no vacío y no compuesto solo por relleno |
| 4 | CTA concreto presente | BR-003 | **Determinista** | Existencia de 1 CTA con acción, destino y alcanzabilidad declarados; más verificación de que no contiene dos acciones |
| 5 | Sin afirmaciones fuera del contexto | BR-005 | **Determinista + asistido** | Determinista: cifras, porcentajes y superlativos de la pieza que no aparecen en el contexto de marca. Asistido: afirmaciones de beneficio sin respaldo literal |
| 6 | Framework declarado | BR-002 | **Determinista** | El campo `framework` pertenece a la taxonomía; si no es `AIDA`, exige `razon_framework` no vacío |
| 7 | Tono alineado con el contexto | BR-001 | **Asistido** | Comparación de la pieza contra el tono y los ejemplos de voz del contexto de marca, con cita del fragmento de respaldo |

**Resumen: 5 ítems deterministas, 2 asistidos (uno de ellos mixto).** El reporte del
checklist **debe** mostrar esta distinción. Un ítem asistido nunca se presenta como
verificado: se presenta como revisado por el modelo y sujeto a lectura humana.

## Límites y aproximaciones declaradas

Estas aproximaciones son parte del contrato: se declaran, no se esconden.

| Ítem | Aproximación aplicada | Qué NO garantiza |
|---:|---|---|
| 1 | "3 segundos" se operacionaliza como ≤ 12 palabras, más un cálculo estimado de sílabas. No hay medición real de tiempo de habla | Que el hook se diga realmente en 3 s: depende del ritmo del hablante |
| 2 | La distinción de ángulo se aproxima con disparador declarado + solapamiento de tokens. No hay comprensión semántica | Que dos hooks con ángulos distintos en apariencia no digan lo mismo en el fondo |
| 3 | "No vacía" se comprueba por longitud mínima y ausencia de marcadores de relleno (`...`, `TBD`, `TODO`, `pendiente`) | Que la capa esté bien escrita; una frase genérica puede superar el umbral |
| 4 | "Concreto" se comprueba por presencia de verbo de acción y destino declarado | Que la acción sea alcanzable por la audiencia real |
| 5 | La detección de cifras y superlativos es por patrón; no cubre afirmaciones implícitas | Que toda afirmación esté respaldada: es el punto ciego conocido del sistema |
| 6 | Sin aproximación: es una comprobación de vocabulario cerrado | — |
| 7 | Juicio del modelo con cita de respaldo. Puede equivocarse en ambos sentidos | Nada de forma determinista. Es el ítem más débil del checklist y así se declara |

## Reglas de uso

1. Los 7 ítems se escriben **siempre**, en este orden, aunque un framework
   alternativo tenga menos capas: los ítems de capas se mapean según
   `reglas/aida.md`.
2. Un ítem en `FALLO` impide el estado `APROBADA` (C-06), sea determinista o
   asistido.
3. Un ítem asistido no puede habilitar por sí solo el estado `APROBADA`: requiere
   confirmación humana (F-014).
4. Añadir o quitar un ítem exige editar este archivo y actualizar
   `codigo/validar_pieza.py` y `docs/product/08-UI-SPEC.md`. La prueba de
   consistencia del orden falla si divergen.
5. Los ítems no se adaptan a una pieza concreta. Si una pieza necesita una
   excepción, la excepción se escribe en este archivo.

## Formato del bloque en la pieza

```markdown
## Checklist
| # | Ítem | Regla | Tipo | Resultado |
|---:|---|---|---|---|
| 1 | Hook en ≤3 s | BR-006 | Determinista | APROBADO |
| 2 | 5 hooks con ángulos distintos | BR-004 | Determinista | APROBADO |
| 3 | Las 4 capas escritas | BR-007 | Determinista | APROBADO |
| 4 | CTA concreto presente | BR-003 | Determinista | APROBADO |
| 5 | Sin afirmaciones fuera del contexto | BR-005 | Determinista + asistido | APROBADO |
| 6 | Framework declarado | BR-002 | Determinista | APROBADO |
| 7 | Tono alineado con el contexto | BR-001 | Asistido | ASISTIDO: revisar |
```
