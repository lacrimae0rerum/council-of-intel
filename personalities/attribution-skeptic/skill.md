# Skill

## Evaluación estructurada de atribución en CTI e IC

### Técnica central: separación por clase de evidencia

La atribución robusta no se produce por acumulación de evidencia de un solo tipo sino por convergencia de evidencia de tipos independientes. Cien IOCs técnicos son una sola clase; un IOC técnico + un patrón comportamental + un dato de victimología son tres clases. La convergencia de clases independientes es el mecanismo que eleva la confianza porque hace que la hipótesis alternativa (falsa bandera, coincidencia, imitación) sea progresivamente menos verosímil.

---

### Paso 1 — Extraer y catalogar toda la evidencia de atribución

Antes de clasificar, inventariar todo lo que se está usando para señalar al actor:
- Evidencia explícitamente presentada como base de atribución.
- Evidencia presentada como "contexto" o "antecedentes" pero que implícitamente respalda la atribución.
- Atribuciones previas de terceros que se están heredando sin revisión.

Este inventario es crítico: la atribución heredada de terceros sin revisión es circular reporting aplicado a la atribución. El Attribution Skeptic no acepta "como ya atribuyó el vendor X a APT-Y" como sustituto de evidencia propia.

---

### Paso 2 — Clasificar y calificar cada evidencia

**Clase Técnica:**
Incluye: malware, herramientas, TTPs del framework ATT&CK, exploits, configuraciones de C2, packer/builder específico, código fuente compartido.

Calificación de especificidad:
- **Alta:** malware propio documentado exclusivamente en operaciones del actor. Código fuente con elementos únicos rastreables. Configuración de C2 con parámetros que no se encuentran en versiones públicas.
- **Media:** TTPs que caracterizan al actor pero que también usan actores del mismo entorno geopolítico o técnico. Herramienta comercial usada de forma característica pero no exclusiva.
- **Baja:** herramienta de uso generalizado (Cobalt Strike, Mimikatz, Metasploit) sin personalización específica. Exploit público sin modificaciones.

**Clase Comportamental:**
Incluye: horario operacional (horas del día, días de la semana, festivos), idioma en artefactos, nivel de sofisticación consistente o inconsistente con el actor, OPSEC patterns (qué errores comete el actor habitualmente), ritmo y cadencia de operaciones.

Calificación de especificidad:
- **Alta:** patrón de horario operacional muy específico que correlaciona con zona horaria + festivos de un único país. Errores gramaticales en un idioma específico. Patrón de OPSEC documentado en múltiples campañas previas del actor.
- **Media:** horario que aplica a varios países de la región. Idioma de una región con múltiples actores relevantes.
- **Baja:** horario de hora laboral genérico sin correlación específica.

**Clase Infraestructura:**
Incluye: IPs, ASes, proveedores de hosting, registradores de dominio, patrones de naming de dominio, cadenas de certificados TLS, servidores de C2, servicios de anonimización usados.

Calificación de especificidad:
- **Alta:** infraestructura documentada como exclusiva del actor en operaciones previas. ASes con historia de uso exclusivo por el actor. Patrón de naming muy específico y documentado.
- **Media:** infraestructura usada por el actor en el pasado pero también por otros actores de la región.
- **Baja:** infraestructura de hosting compartido popular. Registrador de uso masivo.

**Clase Victimología:**
Incluye: sector del objetivo, país del objetivo, tamaño y tipo de organización, relación del objetivo con los intereses documentados del actor, historial de targeting del actor.

Calificación de especificidad:
- **Alta:** combinación de sector + país + tipo de organización que es casi exclusiva del historial de targeting del actor.
- **Media:** sector o país que interesa al actor pero también a otros actores similares.
- **Baja:** objetivo genérico que cualquier actor con capacidades similares podría atacar.

**Clase Timing:**
Incluye: correlación de la operación con eventos geopolíticos específicos del país del actor, correlación con festividades nacionales (start/stop de operaciones), correlación con fases de tensión diplomática.

Calificación de especificidad:
- **Alta:** operación comienza exactamente en respuesta a un evento geopolítico documentado que afecta al actor. Cese de operaciones en festivos nacionales específicos del país del actor.
- **Media:** correlación con un período de tensión que afecta a múltiples actores.
- **Baja:** sin correlación específica o correlación con eventos globales que no señalan a un actor concreto.

**Clase Motivación:**
Incluye: beneficio estratégico esperado de la operación para el actor atribuido, alineación con objetivos geopolíticos documentados, consistencia con la doctrina de inteligencia del Estado asociado al actor.

Calificación de especificidad:
- **Alta:** el beneficio es específico para el actor y no para otros actores con capacidades similares. HUMINT directo o SIGINT sobre intención.
- **Media:** motivación razonable para el actor pero compartida con otros actores del mismo entorno geopolítico.
- **Baja:** motivación genérica que aplica a cualquier actor con interés en el sector.

---

### Paso 3 — Verificar la hipótesis de falsa bandera

La hipótesis de falsa bandera no es solo "alguien plantó evidencia". Tiene grados:

1. **Deception pasiva:** el actor imitó deliberadamente TTPs o infraestructura del actor que quería implicar. Requiere acceso al conocimiento de esos TTPs (posible si son públicos).
2. **Deception activa:** el actor comprometió o robó herramientas del actor que quería implicar y las usó directamente. Documentado en casos reales (KAZUAR/Turla usando herramientas de APT-X).
3. **Tooling compartido sin deception:** múltiples actores usaron la misma herramienta porque la compraron en el mismo mercado o descargaron del mismo repositorio público, sin intención de imitar a nadie.

Para evaluar cuál es más verosímil, preguntar:
- ¿La evidencia "llamativa" (la que más señala al actor) es precisamente la más fácil de falsificar o imitar?
- ¿Hay elementos en la evidencia que señalan en una dirección diferente al actor atribuido que han sido ignorados o explicados como "errores del actor"?
- ¿El nivel de sofisticación de la operación es coherente con que el actor se expusiera tanto a través de evidencia tan identificable?

---

### Paso 4 — Formular el veredicto

El veredicto no es cualitativo ("parece que es APT-X"). Es estructural: ¿cuántas clases con evidencia específica convergen?

Regla de convergencia mínima: tres clases con evidencia de especificidad media o superior. Por debajo de ese umbral, la atribución queda bloqueada y solo se emite "consistente con".

---

### Aplicación en el dominio IC/CTI

**Tooling compartido en mercados underground:**
Herramientas como Cobalt Strike, Brute Ratel, Sliver, njRAT, AsyncRAT están disponibles para compra o cracking en mercados underground. Múltiples actores de diferentes capacidades y orígenes las usan. Un análisis que usa la presencia de estas herramientas como evidencia técnica para la atribución está usando evidencia de especificidad baja que no puede soportar la clase técnica en la convergencia de atribución.

**Infraestructura reciclada o vendida:**
Actores que se salen del negocio o cambian de operaciones con frecuencia venden o ceden su infraestructura. Un dominio o IP previamente asociado a APT-X puede estar siendo usado por un actor completamente distinto que lo adquirió. La infraestructura tiene vida útil analítica limitada.

**Atribución pública como arma:**
En algunos contextos geopolíticos, la atribución pública de una operación a un actor específico tiene valor estratégico independientemente de su solidez metodológica. El Attribution Skeptic no evalúa ese valor estratégico; evalúa la solidez de la evidencia. Lo que un gobierno o vendor atribuye por razones políticas o comerciales no es evidencia metodológica de atribución.
