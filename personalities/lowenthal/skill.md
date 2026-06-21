# Skill

## Evaluación de utilidad para el consumidor de inteligencia

### Técnica central: la prueba de la decisión

Mark Lowenthal define la prueba de calidad de un producto de inteligencia no por su rigor analítico sino por su impacto en la decisión del consumidor: ¿puede el policymaker tomar una decisión distinta con este análisis que sin él? Si la respuesta es no, el análisis ha fallado en su propósito operativo aunque sea analíticamente impecable.

Esta prueba tiene dos dimensiones:

1. **Pertinencia:** ¿el análisis responde la pregunta que el consumidor necesita responder para su decisión?
2. **Calibración al umbral:** ¿la incertidumbre expresada en el análisis es relevante para el umbral de decisión del consumidor?

Un análisis que es pertinente pero mal calibrado al umbral puede ser técnicamente correcto y operativamente inútil. "Posible (30–45%)" no ayuda a un consumidor cuyo umbral de acción es "probable (>60%)"; solo le confirma que la evidencia es insuficiente para actuar.

---

### Paso 1 — Identificar el consumidor y la decisión

El primer paso de la evaluación de utilidad es siempre específico: ¿quién recibe este análisis y qué tiene que decidir?

Los perfiles de consumidor más frecuentes en IC/CTI:
- **Equipo de SOC / analista técnico:** necesita decidir si escalar un evento, si aislarlo o si seguir monitorizando. Umbral de decisión: bajo-medio (actúan ante señales débiles porque el coste de falso positivo es manejable).
- **CISO / director de seguridad:** necesita decidir si activar protocolos de respuesta a incidente, si invertir en mitigación, si comunicar a la dirección. Umbral de decisión: medio-alto (el coste de respuesta es más alto, el coste de inacción también puede serlo).
- **Comité de dirección / stakeholder ejecutivo:** necesita decidir si cambiar postura de riesgo, si comunicar públicamente, si activar planes de continuidad. Umbral de decisión: alto (necesita claridad sobre qué es probable y qué es especulativo).
- **Director de inteligencia / policymaker nacional:** necesita decidir si recomendar medidas preventivas, si escalar diplomáticamente, si activar capacidades defensivas. Umbral de decisión: alto, con sensibilidad política significativa.

---

### Paso 2 — Mapear qué parte del análisis es accionable

Para cada conclusión del análisis, preguntar:

- ¿Esta conclusión le dice al consumidor algo que no sabía ya?
- ¿Le permite tomar una decisión que de otro modo no podría tomar?
- ¿Mueve el umbral de decisión del consumidor en alguna dirección?

Las conclusiones que no pasan este test son de bajo valor de utilidad aunque sean correctas. La información confirmativa (que confirma lo que el consumidor ya sabe) tiene valor de confianza pero no de acción.

---

### Paso 3 — Evaluar la calibración al umbral de decisión

El umbral de decisión del consumidor es el punto de probabilidad en el que cambia de "no actuar" a "actuar". Si el análisis concluye que una hipótesis es "posible (30–45%)" y el umbral del consumidor es 60%, el análisis le dice que no ha llegado al umbral, lo cual puede ser útil (evita una acción prematura) o puede ser frustrante (el consumidor necesita saber cuándo llegará al umbral).

Las preguntas de calibración:
- ¿La estimación de probabilidad está expresada en un rango que es relevante para el umbral del consumidor?
- ¿El análisis dice cuándo la estimación podría cambiar y en qué dirección?
- ¿La confianza en la estimación está separada de la probabilidad? (Alta confianza en "posible" es muy distinta de baja confianza en "posible")

---

### Paso 4 — Detectar señales de contaminación política

La contaminación política es el proceso por el que el análisis se acomoda a la posición del consumidor, consciente o inconscientemente. Lowenthal identificó los mecanismos principales:

**Presión directa:** el consumidor expresa expectativas sobre el resultado del análisis antes de que el análisis esté completo. Los analistas ajustan inconscientemente sus conclusiones.

**Retroalimentación selectiva:** el consumidor solo responde positivamente cuando el análisis confirma su posición. Los analistas aprenden qué tipo de análisis recibe aprobación.

**Estiramiento analítico:** el analista estira la interpretación de evidencia ambigua en la dirección que el consumidor preferiría. La evidencia no cambia; solo cambia la interpretación.

**Suavización del dissent:** los analistas con posiciones disidentes se autocensuran para evitar conflicto. El producto final refleja una convergencia artificial.

Señales observables en el análisis:
- Las conclusiones coinciden exactamente con la posición pública del consumidor.
- La evidencia contraria se menciona pero con calificadores que minimizan su impacto.
- Los calificadores de incertidumbre son más fuertes en la dirección que el consumidor no prefiere.
- No hay dissent registrado en ninguna parte del análisis.

---

### Paso 5 — Formular preguntas de inteligencia para el consumidor

Las preguntas de inteligencia que el análisis no responde pero que el consumidor necesita deben ser formuladas con tres características:

1. **Específicas a la decisión:** no preguntas de inteligencia abstractas, sino preguntas directamente vinculadas a la decisión que el consumidor tiene que tomar.
2. **Coleccionables:** preguntas que pueden responderse con fuentes reales, no preguntas que solo podrían responderse con acceso perfecto al objetivo.
3. **Priorizadas:** las preguntas más importantes para la decisión primero, no ordenadas por facilidad de respuesta.

---

### Aplicación en el dominio IC/CTI

**En análisis técnico de amenazas (C2, malware):**
La evaluación de utilidad pregunta: ¿necesita el SOC aislar el host ahora o puede esperar más evidencia? La respuesta depende de la probabilidad de C2 activo vs. el coste de aislar un host (interrupción de servicio, falso positivo). El análisis debe calibrarse a ese balance, no solo a la probabilidad absoluta.

**En atribución:**
La evaluación de utilidad pregunta: ¿necesita el consumidor saber quién es el actor para la decisión que tiene que tomar? En muchos casos de respuesta a incidente, la identidad del actor no cambia la respuesta táctica (contener, remediar, recuperar) aunque pueda ser relevante para la respuesta estratégica (diplomacia, sanciones, retorsión). El análisis de atribución tiene diferentes consumidores con diferentes necesidades de decisión.

**En warning intelligence:**
La evaluación de utilidad incluye siempre el análisis del coste asimétrico de error: ¿cuánto peor es un falso negativo (no escalar cuando debería) que un falso positivo (escalar cuando no debería)? En warning intelligence, los falsos negativos suelen ser más costosos, lo que puede justificar umbrales de acción más bajos que en otros tipos de inteligencia.
