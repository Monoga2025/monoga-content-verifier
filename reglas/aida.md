# AIDA para guiones de redes sociales

## Índice

1. Qué es AIDA aquí y qué no
2. Las cuatro capas
3. Mapeo a otros frameworks
4. Errores típicos del framework

## 1. Qué es AIDA aquí y qué no

AIDA es la **columna vertebral estructural** de cada pieza: cuatro capas
etiquetadas, cada una con una función distinta y no intercambiable.

**Es** una estructura de decisión del espectador:

| Capa | Función real | Pregunta que responde el espectador |
|---|---|---|
| Atención | Detener el scroll | ¿Esto va conmigo? |
| Interés | Sostener el interés | ¿Esto me pasa a mí o me importa? |
| Deseo | Crear el querer | ¿Qué gano si actúo? |
| Acción | Provocar el paso siguiente | ¿Qué hago ahora, exactamente? |

**No es** una plantilla de relleno. AIDA no dice *qué* decir, dice *en qué orden
decidir*. El contenido de cada capa sale del contexto de marca, nunca del
framework.

**Regla dura:** si una capa se puede quitar y el guion sigue funcionando igual,
esa capa estaba mal escrita.

## 2. Las cuatro capas

### Atención (0–3 s)

- **Objetivo:** ganar el segundo siguiente. Nada más. No informar, no presentarse,
  no saludar.
- **Qué pertenece aquí:** una afirmación incómoda, una contradicción con lo que la
  audiencia cree, un error concreto que comete, una cifra del negocio, una escena
  reconocible en la primera frase.
- **Qué NO pertenece aquí:** "Hola a todos", "hoy os traigo", "¿Sabías que…?",
  presentaciones de marca, contexto previo, agradecimientos.
- **Cómo se reconoce si está bien:** un desconocido que solo lee la primera frase
  quiere saber qué viene después.
- **Ejemplo malo:** "Hola, hoy quiero hablaros de por qué perdemos clientes."
- **Ejemplo bueno:** "Tu cliente no se fue por el precio. Se fue en el minuto 3 de
  la primera llamada."
- **Límite operativo:** ≤ 12 palabras (aproximación al umbral de 3 segundos).

### Interés (3–10 s)

- **Objetivo:** que la audiencia se reconozca en el problema. El interés no se crea
  con datos, se crea con identificación.
- **Qué pertenece aquí:** el problema concreto en su contexto real, la escena que
  la audiencia vive, la consecuencia de seguir igual, el dato que dimensiona el
  problema.
- **Qué NO pertenece aquí:** la solución, el producto, las características, la
  promesa, el precio.
- **Cómo se reconoce si está bien:** la audiencia piensa "esto me pasa a mí", no
  "qué interesante".
- **Ejemplo malo:** "Muchas empresas pierden clientes por mala comunicación."
- **Ejemplo bueno:** "Grabas el vídeo, lo publicas, y a los tres días sigue sin
  responder nadie. Y no sabes si el problema es el vídeo o el momento."

### Deseo (10–20 s)

- **Objetivo:** que la audiencia quiera el resultado. Se construye mostrando la
  consecuencia de actuar, no enumerando características.
- **Qué pertenece aquí:** el antes y el después concreto, el resultado observable,
  qué cambia en el día a día, por qué eso importa a esa audiencia específica.
- **Qué NO pertenece aquí:** listas de funcionalidades, adjetivos
  ("potente", "revolucionario", "profesional"), promesas sin respaldo, precios sin
  contexto, superlativos.
- **Cómo se reconoce si está bien:** la audiencia puede imaginarse el resultado en
  su propia vida, no en abstracto.
- **Ejemplo malo:** "Nuestro sistema es la solución más completa del mercado."
- **Ejemplo bueno:** "La próxima vez que grabes, sabrás en el minuto uno si el
  gancho funciona, sin esperar a ver los números."
- **Límite:** toda afirmación aquí debe estar respaldada por el contexto de marca
  (BR-005). Si no lo está, no se escribe.

### Acción (cierre)

- **Objetivo:** que la audiencia sepa exactamente qué hacer, ahora.
- **Qué pertenece aquí:** un único paso concreto, alcanzable, con su destino
  explícito.
- **Qué NO pertenece aquí:** dos o más acciones (divide la intención), acciones
  vagas ("sígueme para más", "dale like"), acciones imposibles para la audiencia,
  acciones que no se corresponden con el contenido de la pieza.
- **Cómo se reconoce si está bien:** se puede ejecutar sin pensar y sin releer.
- **Ejemplo malo:** "Sígueme y comenta lo que piensas."
- **Ejemplo bueno:** "Guarda este vídeo. La próxima vez que grabes, míralo antes de
  escribir el guion."
- **Regla dura:** exactamente 1 CTA por pieza (BR-003).

## 3. Mapeo a otros frameworks

El sistema usa AIDA por defecto. Se admiten alternativas **declaradas con su razón**
(BR-002). Nunca se usa un framework sin declararlo.

### Video corto: Hook / Substance / Payoff

Es AIDA comprimida para formatos sin espacio de respiración. El mapeo es exacto:

| Hook/Substance/Payoff | AIDA equivalente |
|---|---|
| Hook | Atención |
| Substance | Interés + Deseo |
| Payoff | Acción |

Cuándo usarlo: piezas de ≤ 20 s donde Interés y Deseo no pueden desarrollarse por
separado sin perder retención. La pieza debe declarar que Substance cubre dos capas
y separarlas igualmente en el archivo.

### Copy directo: PAS (Problema–Agitación–Solución)

| PAS | AIDA equivalente |
|---|---|
| Problema | Interés |
| Agitación | Deseo (por contraste: qué pasa si no actúas) |
| Solución | Acción |

Cuándo usarlo: audiencia que ya conoce el problema y no necesita ser detenida, sino
convencida. Exige igualmente una Atención y una Acción explícitas: PAS **no exime**
de hook ni de CTA.

### Copy directo: Before–After–Bridge (BAB)

| BAB | AIDA equivalente |
|---|---|
| Before | Interés |
| After | Deseo |
| Bridge | Acción |

Cuándo usarlo: transformaciones visibles y demostrables. Exige igualmente Atención
y CTA.

### Prohibición

No se admiten frameworks fuera de este catálogo sin actualizar
`reglas/taxonomia.md` y registrar la decisión. Un framework inventado en una pieza
concreta es un fallo, no una excepción creativa.

## 4. Errores típicos del framework

1. **La Atención es un saludo.** Es el error más caro y el más frecuente.
2. **Interés y Deseo son la misma cosa.** Si ambas capas describen el problema, no
   hay deseo, y la pieza no tiene por qué terminar en la acción.
3. **El Deseo son características.** Las características no son deseo; la
   consecuencia de las características sí.
4. **La Acción son tres acciones.** Divide la intención y reduce la conversión.
5. **El framework se nota.** Cuando AIDA se aplica de forma mecánica, la audiencia
   reconoce la plantilla (R-004). Se combate variando el disparador de la Atención y
   el ángulo de la pieza, no abandonando la estructura.
6. **Se rellena la capa en lugar de resolverla.** Una capa con una frase genérica
   está vacía aunque tenga texto. El checklist debe detectarlo.
7. **AIDA se usa donde no encaja.** En video corto, forzar cuatro bloques separados
   cuando el formato no lo permite produce un guion que se lee como esquema. Se
   declara el mapeo y se escribe para el formato.
