---
documento: HOR-OPS-002
titulo: Catálogo de Servicios Críticos, SLA y SLO
version: 7.1
vigencia_desde: 2026-03-01
clasificacion: Uso Interno
propietario: Command Center (OP-CC)
aprobado_por: COTEC
---

# Catálogo de Servicios Críticos, Acuerdos de Nivel de Servicio (SLA) y Objetivos de Nivel de Servicio (SLO)

## 1. Alcance y definiciones

- **SLA (Service Level Agreement):** compromiso formal frente al cliente interno o externo, con consecuencias contractuales o regulatorias en caso de incumplimiento.
- **SLO (Service Level Objective):** meta interna de operación, siempre más exigente que el SLA, que se usa para gestionar el servicio antes de llegar al umbral de incumplimiento.
- **RTO (Recovery Time Objective):** tiempo máximo tolerable para restablecer el servicio después de una interrupción.
- **RPO (Recovery Point Objective):** pérdida máxima tolerable de información medida en tiempo.
- **Error budget:** margen de indisponibilidad consumible en el mes sin incumplir el SLO. Cuando se agota, se congelan los cambios no correctivos del servicio.
- **Ventana de medición:** mes calendario natural, hora del centro de México.

## 2. Catálogo de servicios críticos (Tier 0 y Tier 1)

| ID | Servicio | Tier | Disponibilidad SLA | SLO interno | RTO | RPO | Dueño técnico | Dueño de negocio |
|---|---|---|---|---|---|---|---|---|
| SVC-001 | SPEI — envío y recepción | 0 | 99.90% | 99.95% | 15 min | 0 | OP-PAG | Dirección de Pagos |
| SVC-002 | Switch de tarjetas / autorizaciones | 0 | 99.95% | 99.98% | 10 min | 0 | OP-PAG | Banca de Personas |
| SVC-003 | Core bancario — transaccional en línea | 0 | 99.90% | 99.95% | 20 min | 0 | OP-PLT | Operaciones |
| SVC-004 | App móvil Horizonte Móvil | 1 | 99.70% | 99.90% | 30 min | 5 min | OP-PLT | DN-CLI |
| SVC-005 | Banca en línea (web empresarial) | 1 | 99.70% | 99.90% | 30 min | 5 min | OP-PLT | Banca Empresarial |
| SVC-006 | Red de cajeros automáticos (ATM) | 1 | 99.50% | 99.80% | 45 min | 0 | OP-PLT | Banca de Personas |
| SVC-007 | Cierre batch nocturno del core | 0 | Ventana 22:00–04:30 | Fin ≤ 03:30 | 120 min | 0 | OP-PLT | Contraloría |
| SVC-008 | CoDi | 2 | 99.50% | 99.70% | 60 min | 5 min | OP-PAG | Dirección de Pagos |
| SVC-009 | Contact center (telefonía + CRM) | 1 | 99.50% | 99.80% | 45 min | 15 min | OP-PLT | DN-CLI |
| SVC-010 | Originación de crédito PyME | 2 | 99.00% | 99.50% | 4 h | 30 min | OP-PLT | DN-CRE |
| SVC-011 | Domiciliaciones y cámara (CECOBAN) | 1 | Ciclo diario cumplido | Envío ≤ 13:00 | 3 h | 0 | OP-PAG | Dirección de Pagos |
| SVC-012 | Motor antifraude transaccional | 0 | 99.95% | 99.98% | 10 min | 0 | OP-CIB | Riesgos |

> Nota de lectura: Tier 0 = interrupción con impacto sistémico o regulatorio inmediato. Tier 1 = impacto masivo a clientes. Tier 2 = impacto acotado o diferible.

## 3. SLA de atención (tiempos del Command Center)

Estos tiempos aplican desde la **detección** (alerta automática o reporte) y son los que se auditan.

| Severidad | Tiempo de reconocimiento (ACK) | Tiempo de primer diagnóstico | Objetivo de restauración (MTTR) | Frecuencia de comunicación |
|---|---|---|---|---|
| P1 | 5 minutos | 20 minutos | 2 horas | Cada 30 minutos |
| P2 | 15 minutos | 60 minutos | 8 horas | Cada 2 horas |
| P3 | 4 horas | 8 horas | 3 días hábiles | Diaria |
| P4 | 1 día hábil | 3 días hábiles | 15 días hábiles | Semanal |

Para Major Incident, la frecuencia de comunicación se reduce a cada 20 minutos y se agrega un reporte ejecutivo cada hora.

## 4. Cálculo de disponibilidad

```
Disponibilidad (%) = ((Minutos del mes − Minutos de indisponibilidad computable) / Minutos del mes) × 100
```

Reglas de cómputo:

1. Solo computa la indisponibilidad **no planeada**. Las ventanas de mantenimiento publicadas con al menos 5 días hábiles de anticipación y aprobadas por COTEC quedan excluidas.
2. La degradación severa (latencia p95 superior a 3× la línea base durante más de 10 minutos continuos) computa como indisponibilidad al 50%.
3. La indisponibilidad parcial por región o por canal computa de forma proporcional al porcentaje de transacciones afectadas.
4. El reloj inicia en el primer evento verificable (alerta, log o reporte de cliente), no en la declaración del incidente.

### 4.1 Minutos permitidos por nivel

| Objetivo | Minutos/mes | Minutos/año |
|---|---|---|
| 99.99% | 4.3 | 52.6 |
| 99.95% | 21.6 | 262.8 |
| 99.90% | 43.2 | 525.6 |
| 99.70% | 129.6 | 1,576.8 |
| 99.50% | 216.0 | 2,628.0 |

## 5. Umbrales de impacto para clasificación

Los siguientes umbrales se utilizan para asignar severidad de forma objetiva (ver HOR-OPS-004).

| Dimensión | P1 | P2 | P3 | P4 |
|---|---|---|---|---|
| Clientes afectados | > 50,000 o segmento completo | 5,000–50,000 | 500–5,000 | < 500 |
| Transacciones fallidas | > 5% del volumen horario | 1–5% | 0.2–1% | < 0.2% |
| Impacto financiero estimado | > 5 MDP | 0.5–5 MDP | 50 K–500 K MDP | < 50 K |
| Exposición regulatoria | Notificable a CNBV/Banxico | Probable notificación | Registrable | Sin exposición |
| Servicio afectado | Tier 0 sin alternativa | Tier 0 degradado o Tier 1 caído | Tier 1 degradado o Tier 2 caído | Tier 2 degradado |

Basta con cumplir **una** dimensión para asignar la severidad correspondiente. En caso de duda entre dos niveles, se clasifica en el **más severo** y se reclasifica posteriormente (regla de "escalar primero, ajustar después").

## 6. Régimen de incumplimiento

- **Incumplimiento de SLO:** se congelan los cambios no correctivos del servicio hasta cerrar las acciones del postmortem.
- **Incumplimiento de SLA dos meses consecutivos:** el dueño técnico presenta plan de remediación al COTEC con fechas comprometidas.
- **Incumplimiento de SLA con impacto regulatorio:** se abre evento de riesgo operacional en la base de datos histórica y se evalúa el reporte correspondiente a la autoridad.
- **Incumplimiento de proveedor crítico:** se aplican las penalizaciones del contrato y se activa la revisión prevista en la política de servicios de apoyo tecnológico.

## 7. Ventanas de mantenimiento autorizadas

| Servicio | Ventana estándar | Frecuencia máxima |
|---|---|---|
| Core bancario | Domingo 02:00–05:00 | 1 vez al mes |
| Canales digitales | Martes y jueves 01:00–03:00 | 2 veces al mes |
| Switch de tarjetas | Domingo 03:00–04:30 | 1 vez cada dos meses |
| SPEI | Sin ventana; solo cambios en caliente con doble validación | N/A |

El servicio SPEI no admite ventana de mantenimiento con desconexión, dado el esquema de operación continua del sistema de pagos.
