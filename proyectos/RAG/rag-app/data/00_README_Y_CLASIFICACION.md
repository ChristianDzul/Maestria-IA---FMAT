# Corpus RAG Bancario — Banco Horizonte

## Propósito
Corpus sintético y documental para construir un RAG orientado a operación bancaria, Command Center, gestión de incidentes, escalaciones, clientes, captación, finanzas y pagos.

## Regla fundamental
Este corpus mezcla:
1. **Conocimiento basado en fuentes públicas**: conceptos y requisitos generales tomados de BIS/BCBS, Banco de México, CNBV e ISO 20022.
2. **Conocimiento operativo sintético**: nombres de áreas, SLAs, severidades, matrices, RACI, runbooks y procedimientos internos creados específicamente para este proyecto.

Todo contenido marcado como `SINTÉTICO` debe considerarse una política interna ficticia de Banco Horizonte y NO una regla de un banco real.

## Fuentes públicas principales
- BIS/BCBS — Operational Resilience: gobierno, riesgo operacional, continuidad, dependencias, incident management e ICT resilience.
- Banco de México — SPEI, Circular 14/2017 y documentación pública del sistema.
- CNBV — Disposiciones de carácter general aplicables a instituciones de crédito.
- ISO 20022 — Business Process Catalogue, Data Dictionary y definiciones de mensajes financieros.

## Recomendación para ingestión
Conservar metadatos:
- document_id
- document_type
- area
- process
- subprocess
- criticality
- source_type = PUBLICO | SINTETICO
- jurisdiction = MEXICO | INTERNACIONAL
- effective_date
- version
- confidentiality = PUBLICO | INTERNO_SIMULADO

No mezclar `SINTETICO` con `PUBLICO` durante la recuperación sin conservar la procedencia.
