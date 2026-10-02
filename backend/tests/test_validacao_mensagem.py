import json

import pytest
from ingestor.validador_mensagens import MensagemInvalida, validar_mensagem


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


def test_mensagem_duplicada_e_descartada():
    texto = json.dumps(mensagem_valida())
    mensagens_processadas = set()

    primeira_msg = validar_mensagem(texto, mensagens_processadas)
    segunda_msg = validar_mensagem(texto, mensagens_processadas)

    assert primeira_msg["event_id"] in mensagens_processadas
    assert segunda_msg is None


def test_mensagem_invalida_e_registrada_em_log(caplog):
    with caplog.at_level("WARNING"), pytest.raises(MensagemInvalida):
        validar_mensagem("{isso nao e json")

    assert "Mensagem inválida descartada: JSON malformado" in caplog.text


def test_mensagem_com_estrutura_json_inadequada_e_rejeitada():
    with pytest.raises(MensagemInvalida):
        validar_mensagem(json.dumps(["mensagem", "inadequada"]))


def test_versao_do_esquema_invalida_e_rejeitada():
    msg = mensagem_valida()
    msg["schema_version"] = "2.0"

    with pytest.raises(MensagemInvalida):
        validar_mensagem(json.dumps(msg))


@pytest.mark.parametrize(
    ("campo", "valor"),
    [
        ("event_id", 123),
        ("session_id", 123),
        ("category", 123),
        ("origin", 123),
        ("timestamp", 123),
        ("schema_version", 1.0),
        ("payload", "não é objeto"),
    ],
)
def test_tipo_de_campo_invalido_e_rejeitado(campo, valor):
    msg = mensagem_valida()
    msg[campo] = valor

    with pytest.raises(MensagemInvalida):
        validar_mensagem(json.dumps(msg))


def test_topico_mqtt_valido_e_aceito():
    msg = mensagem_valida()
    topico = f"telemetria/{msg['origin']}/{msg['category']}"

    resultado = validar_mensagem(json.dumps(msg), topico=topico)

    assert resultado["event_id"] == msg["event_id"]


def test_topico_mqtt_invalido_e_rejeitado():
    with pytest.raises(MensagemInvalida):
        validar_mensagem(
            json.dumps(mensagem_valida()),
            topico="outro-topico",
        )


def test_mensagem_valida_e_persistida():
    msg = mensagem_valida()
    persistencia = []

    validar_mensagem(json.dumps(msg), persistencia=persistencia)

    assert persistencia == [msg]
