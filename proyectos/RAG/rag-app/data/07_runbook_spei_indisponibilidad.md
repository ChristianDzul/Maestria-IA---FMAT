---
documento: HOR-RBK-101
titulo: Runbook — Indisponibilidad del servicio SPEI
version: 9.4
vigencia_desde: 2026-07-28
clasificacion: Confidencial
propietario: Dirección de Pagos y Medios (OP-PAG)
severidad_default: P1 / Major Incident
tiempo_objetivo: Restablecimiento en 15 minutos
---

# Runbook HOR-RBK-101 — Indisponibilidad del servicio SPEI

## 1. Cuándo aplica este runbook

Se ejecuta ante cualquiera de estas señales:

- El monitor de conexión al SPEI reporta a Banco Horizonte como desconectado.
- Las órdenes de transferencia enviadas no reciben acuse de liquidación.
- Las transferencias entrantes dejan de abonarse a cuentas de clientes.
- La cola de salida `SPEI_OUT` supera 500 mensajes pendientes o crece sin drenar durante más de 3 minutos.
- El tiempo de acuse (ACK) promedio supera 8 segundos en ventana de 5 minutos.
- Banco de México notifica a la institución una anomalía en su conexión.

**Severidad:** P1 automático. Si la indisponibilidad supera 10 minutos, se convierte en Major Incident por criterio 3 de HOR-OPS-006.

## 2. Contexto operativo relevante

El SPEI opera bajo un esquema de operación continua, las 24 horas, y el día de operación cambia a las 18:00 horas del centro de México. Esto tiene tres consecuencias prácticas para Banco Horizonte:

1. **No existe ventana de mantenimiento natural.** Cualquier cambio en el componente SPEI se hace en caliente, con doble validación y plan de reversión aprobado.
2. **Una indisponibilidad cerca de las 18:00 es más grave**, porque las operaciones pendientes pueden quedar atribuidas al día de operación siguiente, con efectos contables y de conciliación.
3. **La institución está obligada a mantener su conexión** con el sistema y, si la pierde, debe aplicar el procedimiento de contingencia previsto en la normativa del sistema de pagos.

Si por problemas técnicos u operativos no es posible enviar todas las órdenes pendientes antes del cierre del día de operación, existe la figura de **solicitud de ampliación de horario** ante el administrador del sistema, que debe enviarse con anticipación al cierre. En Banco Horizonte, esta solicitud la tramita exclusivamente el Enlace Banco de México (RG-BXO), nunca el área técnica.

## 3. Arquitectura del componente (resumen)

```
Canales (app, web, sucursal)
        │
   Orquestador de Pagos (PAGOS-ORQ, 4 nodos)
        │
   Motor SPEI Horizonte (SPEI-ENG, activo/activo, Qro + Mty)
        │
   Módulo de firma y cifrado (HSM-01 / HSM-02)
        │
   Enlace dedicado a Banco de México (primario + respaldo)
        │
   SPEI (Banco de México)
```

Dependencias críticas: HSM (firma de mensajes), certificados digitales, enlace dedicado, servicio de tipo de cambio (solo SPID), core bancario (para afectación de saldos) y motor antifraude.

## 4. Triage inicial — 5 minutos

Ejecutar en orden, sin saltar pasos:

| # | Verificación | Comando / tablero | Resultado esperado |
|---|---|---|---|
| 1 | Estado de conexión reportado por el administrador del sistema | Monitor público de conexiones SPEI | Institución conectada |
| 2 | Estado de nodos del motor | `hzctl spei status --all` | 4/4 nodos UP en ambos sitios |
| 3 | Profundidad de colas | Tablero HorizonteScope "SPEI Colas" | `SPEI_OUT` < 50, `SPEI_IN` < 50 |
| 4 | Salud del HSM | `hsmctl health` | Ambos HSM responden, sin alarma de batería o tamper |
| 5 | Vigencia de certificados | `hzctl cert list --service spei` | Ningún certificado con vencimiento < 30 días |
| 6 | Enlace a Banco de México | `ping`/`traceroute` sobre enlace dedicado; tablero de red | Latencia < 25 ms, sin pérdida |
| 7 | Cambios recientes | ITSM: RFC cerrados últimas 24 h sobre PAGOS-* | Ninguno, o identificar el sospechoso |
| 8 | Saldo de la cuenta de liquidación | Consola de tesorería | Saldo suficiente para el flujo esperado |

> El paso 5 se agregó a este runbook después del incidente INC-2026-0417 (certificado expirado del canal de firma). Antes, la verificación de certificados aparecía hasta el paso 14.

## 5. Árbol de decisión

```
¿El motor SPEI responde?
├── NO ──► ¿Ambos sitios caídos?
│          ├── SÍ ──► Sección 6.3 (recuperación total) + Comité de Crisis
│          └── NO ──► Sección 6.1 (failover de sitio)
└── SÍ ──► ¿Hay conexión con Banco de México?
           ├── NO ──► ¿Falla de enlace o de credenciales?
           │          ├── Enlace ──► Sección 6.2 (conmutación de enlace)
           │          └── Credenciales/certificado ──► Sección 6.4
           └── SÍ ──► ¿Las colas drenan?
                      ├── NO ──► Sección 6.5 (atasco de cola)
                      └── SÍ ──► Degradación aguas arriba: revisar
                                 orquestador, core o antifraude
```

## 6. Procedimientos

### 6.1 Failover de sitio (Querétaro → Monterrey)

**Riesgo:** medio. **Duración:** 6–9 minutos. **Reversible:** sí. **Autoriza:** Incident Manager.

1. Confirmar que el sitio destino tiene los nodos en estado `STANDBY_READY`.
2. Detener la admisión de nuevas órdenes en el orquestador: `hzctl pagos drain --service spei --grace 60`.
3. Esperar el drenado de mensajes en vuelo (máximo 90 segundos). Registrar cuántos quedaron pendientes.
4. Promover el sitio alterno: `hzctl spei failover --to mty --confirm`.
5. Validar registro de conexión y acuses: `hzctl spei probe --echo`.
6. Reabrir admisión: `hzctl pagos resume --service spei`.
7. Enviar transferencia de prueba de 1.00 MXN a la cuenta institucional de pruebas y verificar acuse y comprobante.
8. Notificar al Enlace Banco de México que la operación continúa desde sitio alterno.

### 6.2 Conmutación de enlace dedicado

**Riesgo:** bajo. **Duración:** 3–5 minutos. **Autoriza:** Jefe de Turno.

1. Validar con el equipo de Redes el estado del enlace primario.
2. Ejecutar la conmutación al enlace de respaldo: `netctl switch --circuit BXO-PRI --to BXO-BKP`.
3. Verificar que las sesiones del motor se restablezcan (no requiere reinicio del motor).
4. Levantar ticket con el carrier con prioridad crítica.
5. No devolver el tráfico al enlace primario durante el incidente; la reversión se programa como cambio normal.

### 6.3 Recuperación total del servicio

**Riesgo:** alto. **Duración:** 25–45 minutos. **Autoriza:** Director de Pagos + Incident Commander.

1. Declarar Major Incident y convocar Comité de Crisis.
2. Notificar de inmediato al Enlace Banco de México para evaluar procedimiento de contingencia aplicable.
3. Aislar y preservar evidencia: copiar logs de `SPEI-ENG`, `PAGOS-ORQ` y HSM antes de cualquier reinicio.
4. Levantar el motor en orden estricto: HSM → motor → orquestador → canales.
5. **No reabrir canales al público hasta completar la conciliación de mensajes en vuelo** (sección 7).
6. Validar con 3 transferencias de prueba: envío, recepción y devolución.
7. Reabrir canales de forma escalonada: sucursal → banca en línea → app móvil.

### 6.4 Falla de certificado o credenciales de firma

**Riesgo:** alto. **Duración:** 15–30 minutos. **Autoriza:** Director de Pagos + CISO.

1. Identificar el certificado afectado y su fecha de expiración.
2. Confirmar si existe certificado de contingencia vigente en el almacén seguro (`hsmctl slot list`).
3. Si existe: activarlo con doble control (dos custodios distintos) y reiniciar únicamente el módulo de firma.
4. Si no existe: iniciar el procedimiento de emisión de emergencia con la autoridad certificadora y notificar a Banco de México el tiempo estimado de restablecimiento.
5. Documentar el evento como falla de control de gestión del ciclo de vida de certificados, no como falla de infraestructura.

### 6.5 Atasco de cola

**Riesgo:** medio. **Duración:** 5–15 minutos.

1. Identificar el mensaje bloqueante: `hzctl spei queue head --queue SPEI_OUT`.
2. **No purgar la cola.** Mover el mensaje a la cola de excepciones: `hzctl spei queue quarantine --id <msg_id>`.
3. Verificar drenado. Si reaparece el patrón, existe un mensaje malformado sistemático: escalar a N3.
4. Cada mensaje en cuarentena requiere resolución individual y trazabilidad hacia el cliente ordenante.

## 7. Conciliación obligatoria post-incidente

Ninguna indisponibilidad de SPEI se cierra sin esta conciliación, que ejecuta el área de Pagos con validación de Contraloría:

| Categoría | Acción |
|---|---|
| Órdenes enviadas sin acuse | Verificar contra el registro del sistema de pagos antes de reenviar. **Reenviar sin verificar es la causa número uno de pagos duplicados.** |
| Órdenes recibidas no abonadas | Abonar con la fecha valor original y calcular intereses si aplica |
| Órdenes rechazadas | Devolver al ordenante y notificar por el canal de origen |
| Cargos a clientes sin transferencia efectiva | Reverso automático dentro de las 2 horas siguientes al restablecimiento |
| Comprobantes electrónicos de pago | Validar que se generen correctamente; considerar que el comprobante tarda alrededor de 30 minutos en estar disponible tras la operación |

## 8. Comunicación

| Destinatario | Momento | Responsable | Contenido |
|---|---|---|---|
| Banco de México | Inmediato si supera 10 min | Enlace RG-BXO | Naturaleza, alcance, tiempo estimado |
| Comité de Crisis | T+15 min | Incident Commander | Estado y opciones |
| Clientes (app, web, redes) | T+20 min | Comunicación | Mensaje aprobado, sin detalle técnico |
| Contact center | T+15 min | DN-CLI | Guion de atención y alternativas |
| CNBV | Según dictamen | Enlace RG-CNBV | Conforme al procedimiento de informe de incidentes |

Mensaje aprobado para clientes (plantilla): *"Estamos presentando intermitencia en las transferencias interbancarias. Tus recursos están seguros. Puedes realizar operaciones entre cuentas Horizonte con normalidad. Te informaremos en cuanto se restablezca el servicio."*

## 9. Anexo — Errores conocidos

| Código | Significado | Acción |
|---|---|---|
| SPEI-E101 | Firma inválida | Revisar HSM y certificado (sección 6.4) |
| SPEI-E204 | Cuenta destino no existe | Devolución automática, sin intervención |
| SPEI-E311 | Saldo insuficiente en cuenta de liquidación | Escalar a Tesorería de inmediato |
| SPEI-E415 | Mensaje malformado | Cuarentena y análisis del canal originador |
| SPEI-E502 | Sin respuesta del administrador del sistema | Verificar enlace (sección 6.2) |
| SPEI-E677 | Día de operación cerrado | Verificar hora de cambio de fecha; evaluar ampliación de horario |
