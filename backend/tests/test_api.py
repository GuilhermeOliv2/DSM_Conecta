from types import SimpleNamespace

import pytest

from ingestor import mqtt_consumer
from ingestor.validador_mensagens import MensagemInvalida


def setup_function():
    mqtt_consumer._mensagens_processadas.clear()


def test_on_connect_assina_topicos_quando_conecta():
    chamadas = []

    client = SimpleNamespace(subscribe=lambda topico, qos: chamadas.append((topico, qos)))

    mqtt_consumer._on_connect(client, None, None, 0)

    assert chamadas == [
        (mqtt_consumer.TOPICO_LEITURAS, 1),
        (mqtt_consumer.TOPICO_STATUS, 1),
    ]


def test_on_connect_nao_assina_topicos_quando_recusado():
    client = SimpleNamespace(subscribe=lambda *_args, **_kwargs: pytest.fail())

    mqtt_consumer._on_connect(client, None, None, 5)


def test_on_message_status_imprime_status(capsys):
    mensagem = SimpleNamespace(topic=mqtt_consumer.TOPICO_STATUS, payload=b"ok")

    mqtt_consumer._on_message(None, None, mensagem)

    assert "STATUS: ok" in capsys.readouterr().out


def test_on_message_invalida_rejeita_evento(monkeypatch, capsys):
    def falha_validacao(*_args, **_kwargs):
        raise MensagemInvalida("erro de validacao")

    monkeypatch.setattr(mqtt_consumer, "validar_mensagem", falha_validacao)
    mensagem = SimpleNamespace(topic=mqtt_consumer.TOPICO_LEITURAS, payload=b"{}")

    mqtt_consumer._on_message(None, None, mensagem)

    assert "RECUSADO: erro de validacao" in capsys.readouterr().out


def test_on_message_aceita_evento_valido(monkeypatch, capsys):
    def retorna_evento(*_args, **_kwargs):
        return {"event_id": "evento-1"}

    monkeypatch.setattr(mqtt_consumer, "validar_mensagem", retorna_evento)
    mensagem = SimpleNamespace(topic=mqtt_consumer.TOPICO_LEITURAS, payload=b"{}")

    mqtt_consumer._on_message(None, None, mensagem)

    saida = capsys.readouterr().out
    assert "ACEITO: event_id=evento-1" in saida
    assert f"topico={mqtt_consumer.TOPICO_LEITURAS}" in saida


def test_on_message_descarta_duplicado(monkeypatch, capsys):
    monkeypatch.setattr(mqtt_consumer, "validar_mensagem", lambda *_args, **_kwargs: None)
    mensagem = SimpleNamespace(topic=mqtt_consumer.TOPICO_LEITURAS, payload=b"{}")

    mqtt_consumer._on_message(None, None, mensagem)

    assert "RECUSADO: mensagem duplicada" in capsys.readouterr().out
