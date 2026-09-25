import json

import pytest

from ingestor.validador import MensagemInvalida, validar_mensagem


def mensagem_valida():
    return {
        "event_id": "9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d",
        "session_id": "sess_a8b9c7",
        "category": "interacao",
        "origin": "app",
        "timestamp": "2026-09-25T10:00:00Z",
        "schema_version": "1.0",
        "payload": {"tela": "matriz_curricular"},
    }


def test_mensagem_valida_e_aceita():
    texto = json.dumps(mensagem_valida())

    resultado = validar_mensagem(texto)

    assert resultado["event_id"] == "9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d"


def test_json_malformado_e_rejeitado():
    with pytest.raises(MensagemInvalida):
        validar_mensagem("{isso nao e json")


def test_mensagem_sem_event_id_e_rejeitada():
    msg = mensagem_valida()
    del msg["event_id"]

    with pytest.raises(MensagemInvalida):
        validar_mensagem(json.dumps(msg))
