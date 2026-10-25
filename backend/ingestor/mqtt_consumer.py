import logging
import os

import paho.mqtt.client as mqtt

from ingestor.validador_mensagens import MensagemInvalida, validar_mensagem

logger = logging.getLogger(__name__)
TOPICO_LEITURAS = "dsm/prod/totem/sensor/contagem"
TOPICO_STATUS = "dsm/prod/totem/sensor/status"
_mensagens_processadas = set()


def _on_connect(client, userdata, flags, reason_code, properties=None):
    if reason_code != 0:
        print(f"RECUSADO: conexão MQTT rejeitada ({reason_code})", flush=True)
        return
    client.subscribe(TOPICO_LEITURAS, qos=1)
    client.subscribe(TOPICO_STATUS, qos=1)
    print("Consumidor conectado e aguardando leituras MQTT.", flush=True)


def _on_message(client, userdata, message):
    texto = message.payload.decode("utf-8")
    if message.topic == TOPICO_STATUS:
        print(f"STATUS: {texto}", flush=True)
        return

    try:
        evento = validar_mensagem(
            texto,
            mensagens_processadas=_mensagens_processadas,
            topico=message.topic,
        )
    except MensagemInvalida as error:
        print(f"RECUSADO: {error}", flush=True)
        return

    if evento is None:
        print("RECUSADO: mensagem duplicada", flush=True)
        return

    print(
        f"ACEITO: event_id={evento['event_id']} "
        f"topico={message.topic}",
        flush=True,
    )


def main():
    logging.basicConfig(level=logging.WARNING)
    client = mqtt.Client(
        callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
        client_id="ingestor-validacao",
    )
    client.username_pw_set(
        os.environ["MQTT_USER"],
        os.environ["MQTT_PASSWORD"],
    )
    client.on_connect = _on_connect
    client.on_message = _on_message
    client.connect(
        os.getenv("MQTT_HOST", "127.0.0.1"),
        int(os.getenv("MQTT_PORT", "1883")),
        keepalive=30,
    )
    client.loop_forever()


if __name__ == "__main__":
    main()
