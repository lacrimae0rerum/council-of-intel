# Skill

## Key Assumptions Check (KAC)

### Técnica central: hacer explícito lo que el análisis da por cierto

Un análisis de inteligencia siempre descansa en supuestos. Los supuestos explícitos son los que el analista menciona; los implícitos son los que no. Los implícitos son el mayor riesgo: si el analista no los ve, nadie los prueba, y si son falsos, la conclusión falla sin que nadie sepa por qué.

La técnica KAC transforma los supuestos implícitos en objeto de análisis explícito. Al hacerlos visibles, permite evaluarlos, priorizarlos por fragilidad y monitorizar si se cumplen o fallan durante el ciclo de inteligencia.

---

### Paso 1 — Separar inferencias de hechos en el análisis

El primer movimiento del KAC es distinguir entre lo que el análisis presenta como hecho observado y lo que presenta como inferencia o conclusión. Las inferencias descansan en supuestos; los hechos, no.

Protocolo:
1. Lee el análisis párrafo por párrafo.
2. Para cada conclusión o inferencia, pregunta: "¿Qué tendría que ser cierto para que esta inferencia sea válida?"
3. La respuesta es el supuesto que sustenta esa inferencia.

Ejemplo:
- Inferencia: "El beaconing con intervalos exactos de 60s sugiere software controlado, no tráfico de usuario."
- Supuesto implícito: "El software legítimo de empresa no usa polling con intervalos exactos de 60s sin jitter."
- Evaluación: este supuesto es razonablemente sólido para la mayoría del software enterprise, pero es falsificable si el inventario de software incluye herramientas de monitorización con esa cadencia.

---

### Paso 2 — Aplicar la rúbrica de categorías de supuesto

Los supuestos en IC/CTI tienden a caer en categorías reconocibles. Revisar cada categoría ayuda a no perder supuestos implícitos:

**Categoría 1: supuestos sobre el actor**
- ¿Asume que el actor es racional y persigue objetivos identificables?
- ¿Asume que la motivación observada en el pasado sigue siendo válida?
- ¿Asume que el actor actúa solo y no en coordinación con otros?
- ¿Asume que el actor no ha detectado que está siendo monitorizados?

**Categoría 2: supuestos sobre la evidencia**
- ¿Asume que las fuentes son representativas del universo de actividad?
- ¿Asume que la ausencia de evidencia de X implica que X no ocurre?
- ¿Asume que los indicadores son exclusivos del actor atribuido?
- ¿Asume que los indicadores son recientes y el actor no ha evolucionado?

**Categoría 3: supuestos sobre el contexto**
- ¿Asume que el contexto geopolítico o operacional no ha cambiado?
- ¿Asume que las condiciones que explican el comportamiento pasado siguen presentes?
- ¿Asume que el targeting del actor refleja sus objetivos reales y no un señuelo?

**Categoría 4: supuestos sobre la colección**
- ¿Asume que lo que los sensores detectan es representativo de toda la actividad?
- ¿Asume que no hay canales de actividad no monitorizados?
- ¿Asume que la colección está funcionando correctamente (sin errores de logging, sin gaps de sensor)?

---

### Paso 3 — Evaluar fragilidad (probabilidad × impacto)

Para cada supuesto identificado, aplicar la rúbrica de fragilidad en dos pasos:

**3a — Probabilidad de ser falso:**
- Alta: hay evidencia o historial de que este tipo de supuesto falla frecuentemente.
- Media: el supuesto es razonable pero tiene excepciones conocidas en este dominio.
- Baja: el supuesto es casi universalmente válido en contextos similares.

**3b — Impacto si falla:**
- La conclusión cambia completamente → impacto alto.
- La conclusión se modifica pero se sostiene → impacto medio.
- La conclusión requiere solo ajuste menor → impacto bajo.

La fragilidad final es:
- **Alta**: probabilidad media-alta O impacto alto (y probabilidad al menos baja).
- **Media**: probabilidad baja-media Y impacto medio.
- **Baja**: probabilidad baja Y impacto bajo.

Criterio conservador: cuando hay incertidumbre sobre la probabilidad, asignar el nivel superior. Es mejor sobreidentificar supuestos frágiles que subidentificarlos.

---

### Paso 4 — Construir señales de ruptura observacionales

Una señal de ruptura es un observable que, si se detecta, indica que el supuesto ha fallado. No es una hipótesis alternativa; es un evento específico monitorizable.

Criterios de calidad de una señal de ruptura:
- **Específica:** "aparecen TTPs distintos a los del cluster documentado" es vago. "El dominio de C2 cambia a un registrador diferente y la infraestructura migra a un AS no previamente asociado al actor" es específico.
- **Temporal:** debe ser detectable dentro del horizonte temporal del análisis, no en un plazo indefinido.
- **Accionable:** debe poder ser monitorizada con alguna fuente de colección existente o planificable.

Si no es posible formular una señal de ruptura específica para un supuesto, eso en sí mismo es información analítica: el supuesto no es falsificable con la colección disponible, lo que limita la confianza independientemente de su fragilidad.

---

### Paso 5 — Seleccionar los supuestos relevantes

El KAC no es un ejercicio de listing exhaustivo. Su valor está en discriminar. Selecciona entre 3 y 6 supuestos según estos criterios:

1. Prioriza los de fragilidad alta sobre los de fragilidad media.
2. Prioriza los que afectan directamente a la conclusión principal sobre los que afectan a inferencias subsidiarias.
3. Descarta los supuestos que, aunque sean supuestos, tienen impacto mínimo si fallan.

Si identificas más de 6 supuestos relevantes, es señal de que el análisis tiene una carga epistémica muy alta y la confianza debería ser baja independientemente del razonamiento.

---

### Aplicación en el dominio IC/CTI

**En análisis de amenaza con beaconing:**
El supuesto de representatividad de la colección es casi siempre relevante. Si el beacon no aparece en el SIEM, el supuesto "la ausencia implica evasión" debe competir con "la ausencia implica fallo de logging". La señal de ruptura para el segundo supuesto es clara: revisar si el mismo VLAN o host tiene otros eventos en el SIEM en el mismo período.

**En atribución:**
Los supuestos más frágiles casi siempre son:
1. Que los TTPs son exclusivos o altamente característicos del actor atribuido.
2. Que la motivación contextual es coherente con el targeting observado.
Ambos son los que con más frecuencia no se declaran y los que más frecuentemente se cumplen porque se construye la narrativa alrededor de ellos.

**En warning intelligence:**
El supuesto más frágil casi siempre es el de estabilidad temporal: que las condiciones que motivaban al actor siguen vigentes. En warning, la pregunta "¿qué ha cambiado desde la última evaluación?" es exactamente una búsqueda de ruptura de este supuesto.
