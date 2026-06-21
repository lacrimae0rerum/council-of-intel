# Skill

## Análisis estratégico adversarial: de la táctica a la intención

### Técnica central: leer la lógica del adversario, no su comportamiento

El análisis convencional describe lo que el adversario hace (observables técnicos, TTPs, indicadores). El análisis estratégico de Sun Tzu pregunta por qué el adversario lo hace: qué resultado espera conseguir y cómo el conjunto de sus acciones sirve a ese resultado.

La diferencia no es solo de abstracción. Es una diferencia de utilidad predictiva: si solo describimos lo que el adversario ha hecho, podemos reaccionar a acciones pasadas. Si entendemos la lógica estratégica del adversario, podemos anticipar las acciones futuras porque emergen de la misma lógica.

---

### Paso 1 — Identificar el objetivo estratégico (no el efecto inmediato)

El efecto inmediato de una operación adversarial (comprometer un host, exfiltrar datos, destruir un sistema) no es el objetivo estratégico. Es el medio. El objetivo estratégico es el resultado que el adversario espera conseguir a través de ese medio en el contexto de sus intereses más amplios.

Para identificar el objetivo estratégico, razonar hacia atrás desde el efecto:
- **Efecto:** el adversario exfiltra datos de RR.HH.
- **Objetivo próximo:** tener información sobre el personal de la organización.
- **Objetivo estratégico probable A:** identificar al personal con acceso a sistemas de alta seguridad para operaciones de ingeniería social futura.
- **Objetivo estratégico probable B:** tener información que pueda usar para chantaje o coerción de empleados clave.
- **Objetivo estratégico probable C:** entender la estructura de la organización para una operación más amplia.

Cada objetivo estratégico sugiere un patrón diferente de comportamiento futuro del adversario, lo que hace la identificación del objetivo estratégico predictivamente útil.

---

### Paso 2 — Leer el engaño como variable estratégica

Sun Tzu: "Todo arte bélico se basa en el engaño." Para Sun Tzu, el engaño no es una táctica de evasión; es el mecanismo central de la obtención de ventaja. El adversario que puede controlar lo que el defensor percibe controla las decisiones del defensor.

Tipos de engaño estratégico:

**Engaño de intención:** el adversario aparenta no tener intención de atacar (operaciones de preparación silenciosa) o aparenta tener una intención que no tiene (operar ruidosamente en un sector como distracción de un sector diferente).

**Engaño de capacidad:** el adversario aparenta tener menos capacidad de la que tiene (tooling simple para una operación de reconocimiento cuando tiene capacidades más avanzadas que no quiere exponer) o más (exagerar el impacto de una operación para aumentar el efecto de señalización).

**Engaño de timing:** el adversario actúa cuando el defensor tiene su atención en otro lugar (coincidencia con un incidente de otro tipo), o actúa más lentamente de lo que el defensor espera para permitir que la detección se relaje.

Para evaluar el engaño en una operación:
1. ¿Qué partes de la operación son inusualmente visibles? Si el adversario hace ruido, está dejando que el defensor lo vea; la pregunta es por qué.
2. ¿Qué partes de la operación son inusualmente ocultas? Si el adversario invierte en evasión excepcional en un área específica, esa área es probablemente donde el objetivo real está.
3. ¿Hay asimetría entre lo que se ve y el nivel de sofisticación del actor? Si un actor sofisticado usa técnicas básicas en un área, puede ser que esté usando sus mejores capacidades en otra área que no se está viendo.

---

### Paso 3 — Analizar el timing estratégico

Sun Tzu: "El guerrero exitoso actúa después de la victoria; el guerrero derrotado actúa primero y busca la victoria después." El timing no es cuándo el adversario actúa por conveniencia técnica; es cuándo el adversario actúa porque la relación de fuerzas le es favorable.

Para analizar el timing estratégico:

**¿Qué ventana aprovecha el adversario?**
- Ventana política: el objetivo está distrayendo atención en otro asunto (elecciones, crisis, reestructuración).
- Ventana técnica: el objetivo tiene una vulnerabilidad temporal (sistema sin patch, credenciales temporalmente ampliadas, sistema de detección temporalmente reducido).
- Ventana de contexto: las relaciones entre los actores relevantes (entre el defensor y sus aliados, entre el adversario y sus socios) favorecen la operación.

**¿Qué urgencia tiene el adversario?**
- Una operación ejecutada con prisa (muchos movimientos en poco tiempo, errores operacionales) sugiere que el adversario percibe una ventana que se está cerrando.
- Una operación paciente (reconocimiento prolongado, movimientos espaciados) sugiere que el adversario puede esperar la condición óptima o que tiene acceso persistente y no necesita urgencia.

---

### Paso 4 — Economía de esfuerzo como indicador de prioridad

El adversario asigna recursos en función de la prioridad del objetivo. Un actor con capacidades avanzadas que usa técnicas básicas en una operación puede estar: (a) preservando sus mejores capacidades para objetivos de mayor prioridad, (b) usando un canal secundario para un objetivo de prueba, o (c) operando en modo "ruido blanco" mientras opera con capacidades avanzadas en otro lugar.

Para leer la economía de esfuerzo:
- **Inversión en infraestructura dedicada vs. reutilizada:** infraestructura dedicada indica mayor prioridad del objetivo.
- **Tooling personalizado vs. compartido/público:** tooling personalizado indica mayor inversión y mayor prioridad.
- **Múltiples fases vs. operación directa:** múltiples fases (reconocimiento extenso, preparación de acceso alternativo, persistencia múltiple) indica que el adversario valora el acceso suficientemente para invertir en resiliencia.
- **Velocidad de operación:** operaciones lentas pueden indicar recursos limitados (solo pueden dedicar cierta cantidad de tiempo al objetivo) o preferencia estratégica (el adversario prefiere no activar alarmas de velocidad).

---

### Aplicación en el dominio IC/CTI

**En análisis de C2/beacon:**
La lectura estratégica de un C2 activo va más allá de confirmar el compromiso. Pregunta: ¿qué está haciendo el adversario durante las sesiones de C2? ¿Está en reconocimiento pasivo (leyendo directorios, mapeando la red) o en preparación activa (instalando herramientas adicionales, creando cuentas, preparando la exfiltración)? La respuesta determina la urgencia de la respuesta del defensor.

**En análisis de atribución:**
La lectura estratégica de la atribución pregunta: si el adversario es el actor atribuido, ¿qué objetivo estratégico de ese actor explica por qué este objetivo, en este momento? Si la atribución no encaja en un objetivo estratégico coherente del actor atribuido, o es incorrecta o el actor ha cambiado sus prioridades.

**En warning intelligence:**
La lectura estratégica del warning pregunta: ¿qué condición estratégica tendría que cambiar para que el adversario actuara? No las señales técnicas de preparación (esas son el dominio de Grabo) sino las condiciones del contexto estratégico que harían que la acción fuera ventajosa para el adversario.
