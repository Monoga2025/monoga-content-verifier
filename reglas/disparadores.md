# Disparadores de hook

**Vocabulario cerrado.** Un hook solo puede usar uno de estos seis disparadores, y
debe declararlo. El disparador explica *por qué* la primera frase detiene el scroll;
sin él, el hook es una frase más.

Cinco hooks de la misma pieza deben usar disparadores y ángulos distintos. Dos
hooks con el mismo disparador **y** el mismo ángulo son una variante falsa (BR-004).

## Tabla de disparadores

| ID | Disparador | Cuándo funciona | Cuándo falla |
|---|---|---|---|
| `curiosidad` | Hay una información retenida que el espectador necesita completar | El vacío de información es real y se resuelve en la pieza | Si el gancho promete algo que la pieza no entrega |
| `contradiccion` | Se contradice una creencia extendida de la audiencia | La creencia es realmente mayoritaria en ese nicho | Si la contradicción es falsa o exagerada |
| `perdida` | Se señala algo que la audiencia está perdiendo ahora mismo | La pérdida es concreta, actual y evitable | Si genera miedo sin ofrecer salida |
| `prueba_social` | Se muestra que otros como ellos ya lo resolvieron | El caso es verificable y comparable con la audiencia | Si el caso es irrepetible o inventado |
| `dato` | Una cifra concreta del negocio cambia la percepción | La cifra está respaldada por el contexto de marca (BR-005) | Si la cifra no está respaldada: es un fallo, no un hook |
| `pregunta` | Una pregunta que la audiencia no puede dejar sin responder | La pregunta es específica y la respuesta le afecta | Si es retórica o genérica ("¿quieres vender más?") |

## Detalle y ejemplos

### `curiosidad`

- **Definición:** se abre un vacío de información concreto, y la pieza lo cierra.
- **Anatomía:** se nombra una causa, una razón o un detalle sin revelarlo.
- **Ejemplo:** "Hay una razón por la que tus vídeos no pasan de 300 visitas, y no es
  el algoritmo."
- **Fallo típico:** prometer un secreto y no entregarlo. Es la forma más rápida de
  perder a la audiencia en el segundo 10.

### `contradiccion`

- **Definición:** se afirma lo contrario de lo que la audiencia da por sentado.
- **Anatomía:** creencia común + negación directa + alternativa insinuada.
- **Ejemplo:** "Publicar más no te va a traer más clientes. Publicar menos, mejor,
  sí."
- **Fallo típico:** contradecir algo que nadie cree. Si la audiencia no sostiene la
  creencia, no hay tensión.

### `perdida`

- **Definición:** se hace visible un coste que la audiencia ya está pagando sin
  saberlo.
- **Anatomía:** situación actual + lo que se está perdiendo + magnitud concreta.
- **Ejemplo:** "Cada semana que no mides el gancho, estás gastando horas en vídeos
  que nadie va a ver."
- **Fallo típico:** miedo sin salida. La capa de Acción debe ofrecer la salida.

### `prueba_social`

- **Definición:** se muestra un caso comparable al de la audiencia.
- **Anatomía:** sujeto reconocible + situación inicial parecida + resultado.
- **Ejemplo:** "Una marca como la tuya tardaba cuatro horas por guion. Ahora tarda
  quince minutos."
- **Fallo típico:** casos irrepetibles o no verificables. Si no está en el contexto
  de marca, no se escribe (BR-005).

### `dato`

- **Definición:** una cifra del negocio que reordena la percepción del problema.
- **Anatomía:** cifra + qué implica + consecuencia práctica.
- **Ejemplo:** "De cada diez guiones que escribimos a mano, siete no pasaban del
  segundo tres."
- **Fallo típico:** cifras redondas sin fuente. **Toda cifra debe estar en el
  contexto de marca.** Si no lo está, el checklist falla y la pieza no se aprueba.

### `pregunta`

- **Definición:** una pregunta específica cuya respuesta afecta directamente a quien
  la lee.
- **Anatomía:** situación concreta + pregunta que fuerza una respuesta interna.
- **Ejemplo:** "¿Cuándo fue la última vez que supiste por qué un vídeo funcionó?"
- **Fallo típico:** preguntas retóricas genéricas que la audiencia puede ignorar sin
  coste.

## Reparto recomendado por pieza

Con 5 hooks, un reparto variado evita la fatiga de plantilla (R-004):

- obligatorio: al menos **3 disparadores distintos** entre los 5 hooks;
- recomendado: cubrir `contradiccion` o `perdida` (tensión) además de `curiosidad`
  o `dato` (información);
- evitar: los 5 hooks concentrados en `pregunta`, que es el disparador más débil y
  el más fácil de escribir en serie.

## Cómo se comprueba

- Cada hook declara su disparador del vocabulario cerrado.
- El verificador comprueba que el disparador existe en este catálogo.
- El verificador detecta hooks con el mismo disparador y solapamiento alto de
  palabras (ángulo repetido) y los marca como variante falsa.
- Un hook cuyo disparador es `dato` y cuya cifra no aparece en el contexto de marca
  falla BR-005.
