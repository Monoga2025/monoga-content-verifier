---
artifact: commercial-scope
phase: 3
status: approved
reason: ""
last_updated: "2026-10-12"
---

# 03 — Alcance comercial de Agente Generador de Contenido

> **Proyecto interno.** No hay cliente externo, facturación ni contrato. Este
> artefacto se mantiene vivo —no se marca `not_applicable`— porque el proyecto sí
> tiene costo operativo, dependencias externas y propiedad de cuentas que deben
> quedar definidas antes de construir.

## Resultado prometido

Un sistema propio que convierte un **tema** en un **guion AIDA publicable con 5
variantes de hook y CTA**, respetando la voz de la marca definida en un documento
de contexto versionado, con checklist de calidad aplicado y banco de piezas
recuperable.

Promesa medida: **≤ 15 min por pieza publicable** y **≥ 7 de 10 piezas usables sin
reescritura de fondo**.

Promesa explícitamente **no** incluida: mejores resultados de marketing que una
agencia, estrategia, producción audiovisual o medición de resultados.

## Entregables incluidos

1. **Documento de contexto de marca** con posicionamiento, audiencia, tono,
   ofertas, prohibiciones y ejemplos de voz.
2. **Agente generador**: instrucciones y conocimiento propio del framework AIDA,
   reglas de estructura y regla de no inventar beneficios.
3. **Checklist de calidad** aplicado por pieza y visible en el reporte.
4. **Banco de contenido**: un archivo markdown por pieza con guion, 5 hooks, CTA,
   metadatos de plataforma y checklist evaluado.
5. **Comportamiento seguro**: rechazo explícito y nombrado de los campos faltantes
   cuando el contexto de marca está ausente o incompleto.
6. **Documentación de uso**: cómo generar una pieza, cómo validarla y cómo
   extender el contexto de marca.

## No incluido

- Aplicación web o interfaz gráfica de cualquier tipo.
- Publicación automática en redes sociales ni integración con sus APIs.
- Generación de audio, voz, video o imágenes.
- Analítica, métricas conectadas o informes de rendimiento.
- Multiusuario, roles, permisos o multi-cliente.
- Estrategia de contenido, calendario editorial o investigación de mercado.
- Reentrenamiento de pesos de un modelo.
- Migración del banco a base de datos.
- Soporte a terceros o formación de terceros.

## Revisiones incluidas

- **Diseño:** no aplica (sin UI). A cambio: **1 ronda de reescritura de las reglas
  del agente** tras las primeras 5 piezas reales, si la prueba de voz falla.
- **Copy:** el contenido generado es revisable por el operador en cada pieza; el
  sistema no garantiza piezas "listas para publicar" sin lectura humana.
- **UAT:** 1 ronda de aceptación interna contra los 7 criterios de aceptación del
  MVP.
- **Otras:** 1 ronda de ajuste del checklist tras detectar un falso positivo o
  falso negativo en las primeras 10 piezas.

## Responsabilidades del cliente

Al ser proyecto interno, Daniel asume ambos lados. Queda registrado para que no
haya ambigüedad cuando el sistema falle:

- **Entregar información:** el contexto de marca (posicionamiento, audiencia,
  tono, ofertas, prohibiciones). Sin esto el sistema no genera nada, por diseño.
- **Aprobar decisiones:** las decisiones Type 1 diferidas a Fase 9 (proveedor de
  modelo, coste de API, instalación de skills de terceros).
- **Crear/pagar cuentas:** la cuenta y la clave del proveedor de modelo, a su
  nombre.
- **Probar:** ejecutar la medición de tiempo y la prueba de indistinguibilidad de
  voz sobre piezas reales.
- **Otras:** aportar el ángulo o tema de cada pieza; revisar temas sensibles antes
  de publicar.

## Dependencias externas

| Dependencia | Responsable | Costo | Riesgo |
|---|---|---|---|
| Proveedor de modelo (API o suscripción) | Daniel | Por definir en Fase 9 | Type 1: coste y política de uso de datos |
| Runtime de agente/skills del entorno | Daniel | Ya en uso | Bajo; entorno conocido |
| `coreyhaines31/marketingskills` u otra skill de terceros | Daniel | 0 € (open source) | R-003: licencia y cambios de esquema ajenos; se resuelve en Fase 9 |
| Plataformas destino (Instagram, TikTok, YouTube, LinkedIn) | Daniel | 0 € | Solo como formato de salida; sin integración |
| Sistema de archivos del repositorio | Nadie | 0 € | Bajo |

## Hitos de aceptación

| Hito | Evidencia | Quién aprueba |
|---|---|---|
| H1 — Contexto de marca validado | `docs/brand/` completo y sin campos vacíos | Daniel |
| H2 — Agente genera una pieza completa | 1 pieza con 4 capas AIDA, 5 hooks distintos y CTA, en disco | Daniel |
| H3 — Rechazo seguro verificado | Prueba con contexto vacío: el agente se detiene y nombra los campos faltantes | Daniel |
| H4 — Voz consistente | 2 de 3 evaluadores no aciertan el origen en la prueba de indistinguibilidad | Daniel |
| H5 — Métrica de tiempo | 5 piezas cronometradas con media ≤ 15 min | Daniel |
| H6 — Banco útil | 3 temas distintos en el banco, recuperables y sin hooks repetidos | Daniel |

## Estimación

| Bloque | Alcance | Estimación |
|---|---|---:|
| Discovery / diseño | Fases 1–8 (Brief, MVP, comercial, dominio, flujos, pantallas, dirección y spec) | 3–4 sesiones de trabajo |
| Implementación | Fases 9–13: arquitectura, datos, plan y construcción del agente, reglas, checklist y banco | 3–5 sesiones de trabajo |
| QA / deploy | Fase 14–16: casos límite, criterios de aceptación, puesta en uso | 1–2 sesiones |
| Handoff | Fase 17: documentación de uso y de extensión del contexto de marca | 1 sesión |
| Contingencia | Reescritura de reglas si falla la prueba de voz (R-001) | 1 sesión |

**Total: 9–13 sesiones de trabajo.** No hay fecha comprometida con terceros. La
estimación es de esfuerzo interno, no de precio, y no incluye el tiempo de
publicación ni de producción audiovisual.

## Precio y forma de pago

- **No aplica.** Proyecto interno sin cliente externo ni facturación.
- Coste del proyecto = tiempo propio + coste del proveedor de modelo (Fase 9).

## Costos recurrentes

| Servicio | Estimado | Quién paga | Cuenta a nombre de |
|---|---:|---|---|
| Proveedor de modelo | Por definir en Fase 9; acotado a 5 hooks + 1 guion por pieza | Daniel | Daniel |
| Almacenamiento del repositorio | 0 € (disco local) | Daniel | Daniel |
| Skills de terceros | 0 € si son open source; licencia a verificar | — | — |

## Propiedad

- **Código:** de Daniel (Monoga), repositorio local en `Desktop\Agente generador de contenido`.
- **Dominio:** no aplica.
- **Datos:** el contexto de marca, el banco de piezas y las claves de API son de
  Daniel. Las claves nunca se versionan en el repositorio.
- **Cuentas:** cuenta del proveedor de modelo a nombre de Daniel.
- **Diseños:** no aplica (sin UI).
- **Licencias:** todo lo escrito dentro del repositorio es propiedad plena. Las
  skills de terceros conservan su licencia original (a verificar en Fase 9).

## Garantía, soporte y mantenimiento

### Garantía por defectos

No aplica en sentido contractual. Internamente: si el agente genera contenido de
marca sin contexto válido, es un defecto crítico que bloquea el uso hasta
corregirse.

### Soporte incluido

El propio Daniel. No hay soporte a terceros.

### Mantenimiento mensual

- Revisar el contexto de marca cuando cambie la oferta o el posicionamiento.
- Ajustar el checklist si aparece un falso positivo o falso negativo.
- Revisar la licencia y el esquema de cualquier skill externa antes de actualizarla.

### No incluido

- Atención a usuarios externos.
- Corrección de contenido ya publicado.
- Mantenimiento de integraciones con plataformas (no existen en V1).
- Recuperación de piezas borradas fuera del repositorio.

## Política de cambios

Toda nueva capacidad se registra en `CHANGE_REQUESTS.md` antes de implementarse.
Cualquier petición que amplíe el alcance hacia publicación automática, video,
analítica o multi-cliente se trata como **Type 1** y reabre la evaluación de
alcance (riesgo R-006).

## Supuestos comerciales

- [ASSUMPTION] El proyecto es de uso propio de Monoga y no se revende como
  servicio (A-004). Si cambia, este artefacto se reabre: aparecen cliente,
  precio, soporte y probablemente arquitectura multi-cliente.
- [ASSUMPTION] El coste de API se mantiene dentro de un uso personal razonable al
  limitar 5 hooks + 1 guion por pieza (R-007).
- [ASSUMPTION] No habrá dependencia estructural de ninguna skill de terceros
  (ADR-001), así que una retirada externa no rompe el producto.

## Gate

- [x] Incluido y excluido están claros.
- [x] Los entregables tienen criterio de aceptación.
- [x] Las revisiones tienen límite.
- [x] Los costos recurrentes tienen responsable.
- [x] La propiedad de cuentas y datos está definida.
- [x] Soporte, garantía y mantenimiento no se confunden.
- [x] Existe proceso para cambios.

## Incertidumbres abiertas

- [ ] [DEFERRED:Fase 9] Coste real y política de uso de datos del proveedor de
      modelo (decisión Type 1, la toma Daniel).
- [ ] [DEFERRED:Fase 9] Licencia vigente de `marketingskills` si finalmente se
      reutiliza.
- [ ] [ASSUMPTION] La estimación de 9–13 sesiones es de esfuerzo interno y no ha
      sido validada con trabajo real; se recalibra al cerrar la Fase 11.
