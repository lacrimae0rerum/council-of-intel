# Knowledge

## Doctrina ACH del analista

### Origen: Richards Heuer y la psicología del análisis de inteligencia

El ACH fue desarrollado por Richards Heuer Jr. en la CIA y formalizado en "Psychology of Intelligence Analysis" (1999). El punto de partida de Heuer es que el cerebro humano no está construido para hacer lo que el ACH exige: buscar evidencia que refute nuestras hipótesis en vez de evidencia que las confirme. El confirmation bias no es un error de lógica; es la forma en que el cerebro reduce el esfuerzo cognitivo. El ACH es un andamiaje externo para superar esa tendencia.

El analista ACH no tiene posición natural. Su trabajo es el proceso, no la conclusión.

---

### Principio 1: la abundancia de evidencia consistente no confirma

Esta es la confusión más frecuente en analistas sin entrenamiento ACH formal. Si tengo diez ítems de evidencia consistentes con mi hipótesis favorita, eso no la hace más probable. Significa que la hipótesis no ha sido refutada por esos diez ítems — nada más. Una hipótesis falsa puede ser consistente con cualquier cantidad de evidencia si está formulada con suficiente vaguedad.

Lo que confirma — en la medida en que el ACH confirma algo — es la ausencia de inconsistencias ante evidencia que debería ser inconsistente si la hipótesis fuera falsa.

---

### Principio 2: la inconsistencia es el único mecanismo de eliminación

Cuando una hipótesis acumula una "I" frente a evidencia de alta calidad, esa hipótesis queda eliminada o seriamente debilitada. No hay un equivalente positivo: ninguna cantidad de "C" compensa una "I" sólida. Este principio viene de la lógica de la falsación (Popper): no puedes verificar una hipótesis universalmente, pero sí puedes refutarla con un solo contraejemplo de peso suficiente.

En términos operativos: buscar la refutación antes que la confirmación.

---

### Principio 3: la evidencia ausente es evidencia

Si una hipótesis predice que cierta evidencia debería existir, y esa evidencia no está disponible, su ausencia es información analítica. La hipótesis que requiere que algo exista y no lo encontramos acumula una "I" por ausencia.

Ejemplo en CTI: si una hipótesis de C2 activo predice que el proceso malicioso debe aparecer en la lista de procesos activos o en los logs de arranque, y no aparece ninguno, esa ausencia es un "I" para la hipótesis de C2 con persistencia (aunque no elimina C2 sin persistencia).

---

### Principio 4: el deception es siempre una hipótesis legítima

En análisis de inteligencia sobre actores con capacidades de engaño (actores estatales, actores con OPSEC sofisticada), la hipótesis "el adversario está construyendo deliberadamente este cuadro para que lleguemos a la conclusión que ellos quieren" no es paranoica: es metodológicamente obligatoria.

Omitir la hipótesis de deception no significa que sea improbable; significa que el analista no la está evaluando. La operación Fortitude (WWII), el uso de testaferros por actores estatales, y las operaciones de false flag modernas son evidencia de que el deception es una herramienta real y frecuente.

---

### Principio 5: hipótesis insuficientes producen falsos empates o falsas certezas

Si el analista solo formula dos hipótesis (verdadero/falso, sí/no, actor A / no-actor A), el ACH produce resultados binarios que no reflejan la complejidad real. Un verdadero análisis ACH incluye al menos:
- La hipótesis dominante.
- Variantes de la hipótesis dominante con supuestos distintos.
- La hipótesis nula.
- La hipótesis de deception o bandera falsa.

---

### Principio 6: la atribución requiere convergencia de clases de evidencia

El ACH no puede, por sí solo, atribuir a un actor concreto. Lo que puede hacer es eliminar hipótesis de atribución. Para que una hipótesis de atribución sobreviva al ACH con confianza media o alta, deben converger al menos tres clases de evidencia independientes:
- Técnica (TTPs, malware, infraestructura).
- Comportamental (timing operacional, targeting, OPSEC).
- Contextual (motivación, geopolítica, historial del actor).

Una atribución respaldada solo por evidencia técnica es una hipótesis que no ha sido falsada en las otras dos dimensiones, no una atribución confirmada.

---

### Marcos complementarios que el analista ACH conoce y usa

**Lógica de Bayesiana cualitativa:** el ACH no es bayesiano en sentido formal, pero el concepto de "evidencia que actualiza la probabilidad relativa entre hipótesis" es compatible. Los ítems discriminantes son los que actualizan más; los no discriminantes, los que no actualizan nada.

**Modelo de "diagnostic value" (Heuer 1999, cap. 8):** la evidencia tiene valor diagnóstico cuando su aparición tiene probabilidades muy distintas bajo diferentes hipótesis. Si P(E|H1) ≈ P(E|H2), la evidencia no discrimina aunque sea "C" para ambas.

**Problema de las evidencias correlacionadas:** si dos ítems de evidencia provienen de la misma fuente o del mismo canal de recolección, no son independientes. Tratarlos como dos "I" separadas sobreestima su peso combinado. El analista ACH debe detectar y documentar correlaciones entre ítems.

**Sesgo de "too few hypotheses":** Heuer identificó que los analistas tienden a formular menos hipótesis de las necesarias porque cada hipótesis adicional aumenta el trabajo. El ACH estructuralmente exige al menos cuatro; cualquier análisis con dos hipótesis debe justificarse explícitamente.

---

### Limitaciones conocidas del método

El ACH no resuelve todo:

1. **No asigna probabilidades absolutas.** Solo ordena hipótesis por número de inconsistencias. La diferencia entre "la más probable" y "la segunda más probable" no se cuantifica directamente.
2. **Depende de la calidad y completitud de la evidencia disponible.** Si hay evidencia clave no disponible (HUMINT, SIGINT clasificado), el resultado de la matriz es provisional.
3. **El deception puede contaminar la evidencia.** Si el adversario planta evidencia diseñada para producir inconsistencias en las hipótesis correctas, el ACH puede ser explotado. Por eso la hipótesis de deception siempre debe estar en la matriz: si sobrevive con pocas inconsistencias, es señal de alerta.
4. **No sustituye al juicio analítico.** La formulación de hipótesis y la evaluación de calidad de la evidencia requieren conocimiento del dominio. El ACH estructura el proceso; no lo automatiza.
