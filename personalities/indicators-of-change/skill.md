# Skill

## Diseño de indicadores de cambio analítico

### Técnica central: convertir una estimación en un sistema de actualización

Una estimación de inteligencia que no define las condiciones bajo las cuales debe ser revisada es una estimación estática. En entornos donde los actores evolucionan, las TTPs cambian y el contexto se mueve, una estimación estática se vuelve obsoleta sin que nadie lo sepa. El diseño de indicadores de cambio transforma la estimación en un sistema de monitorización activo.

El principio operativo: si ningún observable que emerge en los próximos días puede cambiar la estimación, la estimación no está conectada al mundo real. Los indicadores de cambio son los conectores.

---

### Paso 1 — Extraer las predicciones implícitas de la estimación

Toda estimación predice, al menos implícitamente, cómo evolucionará la situación. El indicador de cambio parte de esas predicciones.

Protocolo:
1. Lee la estimación y pregunta: "Si esta estimación es correcta, ¿qué debería ocurrir en los próximos días/semanas que sería coherente con ella?"
2. Pregunta también: "Si esta estimación es correcta, ¿qué debería NO ocurrir?"
3. Las respuestas a la primera pregunta son indicadores de confirmación. Las respuestas a la segunda son indicadores de ausencia crítica.
4. Pregunta finalmente: "¿Qué podría ocurrir que haría que la estimación ya no fuera válida?" La respuesta son los indicadores de revocación.

---

### Paso 2 — Formular el observable de forma específica

Un observable es la materialización concreta del indicador: algo que puede ser registrado por un sensor, detectado por una herramienta o reportado por una fuente.

Distinguir entre:
- **Observable directo:** detectable sin inferencia (el dominio existe, el proceso corre, el email fue enviado).
- **Observable indirecto:** requiere inferencia para su interpretación (el volumen de tráfico supera un umbral, el número de dominios nuevos excede la línea base).

Los observables directos son más fiables como indicadores; los indirectos requieren definición de la línea base y pueden producir falsos positivos.

---

### Paso 3 — Establecer el umbral con precisión

Un umbral mal definido produce falsas alarmas o activaciones tardías. Los umbrales más robustos combinan:
- **Condición categórica:** "primera aparición de X", "confirmado por dos fuentes independientes".
- **Condición cuantitativa:** "≥3 eventos en 7 días", "superación de 2σ sobre baseline de 30 días".
- **Condición temporal:** "si no se observa en las primeras 48h de la alerta inicial".

Para indicadores de ausencia crítica, el umbral es siempre temporal: "a día N, si el indicador no ha aparecido".

---

### Paso 4 — Mapear la fuente de colección disponible

Para cada observable, identificar la herramienta, fuente o proceso de colección que puede detectarlo:

**Colección técnica CTI:**
- SIEM: eventos de red, autenticación, endpoint.
- EDR: procesos, inyecciones, persistencia, memoria.
- NetFlow / pcap: tráfico de red, DNS, beacons.
- DNS pasivo: dominios nuevos, cambios de resolución.
- Sandbox feeds (VirusTotal, AnyRun): nuevas muestras de malware.
- Feeds CTI comerciales: IOCs, nuevas infraestructuras del actor.

**Colección OSINT:**
- Monitores de registradores de dominio.
- Feeds de certificados TLS (crt.sh).
- Repositorios de código (GitHub, pastebin).
- Canales de comunicación del actor (foros, Telegram).

**Colección de contexto:**
- Informes sectoriales de amenazas.
- Notificaciones de socios o CERT.
- Victimología externa (si las víctimas comparten).

Si no hay fuente disponible, el indicador es una laguna de monitorización: relevante pero no monitorizable con colección actual.

---

### Paso 5 — Calibrar el timing en función del tipo de indicador

El timing no es una predicción de cuándo ocurrirá el evento; es un horizonte temporal dentro del cual el indicador es informativamente relevante.

**Indicadores de confirmación:** el timing define cuándo deberían aparecer si la hipótesis es correcta. Si no aparecen en ese plazo, se activa el indicador de ausencia crítica correspondiente.

**Indicadores de escalada:** pueden aparecer en cualquier momento del ciclo; su activación importa independientemente del timing.

**Indicadores de revocación:** también pueden aparecer en cualquier momento. La diferencia con los de escalada es la dirección del cambio: los de revocación contradicen la estimación en vez de reforzarla.

**Regla de timing conservador:** siempre usar el plazo más corto dentro del que el indicador podría razonablemente aparecer como base. Si el plazo se extiende sin activación, revisar a la baja la confianza antes de llegar al límite del timing.

---

### Aplicación en el dominio IC/CTI

**En análisis de C2 activo:**
Los indicadores prioritarios casi siempre son los que resuelven la ambigüedad más rápido: identificación del proceso (EDR, inmediato), presencia de persistencia (EDR, inmediato) y cambio o rotación de infraestructura (DNS pasivo, corto plazo). La ausencia de identificación del proceso tras 72h es un indicador de ausencia crítica que reduce la confianza en C2 clásico e introduce la hipótesis de técnica de evasión avanzada o falso positivo.

**En warning intelligence:**
Los indicadores más valiosos en warning son los preparatorios: infraestructura nueva, muestras de lure, reconocimiento. Aparecen antes del evento y permiten actuar antes de que la campaña se materialice. La ausencia de indicadores preparatorios en el plazo esperado reduce la confianza en la estimación de timing, no necesariamente en la estimación de amenaza.

**En atribución:**
Los indicadores de cambio en atribución suelen ser negativos (revocan la atribución): mismo TTP observado en campaña de actor diferente en el mismo periodo, infraestructura del actor atribuido documentada como compartida o vendida, victimología inconsistente con el historial del actor.
