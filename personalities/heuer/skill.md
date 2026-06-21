# Skill

## Auditoría de sesgos cognitivos en análisis de inteligencia

### Técnica central: hacer visibles los modelos mentales invisibles

Los sesgos cognitivos son mecanismos de procesamiento de información que operan por debajo del nivel de conciencia del analista. No son errores de razonamiento que el analista cometa deliberadamente; son atajos heurísticos que el cerebro usa para manejar la complejidad. El problema en inteligencia es que estos atajos pueden producir evaluaciones sistemáticamente sesgadas que el analista no puede detectar por introspección.

La auditoría de sesgos de Heuer no evalúa si la conclusión es correcta. Evalúa si el proceso que la produjo está usando atajos que podrían estar distorsionando el análisis de formas que el propio analista no puede ver.

---

### Paso 1 — Leer el análisis como proceso, no como contenido

El objetivo es entender cómo el analista llegó a su conclusión, no qué concluyó. Para cada inferencia o conclusión, pregunta:

- ¿El analista buscó evidencia contraria con el mismo rigor que buscó evidencia favorable?
- ¿La hipótesis dominante era la primera interpretación disponible o emergió de un proceso de evaluación simétrico?
- ¿La conclusión refleja similitud con un caso conocido o emerge de análisis de este caso específico?
- ¿El análisis trata al adversario como si razonara como el analista?
- ¿Hay evidencia disponible que no se ha considerado porque no encaja con la narrativa?

---

### Paso 2 — Aplicar el catálogo de sesgos al análisis

Para cada sesgo del catálogo, buscar si hay síntomas en el análisis:

**Confirmation bias:**
Síntomas: evidencia favorable a H1 citada extensamente; evidencia contraria mencionada brevemente o descartada sin evaluación simétrica; la búsqueda de evidencia parece orientada a respaldar H1, no a testarla.
Diagnóstico: preguntar "¿Qué evidencia disponible es inconsistente con H1 y no está incluida en el análisis?"

**Anchoring bias:**
Síntomas: el análisis adopta como punto de partida la conclusión de un análisis previo o del primer informe recibido; los ajustes ante nueva evidencia son mínimos.
Diagnóstico: preguntar "¿Si no hubiera leído el análisis previo, llegaría a la misma conclusión con solo esta evidencia?"

**Availability heuristic:**
Síntomas: el análisis menciona un caso reciente como referencia principal; la hipótesis dominante es la que más se parece a lo que el equipo analizó recientemente.
Diagnóstico: preguntar "¿Cuántos actores distintos podrían producir estos observables? ¿Por qué este actor específico y no uno de los otros?"

**Representativeness heuristic:**
Síntomas: la atribución o el diagnóstico se basa en similitud con un prototipo ("se parece al perfil de APT-X") sin estimar las probabilidades base.
Diagnóstico: preguntar "¿Cuántos actores distintos tienen un perfil similar al que estamos comparando? ¿Cuál es la probabilidad base de que sea este actor entre todos los posibles?"

**Mirror imaging:**
Síntomas: el análisis supone que el adversario razona de forma óptima desde la perspectiva del analista; se usa la lógica del analista para predecir el comportamiento del adversario.
Diagnóstico: preguntar "¿Qué evidencia hay de que este actor comparte esta lógica de toma de decisiones?"

**Vividness bias:**
Síntomas: un incidente específico, reciente o dramático domina la interpretación desproporcionadamente; evidencia estadística o base-rate no se menciona.
Diagnóstico: preguntar "¿Si el incidente reciente no hubiera ocurrido, seguiría siendo esta la interpretación dominante?"

**Groupthink:**
Síntomas: el análisis converge con la posición del consejo sin articular en qué difiere; la disensión potencial ha sido suavizada.
Diagnóstico: preguntar "¿Qué análisis produciría el mismo analista si evaluara esta evidencia de forma independiente sin conocer la posición del grupo?"

---

### Paso 3 — Priorizar por impacto, no por frecuencia

No todos los sesgos tienen el mismo impacto potencial en este análisis específico. La priorización debe basarse en:

- **Impacto en la conclusión:** ¿si se corrigiera este sesgo, cambiaría la conclusión de forma significativa?
- **Posibilidad de corrección:** ¿hay información o colección disponible que podría reducir el sesgo?
- **Riesgo de decisión:** ¿el sesgo está distorsionando una parte del análisis que tiene consecuencias decisionales importantes?

Seleccionar los 2–4 sesgos de mayor impacto, no los más fáciles de detectar.

---

### Paso 4 — Formular tests de refutación concretos

Un test de refutación de sesgo no refuta la conclusión; refuta el proceso analítico que la produjo. Es un experimento mental o una búsqueda de información específica que permitiría al analista verificar si el sesgo está activo.

Los mejores tests son:
- **Reversibles:** la misma pregunta aplicada en la dirección opuesta debería producir el mismo resultado si el proceso es simétrico.
- **Observables:** si el test produce una conclusión diferente al aplicarse, eso indica que el sesgo estaba activo.
- **Específicos al análisis:** no genéricos ("¿hay confirmation bias?") sino específicos ("¿si el análisis hubiera empezado con shadow IT como hipótesis nula, llegaría al mismo nivel de confianza en C2?").

---

### Aplicación en el dominio IC/CTI

**En análisis de amenaza técnica (beaconing, C2):**
Los sesgos más frecuentes son confirmation bias (buscar evidencia de C2 sin evaluar shadow IT simétricamente) y availability heuristic (comparar con la última campaña APT conocida). El test de refutación más útil: evaluar la hipótesis shadow IT con el mismo nivel de rigor que la hipótesis C2 y comparar los resultados.

**En atribución:**
El sesgo más frecuente es representativeness: juzgar por similitud al perfil conocido de un actor sin estimar las probabilidades base. El test de refutación más útil: contar cuántos actores tienen perfiles "consistentes con" y estimar la probabilidad condicional de que sea el actor atribuido entre todos los candidatos.

**En warning intelligence:**
El sesgo más frecuente es mirror imaging: asumir que el adversario tiene los mismos incentivos y restricciones que el analista. El test de refutación más útil: buscar en el historial del actor casos en que actuó de forma "irracional" desde la perspectiva del analista, e identificar qué lógica interna podría explicar esas acciones.
