# Knowledge

## Doctrina de atribución en inteligencia

### El problema fundamental de la atribución

La atribución es uno de los problemas más difíciles en inteligencia porque combina tres dificultades simultáneas:

1. **El adversario tiene acceso al mismo conocimiento que el analista** sobre qué evidencia se usa para atribuir, y puede actuar para distorsionarla.
2. **La evidencia técnica más accesible es la más fácil de falsificar** o la más fácilmente compartida entre actores.
3. **La evidencia más difícil de falsificar** (HUMINT directo sobre el operador, SIGINT sobre la cadena de mando) es la menos disponible para la mayoría de analistas.

El Attribution Skeptic parte de esta asimetría estructural: la evidencia que más abunda en análisis CTI es técnica (IOCs, TTPs, malware) y es precisamente la que menos soporta la atribución por sí sola.

---

### El modelo de convergencia de clases

La doctrina de convergencia múltiple para la atribución tiene raíces en la IC clásica y en la criminología forense: la atribución robusta requiere que evidencia de tipos independientes apunte al mismo actor. La independencia entre clases es lo que hace que la hipótesis de falsa bandera sea progresivamente menos verosímil: para imitar a un actor en seis dimensiones simultáneamente se necesita acceso a su malware exclusivo, conocer sus patrones de comportamiento, usar su infraestructura histórica, atacar exactamente sus objetivos habituales, operar en sus horas de trabajo y tener los mismos intereses estratégicos. En el nivel más sofisticado de actores estatales, esto no es imposible, pero es mucho más costoso que la atribución por una sola clase.

La regla de tres clases mínimas es un umbral pragmático adoptado como estándar por las comunidades IC que trabajan con atribución pública. Por debajo de ese umbral, la probabilidad de error es suficientemente alta como para que la formulación "consistente con" sea más honesta que "atribuido a".

---

### Casos históricos de atribución errónea o explotada

**Shamoon y atribución a Irán (2012):** el análisis técnico del malware apuntó a Irán con razonable solidez técnica. Años después se documentaron variantes del mismo malware usadas en campañas con diferente vector de atribución, lo que indica que el tooling fue reutilizado más allá del contexto original.

**APT1 y el informe de Mandiant (2013):** el informe identificó una unidad del ejército chino (PLA Unit 61398) con un nivel de detalle sin precedentes en atribución pública CTI. La solidez se basó en convergencia de múltiples clases incluida la motivación estratégica. Es uno de los casos de referencia de atribución metodológicamente sólida, pero también de los que más debate generó sobre las implicaciones de hacer pública la atribución.

**Operación Aurora y Google (2010):** atribución a China basada principalmente en victimología (empresas tecnológicas occidentales específicas) y técnica. La motivación era clara; la evidencia técnica era sólida pero no exclusiva. Ejemplo de atribución probable pero no firme por las clases disponibles.

**False flag de CozyBear/APT29 en elecciones (2016):** los debates sobre si partes de la evidencia presentada fueron plantadas deliberadamente ilustran por qué la hipótesis de bandera falsa debe siempre ser evaluada, incluso cuando parece inverosímil.

---

### Principio de no-exclusividad de los IOCs

Un Indicador de Compromiso (IOC) técnico no pertenece exclusivamente al actor que lo generó en primera instancia. Una vez que un IOC se ha publicado en un feed o informe, puede ser:
- **Reutilizado deliberadamente:** un actor diferente lo usa para implicar al actor original.
- **Reutilizado comercialmente:** herramientas derivadas o builds basados en el mismo código base.
- **Reciclado operacionalmente:** el actor original re-usa su infraestructura en una nueva campaña; si fue comprometida o vendida, el nuevo usuario también tiene ese IOC.

La vida útil analítica de un IOC técnico para propósitos de atribución es aproximadamente el tiempo que tarde en ser publicado. Una vez publicado, su valor de atribución cae drásticamente porque cualquier actor que quiera imitar puede usarlo.

---

### El problema del Tooling-as-a-Service

La proliferación del Tooling-as-a-Service (TaaS) y el Malware-as-a-Service (MaaS) en el ecosistema criminal ha cambiado fundamentalmente el paisaje de la atribución técnica. En los años 2000, encontrar un implante personalizado en una intrusión señalaba con relativa precisión a un grupo con capacidades de desarrollo propias. En la actualidad:

- Cobalt Strike (hasta su cracking masivo) era usado por docenas de actores simultáneamente.
- Brute Ratel, Sliver, Havoc, Metasploit son de uso generalizado.
- Ransomware-as-a-Service (RaaS) con múltiples afiliados usa el mismo malware en operaciones de actores completamente distintos.
- Exploit kits comerciales son comunes a múltiples grupos.

Un análisis que identifica Cobalt Strike como base de atribución técnica está identificando un artefacto que usan potencialmente cientos de actores distintos. Su valor de especificidad para la atribución es mínimo sin personalización específica del perfil malleable o sin correlación con otras clases de evidencia.

---

### Doctrina de formulación de atribución

La formulación lingüística de la atribución tiene consecuencias operacionales y legales. El Attribution Skeptic aplica esta escala de formulación:

| Nivel de evidencia | Formulación |
|---|---|
| <3 clases | "Actividad con TTPs consistentes con [actor]. No atribuida." |
| 3 clases, al menos una media | "Probablemente relacionada con [actor] o actores con capacidades similares." |
| 3 clases, al menos dos altas | "Probable atribución a [actor] con confianza media. Pendiente de corroboración." |
| 4–5 clases, mayoría alta especificidad | "Alta confianza en atribución a [actor]." |
| 6 clases convergentes, incluyendo HUMINT/SIGINT | "Atribución firme a [actor]." |

La formulación "atribución firme" requiere HUMINT o SIGINT porque es la única clase de evidencia que puede reducir la hipótesis de falsa bandera a probabilidad negligible. Sin esa clase, la posibilidad de bandera falsa, aunque sea baja, sigue siendo analíticamente relevante.

---

### La atribución como decisión política y la atribución como análisis

El Attribution Skeptic distingue entre:

- **Atribución analítica:** el análisis que describe la evidencia disponible y concluye qué actor es el más probable responsable, con qué confianza y bajo qué supuestos.
- **Atribución pública:** la declaración formal de un Estado, organización o empresa que señala a un actor, con consecuencias legales, diplomáticas o reputacionales.

La atribución pública no necesita cumplir los mismos estándares metodológicos que la analítica: puede hacerse con evidencia incompleta por razones estratégicas, o puede no hacerse aunque la evidencia sea sólida. El Attribution Skeptic evalúa la solidez analítica, no la oportunidad política de la atribución pública.
