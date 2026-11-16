import asyncio
import logging
import os

from ingestor.ingestao import Ingestor
from ingestor.repositorio_postgres import RepositorioPostgres

logger = logging.getLogger(__name__)

TOPICO_ASSINATURA = "dsm/prod/#"
SUFIXO_STATUS = "/status"
TRABALHADORES = 4
TAMANHO_FILA = 1000


def criar_on_message(loop, ingestor):
    def on_message(client, userdata, message):
        texto = message.payload.decode("utf-8", errors="replace")
        if message.topic.endswith(SUFIXO_STATUS):
            logger.info("Status em %s: %s", message.topic, texto)
            return
        asyncio.run_coroutine_threadsafe(
            ingestor.publicar(texto, message.topic), loop
        ).result()

    return on_message


def _on_connect(client, userdata, flags, reason_code, properties=None):
    if reason_code != 0:
        logger.error("Conexão MQTT rejeitada (%s)", reason_code)
        return
    client.subscribe(TOPICO_ASSINATURA, qos=1)
    logger.info("Conectado ao broker, assinando %s", TOPICO_ASSINATURA)


async def rodar():
    import asyncpg
    import paho.mqtt.client as mqtt

    loop = asyncio.get_running_loop()
    pool = await asyncpg.create_pool(
        user=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
        database=os.environ["POSTGRES_DB"],
        host=os.getenv("POSTGRES_HOST", "127.0.0.1"),
        port=int(os.getenv("POSTGRES_PORT", "5432")),
        min_size=1,
        max_size=TRABALHADORES,
    )
    ingestor = Ingestor(RepositorioPostgres(pool), tamanho_fila=TAMANHO_FILA)
    await ingestor.iniciar(trabalhadores=TRABALHADORES)

    client = mqtt.Client(
        callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
        client_id="servico-ingestao",
    )
    client.username_pw_set(os.environ["MQTT_USER"], os.environ["MQTT_PASSWORD"])
    client.on_connect = _on_connect
    client.on_message = criar_on_message(loop, ingestor)
    client.connect(
        os.getenv("MQTT_HOST", "127.0.0.1"),
        int(os.getenv("MQTT_PORT", "1883")),
        keepalive=30,
    )
    client.loop_start()
    try:
        await asyncio.Event().wait()
    finally:
        client.disconnect()
        client.loop_stop()
        await ingestor.aguardar_fila_vazia()
        await ingestor.parar()
        await pool.close()


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    try:
        asyncio.run(rodar())
    except KeyboardInterrupt:
        logger.info("Serviço encerrado.")


if __name__ == "__main__":
    main()
