---
documento: HOR-OPS-005
titulo: Procedimiento de Escalaciones, Guardias y Árbol de Notificación
version: 3.8
vigencia_desde: 2026-05-20
clasificacion: Uso Interno
propietario: Command Center (OP-CC)
---

# Procedimiento de Escalaciones, Guardias y Árbol de Notificación

## 1. Tipos de escalamiento

Banco Horizonte distingue dos escalamientos que no deben confundirse:

- **Escalamiento funcional (horizontal):** se busca más capacidad técnica. Se sube de nivel de soporte (N1 → N2 → N3 → proveedor). No cambia quién decide.
- **Escalamiento jerárquico (vertical):** se busca autoridad para decidir o recursos que el nivel actual no controla. Sube por la línea de mando.

Un incidente puede tener ambos escalamientos activos al mismo tiempo. Confundirlos es el error más frecuente: llamar a un director no aporta capacidad de diagnóstico, y llamar a un ingeniero senior no autoriza gastar dinero ni notificar a una autoridad.

## 2. Niveles de soporte (escalamiento funcional)

| Nivel | Quién | Alcance | Tiempo máximo antes de escalar |
|---|---|---|---|
| N1 | Operador del Command Center | Triage, ejecución de runbooks documentados, reinicio de servicios de bajo riesgo | 15 min (P1) / 45 min (P2) |
| N2 | Ingeniero de guardia del equipo dueño | Diagnóstico profundo, cambios en configuración, failover | 30 min (P1) / 2 h (P2) |
| N3 | Arquitecto o especialista de la plataforma | Cambios estructurales, análisis de código, recuperación de datos | 60 min (P1) / 4 h (P2) |
| N4 | Proveedor o fabricante con contrato de soporte crítico | Bugs de producto, hardware, plataformas de terceros | Según contrato |

## 3. Matriz de escalamiento jerárquico

| Tiempo transcurrido sin restablecimiento | P1 | P2 | P3 |
|---|---|---|---|
| T+0 | Jefe de Turno CC | Jefe de Turno CC | Operador CC |
| T+15 min | Gerente de Operaciones + gerente del área dueña | — | — |
| T+30 min | Director de Plataformas / Director de Pagos (según servicio) | — | — |
| T+1 h | Director de Operaciones y Tecnología; se notifica a Riesgos No Financieros | Gerente del área dueña | — |
| T+2 h | Director General Adjunto; evaluación de Comité de Crisis | Director del área dueña | — |
| T+4 h | Director General; Cumplimiento evalúa notificación a autoridad | Director de Operaciones y Tecnología | Gerente del área |
| T+8 h | Consejo (a través del Comité de Riesgos) | Director General Adjunto | Director del área |

El reloj de escalamiento **no se detiene** por avances parciales de diagnóstico. Solo se detiene con el restablecimiento del servicio o con la reclasificación formal a la baja.

## 4. Escalamiento anticipado (trigger-based)

Existen condiciones que disparan escalamiento inmediato al máximo nivel sin esperar el reloj:

1. Afectación confirmada al SPEI por más de 10 minutos.
2. Sospecha fundada de intrusión, exfiltración o fraude interno.
3. Posible afectación a la integridad de saldos o a la contabilidad del día.
4. Solicitud expresa de una autoridad (CNBV, Banco de México, CONDUSEF).
5. Difusión del incidente en medios o redes sociales con volumen relevante.
6. Fallo simultáneo del sitio primario y del sitio alterno.
7. Indisponibilidad del propio Command Center.

Cualquier persona de la institución puede invocar un escalamiento anticipado. La invocación nunca se sanciona, aunque resulte injustificada. Esta es una política explícita: el costo de una convocatoria innecesaria es menor que el de un silencio prudente.

## 5. Esquema de guardias (on-call)

### 5.1 Reglas

- Cada equipo técnico dueño de un servicio Tier 0 o Tier 1 mantiene guardia primaria y secundaria, 24×7, en rotación semanal (lunes 09:00 a lunes 09:00).
- La guardia primaria debe **reconocer** la llamada en 5 minutos y estar **conectada** al puente en 15 minutos, con conexión estable y acceso vigente a producción.
- Si la primaria no responde tras tres intentos en 10 minutos, HorizonteOnCall escala automáticamente a la secundaria; si la secundaria falla, escala al gerente del área.
- La persona de guardia no puede estar fuera de cobertura de datos, ni en condición que impida operar con seguridad.
- El acceso de emergencia a producción se otorga mediante credencial temporal (*break-glass*) con vigencia de 4 horas, aprobación del Jefe de Turno y auditoría posterior obligatoria en 48 horas.

### 5.2 Cobertura por servicio

| Servicio | Equipo de guardia | Primaria | Secundaria | Escalamiento gerencial |
|---|---|---|---|---|
| SPEI | Pagos Interbancarios | Rotación de 6 ingenieros | Rotación de 3 | Gerente de Pagos |
| Switch de tarjetas | Medios de Pago | Rotación de 5 | Rotación de 3 | Gerente de Medios |
| Core bancario | Plataforma Core | Rotación de 8 | Rotación de 4 | Gerente de Core |
| Canales digitales | Digital Engineering | Rotación de 7 | Rotación de 4 | Gerente Digital |
| Base de datos | DBA | Rotación de 4 | Rotación de 2 | Gerente de Datos |
| Redes y comunicaciones | Infraestructura | Rotación de 5 | Rotación de 3 | Gerente de Infraestructura |
| Ciberseguridad | SOC | Turno fijo 24×7 | Rotación de 4 | CISO |

### 5.3 Higiene de la guardia

- Máximo dos semanas de guardia al mes por persona.
- Si una guardia nocturna implica más de 2 horas de trabajo efectivo entre 00:00 y 06:00, la persona queda liberada de la jornada siguiente.
- Las guardias con más de 5 activaciones por semana disparan revisión obligatoria de ruido de alertas y de deuda técnica del servicio en el COTEC siguiente.

## 6. Árbol de notificación (P1 / Major Incident)

```
                Detección (alerta o reporte)
                            │
                   Operador CC — registra
                            │
                   Jefe de Turno — clasifica P1
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
  Guardia N2 del        Incident Manager   Analista de
  servicio afectado     abre Puente 8000   comunicación
        │                   │                   │
   Guardia N3 y        Convoca dependencias   Notifica a:
   proveedor (si        (DBA, red, seguridad)  - Dirección de Operaciones
   aplica)                    │                - Negocio afectado
                              │                - Riesgos No Financieros
                    ¿Cumple criterios de       - Cumplimiento (si aplica)
                      Major Incident?
                              │
                   Sí ────────┴──────── No
                    │                    │
        Protocolo Major Incident    Continúa como P1
        (HOR-OPS-006)               estándar
```

## 7. Directorio de escalamiento (extracto)

| Rol | Nombre | Contacto interno | Respaldo |
|---|---|---|---|
| Jefe de Turno CC (rotativo) | — | Ext. 8000 / Puente 8000 | Gerente de Operaciones |
| Gerente de Operaciones | Adriana Sosa Peniche | Ext. 8012 | Gerente de Plataformas |
| Director de Plataformas | Héctor Villalobos Arceo | Ext. 8100 | Director de Pagos |
| Director de Pagos y Medios | Susana Márquez del Río | Ext. 8200 | Director de Plataformas |
| Director de Operaciones y TI | Ricardo Ontiveros Mena | Ext. 8001 | Director General Adjunto |
| CISO | Emilio Fuentes Zaldívar | Ext. 8300 | Subdirector de SOC |
| Riesgos No Financieros | Verónica Tamayo Gil | Ext. 8400 | Gerente de Riesgo Tecnológico |
| Enlace CNBV | Alfonso Rendón Bautista | Ext. 8500 | Director Jurídico |
| Enlace Banco de México | Claudia Nieto Barragán | Ext. 8510 | Director de Pagos |
| Comunicación institucional | Ivonne Portilla Cruz | Ext. 8600 | Dirección de Marca |

El directorio completo, con teléfonos personales, se mantiene en el sistema HorizonteOnCall y se valida trimestralmente mediante prueba de marcación no anunciada. La última prueba (julio de 2026) arrojó 91% de contactabilidad en primer intento.

## 8. Errores frecuentes documentados

| Error | Consecuencia observada | Corrección |
|---|---|---|
| Escalar en secuencia y no en paralelo durante P1 | Se perdieron 40 minutos en INC-2026-0298 | Convocatoria simultánea desde el minuto cero |
| Notificar a directivos antes de tener línea de tiempo | Ruido en el puente, IM interrumpido | Comunicación por canal separado del puente técnico |
| Guardia sin acceso vigente a producción | 25 min de retraso en INC-2026-0351 | Validación mensual automatizada de accesos de guardia |
| Reclasificar a P2 para no escalar | Incidente creció a Major Incident sin dirección enterada | Toda reclasificación a la baja requiere segunda firma |
