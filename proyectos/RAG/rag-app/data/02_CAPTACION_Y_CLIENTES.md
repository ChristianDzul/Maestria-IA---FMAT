# Captación y Gestión de Clientes

**Clasificación:** SINTÉTICO

## 1. Captación

Captación comprende los procesos mediante los cuales una institución recibe recursos de sus clientes mediante productos como cuentas de depósito y otros instrumentos permitidos por su modelo de negocio y regulación.

### Ciclo de alta
1. Registro de solicitud.
2. Identificación del cliente.
3. Validaciones de identidad.
4. Evaluaciones aplicables de riesgo/cumplimiento.
5. Alta en sistemas.
6. Creación de producto/cuenta.
7. Activación.
8. Comunicación al cliente.
9. Registro auditable.

## 2. Operaciones frecuentes
- Apertura de cuenta
- Actualización de datos
- Cambio de medios de contacto
- Depósito
- Retiro
- Transferencia
- Bloqueo/desbloqueo
- Cancelación
- Consulta de saldo
- Conciliación

## 3. Incidencias de clientes

Una incidencia debe registrar:
- customer_id
- producto
- operación
- fecha/hora
- canal
- monto cuando aplique
- transaction_id
- mensaje de error
- impacto
- estado
- área responsable
- evidencia
- timestamps de escalación

## 4. Reglas sintéticas

### Cuenta no visible
Nivel 1 verifica identidad, producto y estado del alta.
Nivel 2 revisa replicación/integración entre CRM y core.
Nivel 3 revisa infraestructura o código cuando existe error técnico.

### Depósito no reflejado
1. Confirmar comprobante.
2. Validar transacción.
3. Consultar ledger/core.
4. Revisar cola de procesamiento.
5. Determinar si existe diferencia entre disponibilidad y contabilización.
6. Escalar a conciliación si existe descuadre.

## 5. SLA sintéticos
- Consulta simple: 4 horas hábiles.
- Alta bloqueada: 2 horas.
- Movimiento no reflejado: 60 minutos para diagnóstico.
- Incidente crítico de depósitos: respuesta inicial ≤ 10 minutos.
