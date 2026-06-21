# Knowledge

## Doctrina de evaluación de fuentes e información

### La escala Admiralty: origen y estructura

La escala Admiralty tiene su origen en los sistemas de clasificación de inteligencia naval aliada de la Segunda Guerra Mundial. Fue formalizada en los estándares NATO (STANAG 2511) y adoptada por la mayoría de comunidades IC occidentales como marco de referencia para la evaluación de fuentes.

La escala tiene dos ejes completamente independientes:

**Eje de fiabilidad de la fuente (A–F):** evalúa el historial demostrado de la fuente para reportar información precisa en el dominio relevante. No es una propiedad del ítem específico; es una propiedad de la relación entre el analista y la fuente a lo largo del tiempo. Una fuente nueva (F) no es mala; es desconocida.

**Eje de credibilidad de la información (1–6):** evalúa la plausibilidad y el nivel de corroboración del ítem específico que la fuente reporta en este caso. No es una propiedad de la fuente; es una propiedad del contenido reportado en función del contexto disponible.

El código compuesto (ej. "B3") comunica en dos palabras toda la incertidumbre relevante sobre un ítem de información. "La fuente generalmente fiable reporta información posiblemente cierta sin corroboración" es una declaración más precisa que "fuente de buena reputación dice que X es probable".

---

### Principio central: independencia de los dos ejes

El error doctrinal más grave al aplicar la escala Admiralty es contaminar un eje con el otro. Manifestaciones:

- **Halo de fuente:** asignar credibilidad alta (1–2) a un ítem porque la fuente tiene código A, sin verificar corroboración independiente. Una fuente A puede equivocarse en un ítem concreto.
- **Rehabilitación por contenido:** asignar fiabilidad alta (A–B) a una fuente porque su contenido en este caso parece creíble. La fiabilidad histórica no se actualiza por un acierto puntual no verificado.
- **Castigo cruzado:** asignar credibilidad baja (4–5) a un ítem de una fuente E, independientemente de si el contenido tiene corroboración independiente. Si tres fuentes A, B y C confirman el mismo ítem que también reportó una fuente E, ese ítem merece código 1 aunque la fuente E sea E.

---

### Circular reporting: el defecto estructural más frecuente en IC moderna

El informe circular (circular reporting) ocurre cuando una fuente aparentemente independiente en realidad depende, directa o indirectamente, del mismo origen que otras fuentes citadas como independientes. Tiene tres consecuencias graves:

1. **Inflación artificial de la corroboración:** el analista cuenta N fuentes cuando solo hay 1 origen primario real.
2. **Propagación de errores sin corrección:** si el origen primario contiene un error, todas las fuentes derivadas lo propagan. Cuanto más corroborado parece el error, menos probable es que alguien lo cuestione.
3. **Amplificación de desinformación deliberada:** un actor que quiera que su narrativa sea aceptada solo necesita inyectarla en un nodo del que múltiples fuentes beben. La apariencia de independencia hace el resto.

El escándalo de las WMD iraquíes en 2003 es el caso histórico de referencia: múltiples fuentes de inteligencia occidentales que parecían independientes se remontaban a un número muy pequeño de orígenes, algunos de ellos de fiabilidad cuestionable. La inflación artificial de corroboración contribuyó a la sobreconfianza en los análisis.

---

### Doctrina NATO sobre calidad mínima de fuentes

La doctrina NATO (AJP-2.0 y derivados) establece que las estimaciones de inteligencia que superen el umbral de "probable" (equivalente al 55–70% de confianza) deben basarse en al menos dos fuentes independientes con código de credibilidad 1–2. Las estimaciones basadas en una única fuente, por fiable que sea, no deben superar el umbral de "posible" (25–55%).

Esta regla de corroboración mínima no siempre se aplica explícitamente en los análisis operacionales, pero es el estándar doctrinal de referencia. Cuando el Quality of Info Auditor fija un techo de confianza basado en una única fuente, está aplicando exactamente este principio.

---

### El problema de las fuentes terciarias en la era de los feeds CTI

La proliferación de plataformas de Threat Intelligence ha creado un ecosistema donde la mayor parte de la evidencia CTI disponible es terciaria: agregaciones de agregaciones, cuyos orígenes primarios son frecuentemente anónimos (submissions a VirusTotal, Pastebin, feeds automatizados de honeynet). Las implicaciones doctrinales:

1. **La mayoría de los IOCs disponibles en feeds comerciales tienen código de credibilidad 3 o inferior** porque no están confirmados por observación directa del analista que los usa.
2. **La fiabilidad del feed (A–F) no transfiere automáticamente a los ítems del feed.** Un feed de vendor A puede contener ítems con credibilidad 4 si el vendor los recopiló de fuentes anónimas.
3. **El volumen de indicadores no equivale a corroboración.** 500 IOCs de un solo feed con código A3 valen menos que 3 IOCs de dos fuentes independientes con código B1.

---

### Sesgo de disponibilidad y colección gap

Un defecto estructural en el análisis de inteligencia es tomar las fuentes disponibles como representativas del universo de información. Lo que el analista puede ver depende de qué fuentes tiene acceso, qué colección ha priorizado y qué actores saben que están siendo monitorizados.

El Quality of Info Auditor aplica el principio de "colección gap": cualquier análisis debe identificar explícitamente las clases de evidencia que no están disponibles y que serían relevantes. La ausencia de una clase de evidencia no significa que la evidencia no exista; puede significar que la colección no la alcanza.

Clases de evidencia con colección gap frecuente en IC/CTI:
- **HUMINT sobre intención:** casi nunca disponible a nivel de analista operacional.
- **SIGINT sobre atribución de operador:** disponible solo para actores con capacidades de nivel estatal.
- **Forense de endpoint de víctimas externas:** disponible solo si la víctima coopera.
- **Victimología completa:** los análisis públicos tienden a reportar las víctimas que aceptan ser identificadas, no el universo de objetivos.

---

### La regla del 55%: única fuente sin corroboración

Principio operativo del Quality of Info Auditor: ningún análisis basado en una única fuente sin corroboración puede fijar su confianza por encima del 55%, independientemente de:
- La fiabilidad histórica de esa fuente.
- La plausibilidad del contenido reportado.
- La urgencia del contexto operacional.

La razón es estructural: con una única fuente, no es posible distinguir entre un reporte correcto, un error de la fuente, y deception deliberado. La corroboración independiente es el único mecanismo que puede elevar ese techo.
