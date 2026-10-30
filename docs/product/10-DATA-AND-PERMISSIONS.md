---
artifact: data-permissions
phase: 10
status: approved
reason: ""
last_updated: "2026-10-12"
---

# 10 — Datos, autenticación y permisos de Agente Generador de Contenido

> **No hay base de datos y no hay autenticación.** Por ADR-002 los datos son
> archivos markdown versionados en git, y por el MVP hay un único usuario local.
> Este documento sigue siendo necesario porque las **constraints que una base de
> datos habría impuesto hay que imponerlas ahora en código**, y porque los
> permisos de escritura entre el operador, el agente y el script de verificación
> sí existen y deben quedar explícitos.

## Estrategia de identidad

- **Login:** no aplica. Un único usuario local, sin terceros ni red.
- **Registro/invitación:** no aplica.
- **Recuperación:** no aplica (no hay credenciales).
- **Sesión:** la del sistema operativo.
- **Desactivación:** no aplica.
- **Roles:** dos actores con permisos distintos, sin cuentas: **Operador**
  (Daniel, humano) y **Agente** (sistema). Más un tercer actor sin permisos de
  escritura: **Verificador** (los scripts de `codigo/`).
- **Identidad real:** la del sistema de archivos. No se implementa capa de
  identidad porque no hay nada que aislar.

**Lo que sí se protege:** el agente no puede aprobar, publicar, borrar ni
reescribir el contexto de marca. Esa restricción no se aplica con "no mostrar el
botón" sino con el hecho de que el agente no tiene la operación entre sus
capacidades declaradas en `agente/SKILL.md`, y porque el frontmatter de estado es
escrito por el humano.

## Entidades → almacenamiento

| Entidad | Archivo | Razón |
|---|---|---|
| ContextoDeMarca | `marca/contexto-marca.md` | Fuente de verdad única; se lee en cada generación |
| Versión de contexto | `marca/versiones/vNNN.md` | Copia mínima inmutable para explicar piezas antiguas (BR-008) |
| Pieza | `banco/piezas/<id>-<slug>.md` | Unidad autocontenida, diffeable, auditable |
| Hook | dentro del bloque `HOOKS` de la pieza | No tiene vida propia; siempre hay exactamente 5 |
| Capa | dentro del bloque `CAPAS` de la pieza | Cuatro por pieza, etiquetadas |
| CTA | dentro del bloque `CTA` de la pieza | Uno por pieza, verificable de forma independiente |
| Checklist | dentro del bloque `CHECKLIST` de la pieza | Evidencia de calidad, inseparable de la pieza |
| Taxonomía | `reglas/taxonomia.md` | Vocabulario cerrado de frameworks, plataformas y formatos |
| Resultado | bloque `RESULTADO` de la pieza | Histórico de mediciones manuales |
| Índice del banco | `banco/INDICE.md` | **Derivado** por script; nunca editado a mano |
| Reglas del agente | `reglas/*.md` | Conocimiento auditable, no un prompt invisible |
| Instrucciones del agente | `agente/SKILL.md` | La capacidad declarada del agente |

## Esquema

### `marca/contexto-marca.md`

| Campo | Tipo | Requerido | Regla |
|---|---|---:|---|
| `version` | entero | Sí | Monotónico; se incrementa en cada revalidación con cambio |
| `last_validated` | fecha ISO | Sí | Se actualiza al pasar a `VÁLIDO` |
| `status` | enum | Sí | `INCOMPLETO` \| `VÁLIDO` \| `DESACTUALIZADO` |
| `marca` | texto | Sí | Nombre de la marca |
| Posicionamiento | sección | Sí | No vacía |
| Propuesta de valor | sección | Sí | No vacía |
| Audiencia → Dolores | sección | Sí | Al menos 3 elementos |
| Audiencia → Deseos | sección | Sí | Al menos 3 elementos |
| Tono y voz → Registro y ritmo | sección | Sí | No vacía |
| Tono y voz → Lo que nunca decimos | sección | Sí | Al menos 3 elementos |
| Ofertas vigentes | tabla | Sí | Al menos 1 fila con vigencia |
| Prohibiciones | lista | Sí | Al menos 3 elementos |
| Vocabulario prohibido | lista | Sí | Puede estar vacía, pero la sección debe existir |
| Ejemplos de voz | sección | Sí | **Mínimo 2**, con texto real ya publicado |

**Constraint principal:** si falta cualquiera de los campos obligatorios, `status`
no puede ser `VÁLIDO`. Lo impone `codigo/validar_contexto.py`, no la buena
voluntad del operador.

### `banco/piezas/<id>-<slug>.md`

| Campo | Tipo | Requerido | Regla |
|---|---|---:|---|
| `pieza` | entero | Sí | Único en el banco; sin huecos no es obligatorio |
| `tema` | texto | Sí | No vacío |
| `fecha` | fecha ISO | Sí | Fecha de creación |
| `contexto_marca` | `vN` | Sí | Debe existir esa versión (BR-008) |
| `framework` | enum | Sí | `AIDA` \| `PAS` \| `BAB` \| `Hook/Substance/Payoff` (BR-002) |
| `razon_framework` | texto | Sí si `framework != AIDA` | Obligatorio cuando no es AIDA |
| `plataforma` | enum | Sí | Del vocabulario de `reglas/taxonomia.md` |
| `formato` | enum | Sí | Coherente con la plataforma |
| `duracion_objetivo` | texto | Sí | Segundos, o `n/a` para formatos escritos |
| `estado` | enum | Sí | `BORRADOR` \| `EN_REVISION` \| `APROBADA` \| `PUBLICADA` \| `DESCARTADA` |
| `hook_elegido` | entero o `sin elegir` | Sí | Si hay entero, debe existir ese hook |
| `tema_sensible` | booleano | Sí | Si es `sí`, exige revisión humana antes de publicar (BR-010) |
| `relacionada_con` | ruta o `—` | Sí | Referencia a pieza previa si aplica (UF-007) |
| `publicada_el` | fecha o `—` | Sí | Obligatoria si `estado: PUBLICADA` |
| `motivo_descarte` | texto o `—` | Sí | Obligatorio si `estado: DESCARTADA` (BR-009) |
| Bloque `CAPAS` | 4 secciones | Sí | Exactamente Atención, Interés, Deseo, Acción; ninguna vacía (BR-007) |
| Bloque `CTA` | 1 sección | Sí | Acción + destino + alcanzable (BR-003) |
| Bloque `HOOKS` | tabla | Sí | **Exactamente 5 filas** (BR-004) |
| Bloque `ADAPTACION` | sección | Sí | Plataforma, longitud, ritmo, ajustes |
| Bloque `NOTAS` | tabla | Sí | 4 filas, una por capa |
| Bloque `CHECKLIST` | tabla | Sí | **Exactamente 7 filas**, en orden fijo, cada una con su regla |
| Bloque `RESULTADO` | tabla | Sí | Puede estar vacía (`SIN_MEDIR`) |

### Relaciones

```text
contexto-marca.md (vN) ──1:N──▶ piezas/*.md        (por campo contexto_marca)
pieza ──1:5──▶ hooks        (bloque HOOKS)
pieza ──1:4──▶ capas        (bloque CAPAS)
pieza ──1:1──▶ CTA          (bloque CTA)
pieza ──1:1──▶ checklist    (bloque CHECKLIST)
pieza ──1:N──▶ resultados   (bloque RESULTADO, opcional)
pieza ──0:1──▶ pieza        (relacionada_con, UF-007)
INDICE.md ◀──derivado── piezas/*.md
```

### Constraints

Las que una base de datos habría impuesto y ahora impone `validar_pieza.py`:

- **C-01** Exactamente 4 capas, con los 4 tipos requeridos, ninguna vacía.
- **C-02** Exactamente 5 hooks, salvo la excepción de BR-004 (temas sensibles o de
  nicho), que exige `excepcion_hooks` con motivo escrito en el frontmatter. Sin ese
  campo, cualquier número distinto de 5 es un fallo.
- **C-15** Si existe `excepcion_hooks`, su motivo no puede estar vacío y el número
  de hooks no puede ser 0.
- **C-03** Los 5 hooks tienen disparador declarado y **no comparten el mismo
  disparador con el mismo ángulo** (BR-004). Este es el que detecta el volumen
  falso de variantes.
- **C-04** Exactamente 1 CTA, con acción, destino y alcanzabilidad declarados.
- **C-05** Exactamente 7 ítems de checklist, en el orden de `reglas/checklist.md`.
- **C-06** `estado: APROBADA` o posterior es incompatible con cualquier capa vacía,
  CTA ausente o ítem de checklist en `FALLO`.
- **C-07** `estado: DESCARTADA` exige `motivo_descarte` no vacío.
- **C-08** `estado: PUBLICADA` exige `publicada_el` y exige que `tema_sensible` no
  esté pendiente de revisión humana.
- **C-09** `contexto_marca` debe referenciar una versión existente.
- **C-10** `publicada_el` no puede ser futura.
- **C-11** `framework != AIDA` exige `razon_framework`.
- **C-12** Ningún hook supera 12 palabras (BR-006), salvo formato escrito
  declarado como tal.
- **C-13** Los campos de `plataforma` y `formato` pertenecen al vocabulario de la
  taxonomía.
- **C-14** No puede existir una pieza sin contexto de marca `VÁLIDO` en el momento
  de su generación (BR-001). La validación se hace contra la versión referenciada.

### Índices

No hay índices de base de datos. El índice del banco (`banco/INDICE.md`) es una
tabla derivada por script con las columnas: ID, Tema, Ángulo, Hook elegido,
Estado, Plataforma, Fecha. Se regenera, nunca se edita a mano: un índice manual se
desincroniza el primer día.

### Historial y auditoría

- **Historial:** git. Cada pieza, cada versión del contexto y cada cambio de regla
  es un commit. `git log` sobre un archivo es la auditoría completa.
- **Auditoría de la pieza:** el propio archivo lleva estado, checklist y versión de
  contexto, así que es autodescriptivo sin consultar nada externo.
- **Cambios de estado:** quedan en el historial de git, no en un campo aparte.

### Borrado y retención

- **No se borra nada.** Una pieza descartada se conserva con motivo (BR-009); una
  versión antigua del contexto se conserva porque hay piezas que dependen de ella;
  una regla retirada se marca inactiva.
- **Retención:** indefinida. El volumen es de kilobytes.
- **Borrado excepcional:** solo si una pieza contiene información que no debería
  existir (por ejemplo, un dato de un tercero introducido por error). En ese caso el
  borrado se hace como commit explícito con el motivo, no silenciosamente.
- **Claves y secretos:** en V1 no existen. Si se adopta un proveedor de API, la
  clave vive en una variable de entorno del sistema, **nunca** en el repositorio, y
  `.gitignore` debe cubrir `.env`, `*.key` y `secrets/` antes de eso.

### Timezone, moneda y precisión

- **Fechas:** ISO 8601 (`YYYY-MM-DD`) en hora local del operador. Sin zonas
  horarias: un usuario, una máquina.
- **Moneda:** no aplica (no hay precios ni pagos).
- **Precisión numérica:** solo el `version` del contexto y el `pieza` (id), ambos
  enteros. No hay cálculos monetarios ni métricas con decimales obligatorios.

## Matriz de permisos

| Acción | Operador (humano) | Agente | Verificador | Enforcement |
|---|:---:|:---:|:---:|---|
| Leer contexto de marca | Sí | Sí | Sí | Archivo legible |
| Escribir contexto de marca | Sí | **No** | No | El agente no tiene la operación; solo el humano edita |
| Validar contexto (`status`) | Sí | **No** | Sí (solo lectura + veredicto) | El script reporta; el humano decide |
| Leer reglas y taxonomía | Sí | Sí | Sí | Archivo legible |
| Escribir reglas | Sí | **No** | No | Solo el humano |
| Generar pieza (crear `BORRADOR`) | Sí | **Sí** | No | Es la única escritura del agente |
| Editar una pieza existente | Sí | **No** | No | El agente no reescribe piezas ya guardadas |
| Mover a `EN_REVISION` | Sí | **No** | No | Humano |
| Mover a `APROBADA` | Sí | **No** | No | Humano (BR-012) |
| Mover a `PUBLICADA` | Sí | **No** | No | Humano (BR-012) |
| Mover a `DESCARTADA` | Sí | **No** | No | Humano, con motivo obligatorio |
| Registrar `Resultado` | Sí | **No** | No | Humano |
| Regenerar solo los hooks | Sí | Sí (crea una versión nueva) | No | Humano lo pide |
| Regenerar el índice | Sí | No | **Sí** | El script lo deriva |
| Escribir el checklist | Sí | Sí (en la pieza nueva) | Sí (solo el resultado, en la misma pieza nueva) | El verificador escribe el veredicto, no el contenido |
| Borrar una pieza | Sí (con commit y motivo) | **No** | No | Humano |

**Enforcement real, no cosmético.** No hay botones que ocultar: la restricción se
aplica declarando las capacidades del agente en `agente/SKILL.md` (el agente no
tiene la operación de aprobar) y con `validar_pieza.py`, que rechaza cualquier
archivo cuyo estado sea incompatible con su contenido. La tercera barrera es git:
cualquier cambio queda firmado y visible en el diff.

## Multi-tenant / ownership

- **Multi-tenant:** no aplica. Un solo operador, una sola marca (BR-011).
- **Ownership:** Daniel (Monoga) es dueño de todo: contexto de marca, reglas, banco
  de piezas y cualquier clave futura. No hay datos de terceros ni de clientes.
- **Cross-user / cross-tenant:** imposible por diseño al no existir usuarios ni
  tenants. **Si el proyecto se convirtiera en servicio multi-cliente, este
  documento se reabre**: aparecen aislamiento por marca, permisos, auth y
  probablemente base de datos (registrado en A-004).

## Storage

| Área | Quién escribe | Quién lee | Tipo | Retención |
|---|---|---|---|---|
| `marca/` | Operador | Operador, Agente, Verificador | Markdown | Indefinida |
| `marca/versiones/` | Operador | Operador, Agente | Markdown | Indefinida |
| `reglas/` | Operador | Operador, Agente, Verificador | Markdown | Indefinida |
| `agente/` | Operador | Runtime del agente | Markdown | Indefinida |
| `banco/piezas/` | Agente (crea), Operador (edita) | Operador, Agente, Verificador | Markdown | Indefinida; el descarte no borra |
| `banco/INDICE.md` | Verificador (deriva) | Operador, Agente | Markdown | Regenerable |
| `codigo/` | Operador | Operador, Verificador | Python | Indefinida |
| `.env` (futuro) | Operador | Runtime | Variable de entorno | Nunca en git |

## Datos sensibles

- **No hay datos personales de terceros.** No hay PII en el alcance: no se
  recopilan clientes, correos, teléfonos ni métricas de individuos.
- **Sí hay información competitiva propia:** posicionamiento, ofertas y
  prohibiciones de la marca. No es sensible a nivel legal, pero es material que no
  debe publicarse por accidente.
- **Regla operativa:** el repositorio no se publica, no se sube a un remoto
  público y no se comparte. Un remoto futuro debe ser **privado** (R-008).
- **Etiquetado de sensibilidad:** las piezas se marcan con `tema_sensible` para
  forzar revisión humana antes de publicar (BR-010). Es el único etiquetado de
  sensibilidad del sistema.
- **Sin cifrado en reposo:** el disco del operador. No se añade porque no hay
  datos de terceros y hacerlo obligaría a gestionar claves, que es más riesgo que
  beneficio a esta escala.

## Amenazas y mitigaciones

| Riesgo | Impacto | Mitigación |
|---|---|---|
| El agente genera contenido de marca sin contexto válido | Alto: es el modo de fallo que el producto existe para evitar | BR-001 + `validar_contexto.py` obligatorio antes de generar + el agente se niega por capacidad declarada |
| El modelo afirma un beneficio, cifra o promesa que el negocio no puede respaldar | Alto (reputacional y legal) | BR-005 + ítem determinista del checklist + revisión humana en temas sensibles (BR-010) |
| Una pieza se aprueba con una capa vacía o sin CTA | Medio: pieza inservible que llega a publicación | Invariante del dominio + C-06 en `validar_pieza.py` |
| Se marca `APROBADA` a mano saltándose el checklist | Medio | C-06 lo detecta; git lo muestra en el diff; el checklist debe estar completo en el mismo archivo |
| El índice del banco se desincroniza | Bajo: solo orienta | Se deriva por script, nunca se edita a mano |
| Edición manual del contexto borra una oferta vigente y las piezas antiguas quedan falsas | Medio | Versionado del contexto (C-09) + lista de piezas afectadas al revalidar (UF-006) |
| Una clave de API futura acaba en un commit | Alto | La clave vive en variable de entorno; `.gitignore` cubre `.env`, `*.key`, `secrets/` **antes** de adoptar proveedor |
| Pérdida del disco local | Alto | R-008, pendiente: remoto privado obligatorio antes de usar contenido real (Fase 16) |
| Fuga de información competitiva a un remoto público | Alto | El remoto debe ser privado por decisión registrada; el repo no se publica |

## Gate

- [x] El esquema corresponde al dominio.
- [x] Existen constraints para invariantes.
- [x] Cada acción sensible tiene permiso.
- [x] Se bloquea acceso cross-user/cross-tenant.
- [x] Storage tiene reglas.
- [x] Retención y borrado están definidos.
- [x] Los permisos no dependen de ocultar botones.

**Nota sobre la casilla 4:** se cumple por **inexistencia de usuarios y tenants**
(un solo operador local), no por un control implementado. Queda escrito que, si el
proyecto pasa a multi-cliente, este documento se reabre antes de tocar nada.

## Incertidumbres abiertas

- [x] [ASSUMPTION] Persistencia en archivos markdown (ADR-002). Confirmado: el
      volumen y el caso de uso no justifican base de datos. Se revisa si el banco
      supera ~200 piezas.
- [ ] [ASSUMPTION] Los 12 constraints (C-01 a C-14) son verificables con un script
      sin dependencias externas. Se confirma en el spike 1 de la Fase 12; si alguno
      resulta imposible de verificar de forma determinista, se marca como asistido
      y se documenta (ADR-004).
- [ ] [ASSUMPTION] El umbral de 3 elementos en dolores, deseos, prohibiciones y
      "lo que nunca decimos" es razonable para que el contexto tenga sustancia. Se
      valida escribiendo el contexto real de Monoga.
- [ ] [DEFERRED:Fase 16] Remoto privado de git (R-008, A-015). Bloquea el cierre de
      Fase 16, no el de esta fase.
