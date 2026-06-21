# Skill

## Auditoría de calidad de información con la escala Admiralty

### Técnica central: separación de fiabilidad y credibilidad

El error más frecuente en evaluación de fuentes es confundir la reputación de quien informa con la veracidad de lo que informa. La escala Admiralty impide ese error estructuralmente: obliga a evaluar las dos dimensiones por separado y nunca permite que una compense a la otra.

Una fuente completamente fiable (A) puede reportar información dudosa (4). Un informante poco fiable (D) puede acertar en un ítem concreto que resulta confirmado (1). Ambas combinaciones son válidas y comunes. El auditor evalúa cada dimensión de forma independiente.

---

### Paso 1 — Catalogar y tipar las fuentes

Antes de asignar ningún rating, el auditor construye un inventario exhaustivo de todas las fuentes utilizadas en el análisis:

- **Primarias:** fuentes con acceso directo al objeto de análisis (logs de red propios, capturas forenses, HUMINT de primera mano, SIGINT raw).
- **Secundarias:** fuentes que procesan o reinterpretan información primaria (informes de vendor, advisories gubernamentales, feeds CTI curados).
- **Terciarias:** fuentes que citan fuentes secundarias (blogs de investigadores, OSINT agregado, foros de threat intel).

La tipología importa porque determina la distancia de la fuente al objeto de análisis. Las fuentes terciarias raramente pueden elevar la credibilidad de un ítem más allá de "posiblemente cierto" (3), independientemente de quién las emita.

---

### Paso 2 — Asignar fiabilidad de fuente (A–F)

La fiabilidad es una propiedad de la fuente, no del ítem específico. Se evalúa a partir de:
- Historial documentado de aciertos y errores en el dominio relevante.
- Tipo de acceso que tiene al objeto de análisis (¿tiene visibilidad directa o depende de terceros?).
- Motivación: ¿la fuente tiene incentivos para distorsionar la información?
- Independencia: ¿la fuente es verdaderamente independiente o comparte inteligencia de base con otras fuentes citadas?

Criterio de asignación conservador: cuando no hay historial verificable, asignar F, no C. El código F no es una crítica; es una declaración de incertidumbre sobre la fiabilidad.

---

### Paso 3 — Asignar credibilidad de la información (1–6)

La credibilidad es una propiedad del ítem de información específico, no de la fuente. Se evalúa a partir de:
- ¿Hay otras fuentes independientes que reportan el mismo ítem? (→ 1 o 2)
- ¿El ítem es consistente con el comportamiento conocido del actor o con el contexto? (→ 2 o 3)
- ¿El ítem es plausible pero sin corroboración directa? (→ 3)
- ¿El ítem contradice el comportamiento conocido o el contexto sin explicación? (→ 4 o 5)
- ¿No hay suficiente contexto para juzgar? (→ 6)

Criterio de asignación conservador: la credibilidad 1 requiere corroboración por fuentes verdaderamente independientes. No basta con que dos fuentes digan lo mismo si ambas provienen del mismo origen.

---

### Paso 4 — Trazar el grafo de dependencia para detectar circularidad

La circularidad informativa es el defecto más grave en conjuntos de fuentes CTI. Se produce cuando fuentes que parecen independientes son en realidad nodos de una misma cadena que se remonta a un único origen.

Protocolo de detección:
1. Para cada fuente, pregunta: "¿Qué fuente primaria respalda el ítem específico que reporta?"
2. Si la fuente no puede identificar su origen primario → código F para fiabilidad, 6 para credibilidad.
3. Si dos fuentes se remontan al mismo origen primario → marcarlas como dependientes entre sí.
4. Reduce el conjunto de fuentes "independientes" al número de orígenes primarios distintos reales, no al número de fuentes citadas.

Patrones de circularidad habituales en CTI:
- **Cadena de vendor:** vendor A publica IOC → vendor B incluye el mismo IOC en su feed citando a vendor A → analyst tool agrega ambos feeds y reporta "dos confirmaciones independientes".
- **Laundry chain gubernamental:** gobierno cita vendor → advisory de otro país cita el advisory del primero → el analista cuenta dos fuentes gubernamentales "independientes".
- **OSINT amplificado:** investigador OSINT replica el análisis de un vendor sin acceso a las muestras → se cita como "tercera fuente".

---

### Paso 5 — Identificar lagunas de información

Una laguna es evidencia que debería existir si una hipótesis fuera cierta, y no está disponible. Las lagunas se identifican desde el punto de vista de cada hipótesis, no solo de la dominante.

Para cada laguna, el auditor documenta:
- Clase de fuente que podría cubrirla (HUMINT, SIGINT, forense de endpoint, victimología, metadatos de operador).
- Por qué su ausencia limita la confianza.
- Si la laguna es esperable (el material simplemente no existe) o sospechosa (el material debería estar disponible y no se ha buscado o reportado).

---

### Paso 6 — Evaluar sesgo de confirmación en la selección de evidencia

El sesgo de confirmación en la selección de fuentes se manifiesta como asimetría: el análisis cita múltiples fuentes para la hipótesis favorita y ninguna (o muy pocas) para las alternativas.

El auditor evalúa:
- ¿Se han buscado fuentes que puedan contradecir la hipótesis dominante?
- ¿Las fuentes que contradicen la hipótesis dominante están incluidas en el análisis?
- ¿Las fuentes que apoyan hipótesis alternativas tienen ratings Admiralty más bajos de forma sistemática y justificada, o se les ha asignado un rating bajo para debilitarlas?

---

### Aplicación en el dominio IC/CTI

**En análisis de amenaza con feeds CTI:**
El mayor riesgo de circularidad viene de los feeds comerciales. Muchos feeds agregan los mismos IOCs de origen incierto (Pastebin, GitHub dumps, submissions anónimas). Un analista que cita tres feeds independientes puede estar citando el mismo IOC de origen desconocido tres veces.

Protocolo específico: antes de usar un feed CTI como fuente, preguntar "¿cuál es la fuente primaria de este indicador y con qué frecuencia este vendor publica False Positives en este sector?".

**En informes de atribución:**
La evidencia técnica (TTPs, herramientas, infraestructura) rara vez es de fuente primaria para el analista que la recibe: casi siempre es de vendor o OSINT. La clase de evidencia con mayor probabilidad de ser fuente primaria real es el forense de endpoint propio o el HUMINT de primera mano. Cuando no hay ninguna fuente primaria en el conjunto, la confianza residual máxima es 55% independientemente del número de fuentes secundarias.

**En warning intelligence:**
La calidad de la información tiene asimetría temporal: la evidencia reciente de fuentes primarias vale más que evidencia antigua de fuentes secundarias. Un indicador de cambio de hace 90 días reportado por un vendor vale menos, en contexto de warning, que una observación directa de hace 48 horas, aunque el código Admiralty de la segunda fuente sea más bajo.
