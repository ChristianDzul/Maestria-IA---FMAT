---
documento: HOR-PM-014
titulo: Postmortem INC-2026-0417 — Indisponibilidad de SPEI por expiración de certificado
version: 1.0 (final, validado)
fecha_incidente: 2026-07-14
fecha_documento: 2026-07-21
clasificacion: Confidencial
severidad: P1 / Major Incident
validado_por: Riesgos No Financieros (RG-RNF)
---

# Postmortem INC-2026-0417

## 1. Resumen ejecutivo

El martes 14 de julio de 2026, entre las 11:32 y las 14:20 horas del centro de México, Banco Horizonte no pudo enviar ni recibir transferencias a través del SPEI. La causa raíz fue la expiración de un certificado digital utilizado por el módulo de firma de mensajes del componente SPEI-ENG. El certificado venció a las 11:31:59, exactamente un año después de su emisión.

- **Duración total:** 2 horas 48 minutos.
- **Duración de indisponibilidad total:** 2 horas 16 minutos (11:32–13:48). Los últimos 32 minutos correspondieron a operación degradada durante el drenado de colas.
- **Clientes afectados:** 384,000 con al menos una operación fallida.
- **Operaciones afectadas:** 291,400 órdenes de salida no enviadas; 176,800 recepciones no acreditadas en tiempo.
- **Impacto financiero directo estimado:** 6.8 MDP (devolución de comisiones, intereses compensatorios, horas extraordinarias y penalizaciones contractuales con clientes empresariales).
- **Criterios de amplificación cumplidos:** 1 (duración), 2 (alcance), 3 (sistema de pagos), 6 (regulatorio).

## 2. Línea de tiempo

| Hora | Evento |
|---|---|
| 11:31:59 | Expira el certificado `spei-signing-prod-2025`. |
| 11:32:10 | Primeros errores SPEI-E101 (firma inválida) en la cola de salida. |
| 11:33 | Alerta automática por tasa de error en `SPEI_OUT`. Operador de turno B reconoce. |
| 11:36 | Se abre INC-2026-0417 con severidad P1. Jefe de Turno declara y abre Puente 8000. |
| 11:38 | Convocatoria simultánea a guardias de Pagos, Infraestructura y Ciberseguridad. |
| 11:41 | Se ejecuta el triage del runbook HOR-RBK-101. Pasos 1 a 4 sin hallazgo. |
| 11:52 | Hipótesis inicial errónea: se sospecha del enlace dedicado. Se conmuta al enlace de respaldo (sección 6.2). Sin efecto. |
| 12:04 | Se descarta problema de red. Se escala a N3 de Pagos. |
| 12:09 | Se declara Major Incident por criterio 3 (más de 10 minutos de afectación al sistema de pagos). |
| 12:11 | Se notifica al Enlace Banco de México, quien informa al administrador del sistema. |
| 12:18 | Se activa Comité de Crisis. |
| 12:24 | N3 identifica en los logs del módulo de firma el rechazo por certificado expirado. Causa confirmada. |
| 12:31 | Se verifica la existencia de certificado de contingencia en el almacén seguro. **No existe vigente.** |
| 12:35 | Se inicia el procedimiento de emisión de emergencia con la autoridad certificadora. |
| 12:40 | Célula Negocio habilita comunicación a clientes y refuerza contact center. |
| 13:14 | Se recibe el nuevo certificado. |
| 13:22 | Instalación con doble control de custodios. |
| 13:31 | Reinicio del módulo de firma. Primeras firmas exitosas. |
| 13:36 | Transferencia de prueba de 1.00 MXN enviada y acusada correctamente. |
| 13:48 | Se reabre la admisión de órdenes. Inicia el drenado de la cola acumulada. |
| 14:20 | Cola drenada. Métricas en rango. Se declara restablecimiento. |
| 14:50 | Cierre del Major Incident. Inicia conciliación (sección 7 del runbook). |
| 18:00 | Conciliación concluida sin pagos duplicados. |
| 21:40 | Reversos de comisiones aplicados a 27,300 clientes. |

## 3. Causa raíz

**Causa inmediata.** Expiración del certificado digital de firma del componente SPEI-ENG.

**Causa raíz (análisis de los cinco porqués):**

1. *¿Por qué falló el SPEI?* Porque los mensajes no pudieron firmarse.
2. *¿Por qué no pudieron firmarse?* Porque el certificado había expirado.
3. *¿Por qué expiró sin renovarse?* Porque no existía alerta de vencimiento para ese certificado.
4. *¿Por qué no existía alerta?* Porque el inventario de certificados se alimenta del escaneo automático de endpoints TLS expuestos, y este certificado reside dentro del HSM, sin exposición de red, por lo que nunca fue descubierto por el escáner.
5. *¿Por qué nadie lo detectó manualmente?* Porque el procedimiento de renovación anual se documentó en 2023 en una hoja de cálculo del equipo de Pagos, y ese equipo tuvo rotación completa entre 2024 y 2025. El conocimiento salió de la institución con las personas.

**Causa raíz declarada:** ausencia de un proceso institucional de gestión del ciclo de vida de certificados que cubra los activos no descubribles por escaneo de red, agravada por la pérdida de conocimiento tácito tras la rotación del equipo.

## 4. Factores agravantes

1. **Ausencia de certificado de contingencia.** Añadió 39 minutos al tiempo de restauración. El runbook asumía su existencia; nadie verificaba esa premisa.
2. **Hipótesis inicial errónea.** Se perdieron 32 minutos en la línea de red porque el runbook colocaba la verificación de certificados en el paso 14.
3. **Documentación desactualizada.** El contacto de la autoridad certificadora registrado en el runbook correspondía a una persona que ya no laboraba en el proveedor.
4. **Ruido de alertas.** En los 30 días previos hubo 14 alertas del componente SPEI, 12 de ellas falsos positivos, lo que retrasó el reconocimiento inicial en aproximadamente 1 minuto.

## 5. Factores atenuantes (qué funcionó bien)

1. La declaración de P1 ocurrió en 4 minutos desde la primera alerta, dentro del SLA.
2. La convocatoria simultánea de guardias evitó el escalamiento secuencial.
3. La conciliación posterior fue impecable: **cero pagos duplicados**, gracias a que se respetó la regla de verificar antes de reenviar.
4. La célula Negocio activó comunicación y resarcimiento sin esperar al cierre técnico.
5. El registro del Scribe permitió construir el expediente regulatorio sin reconstrucción posterior.

## 6. Impacto detallado

| Dimensión | Medición |
|---|---|
| Clientes con operación fallida | 384,000 |
| Órdenes de salida encoladas | 291,400 |
| Recepciones no acreditadas en tiempo | 176,800 |
| Llamadas adicionales al contact center | 212,000 |
| Quejas formales derivadas | 4,180 |
| Comisiones devueltas | 3.1 MDP |
| Intereses compensatorios | 0.9 MDP |
| Penalizaciones contractuales (clientes empresariales) | 1.4 MDP |
| Costo operativo extraordinario | 1.4 MDP |
| **Total pérdida bruta** | **6.8 MDP** |
| Recuperaciones (seguro de riesgo operacional) | 0 (por debajo del deducible) |
| Caída de NPS transaccional | −14 puntos |
| Consumo de error budget mensual de SVC-001 | 641% del presupuesto del mes |

Evento registrado en la base de datos histórica de eventos de pérdida por riesgo operacional con clasificación de riesgo tecnológico. Notificado a la autoridad conforme al procedimiento interno HOR-REG-201, sección 3.4.

## 7. Acciones correctivas

| # | Acción | Responsable | Fecha compromiso | Estado al 2026-09-15 |
|---|---|---|---|---|
| 1 | Inventario completo de certificados, incluidos los residentes en HSM y en almacenes internos | Ciberseguridad | 2026-08-15 | Concluida |
| 2 | Alertamiento automático a 90, 60, 30 y 7 días del vencimiento, con escalamiento a gerente | Ciberseguridad | 2026-08-31 | Concluida |
| 3 | Emisión y custodia permanente de certificados de contingencia para todos los componentes Tier 0 | Pagos + Ciberseguridad | 2026-09-30 | En curso (70%) |
| 4 | Reordenar el runbook HOR-RBK-101: verificación de certificados al paso 5 | Pagos | 2026-07-31 | Concluida |
| 5 | Validación trimestral de contactos externos en todos los runbooks | Command Center | 2026-09-30 | En curso |
| 6 | Prueba anual de rotación de certificados en ambiente productivo con ventana controlada | Pagos | 2026-12-15 | No iniciada |
| 7 | Depuración de alertas del componente SPEI para reducir falsos positivos | Command Center | 2026-10-31 | En curso (40%) |
| 8 | Procedimiento de transferencia de conocimiento obligatorio ante rotación en equipos de servicios Tier 0 | Recursos Humanos + OP-PLT | 2026-11-30 | No iniciada |
| 9 | Extender el inventario y alertamiento de certificados a proveedores críticos | Riesgo de Terceros | 2026-12-31 | No iniciada |

## 8. Lecciones

1. **Un runbook que asume premisas no verificadas es una ficción útil hasta que deja de serlo.** La existencia del certificado de contingencia se daba por hecha desde 2023.
2. **El descubrimiento automático solo encuentra lo que está expuesto.** Los activos más críticos suelen ser los menos visibles, precisamente porque están mejor protegidos.
3. **La rotación de personal es un evento de riesgo operacional**, no solo un asunto de recursos humanos.
4. **El orden de los pasos de un runbook es una decisión de diseño con costo medible.** Mover una verificación del paso 14 al paso 5 habría ahorrado media hora.
5. **El ruido de alertas cobra su precio en el peor momento.** Doce falsos positivos previos convirtieron una alerta real en una más.

## 9. Anexo — Preguntas frecuentes internas

**¿Por qué no se usó el sitio alterno?** Porque el certificado es compartido por ambos sitios. El failover no habría resuelto nada, y el runbook actual ahora lo advierte de forma explícita.

**¿Se consideró solicitar ampliación de horario?** Sí, se evaluó a las 12:45. Se descartó porque el restablecimiento estimado permitía drenar la cola con holgura antes del cambio de día de operación de las 18:00.

**¿Hubo pérdida de información?** No. Ninguna orden se perdió; todas quedaron encoladas y se enviaron tras el restablecimiento con verificación previa de no duplicidad.

**¿Se trató de un ataque?** No. Ciberseguridad descartó actividad maliciosa mediante análisis de logs de acceso al HSM y revisión de la cadena de custodia del certificado.
