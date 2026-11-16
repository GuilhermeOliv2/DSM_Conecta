# Diagrama de relacionamento da série temporal

Este diagrama representa as tabelas e visões definidas em
[`query_serieTemporal.sql`](../postgres/init/query_serieTemporal.sql).

```mermaid
erDiagram
    visitor_session ||--o{ consent_record : "possui"
    consent_record o|--o{ telemetry_event : "autoriza"
    telemetry_event_dedup ||..o| telemetry_event : "deduplica por event_id"
    telemetry_event ||--o{ telemetry_hourly : "agrega por hora"
    telemetry_event ||--o{ telemetry_daily : "agrega por dia"
    telemetry_daily ||--o{ public_telemetry_daily : "filtra grupos >= 10"

    visitor_session {
        uuid id PK
        text anonymous_token UK
        text platform
        timestamptz started_at
        timestamptz ended_at
        timestamptz expires_at
    }

    consent_record {
        uuid id PK
        uuid session_id FK
        text consent_type
        boolean granted
        timestamptz granted_at
        timestamptz revoked_at
        text policy_version
    }

    telemetry_event_dedup {
        text event_id PK
        timestamptz first_seen_at
    }

    telemetry_event {
        text event_id PK
        timestamptz occurred_at PK
        text session_id
        uuid consent_id FK
        text category
        text origin
        text topic
        text schema_version
        jsonb payload
        double location_latitude
        double location_longitude
        double location_accuracy
        timestamptz ingested_at
    }

    telemetry_hourly {
        timestamptz bucket
        text category
        text origin
        bigint event_count
        bigint session_count
    }

    telemetry_daily {
        timestamptz bucket
        text category
        text origin
        bigint event_count
        bigint session_count
    }

    public_telemetry_daily {
        timestamptz bucket
        text category
        text origin
        bigint event_count
        bigint session_count
    }
```

## Interpretação

- `visitor_session` possui vários registros de `consent_record`.
- `consent_record` pode ser associado a vários eventos por `consent_id`.
  Como `telemetry_event.consent_id` é opcional, um evento pode não ter esse
  vínculo físico.
- `telemetry_event` é a hypertable central, particionada diariamente por
  `occurred_at`.
- `telemetry_event_dedup` controla a unicidade global de `event_id`, mas não
  possui chave estrangeira declarada para `telemetry_event`; essa relação é
  lógica e é aplicada pelo fluxo de ingestão.
- `telemetry_event.session_id` também representa uma associação lógica com a
  sessão, pois é `text` e não possui `FOREIGN KEY` para `visitor_session.id`.
- `telemetry_hourly` e `telemetry_daily` são agregações contínuas derivadas de
  `telemetry_event`.
- `public_telemetry_daily` é uma visão sobre `telemetry_daily` e publica apenas
  grupos com pelo menos dez sessões.

## Regra de localização

Para eventos de sensor originados pelo aplicativo, somente latitude, longitude
e precisão são persistidas. Luminosidade, movimento, acelerômetro e demais
leituras permanecem no dispositivo e não aparecem como colunas no banco.
