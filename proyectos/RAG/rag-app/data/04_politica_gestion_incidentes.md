---
documento: HOR-OPS-004
titulo: Política de Gestión de Incidentes
version: 6.3
vigencia_desde: 2026-04-01
clasificacion: Uso Interno
propietario: Command Center (OP-CC)
aprobado_por: COTEC y Comité de Riesgos
marco_referencia: ITIL 4, ISO/IEC 20000-1, Principios de resiliencia operacional del Comité de Basilea
---

# Política de Gestión de Incidentes

## 1. Definiciones

- **Evento:** cualquier cambio de estado observable en la infraestructura o en un servicio. La mayoría de los eventos no son incidentes.
- **Incidente:** interrupción no planeada de un servicio o reducción de su calidad respecto del nivel comprometido.
- **Major Incident:** incidente P1 que además cumple al menos uno de los criterios de amplificación descritos en HOR-OPS-006.
- **Problema:** causa subyacente de uno o más incidentes. Se gestiona en un flujo separado (PRB-AAAA-NNNN).
- **Solución temporal (workaround):** acción que restablece el servicio sin eliminar la causa raíz.
- **Cuasi-pérdida:** evento operacional que no produjo pérdida o cuya pérdida se recuperó en corto plazo. Se registra igual que una pérdida efectiva.

## 2. Principio rector

> Primero se restablece el servicio; después se entiende la causa. La evidencia se preserva durante la restauración, nunca a costa de ella.

La única excepción es el incidente con sospecha de intrusión o fraude: en ese caso, Ciberseguridad puede ordenar la preservación forense antes de la restauración, y esa orden prevalece sobre el objetivo de MTTR.

## 3. Clasificación de severidad

La severidad se determina por **impacto** (a quién y a cuánto afecta) y **urgencia** (qué tan rápido se degrada la situación). El resultado se contrasta contra los umbrales objetivos del documento HOR-OPS-002.

### 3.1 P1 — Crítico

Interrupción total o degradación severa de un servicio Tier 0, o afectación masiva a clientes sin solución temporal disponible.

Ejemplos canónicos:
- SPEI no envía ni recibe transferencias.
- Core bancario fuera de línea: no hay saldos ni movimientos en ningún canal.
- Switch de tarjetas rechazando más del 20% de las autorizaciones.
- Fuga de información confirmada de datos de clientes.
- Cierre batch nocturno fallido que impide la apertura operativa de sucursales.

Régimen: atención inmediata, 24×7, sin importar el día u hora. Puente de crisis abierto en 10 minutos. Guardias convocadas en paralelo, no en secuencia. Comunicación cada 30 minutos. Postmortem obligatorio en 5 días hábiles.

### 3.2 P2 — Alto

Degradación importante con solución temporal disponible, o interrupción total de un servicio Tier 1, o interrupción de un servicio Tier 0 para un subconjunto acotado de usuarios.

Ejemplos canónicos:
- App móvil caída pero banca en línea operando con normalidad.
- SPEI operando con latencia elevada: las transferencias se acreditan, pero fuera del tiempo esperado.
- Una región de ATM fuera de servicio (por ejemplo, la zona sureste).
- Contact center sin CRM, atendiendo con proceso manual.

Régimen: atención en horario extendido (06:00–24:00); si inicia en horario nocturno y no se degrada, puede diferirse al turno A previa autorización del Jefe de Turno. Comunicación cada 2 horas. Postmortem obligatorio en 10 días hábiles.

### 3.3 P3 — Medio

Afectación acotada, con alternativa operativa clara y sin riesgo de escalamiento inmediato.

Ejemplos canónicos:
- Falla en la generación de un reporte interno no regulatorio.
- Un cajero automático individual fuera de servicio.
- Lentitud en la originación de crédito PyME sin rechazo de solicitudes.
- Error de despliegue en ambiente de preproducción que bloquea pruebas.

Régimen: horario hábil. Objetivo de resolución en 3 días hábiles. Postmortem opcional (obligatorio solo si es reincidente).

### 3.4 P4 — Bajo

Defecto menor, cosmético o consulta operativa. No hay afectación al servicio.

Ejemplos canónicos:
- Etiqueta mal escrita en la app.
- Alerta de monitoreo mal calibrada que genera falso positivo.
- Solicitud de cambio de umbral en un tablero.

Régimen: horario hábil, cola normal, resolución en 15 días hábiles.

### 3.5 Tabla resumen

| Criterio | P1 | P2 | P3 | P4 |
|---|---|---|---|---|
| Servicio | Tier 0 caído | Tier 0 degradado / Tier 1 caído | Tier 1 degradado / Tier 2 caído | Sin afectación |
| Workaround | No existe | Existe pero costoso | Existe y es viable | No aplica |
| Horario de atención | 24×7 | 06:00–24:00 | Hábil | Hábil |
| ACK | 5 min | 15 min | 4 h | 1 día hábil |
| MTTR objetivo | 2 h | 8 h | 3 días hábiles | 15 días hábiles |
| Puente de crisis | Obligatorio | A criterio del IM | No | No |
| Postmortem | Obligatorio (5 días) | Obligatorio (10 días) | Si reincide | No |
| Notificación a Dirección | Inmediata | ≤ 1 h | En reporte diario | En reporte semanal |

## 4. Ciclo de vida del incidente

1. **Detección.** Por alerta automática (preferente), por reporte de usuario interno, por cliente vía contact center o por aviso de tercero (proveedor, cámara, autoridad).
2. **Registro.** Apertura del ticket INC con: servicio afectado, hora del primer síntoma, canales impactados, evidencia inicial y severidad propuesta.
3. **Clasificación.** El Jefe de Turno confirma o ajusta la severidad. Toda reclasificación queda registrada con hora y justificación.
4. **Triage y diagnóstico.** Se identifican los componentes sospechosos. Se revisan cambios recientes: cerca del 60% de los incidentes P1 y P2 de Banco Horizonte tienen un cambio en las 24 horas previas.
5. **Mitigación.** Se aplica workaround o se ejecuta el runbook correspondiente.
6. **Restablecimiento.** Se confirma con evidencia objetiva: métrica en rango, transacción de prueba exitosa y confirmación del área de negocio.
7. **Cierre.** Se documenta causa, acciones tomadas, duración y ventana de impacto para efectos de SLA.
8. **Aprendizaje.** Postmortem y apertura de PRB si la causa raíz persiste.

## 5. Reglas duras

1. **Regla de los 15 minutos.** Si en 15 minutos no hay hipótesis verificable de causa, se convoca a la siguiente línea de escalamiento. No se espera a "estar seguros".
2. **Regla de un solo comandante.** Durante el incidente hay un único Incident Manager. Si entra un directivo al puente, entra como participante, no como comandante.
3. **Regla de acción única.** Nunca se aplican dos cambios simultáneos en producción durante un incidente: se pierde la capacidad de atribuir el efecto.
4. **Regla de congelamiento.** Declarado un P1, se congelan automáticamente todos los cambios en el servicio afectado y en sus dependencias directas hasta el cierre.
5. **Regla de cliente primero.** Si existe forma de proteger al cliente (revertir cargos, suspender cobros, habilitar canal alterno) se ejecuta antes de terminar el diagnóstico.
6. **Regla de reloj honesto.** La hora de inicio del incidente es la del primer síntoma verificable, no la de la declaración.
7. **Regla de no culpa.** El postmortem describe sistemas y decisiones, no personas. Los nombres aparecen solo como roles.

## 6. Relación con el registro de riesgo operacional

Todo incidente P1 y P2, y todo incidente P3 con pérdida económica o afectación a datos de clientes, se registra como evento de riesgo operacional en la base de datos histórica administrada por Riesgos No Financieros, con los campos mínimos exigidos por la normativa aplicable: fecha de ocurrencia, fecha de descubrimiento, fecha de registro contable, línea de negocio, tipo de evento, monto bruto, montos recuperados, riesgo asociado (tecnológico, legal, operacional puro) y descripción breve. Las cuasi-pérdidas también se registran.

## 7. Prohibiciones

- Cerrar un incidente P1 o P2 sin confirmación explícita del área de negocio afectada.
- Reclasificar a la baja un incidente para evitar el postmortem.
- Resolver un ticket con la leyenda "se resolvió solo" sin hipótesis registrada.
- Modificar la bitácora del incidente después del cierre (las correcciones se agregan como adenda fechada).
- Comunicar externamente sin visto bueno de Comunicación y Cumplimiento.
