# Knowledge

## Doctrina de indicadores analíticos de cambio

### Origen: warning intelligence e indicadores anticipatorios

La teoría de indicadores en inteligencia tiene su raíz en la warning intelligence, desarrollada especialmente por Cynthia Grabo ("A Handbook of Warning Intelligence", 1972, desclasificado 2004). Grabo sistematizó el uso de indicadores anticipatorios para alertar de ataques inminentes: cambios observables en la postura de fuerzas adversarias que señalan una transición de "situación de referencia" a "situación de amenaza".

El Indicators of Change (IoC) analítico es una extensión de ese principio al ciclo de inteligencia general: no solo para detectar ataques inminentes, sino para definir cuándo cualquier estimación analítica —no necesariamente de warning— debe ser revisada.

---

### Principio 1: una estimación sin indicadores de revisión es un sistema cerrado

Una estimación que no define las condiciones de su propia revisión no puede ser actualizada por nueva información. El analista que emite esa estimación ha creado implícitamente un sistema que siempre se confirma: cualquier nueva información se interpreta como consistente con la estimación porque no existe un criterio predefinido para que sea inconsistente.

Este es el origen del "creeping normalcy" en inteligencia: la acumulación gradual de señales que, individualmente, parecen consistentes con la estimación, pero que colectivamente señalan un cambio que la estimación no ha capturado.

Los indicadores de cambio previenen este error al definir ex ante qué observaríamos si la estimación fuera incorrecta o estuviera desactualizada.

---

### Principio 2: los indicadores de ausencia son tan valiosos como los de presencia

En IC y CTI, gran parte del razonamiento operativo depende de la ausencia de información: "no hay señales de que el actor esté preparando X". Este tipo de razonamiento por ausencia es válido solo si se ha definido previamente qué señales se esperarían y se está monitorizando activamente su ausencia.

Un indicador de ausencia crítica formaliza exactamente eso: "a fecha N, si no hemos observado [observable específico] que debería aparecer si la hipótesis fuera correcta, la confianza en la hipótesis debe reducirse".

Sin esta formalización, la ausencia de información no produce ninguna actualización analítica: se registra como "no hay novedades" en vez de "la hipótesis predice señales que no están apareciendo".

---

### Principio 3: los umbrales previenen la "alarm fatigue"

Un sistema de indicadores sin umbrales produce alarmas constantes: cualquier observable activaría la revisión. La alarm fatigue es el estado en que los analistas ignoran las alarmas porque son demasiado frecuentes y demasiado ruidosas. Los umbrales bien calibrados convierten el sistema de indicadores en un detector de señal, no de ruido.

La calibración de umbrales requiere:
- Conocer la línea base de actividad normal (¿cuántos dominios registra el actor por semana en condiciones de no-campaña?).
- Entender la especificidad del observable (¿solo el actor atribuido muestra este patrón, o es común a muchos actores?).
- Estimar la tasa de falsos positivos de la fuente de colección.

Un umbral demasiado bajo produce alarm fatigue. Un umbral demasiado alto produce ausencias críticas falsas (el indicador no se activa aunque la situación haya cambiado).

---

### Principio 4: el timing conecta indicadores con decisión

Sin timing, un indicador no produce presión para actuar. "En algún momento aparecerá evidencia de X" no activa ninguna decisión. "Si no aparece evidencia de X en 48h, la estimación debe revisarse a la baja" sí obliga a tomar una decisión en 48h.

El timing transforma los indicadores en instrumentos de decisión para el consumidor de inteligencia:
- El policymaker sabe cuándo revisar su postura.
- El analista sabe cuándo actualizar su estimación.
- El equipo de colección sabe cuándo priorizar sus recursos.

En warning intelligence, el timing es especialmente crítico porque la ventana de acción preventiva se cierra rápidamente. Grabo sistematizó el concepto de "time-phased indicators": indicadores ordenados por el momento en que aparecerían en el ciclo de preparación del adversario, desde las señales más tempranas (decisión política, movilización logística) hasta las más tardías (despliegue final, primeras acciones).

---

### Relación con el KAC y el Warning Intelligence (Grabo)

El Indicators of Change analítico se diferencia del KAC y de Grabo:

**vs. KAC:**
- El KAC mira hacia adentro: "¿qué supuestos del análisis son frágiles?"
- El IoC mira hacia fuera: "¿qué cambiaría en el mundo que haría que la estimación dejara de ser válida?"
- Los dos son complementarios: el KAC identifica los supuestos más frágiles; el IoC define los observables que señalarían si esos supuestos están fallando.

**vs. Grabo (warning):**
- Grabo se centra en indicadores anticipatorios de un evento inminente (ataque, crisis, escalada).
- El IoC analítico se centra en indicadores de que la estimación actual necesita revisión, que puede ser por escalada, por reversión, o por cambio de hipótesis.
- El IoC tiene un alcance más amplio: no solo warning, sino cualquier estimación que deba ser monitorizada.

---

### Taxonomía de indicadores por función

En la práctica del IoC analítico, los indicadores se clasifican por su función en el ciclo de estimación:

**Indicadores de confirmación:** observables que, al aparecer, refuerzan que la estimación sigue siendo válida. No elevan la confianza por sí solos, pero previenen la degradación de la estimación por ausencia de señales.

**Indicadores de escalada:** observables que señalan que la situación ha evolucionado más rápido o más intensamente de lo estimado. Activan una revisión al alza de confianza o urgencia.

**Indicadores de revocación:** observables que contradicen la estimación de forma directa. Su activación obliga a revisar la hipótesis dominante.

**Indicadores de ausencia crítica:** la no-aparición de observables que la estimación predice. Su activación (por no-aparición en el timing esperado) obliga a reducir la confianza o revisar la hipótesis.

**Indicadores de punto de inflexión:** observables que señalan que la situación ha pasado de un estado a otro cualitativamente diferente (de "preparación" a "campaña activa", de "vigilancia" a "incidente"). Son los más urgentes: al activarse, la estimación deja de ser válida y se necesita un nuevo ciclo analítico.

---

### El error de los indicadores sin colección

Un indicador sin fuente de colección disponible es un deseo, no un sistema de monitorización. El analista que define indicadores que no pueden ser monitorizados crea la ilusión de un sistema de alerta sin la sustancia.

El IoC tiene la obligación de declarar explícitamente qué indicadores no tienen cobertura de colección y qué tipo de colección adicional cubriría esa laguna. Esta declaración tiene valor operativo: permite al consumidor de inteligencia saber dónde invertir en capacidades de colección para mejorar la monitorización futura.
