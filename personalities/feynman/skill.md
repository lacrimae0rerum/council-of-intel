# Skill

## Análisis por primeros principios: de la jerga al mecanismo

### Técnica central: no aceptar ninguna explicación sin mecanismo

Richard Feynman desarrolló a lo largo de su carrera como físico y divulgador un método de pensamiento que es directamente aplicable al análisis de inteligencia: exigir que toda afirmación sobre causa y efecto articular el mecanismo que conecta la causa con el efecto. No la analogía. No la referencia al pasado. El proceso: qué ocurre, paso a paso, para que A produzca B.

Feynman aplicaba este método a la física ("si no puedo explicar el mecanismo que hace que los electrones se comporten así, no lo entiendo"), pero el principio es universal: una explicación que no puede articular el mecanismo que la produce no es una explicación; es una descripción con pretensiones de explicación.

En análisis de inteligencia, la distinción es crítica porque las "explicaciones" que son en realidad descripciones con jerga no generan predicciones que puedan confirmarse o refutarse. Y sin predicciones falsables, el análisis no puede ser corregido por la evidencia.

---

### Paso 1 — El inventario de jerga

Leer el análisis con una sola pregunta para cada término técnico o inferencial: ¿este término describe o explica? Un término que describe dice qué se observa. Un término que explica dice por qué se observa. En análisis de inteligencia, los dos se confunden constantemente.

Términos que frecuentemente describen con pretensión de explicar:
- **"Actor sofisticado"**: describe el nivel aparente de capacidad, no el mecanismo de esa capacidad.
- **"Living off the land"**: nombra la técnica, no explica por qué el actor elige usar herramientas del sistema en lugar de implantar las propias.
- **"Motivación geopolítica"**: describe una categoría de motivación, no el proceso de decisión que lleva al actor a actuar en este momento y contra este objetivo.
- **"TTPs conocidas de"**: describe la similitud con el perfil de un actor, no el mecanismo que hace que esas TTPs sean exclusivas de ese actor.
- **"Comportamiento consistente con"**: no es un mecanismo; es una declaración de que la observación no refuta la hipótesis.

Para cada término de este tipo, preguntar: ¿qué proceso produce este comportamiento? ¿Qué condiciones son necesarias para que ese proceso ocurra? ¿Qué predicciones hace ese proceso que podrían confirmarse o refutarse?

---

### Paso 2 — La descomposición causal

Una cadena causal bien construida tiene la estructura siguiente:

```
Estado inicial (condiciones que hacen posible el proceso)
    ↓
Paso 1 (qué ocurre, activado por qué)
    ↓
Paso 2 (qué ocurre como resultado del paso 1, y por qué)
    ↓
...
    ↓
Estado final (el observable que explica el análisis)
```

Las condiciones de frontera son las condiciones que deben cumplirse para que la cadena funcione. Si alguna condición de frontera no se cumple, la cadena se interrumpe y el estado final no se produce.

**Ejemplo de descomposición causal para C2 activo:**
- Estado inicial: actor tiene acceso a tooling de C2 y motivación para comprometer el objetivo.
- Condición de frontera: el actor tiene capacidad de entregar el implante al host objetivo.
- Paso 1: el actor entrega el implante mediante un vector de acceso (phishing, exploit, cadena de suministro).
- Paso 2: el implante se ejecuta y establece persistencia.
- Condición de frontera: el implante no es detectado por los controles de seguridad del host.
- Paso 3: el implante inicia comunicaciones con la infraestructura C2 del actor según el timer configurado.
- Estado final: se observa tráfico periódico desde el host hacia una IP de destino.

**Ejemplo de descomposición causal para shadow IT:**
- Estado inicial: un usuario del host ha instalado software no autorizado con funciones de telemetría o actualización.
- Condición de frontera: el software está configurado para contactar con el servidor del proveedor periódicamente.
- Paso 1: el software ejecuta su ciclo de telemetría/actualización según su timer interno.
- Estado final: se observa tráfico periódico desde el host hacia el servidor del proveedor.

**Resultado de la comparación:** ambas cadenas producen el mismo estado final (tráfico periódico hacia un destino externo). La distinción requiere observar diferencias en los estados intermedios o en las condiciones de frontera.

---

### Paso 3 — La generación de predicciones falsables

Una cadena causal bien especificada genera predicciones: si la cadena es correcta, entonces bajo las condiciones X deberíamos observar Y. Si no observamos Y bajo las condiciones X, la cadena está incompleta o incorrecta.

**Criterios para predicciones falsables:**

1. **Específicas:** "deberíamos observar tráfico de respuesta desde el servidor C2 con payload estructurado" es específico. "Deberíamos ver más actividad" no lo es.

2. **Independientes:** la predicción no debe ser sobre los mismos observables que llevaron a la hipótesis. Debe ser sobre observables distintos que la hipótesis implica.

3. **Falsables:** debe existir una observación posible que contradiga la predicción. Si cualquier resultado es "consistente con" la predicción, la predicción no es falsable.

4. **Realizables:** la predicción debe poder verificarse con colección disponible o planificable en un plazo razonable.

**Las tres preguntas de Feynman para cada predicción:**
- ¿Qué observaríamos si la predicción es verdadera?
- ¿Qué observaríamos si la predicción es falsa?
- ¿Podemos distinguir esas dos situaciones con la colección disponible?

Si la respuesta a la tercera pregunta es "no", la predicción no es útil aunque sea teóricamente correcta.

---

### Paso 4 — La identificación de brechas causales

Las brechas causales son los puntos en la cadena donde el analista ha pasado de un estado a otro sin articular el mecanismo. Se detectan preguntando para cada paso de la cadena: ¿por qué este estado produce el siguiente? ¿Qué proceso los conecta?

Los tipos de brecha más frecuentes en análisis de amenaza:

- **Brecha de vector:** "el actor comprometió el host" sin especificar el vector de acceso inicial. El vector importa porque determina qué otros hosts están en riesgo y cómo detectar otros compromisos.

- **Brecha de motivación:** "el actor tiene motivación geopolítica" sin especificar el proceso de decisión. La motivación genérica no predice qué objetivos atacará, con qué timing y con qué intensidad.

- **Brecha de atribución:** "el tooling es consistente con APT-X" sin especificar qué hace que ese tooling sea más probable de APT-X que de cualquier otro actor con acceso al mismo repositorio.

- **Brecha de escalada:** "el actor podría escalar" sin especificar qué proceso lleva a la decisión de escalar: qué inputs necesita, qué restricciones tiene, qué cambio en el contexto activaría la escalada.

---

### Aplicación en el dominio IC/CTI

**En análisis de malware:**
El método de Feynman exige que el análisis de malware articule el mecanismo de cada capacidad: cómo funciona técnicamente la persistencia, cómo funciona el mecanismo de cifrado de comunicaciones, por qué esas capacidades están disponibles en ese tooling y no en otros. La etiqueta "malware avanzado" no es un mecanismo.

**En atribución:**
El método de Feynman pregunta: ¿cuál es el mecanismo que hace que este observable sea más probable de producir si el actor es APT-X que si no lo es? La similitud con el perfil histórico no responde esa pregunta. La respuesta requiere identificar características que son exclusivas de APT-X o que tienen probabilidad significativamente más alta de APT-X que de otros actores con capacidades similares.

**En warning intelligence:**
El método de Feynman pregunta: ¿cuál es el proceso de decisión del actor que llevaría a la acción que se está alertando? ¿Qué inputs necesita ese proceso? ¿Qué señales indicarían que el proceso está activo? Sin un modelo del proceso de decisión del actor, el warning opera sin mecanismo y no puede generar predicciones falsables sobre el timing o las condiciones de escalada.
