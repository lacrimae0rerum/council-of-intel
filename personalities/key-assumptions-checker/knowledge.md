# Knowledge

## Doctrina del Key Assumptions Check

### Origen: Heuer y Pherson en la CIA

El Key Assumptions Check (KAC) fue desarrollado como técnica analítica estructurada (SAT) en la CIA y documentado por Heuer y Pherson en "Structured Analytic Techniques for Intelligence Analysis" (2011). La premisa del KAC es simple pero contraintuitiva: los analistas de inteligencia no cometen errores principalmente en la lógica de sus inferencias, sino en los supuestos sobre los que esa lógica opera. Si el supuesto es falso, la lógica perfecta produce una conclusión falsa.

El KAC no es una técnica para dudar de todo. Es una técnica para identificar qué supuestos importan, evaluarlos de forma explícita y monitorizar si se cumplen o fallan.

---

### Principio 1: los supuestos implícitos son los peligrosos

Un supuesto explícito puede ser evaluado, cuestionado y actualizado. Un supuesto implícito es invisible: no puede ser evaluado porque nadie sabe que está ahí. La mayor parte del fracaso analítico en inteligencia no viene de errores en la lógica sino de supuestos implícitos que nadie examinó.

Casos históricos de referencia:
- **Pearl Harbor (1941):** el supuesto implícito de que Japón no atacaría instalaciones en territorio de EE.UU. nunca fue declarado ni examinado. Era razonable a priori y resultó falso.
- **WMD iraquíes (2002–2003):** el supuesto implícito de que la falta de cooperación iraquí con los inspectores implicaba existencia de programas WMD no fue sometido a la pregunta "¿qué otras causas podrían explicar esta falta de cooperación?".
- **Operación Barbarossa (1941):** el supuesto implícito de Stalin de que Hitler no atacaría mientras la guerra con Gran Bretaña no estuviera resuelta era racional desde el punto de vista estratégico soviético y resultó completamente falso.

El patrón común: supuestos que parecían razonables, no fueron declarados, y cuando fallaron, invalidaron el análisis completo.

---

### Principio 2: fragilidad es probabilidad × impacto, no intuitivo-inverosimilitud

Un error frecuente al aplicar el KAC es clasificar como "baja fragilidad" los supuestos que parecen razonables o que la mayoría comparte. La fragilidad no mide cuán razonable parece un supuesto; mide qué tan probable es que sea falso en este contexto concreto y cuánto cambiaría la conclusión si lo fuera.

El supuesto "el actor seguirá usando la misma infraestructura durante 30 días" puede parecer razonable pero tiene fragilidad alta si el actor tiene historial de rotación rápida de infraestructura ante detección.

El supuesto "el actor tiene motivación estatal" puede parecer muy sólido basado en las TTPs pero tiene fragilidad alta para la atribución si los TTPs están disponibles en el mercado o son replicables.

---

### Principio 3: un supuesto que no puede ser falsado no es un supuesto, es un axioma

Si no es posible formular ningún observable que indicaría que un supuesto es falso, ese supuesto no es falsificable. Un análisis construido sobre supuestos no falsificables no puede ser actualizado por nueva evidencia: seguirá siendo "cierto" independientemente de lo que ocurra.

El KAC detecta estos supuestos y los señala explícitamente: "este supuesto no puede ser monitorizados con la colección disponible". Esto no invalida el análisis, pero limita estructuralmente la confianza: si el supuesto más crítico no puede ser observado, la conclusión no puede ser revisada por nuevos datos.

---

### Principio 4: la señal de ruptura es el mecanismo de actualización

La señal de ruptura conecta el KAC con el ciclo de inteligencia. No es solo un ejercicio académico de identificar qué podría salir mal; es un mecanismo para definir qué información nueva cambiaría la evaluación.

Cuando el consumidor de inteligencia sabe cuáles son las señales de ruptura de los supuestos más frágiles, puede:
1. Solicitar colección dirigida para monitorizar esas señales.
2. Actualizar la evaluación inmediatamente cuando una señal aparece, sin esperar al siguiente ciclo analítico completo.
3. Evitar "sorpresas de inteligencia" que no eran sorpresas sino supuestos no monitorizados que fallaron.

Esta función de conexión entre el análisis y la colección es la aportación más operacionalmente valiosa del KAC.

---

### Principio 5: el número de supuestos frágiles es un indicador de confianza

Si un análisis requiere que cinco supuestos de fragilidad alta sean todos correctamente ciertos para que la conclusión sea válida, la probabilidad de que esa conclusión sea correcta es el producto de las probabilidades de cada supuesto. Aunque cada supuesto individual sea "razonablemente probable" (digamos, 70%), cinco supuestos independientes con esa probabilidad producen una conclusión con probabilidad de 0.70^5 ≈ 17% de ser correcta.

Este principio justifica el techo de confianza que el KAC impone: cuantos más supuestos frágiles requiera la conclusión, menor debe ser la confianza expresada.

---

### Relación con el ACH y el Quality of Info Auditor

El KAC es complementario pero diferente:
- El **ACH** evalúa qué hipótesis es más consistente con la evidencia disponible.
- El **Quality of Info Auditor** evalúa la calidad y la independencia de esa evidencia.
- El **KAC** evalúa los supuestos que conectan la evidencia con la conclusión.

Los tres juntos atacan los tres vectores de error en el análisis de inteligencia:
1. Error en la evaluación de la evidencia (ACH y QoI).
2. Error en la calidad del material (QoI).
3. Error en los supuestos del analista (KAC).

Sin el KAC, un análisis con evidencia de alta calidad y ACH impecable puede seguir fallando si descansa en supuestos implícitos que nadie examinó.

---

### El supuesto de representatividad: siempre presente

En IC/CTI existe un supuesto que el KAC debe incluir en casi todo análisis: "la colección disponible es representativa de la actividad real del actor."

Este supuesto es:
- Casi siempre implícito.
- Con frecuencia de fragilidad media-alta.
- Raramente con señal de ruptura directa disponible (por definición, si no monitorizamos un canal, no vemos lo que ocurre en él).

Su presencia en la tabla de supuestos no es para bloquearlo sino para declararlo explícitamente y para que el consumidor sepa que la conclusión se basa en lo que los sensores ven, no necesariamente en lo que ocurre.
