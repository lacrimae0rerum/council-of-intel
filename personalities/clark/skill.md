# Skill

## Análisis target-centric: construir el modelo del objetivo

### Técnica central: el objetivo como sistema, no como descripción

La diferencia entre el análisis convencional y el análisis target-centric no es de contenido sino de estructura mental. El análisis convencional organiza el trabajo alrededor de los informes disponibles (¿qué dice el último SIGINT? ¿qué dijo el vendor?). El análisis target-centric organiza el trabajo alrededor del objetivo (¿qué necesitamos saber sobre el objetivo para responder la pregunta crítica?).

Robert Clark desarrolló este enfoque en "Intelligence Analysis: A Target-Centric Approach" (CQ Press, 2004) como respuesta al fracaso de la inteligencia sobre Iraq 2003: la comunidad tenía informes, pero no tenía un modelo del objetivo que le dijera qué preguntar y qué coleccionar.

---

### Paso 1 — Descomponer el objetivo en subsistemas

Todo objetivo es un sistema con componentes. La primera tarea es descomponer el objetivo en sus partes constitutivas. Para actores amenaza (APT, grupos criminales, Estados), los subsistemas típicos son:

- **Subsistema de mando:** quién toma decisiones, con qué proceso, con qué inputs.
- **Subsistema de capacidades:** qué herramientas, técnicas, infraestructura y personal están disponibles.
- **Subsistema de suministro:** de dónde vienen los recursos (financiación, tooling, personal, infraestructura).
- **Subsistema de comunicaciones:** cómo se coordinan los componentes del objetivo entre sí.
- **Subsistema de objetivos:** qué intenta conseguir el objetivo y con qué indicadores mide el éxito.

Para infraestructura técnica (redes C2, herramientas de malware), los subsistemas son:
- **Componentes de persistencia:** mecanismos de supervivencia en el host víctima.
- **Componentes de comunicación:** protocolos, dominios, IPs, cifrado.
- **Componentes de carga útil:** qué hace el malware una vez activo.
- **Componentes de control:** cómo el operador interactúa con el implante.

---

### Paso 2 — Mapear relaciones y flujos

Una vez identificados los componentes, el paso crítico es mapear las relaciones entre ellos. Las preguntas que guían el mapeo:

- ¿Qué componentes dependen de otros para funcionar?
- ¿Dónde hay un único punto de fallo (single point of failure)?
- ¿Qué relaciones son visibles desde fuera del objetivo y cuáles son opacas?
- ¿Hay relaciones que el objetivo intenta ocultar activamente?

Para cada relación, especificar el tipo de flujo: mando (órdenes de A a B), suministro (recursos de A a B), información (datos de A a B), financiación (dinero de A a B). La dirección del flujo importa para entender dependencias.

---

### Paso 3 — Identificar nodos de alta palanca

Un nodo de alta palanca es un punto del modelo cuya modificación tiene efecto desproporcionado en el sistema. Los nodos de alta palanca se identifican por:

- **Cuello de botella:** un componente que es el único camino para un flujo crítico.
- **Dependencia externa:** algo que el objetivo no puede producir internamente y necesita importar.
- **Punto de decisión único:** cuando solo una entidad puede tomar una decisión determinada.

En inteligencia de amenazas técnicas, los nodos de alta palanca típicos son:
- El dominio C2 principal (si se pierde, el operador pierde contacto con los implantes).
- El mecanismo de persistencia (si se limpia, el acceso se pierde al reiniciar).
- El proveedor de infraestructura (si se identifica y se notifica, puede bajar los servidores).

---

### Paso 4 — Trazar las lagunas de inteligencia

Para cada nodo del modelo, clasificar el estado del conocimiento:

**Conocido con evidencia:** hay fuentes que confirman la información sobre este nodo. La confianza en la representación de este nodo es alta.

**Inferido por relación:** no hay evidencia directa de este nodo, pero su existencia o características se infieren de la relación con nodos que sí tienen evidencia. La confianza es media; el nodo puede no existir como se modela.

**Supuesto sin evidencia:** el nodo se incluye en el modelo porque es típico de este tipo de objetivo, no porque haya evidencia de su existencia en este caso. La confianza es baja; el nodo puede ser incorrecto.

**Desconocido:** se sabe que debería existir un nodo aquí pero no hay ninguna información sobre él. Es una laguna pura.

---

### Paso 5 — Formular IIRs coleccionables

Una IIR mal formulada: "¿Cuáles son las intenciones del actor?"
Una IIR bien formulada: "¿El dominio de destino está asociado a registros de WHOIS de actores conocidos en bases de inteligencia de amenazas?"

La diferencia es la coleccionabilidad. Las IIRs del análisis target-centric tienen estas características:

- **Especificidad:** pregunta por un componente concreto del modelo, no por el objetivo en abstracto.
- **Coleccionabilidad:** puede responderse con fuentes reales disponibles o planificables (OSINT, SIGINT, HUMINT, forense, passive DNS).
- **Impacto en el modelo:** si la IIR se responde, qué parte del modelo cambia y cómo.
- **Prioridad:** ordenar las IIRs por impacto analítico, no por facilidad de respuesta.

---

### Aplicación en el dominio IC/CTI

**En análisis de malware/C2:**
El modelo target-centric descompone el malware en componentes (persistencia, comunicación, carga útil, control), mapea las relaciones (implante → C2, C2 → operador), identifica nodos de alta palanca (dominio C2, mecanismo de cifrado) y formula IIRs sobre los componentes desconocidos (¿hay un segundo canal de comunicación de backup? ¿quién registró el dominio?).

**En atribución:**
El modelo target-centric descompone al actor sospechoso en subsistemas (mando, capacidades, suministro, comunicaciones) y evalúa qué parte de cada subsistema se puede mapear con la evidencia disponible. Las lagunas de inteligencia identifican exactamente qué colección adicional se necesitaría para aumentar la confianza en la atribución.

**En warning intelligence:**
El modelo target-centric identifica los nodos de decisión del objetivo (¿cuándo y cómo decide escalar? ¿qué inputs necesita para tomar esa decisión?) e IIRs sobre el estado de esos nodos (¿está el nodo X en estado que precede a la escalada?).
