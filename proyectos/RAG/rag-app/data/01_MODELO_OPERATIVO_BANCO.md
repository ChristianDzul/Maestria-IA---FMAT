# Banco Horizonte — Modelo Operativo

**Clasificación:** SINTÉTICO  
**Versión:** 1.0

## 1. Áreas principales

### Dirección y gobierno
- Dirección General
- Riesgos
- Cumplimiento
- Auditoría Interna

### Negocio
- Banca Personas
- Banca Empresarial
- Captación
- Crédito
- Tarjetas
- Canales Digitales

### Operaciones
- Operaciones de Clientes
- Operaciones de Pagos
- Conciliaciones
- Back Office
- Command Center

### Finanzas
- Contabilidad
- Tesorería
- Liquidez
- Planeación Financiera
- Control Financiero

### Tecnología
- Aplicaciones
- Infraestructura
- Redes
- Bases de Datos
- Ciberseguridad
- Integraciones/API
- Observabilidad

## 2. Front, Middle y Back Office

**Front Office:** interacción comercial con clientes y generación de operaciones.

**Middle Office:** control, validación, riesgo, límites, monitoreo y supervisión de operaciones.

**Back Office:** procesamiento posterior, conciliación, liquidación, contabilización, documentación y resolución de excepciones.

## 3. Flujo operativo genérico

Cliente → Canal → Validación → Motor de negocio → Core/Sistema especializado → Procesamiento → Liquidación/Contabilización → Conciliación → Reporte.

## 4. Procesos críticos simulados

| Proceso | Área dueña | Criticidad |
|---|---|---|
| Transferencias | Operaciones de Pagos | Crítica |
| Acceso a banca móvil | Canales Digitales | Crítica |
| Autorización de pagos | Pagos | Crítica |
| Apertura de cuenta | Captación | Alta |
| Depósitos/retiros | Captación | Alta |
| Conciliación | Finanzas/Operaciones | Alta |
| Crédito | Crédito | Alta |
| Reportes regulatorios | Cumplimiento/Finanzas | Alta |

## 5. Principio operativo

Un proceso se considera recuperado cuando la operación crítica vuelve a ejecutarse de forma controlada, con integridad de datos, trazabilidad y capacidad de conciliación; no únicamente cuando el sistema vuelve a estar técnicamente disponible.
