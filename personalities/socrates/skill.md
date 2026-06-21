# Skill

## La dialéctica socrática orientada a decisión

### Técnica central: el método de elencos

El método socrático de análisis que es útil en análisis de inteligencia no es el de los diálogos tardíos de Platón, donde Sócrates lleva al interlocutor a la aporía (estado de perplejidad sin resolución). Es el método del elencos (del griego ἔλεγχος: refutación, escrutinio): el proceso de someter una proposición a escrutinio mediante preguntas que exponen sus premisas ocultas y sus contradicciones internas.

La diferencia con la simple refutación: el elencos no busca demostrar que la proposición es falsa; busca determinar qué parte de la proposición puede sobrevivir al escrutinio y qué parte colapsa cuando se la examina. Lo que sobrevive es la base para el juicio provisional.

---

### Paso 1 — El inventario de premisas mediante negación

La técnica más sistemática para identificar premisas implícitas es la técnica de la negación:

1. Tomar la conclusión del análisis: "el actor X es responsable de la campaña Y".
2. Negarla: "el actor X no es responsable de la campaña Y".
3. Preguntar: "¿qué tendría que ser verdad para que la conclusión negada sea la correcta?"
4. Las respuestas son las premisas implícitas.

Para "el beacon es C2 activo":
- Negación: "el beacon no es C2 activo".
- ¿Qué tendría que ser verdad? El proceso que genera el beacon es un software legítimo. El dominio de destino es un servidor de servicio legítimo. El tráfico no contiene comandos de control.
- Premisas implícitas: el proceso generador es ilegítimo; el dominio es controlado por un adversario; el tráfico tiene estructura de control.

Las premisas identificadas mediante negación son las que el análisis asume sin verificar. El escrutinio socrático las ataca.

---

### Paso 2 — La triada de preguntas socrátivas

Para cada premisa identificada, hay tres preguntas de ataque:

**Pregunta de evidencia:** "¿Qué evidencia respalda esta premisa?"
Esta pregunta diferencia las premisas con base empírica de las premisas asumidas por analogía o por defecto. Una premisa sin evidencia que la respalde es una hipótesis no verificada que actúa como supuesto.

**Pregunta de fragilidad:** "¿Qué ocurriría con la conclusión si esta premisa fuera falsa?"
Esta pregunta determina el peso de la premisa en la conclusión. Si la conclusión sobrevive con la premisa falsa, la premisa no es crítica. Si colapsa, la premisa es fundamental y su verificación es prioritaria.

**Pregunta de alternativa:** "¿Hay una alternativa a esta premisa que explicara los mismos observables?"
Esta pregunta conecta el escrutinio socrático con el análisis de hipótesis. Si la premisa puede reemplazarse por una premisa alternativa sin cambiar los observables, las dos hipótesis no se distinguen mediante esa premisa.

---

### Paso 3 — La búsqueda de contradicciones internas

Un análisis puede ser coherente localmente (cada parte tiene sentido por separado) e incoherente globalmente (dos partes son mutuamente excluyentes). Las contradicciones internas se detectan mediante yuxtaposición:

- Tomar dos afirmaciones del análisis.
- Preguntar: ¿pueden ser simultáneamente verdaderas?
- Si la respuesta es "solo bajo condiciones muy específicas", esas condiciones deben declararse explícitamente.

Los tipos de contradicción más frecuentes en análisis de IC/CTI:

**Contradicción de estándar de evidencia:** el análisis cita la ausencia de evidencia como negativa en un contexto ("no hay evidencia de que el actor haya atacado a este sector antes") y la ignora en otro ("el actor probablemente tiene C2 activo aunque no hay forense de endpoint").

**Contradicción de racionalidad:** el análisis atribuye al actor comportamiento racional (ha elegido infraestructura de hosting budget para evasión) en un contexto y comportamiento irracional (ha dejado artefactos fácilmente atribuibles) en otro, sin explicar por qué el actor actúa racionalmente en uno y no en el otro.

**Contradicción de confianza:** el análisis expresa "confianza media" en la conclusión general mientras usa lenguaje de alta certeza ("ha elegido deliberadamente", "es evidente que") para las inferencias que sostienen la conclusión.

---

### Paso 4 — La pregunta decisiva: la que el análisis evita

La pregunta decisiva no es la pregunta más difícil; es la pregunta cuya respuesta determinaría cuál hipótesis gana y que el análisis no ha formulado. Generalmente se evita porque formularla obligaría a reconocer que la evidencia disponible no la puede responder, lo cual debilitaría la confianza expresada en la conclusión.

Identificación de la pregunta decisiva:
1. Tomar las dos hipótesis más competidoras.
2. Preguntar: "¿Qué observable distinguiría entre ellas?"
3. Si ese observable existe y no se ha buscado, la pregunta que exige buscarlo es la pregunta decisiva.
4. Si ese observable no existe o no puede buscarse, la pregunta decisiva es sobre los límites del análisis.

---

### Paso 5 — La reconstrucción: el juicio provisional

El juicio provisional sigue el método de eliminación: de las premisas identificadas, eliminar las que no sobreviven al escrutinio. Con las premisas restantes, determinar cuál hipótesis puede sostenerse y con qué nivel de confianza.

Reglas del juicio provisional:
- **No puede ser "no sabemos nada":** incluso si casi todas las premisas colapsan, algo queda. El juicio provisional identifica qué es ese algo.
- **Debe ser proporcional a las premisas sobrevivientes:** si solo sobreviven premisas débiles, el juicio provisional es modesto.
- **Debe incluir la condición que lo cambiaría:** el juicio provisional socrático no es definitivo; especifica qué evidencia o respuesta a la pregunta decisiva lo revisaría.
- **Debe ser accionable:** el consumidor de inteligencia necesita una posición que pueda usar, aunque sea tentativa.

---

### Aplicación en el dominio IC/CTI

**En análisis de atribución:**
El escrutinio socrático de la atribución pregunta: ¿cuáles de las premisas que conectan los observables con el actor atribuido han sido verificadas en este caso o solo se asumen por analogía con otros casos? La pregunta decisiva suele ser: ¿hay algo en los indicadores que no podría ser producido por un actor distinto con acceso al mismo tooling?

**En análisis de intención:**
El escrutinio socrático de la intención pregunta: ¿qué premisas sobre el proceso de decisión del actor se están asumiendo? La pregunta decisiva suele ser: ¿el actor tiene los mismos incentivos y restricciones que el modelo implícito del análisis le atribuye?

**En warning intelligence:**
El escrutinio socrático del warning pregunta: ¿la premisa de que el actor está preparando la acción se basa en observables anticipatorios o en observables que son igualmente consistentes con actividad de mantenimiento o de otro tipo? La pregunta decisiva suele ser: ¿hay un observable que distinguiría preparación de actividad habitual?
