# Skill

## Análisis de Hipótesis Competitivas (ACH)

### Técnica central: refutación sistemática, no confirmación

El ACH no busca la hipótesis más apoyada por la evidencia. Busca la hipótesis que la evidencia menos puede refutar. Esta distinción es operativamente crítica: cualquier hipótesis falsa puede acumular evidencia consistente si el adversario la construye así, o si el analista la busca. Solo la inconsistencia elimina hipótesis.

---

### Paso 1 — Enumeración completa de hipótesis

**Objetivo:** cubrir el espacio de explicaciones plausibles, no solo las "razonables".

Protocolo:
1. Formula la hipótesis intuitiva (la que la mayoría del consejo asume).
2. Formula la hipótesis nula (no hay actividad intencional; es un artefacto, coincidencia o error de recolección).
3. Formula la hipótesis de deception activo (el adversario está construyendo el cuadro intencionalmente para producir una conclusión errónea).
4. Formula hipótesis intermedias o alternativas que ninguna de las anteriores cubre.

Criterio de completitud: ¿puede la evidencia disponible distinguir entre estas hipótesis? Si todas acumulan solo evidencia consistente, las hipótesis están mal formuladas o la evidencia es insuficiente.

---

### Paso 2 — Extracción y separación de evidencia

**Objetivo:** listar los ítems de evidencia disponibles como unidades independientes.

Protocolo:
1. Cada indicador, observable, registro o infuente es un ítem separado (E1, E2, E3…).
2. No agrupar: "múltiples TTPs del actor X" es varios ítems, no uno.
3. Registrar evidencia ausente como ítem negativo cuando la hipótesis candidata la predice: "E_n: no se observa X, que se esperaría si H1 fuera cierta."
4. Anotar la calidad de cada ítem si está disponible (fuente, modalidad, antigüedad). La evidencia de baja calidad no se descarta; se pondera al evaluar la confianza.

---

### Paso 3 — Construcción de la matriz

**Objetivo:** evaluar cada celda (hipótesis × evidencia) de forma independiente.

Protocolo de evaluación de celda:
- Aplica una sola pregunta: "¿Puede esta hipótesis ser verdadera y este ítem de evidencia existir al mismo tiempo?"
  - Si sí → **C** (consistente).
  - Si no → **I** (inconsistente).
  - Si el ítem no tiene relación con la hipótesis → **N/A**.
  - Si no puedes determinarlo con la información disponible → **?**.

Errores frecuentes al rellenar la matriz:
- Confundir "la evidencia apoya H" con "C": que la evidencia sea consistente no significa que sea especialmente probatoria de H.
- Usar "N/A" para evitar marcar "I": si una hipótesis predice activamente la ausencia de este ítem y el ítem existe, es "I".
- Omitir la columna de evidencia ausente: si H predice que deberíamos ver algo y no lo vemos, es "I" para H.

---

### Paso 4 — Identificación de evidencia discriminante

**Objetivo:** separar la evidencia que diferencia hipótesis de la que no aporta poder analítico.

Un ítem de evidencia es discriminante cuando:
- Es "C" para al menos una hipótesis.
- Es "I" para al menos otra hipótesis.

Un ítem con solo "C" en todas las hipótesis no discrimina: cualquier hipótesis podría ser verdadera. Un ítem con "I" en todas las hipótesis elimina evidencia, no hipótesis (probablemente está mal atribuido).

Protocolo:
1. Calcula el ratio de discriminación para cada ítem: número de "I" vs número de "C". Cuanto más asimétrico, más discriminante.
2. Identifica los 2–3 ítems con mayor ratio: son los que sostienen la conclusión. Si la evidencia que los respalda es frágil, la conclusión es frágil.
3. Comprueba si la hipótesis candidata tiene algún ítem de evidencia "I": si no, la hipótesis no es falsificable con la evidencia disponible y la confianza debe ser baja.

---

### Paso 5 — Conteo de inconsistencias y ordenación

**Objetivo:** identificar la hipótesis candidata de forma objetiva.

Protocolo:
1. Suma las "I" de cada hipótesis.
2. Ordena las hipótesis de menor a mayor número de inconsistencias.
3. La hipótesis con menos "I" es la candidata.
4. Si hay empate: la hipótesis candidata provisional es aquella cuyas "I" son de menor calidad (evidencia más débil) o cuya "I" puede explicarse por lagunas de recolección, no por inconsistencia real.

**Regla sobre ítems de evidencia de baja calidad:** una "I" de un ítem de evidencia de baja calidad pesa menos que una "I" de un ítem de alta calidad. Documenta la ponderación si resulta determinante en el resultado.

---

### Paso 6 — Calibración de confianza

**Objetivo:** traducir el resultado de la matriz en un nivel de confianza defendible.

Protocolo:
1. Cuenta cuántos ítems discriminantes apuntan a la hipótesis candidata.
2. Evalúa la diferencia de inconsistencias entre la hipótesis candidata y la segunda (gap de inconsistencias).
3. Evalúa si la hipótesis candidata predice evidencia que debería estar disponible y no está (evidencia ausente como señal de alerta).
4. Aplica la tabla de calibración del agent.md.

Restricción: no aumentar la confianza porque la hipótesis candidata "parece intuitivamente correcta". La intuición es la variable que el ACH está diseñado a controlar.

---

### Aplicación en el dominio IC/CTI

**Beaconing y C2:** los cuatro ítems de evidencia más discriminantes son casi siempre: patrón temporal (jitter vs intervalos exactos), fingerprint de tráfico (JA3, headers), infraestructura de destino (tipo de AS, antigüedad del dominio) y ausencia de registro en controles internos. Cada uno debe ser un ítem independiente en la matriz.

**Atribución de actor:** cuando hay TTPs atribuibles a más de un actor (Cobalt Strike, herramientas públicas, LOTL), la hipótesis de "actor diferente imitando" siempre debe estar en la matriz. La ausencia de victimología solapada con intrusiones previas no discrimina entre el actor real y un imitador con nuevas infraestructuras.

**Warning intelligence:** la evidencia ausente tiene especial peso en warning. Si un actor habitualmente telegrafía sus operaciones (reconocimiento, staging, test de payload) y en este caso no hay señales previas, es un "I" para la hipótesis de operación en curso y un "C" para la hipótesis de operación ya completada o de deception.
