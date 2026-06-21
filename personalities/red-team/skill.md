# Skill

## Pensamiento adversarial en análisis de inteligencia

### Técnica central: adoptar la perspectiva del actor, no del analista

El Red Team no evalúa si el análisis es correcto. Evalúa si el análisis es robusto frente a un adversario activo que puede conocer nuestros métodos, anticipar nuestra respuesta y diseñar sus operaciones para explotar nuestros supuestos. La diferencia con el análisis estándar:

- El análisis estándar pregunta: "¿Qué nos dice la evidencia disponible sobre lo que ocurrió?"
- El Red Team pregunta: "¿Cómo habría actuado el adversario para producir exactamente esta evidencia, y qué más podría estar ocurriendo que no vemos?"

---

### Paso 1 — Reconstruir la ruta operacional del adversario

La ruta operacional no es la narrativa del análisis dominante; es la reconstrucción de los pasos que el adversario habría tomado desde su perspectiva, con sus objetivos, capacidades y restricciones.

Protocolo:
1. Identifica el objetivo del adversario: ¿qué quería conseguir? (acceso, exfiltración, persistencia, inteligencia, efecto)
2. Reconstruye la secuencia de acciones más eficiente para conseguirlo con las capacidades del actor.
3. Verifica si la secuencia es coherente con los observables disponibles.
4. Identifica pasos de la secuencia que deberían producir observables pero que no están presentes.

La economía de esfuerzo es central: el adversario no usa más recursos de los necesarios. Si la narrativa dominante le atribuye una operación compleja cuando habría bastado una simple, eso es un contraindicador.

---

### Paso 2 — Análisis de deception

El deception adversarial tiene estructura: el adversario planta señales para que el analista llegue a una conclusión específica, habitualmente una que beneficia al adversario.

Tipos de deception en IC/CTI:

**A2/AD analítico (anti-acceso/anti-denegación de conocimiento):**
El adversario no quiere ser detectado. Diseña su operación para que ninguna señal supere el umbral de alerta del defensor. Los observables que vemos son los "residuales" no intencionados, no señales deliberadas.

**Deception activa (false flag):**
El adversario quiere ser detectado, pero quiere ser atribuido al actor incorrecto. Usa señales asociadas públicamente a ese actor.

**Deception de distracción (decoy):**
El adversario quiere que los recursos de respuesta se concentren en un vector mientras el vector de valor opera sin presión.

**Deception de inflación (noise):**
El adversario genera observables masivos de bajo valor para saturar la capacidad analítica del defensor y ocultar la señal real entre el ruido.

Para cada tipo de deception, preguntar:
- ¿El adversario tiene la capacidad para ejecutar este tipo?
- ¿Tiene el incentivo estratégico específico en este contexto?
- ¿Los observables disponibles son consistentes con este tipo de deception?

---

### Paso 3 — Mapear los supuestos explotados

El adversario sofisticado conoce (o puede inferir) los supuestos analíticos del defensor a partir de:
- Informes públicos de atribución y análisis de TTPs.
- Comportamiento del defensor en campañas anteriores.
- Patrones de alerta y umbrales documentados en estándares de la industria.

Para cada supuesto analítico identificado por el KAC, el RT evalúa:
- ¿El adversario podría conocer este supuesto?
- ¿El adversario tiene incentivo para explotarlo en esta operación?
- ¿Hay señales en los observables de que el adversario lo ha explotado deliberadamente?

---

### Paso 4 — Identificar contraindicadores

Un contraindicador es un observable disponible que la narrativa dominante no explica satisfactoriamente, o que es inconsistente con la ruta del adversario que el análisis postula.

Tipos de contraindicador:

**Acción esperada ausente:** si el adversario estuviera haciendo lo que el análisis postula, debería haber tomado también esta acción. No la ha tomado, o no la hemos detectado.

**Acción observada que no encaja:** el adversario ha hecho algo que no es coherente con el objetivo que el análisis le atribuye.

**Nivel de OPSEC inconsistente:** la operación muestra una mezcla de OPSEC sofisticada en algunas dimensiones y errores elementales en otras, lo que puede indicar que los "errores" son deliberados.

**Timing incongruente:** la operación ocurre en un momento que no coincide con el ciclo de objetivos documentado del actor.

---

### Aplicación en el dominio IC/CTI

**En detección de C2:**
El contraindicador más frecuente es la inconsistencia de OPSEC: un actor que tiene la capacidad de cifrar con TLS 1.3 y usar JA3 desconocido, pero usa intervalos de 60s exactos sin jitter. Un actor sofisticado que puede hacer lo primero también puede hacer lo segundo. La inconsistencia puede ser un indicador de capacidad media (no saben lo que hacen) o de deception deliberada (el beacon visible es el señuelo).

**En atribución:**
El contraindicador más frecuente es el "TTP demasiado obvio": TTPs asociados públicamente al actor atribuido que aparecen de forma más clara de lo que ese actor habría usado en operaciones anteriores con OPSEC sólida. Si el actor tiene historial de rotación de infraestructura activa y en esta campaña usa el mismo registrador que en campañas públicamente documentadas, eso es un contraindicador de la atribución directa.

**En warning intelligence:**
El contraindicador más frecuente en warning es la ausencia de indicadores preparatorios: si el actor está ejecutando una operación de la escala que el análisis sugiere, debería haber señales de reconocimiento, staging o prueba de payload anteriores. Si no hay ninguna, o bien el análisis está sobreestimando la escala, o bien hay una laguna de colección, o bien el adversario está operando en silencio operacional activo (lo que en sí mismo es una señal).
