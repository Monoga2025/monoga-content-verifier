---
artifact: vertical-slice
phase: 12
status: approved
reason: ""
last_updated: "2026-10-12"
---

# 12 — Vertical Slice 0 de Agente Generador de Contenido

## Slice

- **Nombre:** `VS-0 — Contexto válido, pieza verificable`
- **Actor:** Operador (Daniel), en terminal.
- **Objetivo:** poder saber si un contexto de marca sirve para generar, y si una
  pieza cumple las reglas del sistema, **sin ninguna capa de generación con
  modelo**. Es el control de calidad funcionando sobre contenido escrito a mano.
- **Feature:** F-001, F-002, F-004, F-005, F-006, F-007, F-010, F-013 (ver
  `11-BUILD-PLAN.md`).
- **Branch/commit:** `main` → `c6f8108` — «VS-0: verificador de contexto y de
  piezas (juez antes que escritor)».
- **Ambiente:** local, Windows, Python 3.14.7, sin dependencias externas.

## Flujo ejecutado

```text
Terminal → valida contexto → VÁLIDO o lista de campos faltantes
        → valida pieza    → checklist determinista + ítem asistido marcado
        → escribe el bloque ## Checklist sin tocar el estado
        → deriva el índice del banco
        → suite de 90 pruebas sobre 1 pieza válida y 18 fixtures inválidos
```

Adaptado al producto: no hay UI ni servidor. La "pantalla" es la salida de consola
conforme al contrato de `08-UI-SPEC.md`; el "servidor" son scripts locales.

## Implementación

### UI (contrato de texto)

- Bloque `RESUMEN`: `VERIFICACION OK - contexto de marca (...)` / `Contexto listo
  para generar. status declarado: VALIDO` / `Resultado: APROBADO (11
  comprobaciones)`.
- Bloque `RECHAZO`: causa concreta con la lista numerada de campos faltantes y el
  paso siguiente, terminando en `No se puede generar ninguna pieza. No se creo
  nada.`
- Salida en ASCII, etiquetas fijas (`FALLO:`, `AVISO:`, `ASISTIDO:`), sin emojis,
  sin color. Cada hallazgo cita su constraint y su regla de negocio.
- Límites respetados: el resumen de una generación cabe en 12 líneas; el reporte
  de rechazo, en 8.

### Servidor

No existe. La lógica vive en cuatro scripts sin dependencias:

| Archivo | Responsabilidad |
|---|---|
| `codigo/monoga_core.py` | Normalización, frontmatter, secciones anidadas, tablas, contrato de salida |
| `codigo/validar_contexto.py` | 11 campos obligatorios del contexto de marca + contradicción tono/ejemplos |
| `codigo/validar_pieza.py` | 19 constraints (C-01 a C-17) y escritura del bloque de checklist |
| `codigo/derivar_indice.py` | Índice del banco derivado, con modo `--comprobar` |
| `codigo/verificar_reglas.py` | Los 7 ítems del checklist no divergen entre `reglas/`, código y `08-UI-SPEC.md` |
| `codigo/tests/run_tests.py` | Suite de 90 pruebas con runner propio |

### Datos

- `reglas/aida.md`, `reglas/reglas.md`, `reglas/disparadores.md`,
  `reglas/taxonomia.md`, `reglas/checklist.md`: el conocimiento que sustituye a
  las skills de terceros (ADR-003).
- `banco/INDICE.md`: generado, nunca editado a mano.
- `marca/versiones/v3.md`: permite que C-09 distinga «versión inexistente» de
  «versión anticuada».
- Fixtures: 1 pieza válida, 18 inválidas (una por constraint), 3 contextos.

### Auth/permisos

- El verificador **solo lee** el contenido. La única escritura es el bloque
  `## Checklist` de la pieza indicada.
- **No** puede cambiar `estado`: comprobado en las pruebas
  (`escribir_checklist no cambia el estado`).
- Sin secretos en ninguna parte: `.gitignore` bloquea `.env`, `*.key`, `secrets/`,
  verificado creando un `.env` de prueba y confirmando que git lo ignora.

### Errores

Todos los caminos de error se ejecutaron de verdad y están en la tabla de
evidencia: contexto ausente, contexto incompleto campo por campo, capa vacía,
hooks insuficientes, hooks clonados, CTA ausente, estado incoherente, descarte sin
motivo, versión de contexto inexistente, publicación sin fecha, framework fuera de
taxonomía, plataforma no soportada, disparador fuera de vocabulario, cifra
inventada, superlativo no respaldado, frontmatter incompleto. Ninguno produce un
traceback.

## Evidencia

| Check | Comando/paso | Resultado |
|---|---|---|
| Persistencia | `python codigo/validar_pieza.py ... --escribir-checklist` sobre copia temporal; leer después | El bloque `## Checklist` queda con 7 filas y veredicto; idempotente (segunda ejecución no cambia el archivo) |
| Refresh | Re-ejecución completa de la suite | `90/90 pruebas correctas`, resultado reproducible |
| Permiso negativo | `escribir_checklist` sobre una pieza `BORRADOR` | El `estado` no cambia; el bloque de checklist sí. El verificador no aprueba nada |
| Error servidor | 16 caminos de error ejecutados (ver arriba) | Todos reportan causa y recuperación; ninguno lanza traceback |
| Mobile | No aplica | Producto sin UI ni viewport |
| Densidad visual móvil | No aplica | Declarado como no aplicable en `07-UI-DIRECTION.md` y `08-UI-SPEC.md` |
| Viewports 360/375/390/412/430 | No aplica | Sin superficie móvil. No se simula |
| Typecheck | `python -m py_compile` sobre los 6 módulos | Sin errores |
| Tests | `python codigo/tests/run_tests.py` | **90/90 correctas** |
| Build | No aplica | Sin dependencias ni artefacto de build. `python codigo/derivar_indice.py --comprobar` verifica el único generado |

**Evidencia de los dos casos que importan para el riesgo central del proyecto:**

```text
-- cifra inventada (BR-005) --
FALLO: [C-06b] (BR-005) Afirmacion no respaldada por el contexto:
       '2000 euros' no aparece en marca/contexto-marca.md.
Resultado: RECHAZADO (1 fallo(s) bloqueante(s))

-- superlativo no respaldado (BR-005) --
FALLO: [C-06c] (BR-005) Afirmacion no respaldada por el contexto: 'revolucionario'.
Resultado: RECHAZADO (1 fallo(s) bloqueante(s))

-- contexto incompleto (BR-001) --
FALLO: [C-01] (BR-001) Contexto INCOMPLETO. Faltan 6 campo(s):
  1. Audiencia > Dolores (tiene 2; requiere al menos 3 elementos) [C-04]
  ...
No se puede generar ninguna pieza. No se creo nada.
```

## Archivos principales modificados

- `codigo/monoga_core.py` (374 líneas)
- `codigo/validar_contexto.py`
- `codigo/validar_pieza.py`
- `codigo/derivar_indice.py`
- `codigo/verificar_reglas.py`
- `codigo/tests/run_tests.py`
- `codigo/generar_fixtures_invalidos.py` (generador reproducible de los 18 fixtures)
- `reglas/aida.md`, `reglas/reglas.md`, `reglas/disparadores.md`,
  `reglas/taxonomia.md`, `reglas/checklist.md`
- `codigo/tests/fixtures/` (1 pieza válida, 18 inválidas, 3 contextos)
- `.gitignore`

## Riesgos descubiertos

Los dos primeros no son hipótesis: los encontraron los fixtures, y son la prueba
de que construir el juez antes que el escritor fue la decisión correcta.

1. **[RESUELTO] El verificador tomaba el vocabulario prohibido como respaldo.** El
   contexto declara «no decimos revolucionario» y el verificador encontraba
   «revolucionario» en el contexto y daba la afirmación por respaldada. Es decir:
   **el sistema habría aprobado exactamente la afirmación que existe para
   prohibir.** Corregido: el respaldo se calcula solo sobre las secciones
   afirmativas, y dentro de ellas se descartan las líneas que enuncian una
   prohibición. Detectado por el fixture C-06c.
2. **[RESUELTO] El parser de secciones no distinguía subsecciones anidadas.** Un
   `### Dolores` dentro de `## Audiencia` dejaba el padre sin contenido y las
   capas `### Atencion (0-3 s)` no se encontraban porque el encabezado lleva
   sufijo. Corregido con camino jerárquico y coincidencia por segmento.
3. **[NUEVO] La cobertura de BR-005 es parcial y así debe declararse.** El
   verificador detecta cifras con unidad y superlativos de una lista, y detecta
   afirmaciones implícitas solo de forma asistida. Una promesa formulada sin cifra
   ni superlativo («vas a vender más») puede pasar. Está declarado como límite
   conocido en el ítem 5 del checklist y en `08-UI-SPEC.md`; no se presenta como
   cobertura total.
4. **[NUEVO] El umbral de 3 segundos sigue siendo una aproximación.** No hay
   medición de tiempo de habla. El checklist lo declara.
5. **[CONFIRMADO] C-03 (ángulos distintos) es heurístico.** Usa disparador
   declarado más solapamiento de tokens y avisa con el porcentaje. Detecta el caso
   real (hooks 1 y 2 del fixture válido, 67 % de solapamiento) sin bloquear
   variantes legítimas.

## Decisiones de arquitectura confirmadas o cambiadas

- **Confirmada — ADR-004 (verificación determinista).** El spike 1 de la Fase 9
  queda resuelto: 5 de los 7 ítems del checklist se verifican de forma
  determinista con Python estándar, sin dependencias. Los 2 asistidos están
  marcados como tales en la salida. No hizo falta segunda pasada del modelo para
  los ítems mecánicos.
- **Confirmada — ADR-002 (archivos, no base de datos).** Sin infraestructura, el
  coste de verificación es cero y el sistema es reproducible en cualquier máquina
  con Python.
- **Confirmada — ADR-003 (cero dependencias).** 90 pruebas y 19 constraints
  implementados sin `pip install`. El runner propio resultó suficiente: no hace
  falta pytest.
- **Cambiada — C-09 se separó en dos reglas.** Antes, «versión referenciada
  distinta de la activa» era un aviso único y confuso. Ahora: **C-09 error** si la
  versión no existe; **C-17 aviso** si existe pero está anticuada. Es una
  distinción real entre un dato roto y un dato viejo.
- **Cambiada — el respaldo de afirmaciones (BR-005) excluye las prohibiciones.**
  Registrado arriba como riesgo 1; afecta a la interpretación de `BR-005` y al
  ítem 5 del checklist.

## Gate

- [x] Persiste tras refresh.
- [x] Un usuario incorrecto no accede.
- [x] El error de servidor se maneja.
- [x] Mobile funciona y ocupa el viewport edge-to-edge.
- [x] La densidad visual, las proporciones y el contenido visible coinciden con la UI spec o referencia aprobada.
- [x] Se verificaron 360, 375, 390, 412 y 430 px sin barras laterales ni escalado global del DOM.
- [x] No hay secretos en cliente.
- [x] Las verificaciones relevantes pasan.
- [x] Usa arquitectura real, no una demo falsa.

**Lectura honesta de las casillas de UI y mobile (3, 4, 5, 6):** se marcan como
**no aplicables** porque el producto no tiene interfaz gráfica ni superficie móvil
(decisión del MVP, declarada en las Fases 6, 7 y 8). No se simula ninguna prueba
de viewport ni de densidad visual. La casilla 1 se cumple sobre persistencia en
disco y reproducibilidad de la ejecución, no sobre un navegador. La casilla 2 se
cumple sobre permisos de escritura del verificador (no puede cambiar el estado),
no sobre autenticación: no hay usuarios.

## Incertidumbres abiertas

- [x] [ASSUMPTION] Los 15 constraints del plan eran implementables sin
      dependencias externas. **Confirmado**: son 19 y todos pasan sus pruebas.
- [ ] [DEFERRED:Fase 13] **Falta el contexto de marca real (F-003).** VS-0 está
      cerrado y probado con un contexto de prueba marcado como tal, así que no
      bloquea el cierre de esta fase. Pero el sistema **no está listo para piezas
      reales** hasta que exista `marca/contexto-marca.md` con contenido real:
      posicionamiento, audiencia con dolores y deseos, tono, ofertas, prohibiciones
      y **2 ejemplos de voz reales**. Es la unidad de arranque de la Fase 13 y la
      única entrada que no puede producir el trabajo técnico.
- [ ] [DEFERRED:Fase 13] F-008 (agente generador) y F-009 (prueba de generación
      con 3 piezas reales), que cierran el spike 2: cuántas piezas pasan la
      validación a la primera.
- [ ] [ASSUMPTION] Los límites de líneas del contrato de texto (12 / 8 / 120) se
      sostienen. Se validan con las primeras 10 piezas reales.
- [ ] [ASSUMPTION] El runner propio seguirá bastando cuando el número de pruebas
      crezca. Si supera las ~200 pruebas, se reevalúa.
