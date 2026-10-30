---
artifact: tech-architecture
phase: 9
status: approved
reason: ""
last_updated: "2026-10-12"
---

# 09 — Arquitectura técnica de Agente Generador de Contenido

## Objetivos técnicos

1. **Convertir el criterio de marketing en archivos versionados.** El
   conocimiento (contexto de marca, framework AIDA, reglas, checklist) debe vivir
   en el repositorio, no dentro de un prompt invisible.
2. **Verificar de forma determinista lo que se pueda verificar.** El checklist
   debe evaluarse con reglas sobre el texto, no con la opinión del mismo modelo
   que escribió el texto.
3. **Nunca generar sin contexto de marca.** La arquitectura debe hacer imposible
   el modo de fallo que el producto existe para evitar.
4. **Sobrevivir al proveedor.** Cambiar de modelo, de runtime o de skill de
   terceros no debe reescribir el producto.
5. **Cero infraestructura.** Sin servidor, sin base de datos, sin despliegue. El
   producto corre donde el operador ya trabaja.

## Restricciones

- Producto interno, un solo usuario, Windows, trabajo de escritorio.
- Sin interfaz gráfica (decisión del MVP): la superficie es consola + archivos.
- Sin publicar, sin medir automáticamente, sin video.
- Coste recurrente acotado y con dueño (fase 3).
- El agente no puede aprobar ni publicar (BR-012).
- No instalar dependencias de terceros sin decisión explícita (ADR-001).

## Diagrama

```text
                    ┌─────────────────────────────────────────┐
   OPERADOR ───────▶│  ENTORNO DE AGENTE (runtime de Daniel)  │
   (terminal)       │  carga la skill generadora y los        │
                    │  archivos de reglas y contexto          │
                    └───────────────┬─────────────────────────┘
                                    │
              ┌─────────────────────┼─────────────────────┐
              ▼                     ▼                     ▼
   ┌────────────────────┐ ┌────────────────────┐ ┌────────────────────┐
   │ contexto-marca.md  │ │ reglas/            │ │ codigo/            │
   │ (fuente de verdad) │ │  aida.md           │ │  validar_contexto  │
   │ version + estado   │ │  reglas.md         │ │  validar_pieza     │
   │                    │ │  disparadores.md   │ │  (Python,          │
   │                    │ │  checklist.md      │ │   determinista)    │
   └─────────┬──────────┘ └─────────┬──────────┘ └─────────┬──────────┘
             │                      │                      │
             └──────────┬───────────┴──────────────────────┘
                        ▼
              ┌───────────────────────────────────┐
              │  GENERACIÓN (modelo de lenguaje)  │
              │  pieza: 4 capas + 5 hooks + CTA   │
              └───────────────┬───────────────────┘
                              ▼
              ┌───────────────────────────────────┐
              │  VERIFICACIÓN (código, no modelo) │
              │  estructura · límites · BR-002..7 │
              └───────┬───────────────────┬───────┘
                 pasa │                   │ falla
                      ▼                   ▼
        ┌──────────────────────┐  ┌──────────────────────────┐
        │ banco/piezas/        │  │ reporte de rechazo       │
        │ <id>-<slug>.md       │  │ (no se guarda pieza      │
        │ + banco/INDICE.md    │  │  incompleta)             │
        └──────────────────────┘  └──────────────────────────┘
                      │
                      ▼
        APROBACIÓN Y PUBLICACIÓN: humanas (BR-012)
```

Nada en este diagrama es remoto. No hay frontend, ni backend, ni base de datos,
ni autenticación, ni hosting.

## Decisiones

| Área | Elección | Problema que resuelve | Alternativa considerada | Razón | Riesgo |
|---|---|---|---|---|---|
| Superficie | Consola + archivos markdown | El operador trabaja en terminal y quiere velocidad, no clics | App web con UI | Una UI añade semanas y no aporta al problema real: la voz de marca y el volumen de variantes | Ninguno relevante; ya está validado en las Fases 6–8 |
| Motor de generación | Modelo de lenguaje del runtime que Daniel ya usa, aislado tras un adaptador | Generar texto con la voz de la marca | API propia con clave y facturación | Evita coste y decisión Type 1 inmediata; el adaptador mantiene la salida futura abierta | Dependencia del runtime actual; mitigada por el adaptador y porque el prompt es un archivo |
| Conocimiento de marca | Archivos markdown versionados en git | Convertir criterio tácito en activo auditable | Base de datos | Revisable, diffeable, sin infraestructura; el modelo lee archivos mejor que consulta SQL | Edición manual descuidada; mitigada por `validar_contexto` |
| Verificación | Script Python determinista sobre el texto generado | Verificar lo verificable sin pedirle al modelo que se juzgue a sí mismo | Segunda pasada del modelo | El mismo modelo que inventó una cifra no la va a detectar de forma fiable | Solo cubre lo verificable; los ítems subjetivos quedan asistidos por el modelo y marcados como tales |
| Persistencia | Sistema de archivos (markdown) | Almacenar piezas, hooks, checklist y versiones | SQLite / Postgres | Sin infraestructura, sin migraciones, recuperable con git; el volumen esperado no justifica una base de datos | Sin consultas agregadas; se resuelve derivando el índice |
| Índice del banco | Derivado de las piezas por el script | Saber qué temas y hooks existen | Archivo mantenido a mano | Un índice manual se desincroniza el primer día | Requiere releer todas las piezas; irrelevante a esta escala |
| Versionado del contexto de marca | Campo `version` en el frontmatter + pieza que lo referencia | Poder explicar por qué una pieza antigua dice lo que dice | Copia histórica del contexto | Trazabilidad suficiente sin duplicar archivos completos | Cambios no versionados a mano; mitigado por la validación |
| Auth | No aplica (un solo usuario, local) | — | Login | No hay terceros ni red | Ninguno |
| Hosting | No aplica (máquina local) | — | VPS | No hay servicio que hospedar | Ninguno |
| Dependencias | Cero dependencias de terceros en V1 | Evitar R-003 y R-006 | Instalar `marketingskills` | El framework AIDA no es el valor; el valor es el contexto y el checklist propio | Hay que escribir el conocimiento AIDA (coste asumido, ~1 sesión) |
| Lenguaje del código de verificación | Python 3.14 (ya instalado) | Validar contexto y piezas | PowerShell / Node | Mejor manejo de texto y tests; ya está en la máquina | Ninguno |

## Frontend

**No aplica.** No hay frontend. La "interfaz" es la salida de consola especificada
en `08-UI-SPEC.md` (contratos `RESUMEN`, `RECHAZO`) y los archivos markdown.

## Backend

**No aplica como servicio.** Lo más cercano son los scripts locales de
verificación:

- **Runtime:** Python 3.14 (`C:\Python314\python.exe`), sin dependencias externas.
- **API:** no hay. La interfaz es línea de comandos sobre archivos.
- **Jobs:** ninguno. Todo es síncrono: el operador pide una pieza y espera.
- **Webhooks:** ninguno.
- **Rate limiting:** no aplica, salvo el límite de producto de 5 hooks + 1 guion
  por generación (restricción de coste de la Fase 2).
- **Manejo de fallos:** si la generación se interrumpe, no se escribe ninguna
  pieza parcial (invariante del dominio). Se escribe el archivo al final, cuando
  la verificación ha terminado.

## Datos e infraestructura

- **DB:** ninguna. El "esquema" es la estructura de archivos definida en
  `10-DATA-AND-PERMISSIONS.md`.
- **Storage:** sistema de archivos local, versionado con git.
- **Cache:** ninguna.
- **Search:** `grep` / `Select-String` sobre el banco. Suficiente a esta escala.
- **Backups:** el repositorio git. Sin remoto configurado todavía: **decisión
  pendiente del operador** (ver Incertidumbres).
- **Restore:** `git checkout` de la pieza o del contexto. Una pieza descartada
  nunca se borra (BR-009), así que el histórico es recuperable por diseño.

### Estructura del repositorio (mapa técnico)

```text
/
├── AGENTS.md
├── .monoga/                      # estado del método de proyecto
├── docs/product/                 # artefactos de las 18 fases
├── design-reference/APPROVED.md  # contratos de texto aprobados (v1)
├── marca/
│   ├── contexto-marca.md         # FUENTE DE VERDAD (obligatorio)
│   └── versiones/                # copias históricas mínimas si se necesita
├── reglas/
│   ├── aida.md                   # definición de las 4 capas y mapeos
│   ├── reglas.md                 # las 12 reglas de negocio con ejemplo
│   ├── disparadores.md           # vocabulario cerrado de hooks
│   └── checklist.md              # los 7 ítems y qué verifica cada uno
├── agente/
│   └── SKILL.md                  # instrucciones del agente generador
├── banco/
│   ├── INDICE.md                 # derivado, no editado a mano
│   └── piezas/
│       └── <id>-<slug>.md
└── codigo/
    ├── validar_contexto.py
    ├── validar_pieza.py
    └── tests/
```

## Integraciones

| Integración | Uso | Auth | Límites | Fallback |
|---|---|---|---|---|
| Runtime de agente (actual) | Motor de generación | Sesión ya existente, sin clave en el repo | Límite de producto: 5 hooks + 1 guion por pieza | Si falla: no se guarda pieza parcial; se reintenta o se aborta |
| Proveedor de modelo alternativo (futuro) | Salida futura si el runtime cambia | Clave propia, fuera del repositorio | Presupuesto por definir | El adaptador aísla el cambio; el prompt es un archivo |
| `marketingskills` u otra skill de terceros | **No se integra en V1** | — | — | Si en el futuro se reutiliza, se hace tras verificar licencia y se aísla como adaptador |
| Plataformas de redes (Instagram, TikTok, YouTube, LinkedIn) | Solo como **formato de salida**, no como integración | Ninguna | — | Publicación manual por humano (BR-012) |

## Ambientes

| Ambiente | URL | Datos | Secretos | Propósito |
|---|---|---|---|---|
| Local | No aplica (sin servicio) | Repositorio real | Ninguno en V1 | Único ambiente. Generar y revisar |
| Staging | No aplica | — | — | No existe despliegue que ensayar |
| Production | No aplica | — | — | El "producto en producción" es el operador usándolo en local |

**Sobre la separación staging/producción:** no hay separación de entornos porque no
hay despliegue. El equivalente funcional es **git**: los cambios en
`reglas/` y `marca/` se revisan como diffs antes de usarlos, y una pieza descartada
o un contexto anterior siempre son recuperables. La separación efectiva es la
revisión humana del diff, no un segundo servidor.

## Observabilidad

- **Logs:** no hay logs de sistema. La evidencia es el propio archivo de pieza
  (frontmatter + checklist) y el resumen de consola. Una pieza es un registro
  auditable.
- **Errors:** los errores se reportan al operador en el momento, con causa
  concreta. No hay captura remota de errores porque no hay servicio remoto.
- **Analytics:** ninguno automático. Existe la entidad `Resultado` alimentada a
  mano (opcional en V1).
- **Alerts:** ninguno.
- **Health:** comprobación directa: `validar_contexto` devuelve `VÁLIDO` o la lista
  de campos faltantes. Es el único chequeo de salud que el producto necesita.

## Costos

| Servicio | Estimado | Escala | Responsable |
|---|---:|---|---|
| Motor de generación (runtime actual) | 0 € incremental en V1 | Con el uso normal del runtime | Daniel |
| Almacenamiento | 0 € (disco local) | Crece en kilobytes por pieza | Daniel |
| Skills de terceros | 0 € y no se instalan en V1 | — | — |
| Proveedor de API alternativo | Por definir si se adopta | Límite de 5 hooks + 1 guion por pieza | Daniel |

## Spikes

| Pregunta | Método | Resultado | Decisión |
|---|---|---|---|
| ¿Un script Python sin dependencias puede verificar los 7 ítems del checklist de forma determinista? | Spike en Fase 12: implementar `validar_contexto.py` y `validar_pieza.py`, ejecutarlos sobre una pieza escrita a mano | **Pendiente** — se resuelve en la Vertical Slice 0 | Determina si los ítems subjetivos (tono alineado, afirmaciones no respaldadas) quedan como verificación determinista parcial o asistida por modelo |
| ¿La salida del modelo respeta de forma fiable el frontmatter y los 5 hooks sin reformatear? | Spike en Fase 12: generar 3 piezas y medir cuántas pasan la validación a la primera | **Pendiente** | Determina si hace falta un paso de normalización o un formato de salida más estricto |
| ¿El contexto de marca cabe en la ventana de contexto junto con las reglas? | Medición directa al escribir `marca/contexto-marca.md` y `reglas/` | A estimar: 4 archivos de reglas + 1 contexto, esperado < 400 líneas en total | Si excede, se dividen las reglas y se cargan por modo (solo las necesarias) |

## ADR relacionados

- **ADR-001** (Fase 1, `DECISIONS.md`) — AIDA como columna vertebral y el contexto
  de marca como fuente de verdad. Es la decisión que gobierna toda esta fase.
- **ADR-002** (esta fase) — Almacenamiento en archivos versionados, sin base de
  datos.
- **ADR-003** (esta fase) — Cero dependencias de terceros en V1; el conocimiento
  AIDA se escribe dentro del repositorio.
- **ADR-004** (esta fase) — Verificación determinista en Python para lo
  verificable; el resto queda asistido y marcado como tal.

## Gate

- [x] Existe diagrama.
- [x] Cada tecnología resuelve un problema.
- [x] Costos y límites están identificados.
- [x] Staging y producción están separados.
- [x] Backups, logs y secretos tienen plan.
- [x] No hay complejidad sin evidencia.

**Nota sobre staging/producción:** se cumple la intención del gate (poder ensayar
un cambio sin romper el uso real) mediante git y revisión de diffs, no mediante un
segundo entorno. Explicado arriba para que no se lea como una casilla marcada en
falso.

## Incertidumbres abiertas

- [x] [ASSUMPTION] El motor de generación será el runtime que Daniel ya usa, sin
      clave de API ni coste incremental en V1. Reversible: el adaptador aísla el
      cambio de proveedor.
- [x] [ASSUMPTION] Python 3.14 sin dependencias externas basta para la
      verificación determinista. Se confirma en el spike de la Fase 12.
- [ ] [DEFERRED:Fase 16] **Remoto de git para backups.** Decisión de Daniel
      (2026-10-12): posponer hasta ver el sistema funcionando. El riesgo queda
      registrado como R-008 y **debe resolverse antes de usar el sistema con
      contenido real de producción**, no antes. La Fase 16 (Producción) no puede
      cerrarse con este punto abierto.
- [ ] [DEFERRED:Fase 10] Estructura exacta de las tablas de datos (piezas,
      versiones, resultados) y sus constraints.
- [ ] [DEFERRED:Fase 12] Resultado de los tres spikes. Si el spike 2 falla, se
      añade normalización de salida; si el spike 1 falla parcialmente, los ítems
      subjetivos del checklist pasan a verificación asistida y se marcan como tal
      en el reporte.
- [ ] [ASSUMPTION] El volumen del banco no superará lo que un `grep` resuelve de
      forma instantánea (cientos de piezas). Si se supera, se evalúa un índice
      estructurado.
