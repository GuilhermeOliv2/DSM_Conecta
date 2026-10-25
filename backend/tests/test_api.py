import json

from fastapi.testclient import TestClient

from API.main import app, clear_received_events


def valid_event():
    return {
        "event_id": "sensor-event-001",
        "session_id": "sensor",
        "category": "sensor",
        "origin": "totem",
        "timestamp": "2026-10-23T02:00:00Z",
        "schema_version": "1.0",
        "payload": {
            "sensor_id": "totem-01",
            "novos_visitantes": 2,
            "total_visitantes": 12,
        },
    }


def setup_function():
    clear_received_events()


def test_recebe_evento_do_sensor():
    client = TestClient(app)

    response = client.post(
        "/api/v1/telemetry/events",
        json=valid_event(),
        headers={"X-MQTT-Topic": "dsm/prod/totem/sensor/totem-01"},
    )

    assert response.status_code == 202
    assert response.json() == {
        "accepted": True,
        "event_id": "sensor-event-001",
    }


def test_rejeita_topico_incompativel():
    client = TestClient(app)

    response = client.post(
        "/api/v1/telemetry/events",
        content=json.dumps(valid_event()),
        headers={
            "Content-Type": "application/json",
            "X-MQTT-Topic": "dsm/prod/app/sensor/device-01",
        },
    )

    assert response.status_code == 422


def test_descarta_evento_duplicado():
    client = TestClient(app)
    event = valid_event()

    primeira = client.post("/api/v1/telemetry/events", json=event)
    segunda = client.post("/api/v1/telemetry/events", json=event)

    assert primeira.status_code == 202
    assert segunda.status_code == 202
    assert segunda.json() == {"accepted": False, "duplicate": True}
