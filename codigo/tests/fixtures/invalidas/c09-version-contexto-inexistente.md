---
pieza: 1
tema: por que se pierden clientes en la primera llamada
fecha: 2026-10-12
contexto_marca: v99
framework: AIDA
razon_framework: ""
plataforma: tiktok
formato: video-corto
duracion_objetivo: 30 s
estado: BORRADOR
hook_elegido: 2
tema_sensible: no
relacionada_con: —
publicada_el: —
motivo_descarte: —
---

# Pieza — por que se pierden clientes en la primera llamada

> FIXTURE DE PRUEBA INVALIDO A PROPOSITO. Debe fallar C-09: Referencia al contexto v99, que no existe.
> No es contenido real y no debe copiarse a banco/piezas/.


## Capas AIDA

### Atencion (0-3 s)

Tu cliente no se fue por el precio. Se fue en el minuto 3.

### Interes (3-10 s)

Grabas la llamada, cuelgas convencido y a los tres dias no responde nadie. Y no
sabes si el problema fue el precio o el momento.

### Deseo (10-20 s)

La proxima vez sabras en el minuto 3 si la conversacion va a avanzar, sin esperar tres dias para descubrirlo.

### Accion (cierre)

Guarda este video y revisa tu ultima llamada antes de la siguiente.

## CTA

- **Accion:** Guarda este video
- **Destino o siguiente paso:** Revisar la ultima llamada antes de la siguiente
- **Alcanzable por la audiencia:** si

## Variantes de hook

| # | Hook | Disparador | Palabras | Es <=3 s | Estado |
|---:|---|---|---:|---|---|
| 1 | Tu cliente no se fue por el precio. Se fue en el minuto 3. | contradiccion | 13 | no | DESCARTADO |
| 2 | La venta se decide mucho antes de que hables de dinero. | curiosidad | 10 | si | ELEGIDO |
| 3 | Hay un minuto exacto en el que pierdes la venta. | curiosidad | 10 | si | PROPUESTO |
| 4 | Cada llamada perdida te cuesta una hora de trabajo. | perdida | 9 | si | PROPUESTO |
| 5 | Cuanto tardas en saber si esa llamada va a avanzar? | pregunta | 10 | si | PROPUESTO |

## Adaptacion

- **Plataforma y formato:** tiktok / video-corto
- **Longitud objetivo:** 30 s
- **Ritmo:** corte cada 3 s, sin musica de fondo
- **Ajustes respecto a la version base:** hook recortado a 9 palabras

## Notas de produccion

| Capa | Que se ve | Recurso necesario |
|---|---|---|
| Atencion | Primer plano, texto en pantalla con el minuto 3 | Camara frontal |
| Interes | Captura de la agenda con la llamada sin respuesta | Captura de pantalla |
| Deseo | Reloj marcando el minuto 3 | Grafico simple |
| Accion | Mano guardando el video | Ninguno |

## Checklist

| # | Item | Regla | Tipo | Resultado |
|---:|---|---|---|---|
| 1 | Hook en <=3 s | BR-006 | Determinista | PENDIENTE |
| 2 | 5 hooks con angulos distintos | BR-004 | Determinista | PENDIENTE |
| 3 | Las 4 capas escritas | BR-007 | Determinista | PENDIENTE |
| 4 | CTA concreto presente | BR-003 | Determinista | PENDIENTE |
| 5 | Sin afirmaciones fuera del contexto | BR-005 | Determinista + asistido | PENDIENTE |
| 6 | Framework declarado | BR-002 | Determinista | PENDIENTE |
| 7 | Tono alineado con el contexto | BR-001 | Asistido | PENDIENTE |

## Resultado

| Fecha | Ventana | Metrica | Valor |
|---|---|---|---|
