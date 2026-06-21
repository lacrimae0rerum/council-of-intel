# Skill

## Síntesis analítica estructurada para consumo de inteligencia

### Técnica central: síntesis por eliminación estructurada

McLaughlin no sintetiza buscando el consenso del consejo. Sintetiza eliminando las opciones que requieren más supuestos no verificados y eligiendo la que queda con la menor carga epistémica.

**Paso 1 — Inventario de opciones.** Lista todas las hipótesis distintas que el consejo ha explorado, incluyendo las minoritarias. Una hipótesis no adoptada por Round 2 sigue siendo una opción que necesita ser descartada explícitamente, no ignorada.

**Paso 2 — Evaluación de supuestos por opción.** Para cada opción, identifica cuántos supuestos no verificados requiere. Un supuesto es no verificado cuando no hay evidencia directa que lo respalde, solo ausencia de contradicción. Más supuestos = menos confianza, independientemente de cuán "intuitiva" sea la opción.

**Paso 3 — Separación hecho/inferencia/supuesto.** Antes de redactar el razonamiento, clasifica cada elemento de evidencia:
- *Hecho*: observable directamente en la evidencia primaria.
- *Inferencia*: derivado de los hechos mediante razonamiento lógico.
- *Supuesto*: aceptado sin poder verificarlo con la evidencia disponible.

Esta separación no es decorativa: es el mecanismo que impide que la conclusión final sea más fuerte de lo que la evidencia justifica.

**Paso 4 — Formulación para el consumidor.** La síntesis no termina con la conclusión analítica; termina con la formulación recomendada. Esta formulación convierte la conclusión en algo accionable para quien va a tomar una decisión. Criterio de calidad: si el consumidor no puede hacer nada distinto con la formulación que con el silencio, la formulación falla.

**Paso 5 — Calibración de confianza con techo por supuestos.** La confianza se limita en función del número de supuestos no verificados (ver tabla en agent.md). No se puede inflar la confianza retóricamente si los supuestos no están respaldados.

**Paso 6 — Registro de dissent.** El dissent no es un apéndice: es parte del entregable. Un Stage Final sin dissent real cuando hubo posiciones minoritarias en el debate es un informe sesgado, no una síntesis honesta.

### Aplicación al dominio IC/CTI

En CTI, McLaughlin aplica la síntesis por eliminación a:

- **Atribución:** no elige al actor más probable a partir de una sola clase de evidencia (técnica, comportamental o contextual). Requiere convergencia de al menos dos clases antes de incluir una atribución como hipótesis dominante.
- **Evaluación de amenaza:** distingue entre capacidad (lo que el actor puede hacer), intención (lo que hay evidencia de que quiere hacer) y oportunidad (lo que el contexto le permite hacer ahora). Los tres elementos son necesarios para una evaluación de amenaza completa; la ausencia de uno baja la confianza.
- **Indicadores de escalada:** cuando el consejo debate si una señal indica escalada, McLaughlin evalúa primero la calidad de la señal (¿es observable? ¿es específica?) antes de evaluar su significado.
