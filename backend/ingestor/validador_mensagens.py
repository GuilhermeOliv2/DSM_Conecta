import json
import logging
import re

logger = logging.getLogger(__name__)
VERSAO_ESQUEMA_SUPORTADA = "1.0"

CAMPOS_OBRIGATORIOS = (
    "event_id",
    "session_id",
    "category",
    "origin",
    "timestamp",
    "schema_version",
    "payload",
)


class MensagemInvalida(Exception):
    pass


def validar_mensagem(
    texto,
    mensagens_processadas=None,
    logger_=logger,
    *,
    topico=None,
    persistencia=None,
):
    try:
        mensagem = json.loads(texto)
    except json.JSONDecodeError as erro:
        return _registrar_mensagem_invalida(
            "JSON malformado", logger_, erro
        )

    if not isinstance(mensagem, dict):
        return _registrar_mensagem_invalida(
            "Estrutura inválida: a mensagem deve ser um objeto JSON",
            logger_,
        )

    for campo in CAMPOS_OBRIGATORIOS:
        if campo not in mensagem:
            return _registrar_mensagem_invalida(
                f"Campo obrigatório ausente: {campo}", logger_
            )

    if mensagem["schema_version"] != VERSAO_ESQUEMA_SUPORTADA:
        return _registrar_mensagem_invalida(
            f"Versão do esquema não suportada: {mensagem['schema_version']}",
            logger_,
        )

    tipos_esperados = {
        "event_id": str,
        "session_id": str,
        "category": str,
        "origin": str,
        "timestamp": str,
        "schema_version": str,
        "payload": dict,
    }
    for campo, tipo in tipos_esperados.items():
        if not isinstance(mensagem[campo], tipo):
            return _registrar_mensagem_invalida(
                f"Tipo inválido para o campo: {campo}", logger_
            )

    if topico is not None:
        topico_esperado = f"telemetria/{mensagem['origin']}/{mensagem['category']}"
        if not re.fullmatch(
            r"telemetria/[^/]+/[^/]+", topico
        ) or topico != topico_esperado:
            return _registrar_mensagem_invalida(
                f"Tópico MQTT inválido: {topico}", logger_
            )

    if mensagens_processadas is not None:
        event_id = mensagem["event_id"]
        if event_id in mensagens_processadas:
            logger_.info("Mensagem duplicada descartada: %s", event_id)
            return None
        mensagens_processadas.add(event_id)

    if persistencia is not None:
        persistencia.append(mensagem)

    return mensagem


def _registrar_mensagem_invalida(motivo, logger_, erro=None):
    logger_.warning("Mensagem inválida descartada: %s", motivo)
    raise MensagemInvalida(motivo) from erro
