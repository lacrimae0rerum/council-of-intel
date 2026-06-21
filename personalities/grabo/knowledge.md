# Knowledge

## Doctrina de Cynthia Grabo sobre warning intelligence

### Quién es Cynthia Grabo y por qué importa

Cynthia Grabo pasó 25 años como analista de warning en la Agencia de Inteligencia de Defensa (DIA) y en la comunidad de inteligencia estadounidense. Su trabajo más influyente, "Handbook of Warning Intelligence" (escrito en los años 70 para uso interno de la DIA, desclasificado y publicado por Scarecrow Press en 2004), es el texto fundacional de la warning intelligence como disciplina separada del análisis convencional.

Grabo escribió el manual en respuesta a los fracasos de warning más importantes del siglo XX: la sorpresa de Pearl Harbor (1941), la invasión de Corea del Norte (1950), el ataque egipcio del Yom Kippur (1973). En todos esos casos, la inteligencia tenía indicadores; el problema fue que el sistema de warning no los interpretó correctamente o no los comunicó al consumidor a tiempo.

---

### El argumento central de Grabo: el warning no puede esperar certeza

El principio más contraintuitivo de la doctrina de Grabo es que el warning exitoso opera con evidencia insuficiente para certeza. La razón es matemática: si el analista espera tener suficiente evidencia para estar seguro de que el evento va a ocurrir, ese nivel de evidencia solo está disponible cuando el evento ya está en curso o es inminente. Para ese momento, el tiempo de respuesta del consumidor puede ser insuficiente.

Grabo establece que el umbral de warning no es la certeza del evento sino la suficiencia de los indicadores para justificar que el consumidor inicie sus preparaciones. El warning es accionable cuando la preparación del consumidor tiene sentido dado el patrón de indicadores, aunque la certeza del evento sea solo parcial.

---

### Los principios de la warning intelligence

**Principio 1 — Capacidad y intención son variables independientes.**
El error más frecuente en warning intelligence es inferir intención de la existencia de capacidad. Un actor que tiene capacidad de ataque y que en el pasado la ha usado no está actualmente preparando un ataque; eso es una descripción de su historial, no una evaluación de su estado actual. El warning requiere evidencia de cambio en la intención, no solo de existencia de la capacidad.

**Principio 2 — La ausencia de señal puede ser evidencia negativa o laguna de colección.**
Grabo insiste en que el analista no puede interpretar la ausencia de indicadores como ausencia de preparación sin primero verificar que la colección es suficiente para detectar esos indicadores. Si no se está monitorizando la infraestructura relevante, la ausencia de señal solo indica que no se está mirando.

**Principio 3 — Los indicadores anticipatorios deben distinguirse de los indicadores de confirmación.**
Los indicadores anticipatorios aparecen antes del evento. Los indicadores de confirmación aparecen cuando el evento ya está ocurriendo o es inevitable. Un sistema de warning que solo identifica indicadores de confirmación no está haciendo warning; está haciendo detección tardía.

**Principio 4 — El coste del falso negativo en alta consecuencia justifica umbrales bajos.**
Grabo reconoce que los warnings prematuros tienen coste (movilización de recursos, pérdida de credibilidad si no ocurre el evento). Pero en eventos de alta consecuencia e irreversibilidad, ese coste es sistemáticamente menor que el coste de un warning tardío. La asimetría del error justifica operar con evidencia parcial.

**Principio 5 — Todo warning debe incluir señales de revisión.**
Una evaluación de warning sin señales de revisión es una evaluación estática que no puede actualizarse cuando la situación cambia. Las señales de revisión son los observables que, si aparecen, cambian el nivel de alerta (hacia arriba o hacia abajo). Sin ellas, el warning no puede ser dinámico.

---

### Los fallos clásicos de warning intelligence

Grabo analizó exhaustivamente los fallos de warning históricos. Los patrones recurrentes son:

**"The cry wolf" syndrome:** cuando hay demasiadas alertas y pocas se confirman, los consumidores empiezan a ignorarlas. El sistema de warning pierde credibilidad y los warnings genuinos se filtran junto con los falsos positivos. La solución no es bajar el número de alertas sino mejorar la especificidad de los indicadores.

**Satisfacción con la inteligencia disponible:** el analista asume que la inteligencia actual es suficiente para determinar que no hay amenaza inminente, cuando en realidad la inteligencia actual simplemente no está mirando los indicadores relevantes.

**Fijación en el pasado:** el analista usa el historial del actor como predictor del comportamiento presente sin ajustar cuando el contexto situacional del actor ha cambiado. Un actor que históricamente ha tolerado la presión puede haber llegado a un punto en que la tolerancia se agota; el historial no captura ese punto de inflexión.

**Normalización de anomalías:** cuando los indicadores de preparación son graduales, el analista tiende a normalizarlos uno a uno. Cada nuevo indicador se incorpora como "ligeramente anómalo pero explicable". El patrón acumulado que debería activar el warning no se reconoce como tal porque cada elemento individual fue normalizado.

**El comité y el consenso:** en las organizaciones de inteligencia, el warning rara vez lo emite un analista individual; pasa por capas de revisión y aprobación. Cada capa tiene incentivos para suavizar la alerta ("no tenemos suficiente evidencia", "podría ser una explicación alternativa"). El warning que llega al consumidor a menudo está diluido respecto al que el analista individual habría emitido.

---

### Warning intelligence y Pearl Harbor

El caso de Pearl Harbor es el caso de estudio central de la doctrina de warning. En las semanas previas al ataque (7 de diciembre de 1941), la comunidad de inteligencia estadounidense tenía indicadores de que Japón estaba preparando operaciones militares. Los problemas:

1. Los analistas no habían construido un framework de indicadores específico para un ataque a Pearl Harbor; los indicadores disponibles no se interpretaron como señales anticipatorias de ese objetivo.
2. La comunidad asumía que Japón no atacaría Pearl Harbor porque ese ataque parecía irracional desde la perspectiva norteamericana (mirror imaging).
3. Los indicadores se normalizaron uno a uno sin evaluar el patrón acumulado.
4. El warning habría requerido operar con evidencia incompleta e inferir intención de señales ambiguas; eso no ocurrió.

La lección que Grabo extrae: un sistema de warning debe tener frameworks de indicadores pre-construidos para los escenarios adversos más críticos, no construirlos sobre la marcha cuando los indicadores ya están activos.

---

### Warning intelligence en CTI: la kill chain como framework de indicadores

En el dominio de ciberseguridad, el framework de indicadores de Grabo se aplica naturalmente a las fases de la cadena de ataque (kill chain de Lockheed Martin):

- **Reconocimiento:** el actor mapea los objetivos potenciales. Indicadores: escaneos de red desde infraestructura conocida del actor, consultas DNS hacia los objetivos, acceso a registros públicos de la organización.
- **Armamentización:** el actor prepara el tooling. Indicadores: compilación de malware en infraestructura conocida, registro de dominios con patrones similares a campañas anteriores.
- **Entrega:** el actor envía el vector de acceso inicial. Indicadores: spear-phishing con targeting específico, publicación de exploits relacionados con tecnologías del objetivo.
- **Explotación y persistencia:** el actor establece acceso. Indicadores: detección de tooling del actor en la red objetivo.

Un warning efectivo en CTI detecta indicadores de reconocimiento y armamentización, no espera a los indicadores de entrega o explotación. Para cuando el acceso inicial está establecido, el warning llega tarde.

---

### Relación con otros seats del consejo

- **indicators-of-change (Familia A):** la tabla de indicadores de IoC y la tabla de indicadores de Grabo son complementarias pero distintas. IoC rastrea indicadores que confirmarían o revocarían hipótesis activas; Grabo busca indicadores anticipatorios que señalan que algo está a punto de ocurrir que todavía no es una hipótesis establecida.
- **lowenthal (Familia B):** Grabo identifica los indicadores y calibra el nivel de alerta; Lowenthal evalúa si ese nivel de alerta está calibrado al umbral de decisión del consumidor y si el coste asimétrico se comunica de forma accionable.
- **key-assumptions-checker (Familia A):** muchos fallos de warning son fallos de supuestos implícitos (mirror imaging sobre la racionalidad del adversario, normalización de anomalías). KAC hace visible los supuestos que Grabo necesita que estén explícitos para que el framework de indicadores sea válido.
