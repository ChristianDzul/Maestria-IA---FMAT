# Corpus documental — Banco Horizonte (sistema operativo bancario)

Corpus sintético para pruebas de RAG. Dominio: operación, incidentes y cumplimiento de una institución de banca múltiple mexicana ficticia (**Banco Horizonte, S.A.**).

## Manifiesto

| # | Archivo | Formato | Rama del árbol |
|---|---|---|---|
| 01 | `01_gobierno_y_estructura_organizacional.md` | Markdown | Raíz: Negocio / Operaciones / Regulación |
| 02 | `02_catalogo_servicios_criticos_y_sla.md` | Markdown | Operaciones → SLA |
| 03 | `03_command_center_operacion_y_matriz_raci.md` | Markdown | Operaciones → Command Center → RACI |
| 04 | `04_politica_gestion_incidentes.md` | Markdown | Incidentes → P1/P2/P3/P4 |
| 05 | `05_procedimiento_escalaciones_y_guardias.md` | Markdown | Command Center → Escalaciones |
| 06 | `06_protocolo_major_incident.md` | Markdown | Incidentes → Major Incident → TI/Negocio/Riesgos |
| 07 | `07_runbook_spei_indisponibilidad.md` | Markdown | Major Incident → Runbooks |
| 08 | `08_runbook_cierre_batch_core.md` | Markdown | Major Incident → Runbooks |
| 09 | `09_runbook_canales_digitales_y_autenticacion.md` | Markdown | Major Incident → Runbooks |
| 10 | `10_marco_regulatorio_cnbv.pdf` | PDF | Regulación → CNBV |
| 11 | `11_banxico_spei_obligaciones_operativas.pdf` | PDF | Regulación → Banxico |
| 12 | `12_bis_basilea_resiliencia_operacional.pdf` | PDF | Regulación → BIS |
| 13 | `13_lineas_de_negocio_captacion_credito_clientes.md` | Markdown | Negocio → Captación / Crédito / Clientes |
| 14 | `14_postmortem_INC-2026-0417.md` | Markdown | Incidentes → caso real documentado |
| 15 | `15_glosario_y_acronimos.txt` | Texto plano | Transversal |

Extensión aproximada: 21,000 palabras. Tres formatos distintos para ejercitar el pipeline de ingesta.

## Qué es real y qué es inventado

**Real (verificado en fuentes públicas, parafraseado):**
- Estructura del marco CNBV: CUB y sus anexos 1-D Bis, 12-A, 52, 64 Bis, 71 y 72; reportes serie R28 enviados por SITI; figura del Plan Director de Seguridad; concepto de cuasi-pérdida.
- SPEI: operación continua 24×7, cambio de fecha de operación a las 18:00, obligación de mantener conexión y aplicar contingencia al perderla, solicitud de ampliación de horario, firmeza e irrevocabilidad de las transferencias liquidadas, CEP disponible ~30 minutos después del movimiento.
- BIS/Basilea: Principios para la Resiliencia Operacional (31 de marzo de 2021), sus siete categorías, la definición de resiliencia operacional y de tolerancia a la interrupción, y su relación con los PSMOR (2011, revisados 2014 y 2021).

**Inventado con detalle:** Banco Horizonte y toda su operación — nombres, cifras, SLA, RACI, runbooks, comandos, incidentes, postmortem, personas y estructura interna. Cualquier parecido con una institución real es coincidencia.

Los documentos no citan números de artículo específicos de la CUB: esas referencias cambian con cada reforma publicada en el DOF y habrían envejecido mal dentro del corpus.

## Preguntas de prueba sugeridas

**Recuperación simple (un documento):**
1. ¿En cuántos minutos debe reconocerse un incidente P1?
2. ¿Cuál es el RTO del servicio SPEI en Banco Horizonte?
3. ¿A qué hora cambia el SPEI de fecha de operación?
4. ¿Qué es una cuasi-pérdida?

**Recuperación multi-documento (requieren unir fuentes):**
5. Si el SPEI se cae 12 minutos un martes a las 16:50, ¿qué pasa exactamente? (cruza runbook 07, política 04, protocolo 06 y obligaciones 11)
6. ¿Quién aprueba la declaración de un Major Incident y quién puede vetar una acción del Incident Commander? (cruza 03, 05 y 06)
7. ¿Qué relación hay entre el postmortem de INC-2026-0417 y la brecha de "aprendizaje post-evento" identificada frente a los principios de Basilea? (cruza 14 y 12)
8. ¿Por qué el failover de sitio no habría resuelto el incidente de julio de 2026? (cruza 07 y 14)

**Razonamiento sobre tablas:**
9. ¿Cuántos minutos de indisponibilidad al mes permite un SLO de 99.95%?
10. ¿Qué severidad corresponde a un incidente con 8,000 clientes afectados y sin workaround?

**Preguntas imposibles de responder con el corpus** (para validar que el sistema dice "no sé" en lugar de alucinar):
11. ¿Cuál fue la utilidad neta de Banco Horizonte en 2025?
12. ¿Qué proveedor específico presta el servicio de biometría facial? *(el corpus lo menciona pero nunca lo nombra, por política interna)*
13. ¿Cuántos empleados tiene el área de Ciberseguridad?
14. ¿Cuál es el número de artículo de la CUB que obliga al Plan Director de Seguridad?
15. ¿Qué dice la cláusula de penalización del contrato con el agregador de SMS?

## Notas para la ingesta

- Los encabezados `##` y `###` funcionan bien como fronteras naturales de chunk. Un chunk de 800–1,000 tokens con solapamiento de 100–150 captura secciones completas sin partir tablas.
- Las tablas Markdown se degradan mucho si el chunker corta a la mitad; conviene tratarlas como bloque atómico o convertirlas a texto plano antes de indexar.
- Los tres PDF extraen texto limpio con `pypdf` o `pdfplumber`; el pie de página se repite en cada página y conviene filtrarlo en el preprocesamiento.
- Los identificadores (`HOR-OPS-004`, `INC-2026-0417`, `SVC-001`) son ganchos deliberados de referencia cruzada: sirven para probar si el recuperador sigue enlaces entre documentos.
- El glosario en `.txt` es buen caso de prueba para chunking por separadores distintos a Markdown.
