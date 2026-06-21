# Skill

## Calibración de lenguaje estimativo

### Técnica central: la ambigüedad probabilística como defecto analítico

Sherman Kent demostró empíricamente en la CIA que términos como "probable" o "es posible" generan interpretaciones numéricas radicalmente distintas entre analistas y policymakers. En un estudio interno, analistas que usaban "probable" tenían en mente probabilidades que iban del 55% al 90%, según el individuo. Esa ambigüedad no es un problema estilístico; es un problema de comunicación que puede producir decisiones distintas basadas en el mismo análisis.

La técnica de calibración de Kent resuelve esto en cuatro pasos: inventariar, traducir, verificar consistencia y reescribir.

---

### Paso 1 — Inventariar el lenguaje estimativo del análisis

Leer el análisis con foco en las expresiones que indican probabilidad, incertidumbre o confianza. Catalogarlas exhaustivamente: no solo las expresiones explícitas ("probablemente") sino las implícitas ("no hay indicios de", "parece ser", "todo apunta a").

Tipos de expresión a buscar:
- **Calificadores directos de probabilidad:** probable, posible, improbable, casi cierto.
- **Calificadores de confianza:** con alta confianza, con evidencia sólida, con base limitada.
- **Expresiones de exclusión:** "no puede descartarse", "no hay indicios de que no".
- **Expresiones de tendencia:** "todo apunta a", "el conjunto de la evidencia sugiere".
- **Calificadores cuantitativos no calibrados:** "riesgo significativo", "probabilidad elevada", "amenaza considerable".

---

### Paso 2 — Traducir al sistema de calificadores normalizados

Para cada expresión catalogada, asignar el rango normalizado o marcar como ambiguo:

**Tabla de traducción normalizada:**

| Expresión frecuente | Rango normalizado |
|---|---|
| "casi con certeza" / "es prácticamente seguro" | 95–99% |
| "muy probablemente" / "muy probable" | 80–95% |
| "probablemente" / "es probable" | 55–80% |
| "hay probabilidad aproximadamente igual" | 45–55% |
| "posiblemente" / "es posible" | 25–55% |
| "improbablemente" / "es improbable" | 5–25% |
| "muy improbablemente" | 1–5% |
| "casi imposible" | <1% |

**Expresiones que requieren reescritura (no tienen rango directo):**
- "riesgo significativo" → reescribir como "posible (X–Y%)" o "probable (X–Y%)" con rango específico.
- "no puede descartarse" → reescribir como "posible (X–Y%)" o al menos "no desestimable (>5%)".
- "probabilidad razonable" → reescribir con rango específico.
- "preocupación considerable" → no es estimativo; reescribir como evaluación de probabilidad.
- "todo apunta a" → implica "probable" pero sin compromiso; reescribir con rango.

---

### Paso 3 — Verificar la separación entre probabilidad y confianza

Esta distinción es la más crítica y la más frecuentemente ignorada:

**Probabilidad:** la estimación de cuán verosímil es la hipótesis. Responde a "¿qué tan probable es que esto sea verdad?"

**Confianza:** la solidez de la evidencia que respalda la estimación. Responde a "¿qué tan seguros estamos de esa probabilidad?"

Ejemplos de la distinción:

- "Probable (65–75%) con confianza media": creemos que es probable, pero la evidencia es limitada y la estimación podría cambiar con nueva información.
- "Posible (30–40%) con confianza alta": creemos que es solo posible (no probable), pero la evidencia que nos lleva a esa conclusión es sólida.
- "Probable (65–75%) con confianza alta": la hipótesis es probable y la evidencia que respalda esa estimación es sólida.

Cuando el análisis usa expresiones como "con alta confianza que X es probable", el analista está combinando las dos dimensiones en una sola frase. Esto puede ser correcto si se interpreta como "probable con alta confianza", pero requiere verificación.

---

### Paso 4 — Verificar consistencia interna

Si el análisis presenta múltiples hipótesis, las probabilidades asignadas deben ser coherentes:

**Para hipótesis mutuamente excluyentes y exhaustivas:** la suma de sus probabilidades debe ser 100%.

**Para hipótesis mutuamente excluyentes pero no exhaustivas:** la suma debe ser ≤100%; el resto representa la probabilidad de hipótesis no contempladas.

**Inconsistencia frecuente:** el análisis dice que H1 es "probable" (55–80%) y H2 es "improbable" (5–25%), lo que deja 20–40% sin hipótesis asignada. Si el espacio de hipótesis no está cerrado, debe declararse explícitamente.

---

### Paso 5 — Reescribir la estimación con lenguaje calibrado

La reescritura no cambia la conclusión del análisis; cambia la forma en que se expresa para que sea accionable. La estimación reescrita debe:

1. Usar calificadores de la escala normalizada.
2. Especificar el rango numérico entre paréntesis cuando el calificador verbal puede ser ambiguo.
3. Separar la probabilidad de la confianza cuando ambas son relevantes.
4. Declarar si el espacio de hipótesis está cerrado o no.

---

### Aplicación en el dominio IC/CTI

**En análisis de C2:** el lenguaje más frecuentemente no calibrado es "indica que" o "consistente con". "Consistente con C2" no es una estimación de probabilidad; indica que no hay inconsistencia, pero dice nada sobre la probabilidad. La versión calibrada: "Los observables son consistentes con C2 activo (hipótesis probable, 60–75%) y también con shadow IT (hipótesis posible, 20–30%). La confianza en estas estimaciones es media dado que no hay forense de endpoint."

**En atribución:** el lenguaje más frecuentemente no calibrado es "hay evidencia de que". "Hay evidencia de que el actor es APT-X" no es una estimación; es una declaración sobre la existencia de evidencia. La versión calibrada: "La evidencia disponible respalda la atribución a APT-X como hipótesis probable (55–65%) con confianza media."

**En warning:** el lenguaje más frecuentemente no calibrado es "el riesgo es elevado" o "existe amenaza significativa". "Riesgo elevado" no es una estimación de probabilidad de ningún evento específico. La versión calibrada requiere especificar el evento: "La probabilidad de un ataque contra [objetivo] en [plazo] es posible (35–55%) con confianza media."
