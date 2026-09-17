---
documento: HOR-GOB-001
titulo: Manual de Gobierno y Estructura Organizacional
version: 4.2
vigencia_desde: 2026-01-15
clasificacion: Uso Interno
propietario: Dirección General de Operaciones y Tecnología
aprobado_por: Comité de Dirección
proxima_revision: 2027-01-15
---

# Manual de Gobierno y Estructura Organizacional — Banco Horizonte, S.A.

## 1. Propósito

Este documento describe la estructura organizacional de Banco Horizonte, S.A., Institución de Banca Múltiple, y define las responsabilidades de gobierno sobre los procesos operativos críticos. Es el documento raíz del marco normativo interno: todos los demás manuales, políticas y runbooks derivan de las responsabilidades aquí establecidas.

## 2. Perfil institucional

| Concepto | Dato |
|---|---|
| Razón social | Banco Horizonte, S.A., Institución de Banca Múltiple |
| Fundación | 1994 |
| Sede corporativa | Torre Horizonte, Av. Paseo de la Reforma 615, Ciudad de México |
| Centros de cómputo | CPD-Primario (Querétaro), CPD-Alterno (Monterrey), zona cloud híbrida (región mx-central) |
| Sucursales | 412 en 31 entidades federativas |
| Clientes activos | 6.8 millones (4.9 M personas físicas, 1.9 M PyME y empresas) |
| Empleados | 11,340 |
| Clave de institución (SPEI) | 40999 (ficticia, para efectos de este corpus) |
| Segmentos | Banca de Personas, Banca PyME, Banca Empresarial, Banca Patrimonial |

## 3. Estructura de primer nivel

La institución se organiza en tres pilares que reportan a la Dirección General:

```
                    BANCO HORIZONTE
                           │
        ┌──────────────────┼──────────────────┐
     NEGOCIO           OPERACIONES        REGULACIÓN
```

### 3.1 Pilar NEGOCIO

Responsable de la relación comercial, el diseño de producto y el resultado financiero. Se divide en tres direcciones:

- **Dirección de Captación (DN-CAP).** Cuentas de cheques, cuentas de ahorro, Pagaré con Rendimiento Liquidable al Vencimiento (PRLV), depósitos a plazo e inversión de disponibilidad inmediata. Titular: Mariana Escobedo Rangel.
- **Dirección de Crédito (DN-CRE).** Crédito simple, crédito revolvente (tarjeta), crédito automotriz, hipotecario y crédito PyME. Titular: Jorge Iván Lemus Treviño.
- **Dirección de Clientes y Experiencia (DN-CLI).** Contact center, gestión de quejas y aclaraciones, UNE (Unidad Especializada de Atención a Usuarios), NPS y diseño de journeys. Titular: Paola Cárdenas Uribe.

### 3.2 Pilar OPERACIONES

Responsable de que los servicios funcionen. Contiene:

- **Command Center (OP-CC).** Centro de mando operativo 24×7. Monitoreo, detección, clasificación y coordinación de incidentes. Es el único punto autorizado para declarar un Major Incident. Titular: Ricardo Ontiveros Mena.
- **Dirección de Pagos y Medios (OP-PAG).** SPEI, SPID, CoDi, domiciliaciones, cámara de compensación (CECOBAN), adquirencia y switch de tarjetas.
- **Dirección de Plataformas (OP-PLT).** Core bancario (Horizonte Core, sobre AS/400 modernizado + capa de servicios Java), canales digitales, middleware ESB, bases de datos y cloud.
- **Dirección de Ciberseguridad (OP-CIB).** SOC, gestión de identidades, DLP, respuesta a incidentes de seguridad de la información.

### 3.3 Pilar REGULACIÓN

Responsable del cumplimiento y de la relación con autoridades:

- **Enlace CNBV (RG-CNBV).** Reportes regulatorios de la serie R28, informes de incidentes de seguridad de la información, visitas de inspección.
- **Enlace Banco de México (RG-BXO).** Cumplimiento de las Reglas del SPEI, reportes de disponibilidad y participación en pruebas del sistema de pagos.
- **Alineación a estándares internacionales (RG-BIS).** Traducción de los principios de Basilea (resiliencia operacional, riesgo operacional, BCBS 239) a políticas internas.
- **Dirección de Riesgos No Financieros (RG-RNF).** Riesgo operacional, riesgo tecnológico, continuidad de negocio y base de datos histórica de eventos de pérdida.

## 4. Comités de gobierno

| Comité | Frecuencia | Preside | Alcance operativo |
|---|---|---|---|
| Comité de Dirección | Semanal | Director General | Aprueba apetito de riesgo y tolerancia a la interrupción |
| Comité de Riesgos | Mensual | Director de Riesgos (CRO) | Revisa eventos de pérdida, KRI y umbrales de impacto |
| Comité de Tecnología y Operación (COTEC) | Quincenal | Director de Operaciones y Tecnología | Aprueba cambios mayores, revisa SLA y tendencias de incidentes |
| Comité de Continuidad de Negocio (CCN) | Trimestral | Director General Adjunto | Aprueba RTO/RPO, calendario de pruebas y planes de contingencia |
| Comité de Crisis | Bajo convocatoria | Director General | Se activa por Major Incident con impacto sistémico o reputacional |
| Comité de Seguridad de la Información | Mensual | CISO | Plan Director de Seguridad e indicadores de seguridad |

## 5. Modelo de tres líneas de defensa

1. **Primera línea:** las áreas de Negocio y Operaciones, dueñas del riesgo en sus procesos. El Command Center y los equipos de plataforma pertenecen a esta línea.
2. **Segunda línea:** Riesgos No Financieros, Ciberseguridad (función de gobierno) y Cumplimiento. Definen metodología, vigilan y retan a la primera línea.
3. **Tercera línea:** Auditoría Interna, con reporte directo al Consejo de Administración a través del Comité de Auditoría.

Ninguna persona puede ejercer funciones de primera y segunda línea sobre el mismo proceso. La declaración de un Major Incident es facultad exclusiva de primera línea (Command Center); la validación del postmortem es facultad de segunda línea.

## 6. Principio de operación crítica

Banco Horizonte define como **operación crítica** todo proceso cuya interrupción afecte de forma material a clientes, a contrapartes o al sistema de pagos. El catálogo de operaciones críticas se mantiene en el documento HOR-OPS-002 (Catálogo de Servicios Críticos y SLA) y su modificación requiere aprobación del COTEC y notificación al Comité de Riesgos.

## 7. Cadena de mando en horario no hábil

Fuera de horario de oficina, la autoridad operativa recae en el **Jefe de Turno del Command Center** (rol rotativo, cuatro turnos). El Jefe de Turno puede:

- Declarar incidentes de cualquier severidad, incluido P1.
- Convocar a guardias de cualquier área sin autorización previa.
- Autorizar la ejecución de runbooks con impacto reversible.
- Solicitar la activación del Comité de Crisis.

No puede, sin autorización del Director de Operaciones: autorizar cambios no reversibles en producción, declarar contingencia ante Banco de México, ni emitir comunicación pública.
