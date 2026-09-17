# Command Center Bancario

**Clasificación:** SINTÉTICO

## 1. Objetivo

El Command Center coordina la respuesta ante eventos que afectan o pueden afectar procesos críticos. No sustituye a los equipos especialistas; coordina, mantiene una visión transversal, controla tiempos, comunicación, escalación y recuperación.

## 2. Responsabilidades

- Monitorear eventos relevantes.
- Determinar severidad inicial.
- Nombrar Incident Manager.
- Convocar áreas.
- Mantener timeline.
- Coordinar comunicaciones.
- Vigilar SLA/OLA.
- Registrar decisiones.
- Coordinar recuperación.
- Solicitar validación de negocio.
- Cerrar el incidente.
- Solicitar postmortem.

## 3. Roles

### Incident Manager
Responsable de coordinar el incidente de extremo a extremo.

### Technical Lead
Coordina diagnóstico y recuperación técnica.

### Business Lead
Determina impacto al negocio y valida recuperación funcional.

### Communications Lead
Administra comunicaciones internas y externas autorizadas.

### Scribe
Mantiene timeline, decisiones y evidencias.

## 4. Flujo

Detectar → Triage → Clasificar → Declarar incidente mayor → Convocar → Diagnosticar → Mitigar → Recuperar → Validar → Monitorear → Cerrar → Postmortem.

## 5. Reglas de activación sintéticas

Activar Command Center cuando:
- un proceso crítico está indisponible;
- existe impacto masivo;
- existe riesgo financiero significativo;
- existe pérdida potencial de integridad de datos;
- múltiples áreas están involucradas;
- se aproxima o incumple el RTO;
- un incidente tecnológico amenaza un servicio crítico.

## 6. Timeline mínimo

Cada evento debe registrar:
`timestamp | evento | responsable | evidencia | decisión | siguiente acción`

## 7. Comunicación

Actualizaciones sintéticas:
- P1: cada 15 minutos.
- P2: cada 30 minutos.
- P3: cada 60 minutos.

La frecuencia puede cambiar si Incident Manager determina que el impacto requiere mayor frecuencia.
