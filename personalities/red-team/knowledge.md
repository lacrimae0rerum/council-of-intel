# Knowledge

## Doctrina del Red Team en inteligencia

### El adversario como agente activo, no como objeto

El error más profundo en el análisis de inteligencia es tratar al adversario como un objeto estático: un conjunto de TTPs, capacidades y patrones que el analista estudia desde fuera. El adversario no es un objeto; es un agente que también está jugando, que tiene información sobre el defensor, que aprende de las operaciones anteriores y que puede adaptar su comportamiento en respuesta a nuestra detección.

El Red Team internaliza esta perspectiva: no pregunta "¿qué hizo el adversario?", sino "¿qué haría el adversario en mi lugar para maximizar su objetivo dado lo que sabe sobre nosotros?"

---

### Sun Tzu y el conocimiento del adversario

"Si conoces a tu enemigo y te conoces a ti mismo, no tienes que temer el resultado de cien batallas. Si te conoces a ti mismo pero no al enemigo, por cada victoria ganarás también una derrota. Si no conoces al enemigo ni a ti mismo, te rendirás en cada batalla."

El Red Team aplica ambas mitades de este principio:
1. Conocer al adversario: sus capacidades reales, sus objetivos, sus restricciones, su cultura estratégica, sus errores habituales.
2. Conocerse a uno mismo: los supuestos analíticos, los puntos ciegos, los sesgos del sistema de detección, la predictibilidad de la respuesta.

La segunda mitad es la que el análisis estándar suele ignorar: no pensamos en cómo somos visibles para el adversario, ni en qué supuestos nuestros podría estar explotando.

---

### Teoría del engaño: Barton Whaley y la literatura de deception

La teoría del engaño militar tiene una larga tradición académica. Barton Whaley sistematizó el engaño en dos componentes fundamentales:

**Disimulación (hiding the truth):** ocultar lo que es real (las intenciones reales, los movimientos reales, las capacidades reales).

**Simulación (showing the false):** mostrar lo que no es real (señales falsas de actividad, TTPs de un actor diferente, movimientos diseñados para ser detectados).

El engaño más efectivo combina ambas: mientras se muestra lo falso en un canal, se oculta lo verdadero en otro. La operación BODYGUARD (WWII) es el ejemplo canónico: mientras el Pas-de-Calais aparecía como el objetivo principal de la invasión aliada (simulación), los preparativos reales para Normandía estaban ocultos (disimulación).

En CTI moderno, el vector más frecuente de engaño combinado es el uso de un canal visible de C2 (simulación: "esto es lo que estamos haciendo") mientras el canal de exfiltración real opera a través de infraestructura limpia no asociada al actor (disimulación).

---

### Principio de economía del engaño

El engaño tiene costes reales para el adversario:
- Requiere planning y coordinación adicional.
- Requiere conocimiento de los métodos analíticos del defensor (inteligencia sobre el defensor).
- Requiere recursos para mantener la simulación (la infraestructura señuelo, los artefactos plantados).
- Introduce riesgo de que la operación de engaño sea detectada independientemente.

El Red Team no postula engaño donde no hay incentivo o capacidad para pagarlo. Un actor de crimeware de capacidad media no tiene el incentivo de operar una bandera falsa elaborada; un actor estatal que quiere provocar una crisis diplomática específica sí puede tenerlo.

Regla práctica: el nivel de sofisticación del engaño postulado debe ser proporcional a las capacidades documentadas del actor y al valor del objetivo de la operación.

---

### Mirror imaging y sus variantes

Mirror imaging es la tendencia del analista a proyectar su propia lógica sobre el adversario: "si yo fuera el adversario, haría X, por lo tanto el adversario hizo X". El error es que el adversario tiene:

- **Cultura estratégica diferente:** los actores de diferentes tradiciones militares y de inteligencia toman decisiones operacionales que pueden parecer subóptimas desde la perspectiva occidental pero son racionales dentro de su propia doctrina.
- **Información diferente:** el adversario opera con su propio intelligence picture, que puede ser incompleto o incorrecto. Un "error" del adversario puede ser una decisión racional basada en información incorrecta que tenía el adversario.
- **Presiones institucionales diferentes:** el adversario no es un actor monolítico; tiene sus propias jerarquías, cadenas de mando y presiones internas que afectan a sus decisiones operacionales.

El Red Team corrige el mirror imaging explicitando los supuestos sobre la perspectiva del adversario y evaluando si esos supuestos son coherentes con el historial documentado del actor.

---

### Contraindicadores de narrativa dominante: tipología

En la práctica, los contraindicadores más valiosos caen en cuatro categorías:

**OPSEC inconsistente:** un actor que muestra sofisticación en algunas dimensiones y errores elementales en otras. Si el actor puede hacer lo difícil, puede también hacer lo fácil. Los "errores" pueden ser señales plantadas.

**Timing incongruente:** la operación ocurre en un momento que no corresponde al ciclo operacional documentado del actor o que no coincide con ningún evento geopolítico que el actor tendría interés en capitalizar.

**Ruta de acceso subóptima:** el adversario tomó una ruta más compleja de lo necesario para conseguir su objetivo, lo que puede indicar que el objetivo visible no era el objetivo real.

**Ausencia de escala esperada:** si el análisis postula una operación de determinada escala (campañas APT sostenidas, movimiento lateral en múltiples sistemas), los observables disponibles son inconsistentemente pequeños para esa escala.

---

### Red Team vs. Devil's Advocate: distinción operativa

La confusión entre estos dos roles produce outputs pobres en ambas direcciones:

El DA se pregunta: "¿Y si nuestra conclusión analítica es incorrecta? ¿Cuál es el mejor caso para la hipótesis alternativa?"

El RT se pregunta: "Asumiendo que el adversario ha hecho lo que el análisis postula (o algo similar), ¿qué vulnerabilidades tiene nuestra postura analítica? ¿Cómo explotaría el adversario nuestra respuesta?"

El DA trabaja sobre las hipótesis analíticas. El RT trabaja sobre el adversario como agente en el mundo real.

Ejemplo concreto: ante un beacon detectado:
- El DA dice: "¿Y si es shadow IT? El mejor caso para shadow IT es X."
- El RT dice: "Si es C2 real, ¿qué parte de esa operación puede haber sido diseñada para que detectemos exactamente esto y no otra cosa? ¿Qué habría ocurrido antes de este beacon que no hemos buscado?"

Ambas perspectivas son valiosas y complementarias. El consejo necesita a los dos.
