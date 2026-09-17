# Matriz de Severidad de Incidentes

**Clasificación:** SINTÉTICO

## 1. Criterios

La severidad se determina usando:
- clientes afectados;
- procesos críticos;
- monto/impacto financiero;
- duración;
- disponibilidad;
- integridad de datos;
- riesgo regulatorio;
- seguridad/ciberseguridad;
- posibilidad de propagación;
- existencia de workaround.

## 2. P1 — Crítico

Características:
- proceso crítico indisponible;
- impacto masivo;
- riesgo de integridad de datos;
- posible impacto financiero material;
- ausencia de workaround efectivo;
- evento de seguridad de alta criticidad.

Objetivos:
- reconocimiento ≤ 5 min;
- Incident Manager ≤ 10 min;
- Command Center ≤ 15 min;
- primera comunicación ≤ 15 min;
- actualizaciones cada 15 min.

## 3. P2 — Alto

Características:
- impacto relevante pero limitado;
- servicio degradado;
- workaround disponible;
- grupo limitado de clientes;
- riesgo de incumplir SLA crítico.

Objetivos:
- reconocimiento ≤ 10 min;
- responsable ≤ 15 min;
- actualización cada 30 min.

## 4. P3 — Medio

Características:
- impacto limitado;
- pocos clientes;
- proceso no crítico;
- workaround disponible.

Objetivos:
- reconocimiento ≤ 30 min;
- actualización cada 60 min.

## 5. P4 — Bajo

Solicitud o incidencia sin impacto relevante sobre operación crítica.

Atención mediante operación normal.

## 6. Regla de escalación

Si existen criterios de diferentes niveles, se aplica temporalmente el nivel superior hasta completar el análisis.

La severidad puede subir o bajar conforme cambia la evidencia.
