# Runbook — Transferencia Pendiente

**Clasificación:** SINTÉTICO

## Síntoma

Cliente reporta que una transferencia permanece pendiente o no observa el resultado esperado.

## Objetivo

Determinar si la operación:
1. no salió del banco;
2. fue enviada;
3. fue aceptada;
4. fue liquidada;
5. fue rechazada;
6. fue devuelta;
7. quedó inconsistente internamente.

## Paso 1 — Identificación

Obtener:
- transaction_id;
- customer_id;
- cuenta origen;
- fecha/hora;
- monto;
- institución destino;
- canal;
- referencia.

## Paso 2 — Estado interno

Consultar:
- estado transaccional;
- ledger;
- cola;
- logs;
- respuesta del gateway.

## Paso 3 — Evitar duplicidad

Si existe evidencia de envío, NO crear una segunda instrucción sin determinar el estado de la primera.

## Paso 4 — Conciliación

Comparar:
`estado del pago` vs `movimiento de cuenta` vs `respuesta externa`.

## Paso 5 — Decisión

### Caso A
No existe instrucción válida → tratar como error de canal/proceso.

### Caso B
Existe instrucción pero no respuesta concluyente → escalar a Pagos.

### Caso C
Existe confirmación externa pero no reflejo interno → escalar a conciliación/core.

### Caso D
Existe rechazo → aplicar procedimiento de rechazo.

### Caso E
Existe devolución → validar motivo y aplicación de devolución.

## Criterios de P1

- muchas operaciones pendientes;
- impacto en proceso crítico;
- posible duplicidad masiva;
- discrepancias de saldos;
- pérdida de trazabilidad;
- imposibilidad de reconciliar.

## Evidencia requerida

Nunca cerrar el incidente únicamente con "ya funciona". Debe existir evidencia de:
- operación recuperada;
- consistencia de saldo;
- conciliación;
- monitoreo posterior.
