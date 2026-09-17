---
documento: HOR-OPS-006
titulo: Protocolo de Major Incident (MIM)
version: 4.0
vigencia_desde: 2026-06-01
clasificacion: Uso Interno / Confidencial en anexos
propietario: Dirección de Operaciones y Tecnología
---

# Protocolo de Major Incident Management (MIM)

## 1. Qué es un Major Incident

Un Major Incident (MI) es un incidente P1 que además cumple **al menos uno** de los siguientes criterios de amplificación:

| # | Criterio de amplificación | Umbral |
|---|---|---|
| 1 | Duración | P1 que supera 60 minutos sin restablecimiento ni ruta clara de solución |
| 2 | Alcance | Más de 100,000 clientes afectados o una línea de negocio completa detenida |
| 3 | Sistema de pagos | Afectación a SPEI, SPID o cámara de compensación por más de 10 minutos |
| 4 | Integridad de datos | Duda razonable sobre saldos, movimientos o posiciones contables |
| 5 | Seguridad | Intrusión confirmada o sospecha fundada de exfiltración de datos de clientes |
| 6 | Regulatorio | Evento notificable a CNBV o a Banco de México |
| 7 | Reputacional | Cobertura en medios nacionales o tendencia en redes con volumen relevante |
| 8 | Financiero | Pérdida estimada superior a 20 millones de pesos |
| 9 | Resiliencia | Falla simultánea de sitio primario y alterno, o de un proveedor crítico único |

**Todo MI es P1. No todo P1 es MI.**

La declaración es facultad del Jefe de Turno del Command Center y no requiere autorización previa. Puede declararse por precaución y desactivarse después; la desactivación sí requiere autorización del Director de Operaciones y Tecnología.

## 2. Estructura de mando durante un MI

```
                    MAJOR INCIDENT
                           │
                 Incident Commander (IC)
                           │
       ┌───────────────┬───┴────┬───────────────┐
       │               │        │               │
   Célula TI      Célula Negocio  Célula Riesgos  Scribe
       │               │        │
  Runbooks       Contención    Evaluación de
  y recuperación  al cliente    exposición
```

### 2.1 Incident Commander (IC)

- Rol asumido por el Jefe de Turno hasta que se incorpore un IC certificado (lista de 14 personas certificadas en la institución).
- **Decide, no diagnostica.** Su trabajo es mantener la línea de tiempo, asignar tareas, cortar discusiones y decidir cuándo se aplica un cambio.
- Única persona autorizada a aprobar acciones sobre producción durante el MI.
- No puede ser simultáneamente el especialista técnico principal. Si esto ocurre, se transfiere el rol de IC explícitamente y se anuncia en el puente.

### 2.2 Célula TI

Integra a los equipos técnicos convocados y a los proveedores. Entrega al IC: hipótesis, opciones con su riesgo asociado, tiempo estimado y plan de reversión. **Nunca ejecuta sin autorización del IC durante el MI.**

Perfil mínimo convocado en un MI de core o pagos: plataforma dueña, DBA, redes, seguridad, y el líder de la última liberación al servicio afectado.

### 2.3 Célula Negocio

Responsable de proteger al cliente mientras TI repara:

- Habilitar canales alternos (sucursal, corresponsales, atención telefónica con proceso manual).
- Suspender campañas, cobros automáticos o cargos que puedan duplicarse.
- Definir el mensaje al cliente junto con Comunicación.
- Estimar el impacto comercial y el volumen de operaciones pendientes.
- Preparar el plan de resarcimiento (devolución de comisiones, ajuste de intereses, atención prioritaria a reclamaciones).

### 2.4 Célula Riesgos

- Evalúa exposición financiera, legal y regulatoria en tiempo real.
- Determina si el evento es notificable y en qué plazo.
- Activa el registro del evento de pérdida operacional.
- Valida que las acciones de mitigación no generen un riesgo mayor que el incidente (por ejemplo: reabrir un canal sin controles antifraude).
- Es la única célula con facultad de **vetar** una acción del IC, y debe hacerlo por escrito en el canal del incidente.

### 2.5 Scribe

Registra cronología con marca de tiempo: qué se supo, qué se decidió, quién lo decidió y qué se ejecutó. El registro del Scribe es el documento fuente del postmortem y, si el evento es notificable, del expediente regulatorio. No participa en el diagnóstico.

## 3. Cadencia de un MI

| Momento | Acción |
|---|---|
| T+0 | Declaración. Apertura de Puente 8000 y canal dedicado #mi-INC-AAAA-NNNN |
| T+5 min | Nombramiento de IC y Scribe. Pase de lista de células |
| T+10 min | Primera línea de tiempo consolidada. Hipótesis inicial |
| T+15 min | Primer comunicado interno a Dirección |
| T+20 min | Decisión sobre canales alternos (célula Negocio) |
| T+30 min | Primer dictamen de notificabilidad (célula Riesgos) |
| Cada 20 min | Actualización en el canal y en el puente |
| Cada 60 min | Reporte ejecutivo escrito a Comité de Dirección |
| Restablecimiento | Confirmación técnica + confirmación de negocio + transacción de prueba |
| T+60 min post | Cierre del MI y paso a modo seguimiento |
| T+24 h | Reporte preliminar de causa |
| T+5 días hábiles | Postmortem formal validado por Riesgos |
| T+30 días | Revisión de cumplimiento de acciones correctivas en COTEC |

## 4. Comité de Crisis

Se activa cuando el MI cumple criterios 3, 4, 5, 6 o 7 y su duración estimada supera 2 horas.

| Integrante | Rol en el comité |
|---|---|
| Director General | Preside; decide comunicación pública y medidas extraordinarias |
| Director de Operaciones y Tecnología | Reporta estado técnico; canal único con el IC |
| Director de Riesgos (CRO) | Exposición, notificaciones y registro del evento |
| Director Jurídico | Implicaciones legales y contractuales |
| Director de Comunicación | Mensaje a clientes, medios y colaboradores |
| Director de la línea de negocio afectada | Impacto comercial y resarcimiento |
| Enlace regulatorio correspondiente | Interlocución con la autoridad |

El Comité de Crisis **no dirige el incidente**. Dirige la respuesta institucional. El IC conserva el mando técnico. Esta separación es la falla más común en simulacros: en el ejercicio de continuidad de marzo de 2026 el comité tomó decisiones técnicas durante 18 minutos y el equipo perdió el hilo del diagnóstico.

## 5. Criterios de salida

Un MI se cierra cuando se cumplen simultáneamente:

1. El servicio opera dentro de parámetros normales por al menos 30 minutos continuos.
2. El área de negocio confirma que la operación fluye.
3. No existen transacciones en estado inconsistente sin plan de regularización.
4. Se documentó la causa o, si no se conoce, se documentó el plan de investigación y el riesgo residual aceptado por el Director de Operaciones.
5. Se ejecutó la conciliación de la ventana afectada.

## 6. Post-MI inmediato

- **Reunión en caliente (hot debrief):** 30 minutos, dentro de las 4 horas siguientes al cierre, con todas las células. Objetivo: capturar lo que aún está fresco, no asignar responsabilidad.
- **Conservación de evidencia:** logs, volcados, capturas y grabación del puente se preservan por 5 años cuando el evento es notificable.
- **Reconciliación:** Contraloría valida que la contabilidad del día refleje correctamente el incidente y sus reversos.
- **Atención al cliente:** DN-CLI activa protocolo de reclamaciones prioritarias con SLA reducido a 48 horas para los clientes identificados como afectados.

## 7. Escenarios documentados de MI (histórico 2024–2026)

| ID | Fecha | Escenario | Duración | Criterio de amplificación |
|---|---|---|---|---|
| INC-2024-0712 | 2024-08-19 | Falla de storage en CPD primario, core degradado | 4 h 12 min | 1, 2, 4 |
| INC-2025-0233 | 2025-04-03 | Corrupción de índice en base de saldos tras liberación | 6 h 40 min | 1, 4, 8 |
| INC-2025-0891 | 2025-11-28 | Saturación de app móvil en Buen Fin | 3 h 05 min | 2, 7 |
| INC-2026-0417 | 2026-07-14 | Indisponibilidad SPEI por certificado expirado | 2 h 48 min | 1, 2, 3, 6 |
| INC-2026-0502 | 2026-08-22 | Proveedor de autenticación biométrica caído | 1 h 55 min | 2, 9 |

El detalle del incidente INC-2026-0417 se documenta en HOR-PM-014.
