---
documento: HOR-RBK-102
titulo: Runbook — Falla del cierre batch nocturno del core bancario
version: 11.2
vigencia_desde: 2026-06-15
clasificacion: Confidencial
propietario: Dirección de Plataformas (OP-PLT)
severidad_default: P1
---

# Runbook HOR-RBK-102 — Falla del cierre batch nocturno del core bancario

## 1. Contexto

El cierre nocturno es el proceso que consolida la operación del día en el core bancario Horizonte Core. Sin cierre exitoso no hay apertura: las sucursales no pueden operar, los saldos no reflejan la realidad y los reportes regulatorios del día no se generan.

- **Ventana autorizada:** 22:00 a 04:30.
- **Objetivo interno (SLO):** terminar antes de las 03:30.
- **Punto de no retorno:** 03:00. Si a esa hora el cierre no ha superado la fase 6, se evalúa apertura en modo contingencia.
- **Hora crítica:** 06:30, apertura de las primeras sucursales en zona horaria del sureste.

## 2. Fases del cierre

| Fase | Nombre | Duración típica | Reversible | Dependencias |
|---|---|---|---|---|
| 1 | Corte de captura en línea | 5 min | Sí | Canales digitales |
| 2 | Recepción de archivos externos (cámara, buró, proveedores) | 25 min | Sí | CECOBAN, terceros |
| 3 | Aplicación de movimientos del día | 45 min | Sí | — |
| 4 | Cálculo de intereses y comisiones | 35 min | Sí | Tablas de tasas |
| 5 | Devengo contable y provisiones | 30 min | Parcial | Contraloría |
| 6 | Generación de saldos finales | 20 min | **No** | Fases 1–5 |
| 7 | Extracción para reportes regulatorios | 40 min | Sí | Fase 6 |
| 8 | Respaldo y punto de recuperación | 30 min | N/A | Almacenamiento |
| 9 | Apertura del día siguiente | 10 min | Sí | Fase 6 y 8 |

**La fase 6 es la frontera.** Después de generar saldos finales, la reversión implica restaurar desde respaldo y reprocesar, lo que cuesta entre 2 y 4 horas.

## 3. Señales de falla

- El orquestador reporta job en estado `ABEND` o `SUSPENDED`.
- Una fase supera 200% de su duración típica.
- Diferencia en el cuadre contable de la fase 5.
- Archivo externo no recibido después de 01:00.
- Espacio en el tablespace de movimientos por debajo de 10%.
- Bloqueo de base de datos con más de 15 minutos de duración.

## 4. Triage — primeros 10 minutos

```bash
# Estado general del cierre
hzctl batch status --date $(date -d yesterday +%Y-%m-%d)

# Fase actual y jobs con error
hzctl batch phase --current --show-errors

# Bloqueos activos en base de datos
dbctl locks --blocking --min-duration 300

# Espacio en tablespaces críticos
dbctl space --tablespace MOV,SAL,CTB

# Archivos externos esperados vs recibidos
hzctl batch files --expected --missing
```

Registrar siempre: fase en que falló, hora exacta del error, código de error, jobs completados y tiempo restante hasta las 03:00.

## 5. Escenarios y procedimientos

### 5.1 Archivo externo no recibido (fase 2)

**Frecuencia:** el escenario más común (≈40% de las fallas de cierre).

1. Confirmar con el proveedor o la cámara el estatus del envío.
2. Si el archivo llegará en menos de 45 minutos: pausar el cierre con `hzctl batch hold --phase 2` y esperar.
3. Si no llegará esta noche: aplicar **cierre con exclusión**, que procesa el resto y deja el lote pendiente marcado.
   ```bash
   hzctl batch exclude --file <ID_ARCHIVO> --reason "no recibido" --ticket INC-AAAA-NNNN
   hzctl batch resume
   ```
4. Notificar a Contraloría **antes** de continuar: la exclusión tiene efecto contable.
5. Registrar el lote pendiente para aplicación en el cierre siguiente, con fecha valor original.

### 5.2 Falla en aplicación de movimientos (fase 3)

1. Identificar los registros rechazados: `hzctl batch rejects --phase 3 --export`.
2. Si son menos de 100 registros y no afectan cuentas con saldo crítico: continuar y regularizar en horario hábil.
3. Si superan 100 o afectan cuentas institucionales: detener y escalar a N3 del equipo de Core.
4. Nunca editar registros directamente en base de datos. La corrección se hace por el proceso de reproceso controlado: `hzctl batch reprocess --range <ini>-<fin> --dry-run` y después sin `--dry-run` con autorización del IM.

### 5.3 Descuadre contable (fase 5)

**Severidad: P1 sin excepción.** Convocar de inmediato a Contraloría, aunque sea de madrugada.

1. Detener el cierre: `hzctl batch stop --phase 5`.
2. Obtener el reporte de diferencias: `hzctl batch balance --detail --export`.
3. Clasificar la diferencia: de redondeo (< 1 peso por cuenta), de partida específica o sistémica.
4. Diferencias de redondeo: aplicar cuenta puente autorizada y continuar.
5. Diferencias de partida o sistémicas: **no continuar**. Restaurar al punto previo a la fase 5 y reprocesar. Si el reproceso no cuadra, se aplica el escenario 5.5.
6. Todo descuadre se registra como evento de riesgo operacional, incluso si se resuelve la misma noche.

### 5.4 Cierre incompleto al llegar a las 03:00

Decisión del Director de Plataformas, con acuerdo del Director de Operaciones:

| Opción | Cuándo | Consecuencia |
|---|---|---|
| Continuar | Fase ≥ 6 y avance estable | Riesgo de invadir horario de apertura |
| Apertura en contingencia | Fase < 6 | Sucursales operan con saldos del día anterior; se bloquean operaciones de alto monto |
| Cierre diferido | Falla estructural | Operación en modo restringido todo el día; notificación regulatoria probable |

**Modo contingencia — restricciones automáticas:**
- Retiros en ventanilla limitados a 20,000 MXN por cliente.
- Transferencias salientes limitadas a 50,000 MXN por cliente y por día.
- Sin apertura de productos nuevos.
- Sin liberación de créditos.
- Consulta de saldos con leyenda visible "saldo sujeto a actualización".

### 5.5 Recuperación desde respaldo

**Riesgo: crítico. Autoriza: Director de Operaciones y Tecnología. Duración: 2 a 4 horas.**

1. Declarar Major Incident.
2. Identificar el último punto de recuperación consistente: `dbctl restore list --consistent`.
3. Validar integridad del respaldo antes de restaurar (nunca restaurar sin verificación de suma de comprobación).
4. Restaurar en el ambiente de recuperación, no directamente sobre producción.
5. Reprocesar el día completo con la fuente original de movimientos.
6. Conciliar contra los totales de control del día: número de movimientos, monto total, número de cuentas afectadas.
7. Promover a producción únicamente con firma de Contraloría y del Director de Plataformas.

## 6. Matriz de decisión rápida

| Hora | Fase alcanzada | Decisión |
|---|---|---|
| 01:00 | ≤ 3 | Escalar a N3; probable retraso |
| 02:00 | ≤ 4 | Notificar a Director de Plataformas |
| 03:00 | < 6 | Evaluar apertura en contingencia |
| 04:00 | < 6 | Apertura en contingencia obligatoria |
| 04:30 | ≥ 6 | Continuar, aceptar retraso en fases 7–9 |
| 05:30 | < 6 | Major Incident + Comité de Crisis |

## 7. Comunicación nocturna

A diferencia de otros incidentes, el cierre batch tiene destinatarios que deben enterarse aunque estén dormidos:

- **Contraloría:** ante cualquier descuadre o exclusión de archivo, sin importar la hora.
- **Director de Plataformas:** si el cierre supera las 02:00 sin llegar a fase 5.
- **Dirección de Sucursales:** antes de las 05:00 si habrá apertura en contingencia, para que el mensaje llegue a gerentes antes de abrir puertas.
- **Contact center:** antes de las 06:00 con guion de atención.
- **Regulación:** si se prevé retraso en la generación de reportes con fecha de entrega comprometida.

## 8. Histórico de fallas del cierre (2026)

| Mes | Fallas | Causa predominante | Aperturas en contingencia |
|---|---|---|---|
| Enero | 3 | Archivos externos | 0 |
| Febrero | 2 | Espacio en tablespace | 1 |
| Marzo | 5 | Liberación defectuosa de tasas | 1 |
| Abril | 1 | Archivos externos | 0 |
| Mayo | 4 | Bloqueos de base de datos | 2 |
| Junio | 2 | Archivos externos | 0 |
| Julio | 3 | Bloqueos de base de datos | 1 |
| Agosto | 2 | Archivos externos | 0 |

Los bloqueos de base de datos de mayo y julio comparten causa raíz (proceso de reportería analítica ejecutándose dentro de la ventana batch) y se atienden en el problema PRB-2026-0042.
