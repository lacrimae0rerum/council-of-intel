# Skill

## Técnica de abogado del diablo en análisis de inteligencia

### Técnica central: construir el mejor caso contrario, no el fácil de rebatir

El error más frecuente en el rol de Devil's Advocate es construir una versión débil de la hipótesis minoritaria para que parezca que ha tenido audiencia antes de ser descartada. Esta es la variante más dañina del pensamiento de grupo: el dissenso aparente que en realidad refuerza el consenso.

La técnica correcta exige construir el caso más sólido posible para la hipótesis minoritaria: identificar la evidencia que la favorece, reinterpretar la evidencia que parece favorecer a la hipótesis dominante, y articular el argumento más convincente para que la hipótesis minoritaria sea tomada en serio.

---

### Paso 1 — Identificar qué hipótesis necesita defensa

No todas las hipótesis alternativas necesitan un Devil's Advocate. La técnica es útil cuando:

- La hipótesis dominante tiene apoyo generalizado sin haber sido sometida a un test de refutación serio.
- Hay una hipótesis alternativa plausible que el consejo ha descartado rápidamente o por consenso.
- La evidencia disponible es ambigua y podría interpretarse de dos formas igualmente consistentes.
- La hipótesis dominante requiere que múltiples supuestos favorables sean simultáneamente ciertos.

No es útil cuando:
- La hipótesis alternativa ha sido descartada por evidencia específica (no por consenso).
- La hipótesis alternativa requiere asumir cosas no respaldadas por ninguna evidencia disponible.

---

### Paso 2 — Reinterpretar la evidencia desde la perspectiva de la hipótesis minoritaria

El Devil's Advocate no inventa evidencia nueva. Trabaja con la misma evidencia que el consejo, pero la interpreta desde la perspectiva de la hipótesis minoritaria.

Para cada ítem de evidencia que el consejo usa para respaldar la hipótesis dominante, el DA pregunta:
- ¿Es esta evidencia inconsistente con la hipótesis minoritaria, o solo "consistente con" la hipótesis dominante?
- ¿Existe una interpretación de esta evidencia que sea consistente con la hipótesis minoritaria?
- ¿Qué supuesto se necesita para que esta evidencia sea inconsistente con la hipótesis minoritaria?

Si la evidencia es solo "consistente con" la hipótesis dominante y no descarta activamente la hipótesis minoritaria, el consejo no ha usado esa evidencia para descartar la alternativa: la ha usado para respaldar su preferencia.

---

### Paso 3 — Construir la narrativa más coherente para la hipótesis minoritaria

Una hipótesis analítica no es solo una lista de evidencia a favor. Es una narrativa que explica todos los observables disponibles de forma coherente. El DA construye esa narrativa:

- ¿Cómo explicaría la hipótesis minoritaria los observables más importantes?
- ¿Qué observables predice la hipótesis minoritaria que aún no se han buscado?
- ¿Cuál es la secuencia de eventos que la hipótesis minoritaria postula?

Si la narrativa de la hipótesis minoritaria es más parsimoniosa que la dominante (requiere menos supuestos para explicar los mismos observables), es una señal seria de que la hipótesis minoritaria debería ser considerada con más peso.

---

### Paso 4 — Identificar las condiciones de victoria de la hipótesis minoritaria

Las condiciones de victoria no son "si aparece más evidencia a favor". Son las condiciones específicas bajo las cuales la hipótesis minoritaria explicaría mejor la situación que la hipótesis dominante:

- ¿Qué premisa de la hipótesis dominante debería resultar falsa?
- ¿Qué observable debería aparecer o no aparecer para que la hipótesis minoritaria sea la más parsimoniosa?
- ¿Cuándo dejaría de ser posible que la hipótesis dominante sea correcta sin que la minoritaria sea la alternativa?

---

### Paso 5 — Diseñar los tests que matarían la hipótesis minoritaria

El test no es "buscar más evidencia de la hipótesis dominante". El test es una observación específica que la hipótesis minoritaria predice que NO debería existir, pero que aparecería si la hipótesis dominante es correcta.

Criterios de un buen test discriminante:
- La hipótesis dominante predice que el observable existe.
- La hipótesis minoritaria predice que el observable no existe, o que solo existiría bajo condiciones específicas que también pueden verificarse.
- Si el observable aparece → hipótesis minoritaria descartada.
- Si el observable no aparece → hipótesis dominante debilitada.

El DA formula los tests porque son la única forma de que el debate entre hipótesis se resuelva por evidencia en vez de por preferencia o consenso.

---

### Aplicación en el dominio IC/CTI

**En análisis de C2 vs. shadow IT:**
El test más discriminante casi siempre es la identificación del proceso. Shadow IT predice un proceso firmado por un vendor conocido; C2 predice un proceso sin firma, inyectado, o que ejecuta desde una ruta inusual. Si el forense de endpoint puede realizar ese test, el debate se resuelve en horas. El DA empuja para que ese test se realice antes de que se adopte la hipótesis C2 como definitiva.

**En análisis de atribución:**
El test más discriminante es la presencia de artefactos exclusivos del actor (malware propio, configuración única) o de evidencia HUMINT/SIGINT que no puede ser replicada por un actor que pretende imitar. El DA empuja para que esos tests se formulen y se busquen antes de adoptar la atribución como definitiva.

**En warning intelligence:**
El DA defiende la hipótesis de que la señal de warning es un artefacto, un error de colección o una operación de engaño activo. Los tests que matarían esa hipótesis son los indicadores de segunda y tercera clase que son más difíciles de falsificar: comportamental, timing correlacionado con un evento específico, victimología consistente con historial del actor.
