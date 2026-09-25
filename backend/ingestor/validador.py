import json

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


def validar_mensagem(texto):
    try:
        mensagem = json.loads(texto)
    except json.JSONDecodeError as erro:
        raise MensagemInvalida("JSON malformado") from erro

    for campo in CAMPOS_OBRIGATORIOS:
        if campo not in mensagem:
            raise MensagemInvalida(f"campo obrigatorio ausente: {campo}")

    return mensagem
