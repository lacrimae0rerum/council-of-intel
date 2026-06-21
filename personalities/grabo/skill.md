# Skill

## Warning intelligence: detectar antes de que ocurra

### Técnica central: el warning como análisis bajo incertidumbre irreducible

El warning intelligence no es análisis convencional con menos evidencia. Es una disciplina analítica con sus propias reglas, porque opera bajo una restricción fundamental: si el analista espera tener suficiente evidencia para estar seguro, llega tarde. El warning exitoso trabaja con señales imperfectas, bajo alta incertidumbre, con el objetivo de dar tiempo al consumidor para preparar una respuesta.

La distinción clave que Grabo establece: **warning es distinto de predicción**. La predicción dice "esto ocurrirá". El warning dice "las señales actuales aumentan la probabilidad de que esto ocurra en una ventana de tiempo determinada, y hay que prepararse para ello ahora". No hay certeza; hay señal suficiente para actuar.

---

### Paso 1 — Establecer la línea base de comportamiento del actor

Antes de identificar indicadores de warning, hay que saber cuál es el comportamiento normal del actor. Sin línea base, cualquier desviación puede parecer un indicador; con línea base, las desviaciones significativas se distinguen del ruido.

La línea base incluye:
- Patrones de actividad habituales (frecuencia, volumen, horario).
- Postura habitual de las capacidades (cómo las mantiene, cómo las despliega).
- Patrones de comunicación habituales (con quién, cuándo, por qué canales).
- Comportamiento en situaciones similares en el pasado.

La desviación de la línea base es la señal; la línea base es el contexto que la hace significativa.

---

### Paso 2 — Distinguir capacidad de intención

La confusión entre capacidad e intención es uno de los errores más frecuentes en warning intelligence. Capacidad es lo que el actor puede hacer; intención es lo que está decidido a hacer ahora.

Un actor que tiene capacidad de ataque y que en el pasado ha usado esa capacidad no está actualmente preparando un ataque. La inferencia de intención requiere señales de cambio en el comportamiento, no solo de existencia de la capacidad.

Señales que indican cambio de intención (más allá de la capacidad existente):
- El actor está redistribuyendo capacidades de una postura defensiva a una postura ofensiva.
- El actor está adquiriendo capacidades específicas que solo tiene sentido en el contexto de un plan de ataque.
- El actor está contactando a otros actores con quienes no tenía relación previa.
- El actor está adoptando patrones de comportamiento que históricamente han precedido a ataques.

---

### Paso 3 — Construir el framework de indicadores

Un indicador de warning no es cualquier observable que se relaciona vagamente con un evento adverso. Tiene características específicas:

**Anticipatorio:** debe aparecer antes del evento, no durante ni después. Un indicador que aparece simultáneamente con el evento es un indicador de detección; sirve para confirmar que el evento está ocurriendo, no para advertir que está a punto de ocurrir.

**Específico:** debe distinguir la preparación del evento adverso de actividad habitual del actor. "Actividad de red inusual" no es un indicador específico. "Tráfico cifrado hacia servidores no usados previamente durante horas fuera del horario habitual del actor" es un indicador específico.

**Coleccionable:** debe poder observarse con fuentes disponibles o planificables. Un indicador que solo podría observarse con colección que no existe no es útil para warning.

**Discriminante:** debe poder distinguirse de actividad habitual o de actividad que tiene explicaciones alternativas plausibles.

---

### Paso 4 — Evaluar el patrón de indicadores

Los indicadores individuales raramente justifican un warning. El warning emerge del patrón: varios indicadores que convergen en la misma dirección tienen más peso que cualquiera de ellos solo.

Evaluación del patrón:
- ¿Cuántos indicadores están activos? (no todos tienen el mismo peso)
- ¿Los indicadores activos son de tipos distintos (preparatorios, posturales, relacionales, temporales) o son todos del mismo tipo?
- ¿Los indicadores activos se pueden explicar individualmente por razones alternativas, pero no todos juntos?
- ¿Hay indicadores que deberían estar presentes si el actor estuviera preparando el evento y no están? ¿Es eso evidencia negativa o laguna de colección?

---

### Paso 5 — Calibrar el umbral al coste asimétrico

El umbral de alerta no es el mismo para todos los eventos. Depende del coste relativo de los dos tipos de error:

**Para eventos de alta consecuencia y baja reversibilidad** (ataques cinéticos, exfiltración masiva de datos, compromiso de infraestructura crítica): el umbral debe ser bajo. Es preferible una alerta prematura que cause movilización innecesaria a una alerta tardía que deje al consumidor sin tiempo de respuesta.

**Para eventos de baja consecuencia y alta reversibilidad** (actividad de reconocimiento, movimiento lateral temprano): el umbral puede ser más alto. Un falso positivo frecuente en eventos de baja consecuencia desgasta la credibilidad del sistema de warning.

La regla general: el umbral de alerta debe ser inversamente proporcional al coste del falso negativo y directamente proporcional al coste del falso positivo.

---

### Aplicación en el dominio IC/CTI

**En análisis de amenaza técnica (C2, intrusión):**
El framework de Grabo distingue entre warning de acceso (¿hay un adversario dentro?) y warning de fase (¿en qué fase de la cadena de ataque está el adversario?). El warning de fase es más accionable: si el adversario está en fase de reconocimiento, hay tiempo; si está en fase de preparación de exfiltración, el tiempo es mucho más limitado.

Los indicadores anticipatorios en CTI se organizan por fase de la kill chain: reconocimiento → armamentización → entrega → explotación → persistencia → movimiento lateral → exfiltración. Warning temprano detecta señales de reconocimiento o armamentización; warning tardío detecta señales de persistencia o movimiento lateral.

**En inteligencia estratégica:**
El framework de Grabo distingue entre señales de capacidad (el actor aumenta sus capacidades militares o técnicas) y señales de intención (el actor cambia la postura de esas capacidades, el timing, los patrones de comunicación). El error clásico de warning estratégico es tratar las señales de capacidad como señales de intención.

**En warning de campaña APT:**
Los indicadores anticipatorios de una campaña APT incluyen: registro de infraestructura nueva con patrones similares a campañas anteriores (preparatorio), reconocimiento activo contra los tipos de objetivo esperados (preparatorio), actividad de compilación o adaptación de tooling (preparatorio). Los indicadores de ejecución (spear-phishing, entrega de malware) son demasiado tardíos para un warning efectivo.
