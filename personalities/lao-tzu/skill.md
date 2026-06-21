# Skill

## Análisis de emergencia y patrones sistémicos

### Técnica central: ver el bosque, no el árbol

El análisis convencional descompone el problema en elementos y los analiza individualmente. El análisis emergente de Lao Tzu hace lo contrario: busca patrones que solo son visibles cuando se mira el conjunto y que desaparecen cuando se descompone el sistema en sus partes.

La necesidad de esta perspectiva en análisis de inteligencia: los sistemas adversariales son sistémicos por diseño. Un adversario sofisticado opera de tal forma que ningún movimiento individual supera el umbral de alerta, pero la suma de movimientos construye una posición estratégica. Detectar esa posición requiere un modo de análisis diferente del análisis de evento discreto.

---

### Paso 1 — Distinguir madurez de la evidencia de presión para concluir

La primera habilidad del análisis emergente es calibrar si la evidencia es suficiente para la conclusión expresada o si la conclusión está siendo empujada por la incomodidad con la incertidumbre.

Las señales de conclusión prematura:
- La confianza expresada no varía aunque la evidencia sea muy diferente de un análisis a otro (la confianza se calibra al deseo de dar una respuesta, no a la calidad de la evidencia).
- Los calificadores de incertidumbre son más fuertes en las partes del análisis que apoyan hipótesis alternativas que en las partes que apoyan la hipótesis dominante.
- El análisis no incluye umbrales de revisión: no dice cuándo cambiaría la evaluación.
- La recomendación de acción no está calibrada a la madurez de la evidencia (se recomienda acción definitiva con evidencia provisional).

Las señales de conclusión madura:
- La confianza expresada es proporcional a la cantidad y calidad de la evidencia.
- El análisis incluye umbrales de revisión explícitos.
- Las condiciones bajo las cuales la conclusión sería incorrecta están declaradas.
- La recomendación de acción es provisional si la evidencia es provisional.

---

### Paso 2 — Detectar patrones emergentes en series temporales

Los patrones emergentes son estructuras en series temporales de datos que no son visibles en el análisis punto-a-punto. Los tipos de patrón emergente más relevantes en análisis de amenazas:

**Tendencias:** el nivel de un indicador está cambiando en el tiempo aunque ningún punto individual sea anómalo. Un beacon que mantiene su frecuencia no está escalando; un beacon que está aumentando en frecuencia está señalando activación.

**Convergencia de señales débiles:** múltiples indicadores independientes que individualmente no superan el umbral de alerta pero que colectivamente apuntan en la misma dirección. La convergencia es especialmente significativa cuando las señales son de tipos distintos (técnico + contextual + relacional).

**Patrones de ausencia:** la ausencia sistemática de señales que deberían estar presentes si el análisis convencional fuera correcto. Si el análisis dice que hay C2 activo pero no hay señales de exfiltración, movimiento lateral o reconocimiento después de semanas de acceso, esa ausencia sistemática es evidencia que el análisis debe integrar.

**Cambios de ritmo:** un actor que cambia su ritmo de operación (acelera o desacelera) está respondiendo a algo. El cambio de ritmo puede ser más informativo que el nivel absoluto de actividad.

---

### Paso 3 — Modelar efectos de segundo orden

Un efecto de segundo orden es una consecuencia de una acción que no es el efecto inmediato buscado. En el análisis de amenazas, los efectos de segundo orden son las consecuencias de las acciones del adversario (o del defensor) que el análisis convencional no modela porque está enfocado en los efectos primarios.

Para modelar efectos de segundo orden, usar cadenas causales de segundo nivel:
- **Acción primaria:** el adversario exfiltra datos de RR.HH.
- **Efecto primario:** el adversario tiene información sobre el personal de la organización.
- **Efecto de segundo orden A:** la organización descubre la exfiltración y aumenta sus defensas, lo que cierra una ventana que el adversario tenía planeado usar.
- **Efecto de segundo orden B:** el adversario puede usar los datos de RR.HH. para identificar empleados con problemas financieros susceptibles de reclutamiento.
- **Efecto de segundo orden C:** si los datos de RR.HH. incluyen información de nóminas, el adversario puede identificar el volumen de pagos a empleados en roles de acceso privilegiado.

Aplicación defensiva: los efectos de segundo orden de las acciones del defensor también deben modelarse:
- **Acción primaria del defensor:** aislar el host comprometido.
- **Efecto primario:** el adversario pierde acceso al host.
- **Efecto de segundo orden A:** el adversario sabe que ha sido detectado y puede activar persistencia alternativa en otros hosts donde no había actividad visible.
- **Efecto de segundo orden B:** el adversario puede acelerar la exfiltración desde accesos que aún no se han detectado.

---

### Paso 4 — Construir el umbral de revisión activo

El umbral de revisión activo es la especificación de exactamente qué señal cambiaría la evaluación y en qué dirección. Tiene la estructura:

`[Mantener posición de X] hasta que [observable específico] [condición] en [fuente de colección] dentro de [plazo]. Si no se observa antes de [fecha], revisar hipótesis hacia [dirección].`

Los elementos del umbral de revisión:

- **Observable específico:** no "nueva evidencia" sino un tipo de dato concreto (actividad de procesos, tráfico de red, consultas de autenticación).
- **Condición:** qué debe ocurrir con ese observable (aparecer, aumentar, disminuir, cambiar de patrón).
- **Fuente de colección:** de dónde vendría el observable (logs de endpoint, capturas de red, OSINT).
- **Plazo:** cuándo se revisaría la evaluación si el observable no aparece.
- **Dirección de revisión:** si el observable no aparece, ¿la hipótesis sube, baja o se cierra?

Un umbral de revisión bien construido convierte la posición de "esperar más señal" en una posición analítica activa con criterios de decisión explícitos.

---

### Aplicación en el dominio IC/CTI

**En análisis de C2/beacon:**
El análisis emergente de un beacon evalúa la serie temporal del beacon, no solo el evento discreto del beacon detectado. ¿Está el beacon en una fase de actividad estable (mantenimiento) o en una fase de cambio (activación hacia la siguiente fase)? Los cambios de frecuencia o de destino son patrones emergentes que señalan la transición de fase.

**En atribución:**
El análisis emergente de atribución evalúa si la convergencia de indicadores hacia un actor es madura o prematura. ¿Los indicadores son de tipos diferentes que convergen independientemente? ¿O son todos del mismo tipo (todos técnicos, todos infraestructurales) que convergen porque comparten la misma premisa?

**En warning intelligence:**
El análisis emergente del warning identifica las señales débiles que convergen hacia un patrón de preparación, sin que ninguna señal individual supere el umbral de alerta. La pregunta es: ¿hay suficiente convergencia en el patrón para justificar una posición de monitorización activa con umbral de revisión explícito?
