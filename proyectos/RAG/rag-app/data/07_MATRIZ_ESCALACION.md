# Matriz de Escalación

**Clasificación:** SINTÉTICO — creada para este corpus.

## 1. Escalación funcional

| Evento | Nivel 1 | Nivel 2 | Nivel 3 |
|---|---|---|---|
| Pago pendiente | Operaciones Pagos | Especialista Pagos | Proveedor/Infraestructura |
| Cuenta no visible | Atención/Operación | Core Bancario | Aplicaciones |
| Error API | Monitoreo | Integraciones | Desarrollo |
| Diferencia conciliación | Back Office | Finanzas | Contabilidad/Riesgo |
| Fraude potencial | Operaciones | Fraude | Riesgo/Compliance |
| Caída canal móvil | Canales | Aplicaciones | Infraestructura |

## 2. Escalación jerárquica

Se escala al responsable de gestión cuando:
- se aproxima el SLA;
- el equipo no tiene autoridad para ejecutar la acción;
- existe conflicto entre áreas;
- se requiere decisión de negocio;
- existe riesgo financiero/regulatorio.

## 3. Escalación por tiempo

### P1
- T+0: equipo detector.
- T+5: Incident Manager.
- T+10: equipos técnicos.
- T+15: Command Center.
- T+20: responsable ejecutivo de guardia.
- T+30: negocio + riesgo si el impacto continúa.

### P2
- T+0: equipo responsable.
- T+15: especialista.
- T+30: manager.
- T+60: Command Center si persiste y el impacto aumenta.

### P3
Escalación cuando se alcanza 75% del SLA o aumenta el impacto.

## 4. Escalación por impacto

Escalar inmediatamente si:
- el número de clientes afectados cruza el umbral definido para el proceso;
- aumenta rápidamente;
- aparecen múltiples productos;
- existe riesgo de duplicidad financiera;
- existe pérdida o corrupción de información;
- aparece un evento de ciberseguridad.

## 5. Escalación geográfica

Si un servicio regional afecta múltiples zonas, el incidente pasa de gestión local a coordinación nacional.

## 6. Escalación a terceros

Se activa cuando:
- un proveedor controla un componente indispensable;
- se necesita soporte especializado;
- se requiere recuperación contractual;
- existe dependencia tecnológica externa.

El responsable interno sigue siendo dueño de la coordinación aunque el diagnóstico dependa del tercero.

## 7. Matriz de autoridad

| Acción | Operador | Especialista | Manager | Ejecutivo |
|---|---|---|---|---|
| Reinicio controlado | Sí | Sí | Según riesgo | No |
| Cambio de configuración | No | Sí | Aprobación | No |
| Activar DR | No | Recomienda | Autoriza | Según impacto |
| Comunicar incidente mayor | No | Recomienda | Sí | Sí |
| Suspender producto | No | Recomienda | Sí | Según impacto |
| Compensación cliente | No | No | Según política | Según umbral |

## 8. Regla de oro

La escalación no transfiere automáticamente la responsabilidad. El equipo que detectó el incidente debe mantener el contexto y entregar evidencia suficiente al equipo receptor.
