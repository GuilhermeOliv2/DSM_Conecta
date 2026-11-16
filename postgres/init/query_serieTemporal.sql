CREATE EXTENSION IF NOT EXISTS timescaledb;

-- Diagrama das relações: ../docs/diagrama-relacionamento-serie-temporal.md

-- Sessão anônima do visitante
CREATE TABLE IF NOT EXISTS visitor_session (
    id uuid PRIMARY KEY,
    anonymous_token text NOT NULL UNIQUE,
    platform text NOT NULL,
    started_at timestamptz NOT NULL,
    ended_at timestamptz,
    expires_at timestamptz NOT NULL,
    CONSTRAINT visitor_session_time_ck CHECK (
        ended_at IS NULL OR ended_at >= started_at
    )
);

-- Consentimento do visitante
CREATE TABLE IF NOT EXISTS consent_record (
    id uuid PRIMARY KEY,
    session_id uuid NOT NULL REFERENCES visitor_session(id),
    consent_type text NOT NULL,
    granted boolean NOT NULL,
    granted_at timestamptz NOT NULL,
    revoked_at timestamptz,
    policy_version text NOT NULL,
    CONSTRAINT consent_record_time_ck CHECK (
        revoked_at IS NULL OR revoked_at >= granted_at
    )
);

CREATE INDEX IF NOT EXISTS consent_record_session_type_idx
    ON consent_record (session_id, consent_type, granted_at DESC);

-- Controle de deduplicação por event_id
CREATE TABLE IF NOT EXISTS telemetry_event_dedup (
    event_id text PRIMARY KEY,
    first_seen_at timestamptz NOT NULL DEFAULT now()
);

-- Fato bruto da telemetria
CREATE TABLE IF NOT EXISTS telemetry_event (
    event_id text NOT NULL,
    session_id text NOT NULL,
    consent_id uuid REFERENCES consent_record(id),
    category text NOT NULL,
    origin text NOT NULL,
    topic text NOT NULL,
    schema_version text NOT NULL,
    occurred_at timestamptz NOT NULL,
    payload jsonb NOT NULL,
    location_latitude double precision,
    location_longitude double precision,
    location_accuracy double precision,
    ingested_at timestamptz NOT NULL DEFAULT now(),
    PRIMARY KEY (event_id, occurred_at),

    CONSTRAINT telemetry_event_category_ck CHECK (
        category IN ('interacao', 'quiz', 'presenca', 'sensor')
    ),
    CONSTRAINT telemetry_event_origin_ck CHECK (
        origin IN ('app', 'totem')
    ),
    CONSTRAINT telemetry_event_payload_object_ck CHECK (
        jsonb_typeof(payload) = 'object'
    ),

    -- Garantia de integridade da localização
    CONSTRAINT telemetry_event_location_complete_ck CHECK (
        (location_latitude IS NULL
         AND location_longitude IS NULL
         AND location_accuracy IS NULL)
        OR
        (location_latitude IS NOT NULL
         AND location_longitude IS NOT NULL
         AND location_accuracy IS NOT NULL)
    ),

    CONSTRAINT telemetry_event_location_bounds_ck CHECK (
        location_latitude IS NULL
        OR (
            location_latitude BETWEEN -90 AND 90
            AND location_longitude BETWEEN -180 AND 180
            AND location_accuracy >= 0
        )
    ),

    -- Regra de minimização: no celular, somente latitude/longitude/precisão serão persistidos.
    -- Outros sensores ficam no dispositivo e não entram no banco.
    CONSTRAINT telemetry_event_sensor_location_ck CHECK (
        (category = 'sensor' AND origin = 'app'
         AND location_latitude IS NOT NULL
         AND location_longitude IS NOT NULL
         AND location_accuracy IS NOT NULL)
        OR
        (NOT (category = 'sensor' AND origin = 'app')
         AND location_latitude IS NULL
         AND location_longitude IS NULL
         AND location_accuracy IS NULL)
    )
);

-- Criação da hipertabela temporal
SELECT create_hypertable(
    'telemetry_event',
    by_range('occurred_at', INTERVAL '1 day'),
    if_not_exists => TRUE
);

-- Índices para consultas temporais e filtros de negócio
CREATE INDEX IF NOT EXISTS telemetry_event_category_time_idx
    ON telemetry_event (category, occurred_at DESC);

CREATE INDEX IF NOT EXISTS telemetry_event_session_time_idx
    ON telemetry_event (session_id, occurred_at DESC);

CREATE INDEX IF NOT EXISTS telemetry_event_origin_time_idx
    ON telemetry_event (origin, occurred_at DESC);

CREATE INDEX IF NOT EXISTS telemetry_event_location_time_idx
    ON telemetry_event (occurred_at DESC)
    WHERE location_latitude IS NOT NULL;

-- Compressão dos dados brutos após 30 dias
ALTER TABLE telemetry_event SET (
    timescaledb.compress,
    timescaledb.compress_segmentby = 'category,origin',
    timescaledb.compress_orderby = 'occurred_at DESC'
);

SELECT add_compression_policy(
    'telemetry_event',
    compress_after => INTERVAL '30 days',
    if_not_exists => TRUE
);

-- Retenção dos fatos brutos após 90 dias
SELECT add_retention_policy(
    'telemetry_event',
    drop_after => INTERVAL '90 days',
    if_not_exists => TRUE
);

-- Agregação contínua por hora
CREATE MATERIALIZED VIEW IF NOT EXISTS telemetry_hourly
WITH (timescaledb.continuous) AS
SELECT
    time_bucket(INTERVAL '1 hour', occurred_at) AS bucket,
    category,
    origin,
    count(*) AS event_count,
    count(DISTINCT session_id) AS session_count
FROM telemetry_event
GROUP BY bucket, category, origin
WITH NO DATA;

SELECT add_continuous_aggregate_policy(
    'telemetry_hourly',
    start_offset => INTERVAL '7 days',
    end_offset => INTERVAL '1 minute',
    schedule_interval => INTERVAL '5 minutes',
    if_not_exists => TRUE
);

-- Agregação contínua por dia
CREATE MATERIALIZED VIEW IF NOT EXISTS telemetry_daily
WITH (timescaledb.continuous) AS
SELECT
    time_bucket(INTERVAL '1 day', occurred_at) AS bucket,
    category,
    origin,
    count(*) AS event_count,
    count(DISTINCT session_id) AS session_count
FROM telemetry_event
GROUP BY bucket, category, origin
WITH NO DATA;

SELECT add_continuous_aggregate_policy(
    'telemetry_daily',
    start_offset => INTERVAL '120 days',
    end_offset => INTERVAL '1 hour',
    schedule_interval => INTERVAL '1 hour',
    if_not_exists => TRUE
);

-- Visão pública: expõe só agregados e grupos com mínimo de 10 sessões
CREATE OR REPLACE VIEW public_telemetry_daily AS
SELECT
    bucket,
    category,
    origin,
    event_count,
    session_count
FROM telemetry_daily
WHERE session_count >= 10;