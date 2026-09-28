# Pagos y Transferencias

**Clasificación:** MIXTO — conceptos públicos + procedimiento operativo sintético.

## 1. Contexto público

Banco de México describe SPEI como un sistema de pagos que permite enviar y recibir transferencias electrónicas entre cuentas de distintas instituciones financieras en moneda nacional y opera 24/7. La operación se encuentra sujeta a su marco normativo y reglas aplicables. 

## 2. Modelo interno sintético

Canal cliente → autenticación → validación → antifraude → autorización → creación de instrucción → gateway de pagos → SPEI/infraestructura correspondiente → confirmación → actualización de cuenta → notificación → conciliación.

## 3. Estados internos simulados

RECEIVED  
VALIDATING  
AUTHORIZED  
SENT  
ACCEPTED  
SETTLED  
REJECTED  
RETURNED  
PENDING  
TIMEOUT  
RECONCILIATION_REQUIRED

## 4. Transferencia pendiente

El operador debe:
1. Obtener transaction_id.
2. Confirmar hora de creación.
3. Consultar estado interno.
4. Revisar respuesta de la infraestructura de pagos.
5. Verificar si existe confirmación, rechazo o devolución.
6. Comparar ledger y estado de pago.
7. Evitar duplicar la instrucción.
8. Si no existe estado concluyente, abrir investigación.
9. Escalar según severidad.

## 5. Regla crítica sintética

Nunca reenviar automáticamente una transferencia únicamente porque el canal del cliente muestra timeout. Primero debe determinarse si la instrucción original fue aceptada o liquidada, para evitar duplicidad.

## 6. Indicadores de pagos
- tasa de éxito;
- tasa de rechazo;
- pagos pendientes;
- tiempo de procesamiento;
- timeouts;
- devoluciones;
- diferencias de conciliación;
- clientes afectados.

## 7. Nota sobre ISO 20022

ISO 20022 proporciona un enfoque común para modelar áreas de negocio financiero, transacciones y flujos de mensajes, además de un diccionario de elementos de negocio y esquemas de mensajes. Esto puede utilizarse en el RAG para enriquecer conceptos de pagos y mensajería financiera.
