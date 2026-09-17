---
documento: HOR-NEG-050
titulo: Líneas de Negocio — Captación, Crédito y Clientes
version: 8.0
vigencia_desde: 2026-03-15
clasificacion: Uso Interno
propietario: Dirección General de Negocio
---

# Líneas de Negocio — Captación, Crédito y Clientes

## 1. Captación (DN-CAP)

### 1.1 Catálogo de productos

| Producto | Clave | Segmento | Saldo mínimo | Comisión de manejo | Sistema origen |
|---|---|---|---|---|---|
| Cuenta Horizonte Básica | CTA-001 | Personas | 0 | Sin comisión | Core |
| Cuenta Horizonte Clásica | CTA-002 | Personas | 3,000 MXN | 120 MXN/mes, exenta con saldo promedio | Core |
| Cuenta Horizonte Premium | CTA-003 | Patrimonial | 250,000 MXN | Sin comisión | Core + Patrimonial |
| Cuenta Horizonte Negocios | CTA-010 | PyME | 10,000 MXN | 350 MXN/mes | Core |
| Ahorro Programado | AHO-001 | Personas | 100 MXN | Sin comisión | Core |
| Pagaré con Rendimiento Liquidable al Vencimiento (PRLV) | INV-001 | Todos | 10,000 MXN | Sin comisión | Tesorería |
| Depósito a plazo 28/91/182/364 días | INV-002 | Todos | 25,000 MXN | Sin comisión | Tesorería |
| Nómina Horizonte | NOM-001 | Personas (empresas convenio) | 0 | Sin comisión | Core + Nómina |

### 1.2 Procesos operativos críticos

- **Apertura de cuenta digital.** Identificación remota con validación biométrica y consulta a listas. Tiempo objetivo: 8 minutos. Depende de: motor biométrico, proveedor de verificación de identidad y core.
- **Dispersión de nómina.** Ventana de procesamiento 22:00–01:00. Volumen pico: 640 mil abonos el día 15 y el último día del mes. Una falla en esta ventana es P1 automático por criterio de alcance.
- **Vencimiento y renovación de inversiones.** Proceso batch diario dentro del cierre nocturno. La falla de renovación automática genera reclamación y posible pago de intereses compensatorios.
- **Cálculo de intereses.** Fase 4 del cierre. Un error en tablas de tasas afecta a toda la cartera de captación y se clasifica como P1 por integridad de datos.

### 1.3 Indicadores

| Indicador | Meta 2026 | Resultado Q2-2026 |
|---|---|---|
| Cuentas nuevas por mes | 62,000 | 58,400 |
| Tasa de abandono en apertura digital | ≤ 18% | 23% |
| Saldo promedio por cuenta activa | 34,000 MXN | 31,800 MXN |
| Reclamaciones por cobro de comisión | ≤ 900/mes | 1,140 |

## 2. Crédito (DN-CRE)

### 2.1 Catálogo de productos

| Producto | Clave | Monto | Plazo | Tasa anual (referencia) | Motor de decisión |
|---|---|---|---|---|---|
| Tarjeta Horizonte Azul | TDC-001 | Línea 15 mil – 120 mil | Revolvente | 38.9% | Motor TDC |
| Tarjeta Horizonte Oro | TDC-002 | Línea 80 mil – 400 mil | Revolvente | 32.5% | Motor TDC |
| Crédito Personal | CRE-010 | 20 mil – 500 mil | 12 a 60 meses | 26.9% | Motor Personas |
| Crédito de Nómina | CRE-011 | 10 mil – 350 mil | 6 a 48 meses | 21.4% | Motor Nómina |
| Crédito Automotriz | CRE-020 | 80 mil – 1.5 M | 12 a 72 meses | 14.8% | Motor Auto |
| Crédito Hipotecario | CRE-030 | 500 mil – 12 M | 5 a 20 años | 11.2% | Motor Hipotecario |
| Crédito Simple PyME | CRE-040 | 100 mil – 8 M | 6 a 60 meses | 18.5% | Motor PyME |
| Línea Revolvente Empresarial | CRE-041 | 500 mil – 25 M | Revolvente | TIIE + 6.5 pp | Comité de Crédito |

### 2.2 Flujo de originación

```
Solicitud (canal) → Prevalidación → Consulta a sociedad de información crediticia
   → Motor de decisión → Análisis (si aplica) → Aprobación → Formalización
   → Disposición → Alta en core → Primer corte
```

Puntos de falla más frecuentes, en orden de incidencia:

1. Indisponibilidad del servicio de consulta a la sociedad de información crediticia (43% de los incidentes de originación).
2. Timeout del motor de decisión bajo carga de campaña (26%).
3. Errores en la generación del documento de formalización (14%).
4. Desfase entre la aprobación y el alta en core, que genera crédito aprobado no dispuesto (11%).
5. Otros (6%).

### 2.3 Reglas operativas relevantes para incidentes

- Una solicitud aprobada que no se dispone en 30 días naturales caduca. Si un incidente impide la disposición, se extiende el plazo y se documenta como excepción autorizada por el Director de Crédito.
- Si el motor de decisión está caído, **no** se aprueba manualmente crédito de consumo. Sí se permite continuar con crédito empresarial que ya pasó por Comité.
- La falla en el cálculo de la tabla de amortización es P1 por integridad de datos, aunque no haya afectación visible al cliente.
- Toda afectación que implique cobro indebido de intereses obliga a reverso con fecha valor original y notificación al cliente en 5 días hábiles.

### 2.4 Cartera (cierre agosto 2026)

| Producto | Saldo (MDP) | Clientes | Índice de morosidad |
|---|---|---|---|
| Tarjeta de crédito | 18,400 | 1,240,000 | 4.1% |
| Crédito personal y nómina | 22,700 | 610,000 | 3.2% |
| Automotriz | 14,100 | 96,000 | 1.8% |
| Hipotecario | 41,300 | 58,000 | 2.4% |
| PyME y empresarial | 36,900 | 21,400 | 2.9% |
| **Total** | **133,400** | — | **3.0%** |

## 3. Clientes y Experiencia (DN-CLI)

### 3.1 Canales de atención

| Canal | Volumen mensual | SLA de respuesta | Horario |
|---|---|---|---|
| Contact center telefónico | 1.9 M llamadas | 80% atendidas en 40 s | 24×7 |
| Chat en app | 740 mil conversaciones | Primera respuesta ≤ 60 s | 07:00–23:00 |
| Sucursal | 3.4 M visitas | Espera ≤ 12 min | Horario de sucursal |
| Redes sociales | 96 mil menciones | Respuesta ≤ 30 min | 08:00–22:00 |
| UNE (Unidad Especializada) | 14 mil casos | Resolución ≤ 20 días hábiles | Hábil |

### 3.2 Gestión de quejas y aclaraciones

Tipos más frecuentes en 2026:

| Motivo | % del total | Tendencia |
|---|---|---|
| Transferencia no reconocida | 21% | Al alza |
| Cargo no reconocido en tarjeta | 19% | Estable |
| Cobro de comisión | 15% | Al alza |
| Transferencia no acreditada | 11% | Al alza tras INC-2026-0417 |
| Problemas de acceso a la app | 9% | A la baja |
| Cálculo de intereses | 7% | Estable |
| Otros | 18% | — |

### 3.3 Rol de DN-CLI durante incidentes

DN-CLI integra la **célula Negocio** en todo Major Incident. Sus responsabilidades:

1. Activar guion de atención en un máximo de 15 minutos desde la declaración.
2. Reforzar dotación del contact center (protocolo de llamada a personal fuera de turno).
3. Identificar y segmentar a los clientes afectados para atención prioritaria.
4. Proponer el plan de resarcimiento: devolución de comisiones, ajuste de intereses, exención temporal.
5. Medir el impacto en volumen de contacto y en NPS transaccional posterior al evento.

### 3.4 Impacto histórico de incidentes en atención

| Incidente | Llamadas adicionales | Quejas formales | Caída de NPS |
|---|---|---|---|
| INC-2025-0891 (app en Buen Fin) | +148,000 | 2,340 | −9 puntos |
| INC-2026-0417 (SPEI) | +212,000 | 4,180 | −14 puntos |
| INC-2026-0502 (biometría) | +61,000 | 790 | −4 puntos |

La regla derivada de estos datos: cada hora de indisponibilidad de un servicio Tier 0 en horario hábil genera aproximadamente 70 mil contactos adicionales y 1,400 quejas formales. Este coeficiente se usa para dimensionar la respuesta desde el minuto cero, sin esperar a que el volumen llegue.
