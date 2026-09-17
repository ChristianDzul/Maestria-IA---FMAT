---
documento: HOR-RBK-103
titulo: Runbook — Degradación de canales digitales y fallas de autenticación
version: 6.7
vigencia_desde: 2026-08-05
clasificacion: Confidencial
propietario: Dirección de Plataformas (OP-PLT) / Ciberseguridad (OP-CIB)
severidad_default: P2, escalable a P1
---

# Runbook HOR-RBK-103 — Degradación de canales digitales y fallas de autenticación

## 1. Alcance

Cubre app móvil Horizonte Móvil (SVC-004), banca en línea empresarial (SVC-005) y los servicios transversales de autenticación: contraseña, segundo factor, biometría y token.

Volumen de referencia: 4.1 millones de sesiones diarias en app móvil, pico de 180 mil sesiones concurrentes entre las 13:00 y 15:00 de días de quincena.

## 2. Síntomas y clasificación inicial

| Síntoma | Severidad inicial | Escala a P1 si… |
|---|---|---|
| Tasa de error de login > 5% | P2 | Supera 25% o dura más de 30 min |
| Latencia p95 de consulta de saldo > 4 s | P2 | Supera 10 s o afecta también a sucursal |
| Transferencias internas fallando | P2 | Supera 10% del volumen |
| App no abre (crash al inicio) | P1 | Siempre |
| Sesiones cruzadas (un usuario ve datos de otro) | P1 | Siempre + activación de Ciberseguridad |
| Segundo factor no llega (SMS/push) | P2 | Si impide operar a más de 50,000 clientes |
| Biometría rechaza a todos los usuarios | P2 | Si no hay método alterno habilitado |

> **Sesiones cruzadas: parada inmediata del canal.** Es el único escenario de este runbook donde se apaga el servicio antes de diagnosticar. El riesgo de confidencialidad supera cualquier consideración de disponibilidad.

## 3. Cadena de dependencias

```
App móvil / Web
      │
   API Gateway (GW-DIG)
      │
 ┌────┴─────┬──────────────┬───────────────┐
 │          │              │               │
Auth       BFF          Motor          Notificaciones
(IAM)   (agregación)   antifraude       (push/SMS)
 │          │              │
 │      Core bancario   Reglas de riesgo
 │
Proveedor biométrico (tercero)
```

Proveedores externos con dependencia única: proveedor de biometría facial (contrato con SLA de 99.5%) y agregador de SMS. Ambos representan riesgo de concentración identificado por Riesgos No Financieros y documentado en el inventario de terceros críticos.

## 4. Triage — 10 minutos

| # | Verificación | Herramienta | Umbral normal |
|---|---|---|---|
| 1 | Tasa de éxito de login por método | Tablero "Auth Funnel" | > 96% |
| 2 | Latencia p50/p95/p99 del gateway | Tablero "GW-DIG" | 180 ms / 900 ms / 2.1 s |
| 3 | Saturación de pods del BFF | `kubectl top pods -n digital` | CPU < 70% |
| 4 | Errores 5xx por endpoint | Tablero "API Errors" | < 0.5% |
| 5 | Salud del proveedor biométrico | Endpoint de estatus del proveedor | 200 OK |
| 6 | Cola de notificaciones | Tablero "Push/SMS" | Retraso < 20 s |
| 7 | Tiempo de respuesta del core | Tablero "Core API" | p95 < 600 ms |
| 8 | Versión liberada en las últimas 24 h | ITSM / pipeline | Identificar cambio |

## 5. Procedimientos

### 5.1 Saturación por demanda (pico legítimo)

Señal: latencia alta, CPU alta, tasa de error creciente, sin errores de lógica.

1. Escalar horizontalmente el BFF y el gateway: `hzctl scale --service bff,gw-dig --replicas +50%`.
2. Activar degradación elegante (*graceful degradation*) con `hzctl feature disable` en este orden:
   - Widgets de recomendación personalizada.
   - Historial extendido (mantener solo 30 días).
   - Precarga de estado de cuenta en PDF.
   - Animaciones y contenido enriquecido de inicio.
3. Activar limitación de tasa por usuario (no por IP, para no castigar redes corporativas).
4. Nunca degradar: consulta de saldo, transferencias, bloqueo de tarjeta ni contacto con el banco.

### 5.2 Falla del proveedor de biometría

1. Confirmar la falla con el proveedor por su canal de soporte crítico y registrar el ticket externo.
2. Activar el método alterno: `hzctl auth fallback --from biometric --to otp-push`.
3. Validar que el motor antifraude eleve su nivel de escrutinio durante la contingencia (el fallback reduce la fortaleza del factor de autenticación).
4. Comunicar a clientes: mensaje neutro, sin nombrar al proveedor.
5. Al restablecerse: reactivar de forma escalonada (10% → 50% → 100%) verificando tasa de éxito en cada escalón.

**Restricción de riesgos:** el fallback no puede permanecer activo más de 8 horas sin autorización expresa del CISO, porque implica operar con un factor de autenticación distinto del aprobado para ciertas operaciones.

### 5.3 Segundo factor no entregado

1. Determinar si el problema es del canal push, del canal SMS o de ambos.
2. Si es SMS: conmutar de agregador `hzctl sms switch --provider secundario`.
3. Si es push: revisar credenciales de las plataformas de notificación y vigencia de certificados de notificación.
4. Si ambos fallan: habilitar token de contingencia para clientes empresariales y proceso asistido en sucursal para personas físicas.
5. **No** deshabilitar el segundo factor. Ninguna circunstancia operativa justifica operar sin segundo factor.

### 5.4 Liberación defectuosa

1. Identificar la versión: `hzctl release current --service <svc>`.
2. Evaluar reversión inmediata. La regla interna es **revertir primero, investigar después**, salvo que la reversión implique migración de datos irreversible.
3. Ejecutar: `hzctl release rollback --service <svc> --to <version_anterior> --confirm`.
4. Para la app móvil, la reversión de tienda no es inmediata: se usa el interruptor de servidor (`feature kill-switch`) para inhabilitar la funcionalidad defectuosa sin nueva publicación.
5. Documentar en el RFC que originó el cambio y bloquear nuevas liberaciones del servicio hasta el postmortem.

### 5.5 Sesiones cruzadas o fuga de datos

**Acción inmediata, en este orden, sin consultar:**

1. Apagar el canal afectado: `hzctl service disable --service <svc> --reason security`.
2. Invalidar todas las sesiones activas: `hzctl auth revoke --all-sessions`.
3. Notificar al CISO y al Jefe de Turno. Declarar P1 y Major Incident.
4. Preservar evidencia antes de cualquier reinicio (logs de gateway, BFF y caché).
5. Ciberseguridad determina si hubo acceso indebido efectivo a datos personales y, en su caso, se activa el procedimiento de notificación regulatoria e informe de incidente de seguridad de la información.
6. La reapertura del canal requiere autorización conjunta de CISO y Director de Operaciones.

## 6. Comunicación a clientes

| Escenario | Mensaje aprobado |
|---|---|
| Lentitud | "Estamos presentando lentitud en la app. Estamos trabajando para normalizar el servicio." |
| Login no disponible | "El acceso a la app está temporalmente no disponible. Tus recursos están seguros. Puedes usar banca en línea o acudir a sucursal." |
| Segundo factor | "Puede haber retraso en la llegada de tu código de verificación. Intenta nuevamente en unos minutos." |
| Seguridad | Sin mensaje automático. Todo mensaje lo aprueban Comunicación, Jurídico y Cumplimiento. |

Prohibido en comunicación externa: nombrar proveedores, dar detalle técnico de la causa, prometer hora exacta de restablecimiento y usar la palabra "hackeo" antes de dictamen formal.

## 7. Verificación de restablecimiento

No basta con que las métricas vuelvan a rango. Se requiere:

1. Login exitoso con cada método de autenticación (contraseña, biometría, token).
2. Consulta de saldo consistente con el core.
3. Transferencia interna y transferencia SPEI de prueba.
4. Recepción efectiva de notificación push y SMS.
5. Confirmación del contact center de que bajó el volumen de llamadas por la causa.
6. 30 minutos de métricas estables antes de declarar cierre.
