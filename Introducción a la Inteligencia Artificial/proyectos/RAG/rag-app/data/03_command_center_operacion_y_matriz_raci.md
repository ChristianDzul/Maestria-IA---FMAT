---
documento: HOR-OPS-003
titulo: Command Center — Modelo de Operación y Matriz RACI
version: 5.0
vigencia_desde: 2026-02-10
clasificacion: Uso Interno
propietario: Command Center (OP-CC)
---

# Command Center — Modelo de Operación y Matriz RACI

## 1. Misión

El Command Center (CC) de Banco Horizonte es el centro nervioso de la operación: detecta, clasifica, coordina y comunica todo evento que afecte o pueda afectar a un servicio del catálogo crítico. Opera 24 horas, 365 días al año, desde el piso 14 de Torre Horizonte, con sitio espejo en el CPD-Alterno de Monterrey.

El CC **no repara**. El CC **coordina la reparación**. Esta distinción es deliberada: quien coordina no debe tener las manos dentro del sistema, porque pierde visión de conjunto.

## 2. Estructura de turnos

| Turno | Horario | Dotación mínima |
|---|---|---|
| A (matutino) | 06:00 – 14:00 | 1 Jefe de Turno, 4 operadores, 1 analista de comunicación |
| B (vespertino) | 14:00 – 22:00 | 1 Jefe de Turno, 4 operadores, 1 analista de comunicación |
| C (nocturno) | 22:00 – 06:00 | 1 Jefe de Turno, 3 operadores |
| D (relevo y fines de semana) | Rotativo | 1 Jefe de Turno, 3 operadores |

El traspaso de turno (*handover*) dura 20 minutos, se documenta en la bitácora HOR-CC-LOG y debe incluir: incidentes abiertos con su severidad, cambios en curso, servicios en observación, guardias activas y riesgos previstos para el turno entrante. Un incidente P1 abierto nunca se traspasa sin llamada verbal entre Jefes de Turno.

## 3. Roles del CC

- **Jefe de Turno (Shift Lead).** Máxima autoridad operativa durante su turno. Declara severidad, convoca guardias y decide la activación del protocolo de Major Incident.
- **Operador de monitoreo.** Vigila tableros, atiende alertas, ejecuta triage de primer nivel y abre el ticket.
- **Incident Manager (IM).** Rol que se activa para P1 y P2. Conduce el puente técnico, controla la línea de tiempo y es el único que autoriza acciones sobre producción durante el incidente.
- **Analista de comunicación.** Redacta y distribuye los comunicados a negocio, dirección y, cuando aplica, al área regulatoria.
- **Scribe (relator).** Rol obligatorio en Major Incident. Registra la cronología minuto a minuto; es insumo forzoso del postmortem.

## 4. Herramientas

| Función | Herramienta | Notas |
|---|---|---|
| Observabilidad | HorizonteScope (stack propio sobre Prometheus + Grafana) | 1,840 tableros, 6,200 alertas configuradas |
| Gestión de tickets | ServiceDesk Horizonte (ITSM) | Nomenclatura INC-AAAA-NNNN |
| Puente de crisis | Sala Puente 8000 (audio dedicado) + sala de video de respaldo | Siempre abierta, sin necesidad de convocatoria |
| Localización de guardias | HorizonteOnCall (marcación en cascada con escalamiento automático) | Tres intentos por persona antes de escalar |
| Estatus público | status.bancohorizonte.mx | Publicación requiere visto bueno de Comunicación |

## 5. Matriz RACI

Convención: **R** = Responsable de ejecutar, **A** = Aprobador / rinde cuentas (uno solo por fila), **C** = Consultado, **I** = Informado.

### 5.1 RACI del ciclo de vida de incidentes

| Actividad | Command Center | Equipo técnico dueño | Dirección de Operaciones | Negocio afectado | Riesgos No Financieros | Cumplimiento / Regulación | Comunicación |
|---|---|---|---|---|---|---|---|
| Detección y registro | A/R | C | I | I | — | — | — |
| Clasificación de severidad | A/R | C | I | C | I | — | — |
| Convocatoria de guardias | A/R | R | I | I | — | — | — |
| Diagnóstico técnico | C | A/R | I | I | — | — | — |
| Decisión de mitigación (workaround) | R | C | A | C | I | — | — |
| Ejecución de cambio de emergencia | C | R | A | I | I | — | — |
| Declaración de Major Incident | A/R | C | C | I | I | I | I |
| Activación del Comité de Crisis | R | I | A | C | C | C | C |
| Comunicación a clientes | C | — | C | C | — | C | A/R |
| Notificación a CNBV / Banxico | C | C | C | I | C | A/R | I |
| Restablecimiento y confirmación | R | A/R | I | C | I | I | I |
| Cierre del incidente | A/R | C | I | C | I | I | — |
| Elaboración del postmortem | R | A/R | C | C | C | I | — |
| Validación del postmortem | C | C | C | I | A/R | C | — |
| Seguimiento de acciones correctivas | C | R | A | I | C | I | — |
| Registro del evento de pérdida operacional | I | C | I | C | A/R | C | — |

### 5.2 RACI de gestión de cambios en servicios críticos

| Actividad | Solicitante | Equipo técnico | CAB | Command Center | Riesgos |
|---|---|---|---|---|---|
| Solicitud de cambio (RFC) | A/R | C | I | I | — |
| Evaluación de impacto y rollback | C | A/R | C | C | I |
| Aprobación de cambio normal | C | C | A/R | I | I |
| Aprobación de cambio de emergencia | C | R | I | A | I |
| Ventana de ejecución | I | R | I | A | — |
| Verificación post-cambio | I | R | I | A/R | — |
| Reversión (rollback) | I | R | I | A | I |

### 5.3 Reglas de interpretación del RACI

1. **Un solo A por fila.** Si dos áreas creen tener la A, la ambigüedad se resuelve a favor del Command Center durante el incidente y a favor de Riesgos después del cierre.
2. La **A** no se delega hacia abajo; la **R** sí.
3. Un área con **C** que no responde en el tiempo de SLA no bloquea la decisión: se documenta la consulta no atendida y se avanza.
4. Un área marcada con **I** no puede exigir participación en la decisión después del hecho.
5. El RACI aplica igual en horario hábil y no hábil; lo que cambia es la persona, no el rol.

## 6. Indicadores del Command Center

| Indicador | Definición | Meta 2026 | Resultado Q2-2026 |
|---|---|---|---|
| MTTD | Tiempo medio de detección | ≤ 4 min | 3.2 min |
| MTTA | Tiempo medio de reconocimiento | ≤ 6 min | 5.1 min |
| MTTR P1 | Tiempo medio de restauración P1 | ≤ 120 min | 141 min |
| % detección proactiva | Incidentes detectados por monitoreo antes que por cliente | ≥ 85% | 78% |
| Ruido de alertas | Alertas sin acción / alertas totales | ≤ 20% | 34% |
| Reincidencia a 30 días | Incidentes con misma causa raíz en 30 días | ≤ 5% | 9% |
| Cumplimiento de handover | Traspasos documentados completos | 100% | 96% |

Los dos indicadores en rojo sostenido durante 2026 son el **ruido de alertas** (34% contra meta de 20%) y la **reincidencia a 30 días** (9% contra meta de 5%). Ambos tienen plan de remediación aprobado por COTEC con fecha compromiso al 31 de diciembre de 2026.
