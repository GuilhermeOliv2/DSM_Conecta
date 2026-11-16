import asyncio
import threading
from types import SimpleNamespace

from ingestor.servico_ingestao import criar_on_message

TOPICO = "dsm/prod/app/interacao/tela"


class IngestorFalso:
    def __init__(self, liberar=None):
        self.recebidas = []
        self.liberar = liberar

    async def publicar(self, texto, topico=None):
        if self.liberar is not None:
            await self.liberar.wait()
        self.recebidas.append((texto, topico))


class LoopEmSegundoPlano:
    def __enter__(self):
        self.loop = asyncio.new_event_loop()
        self.thread = threading.Thread(target=self.loop.run_forever, daemon=True)
        self.thread.start()
        return self.loop

    def __exit__(self, *args):
        self.loop.call_soon_threadsafe(self.loop.stop)
        self.thread.join()
        self.loop.close()


def mensagem(topico, payload):
    return SimpleNamespace(topic=topico, payload=payload)


def test_leitura_vai_para_a_ingestao_com_o_topico():
    ingestor = IngestorFalso()

    with LoopEmSegundoPlano() as loop:
        on_message = criar_on_message(loop, ingestor)
        on_message(None, None, mensagem(TOPICO, b'{"a": 1}'))

    assert ingestor.recebidas == [('{"a": 1}', TOPICO)]


def test_mensagem_de_status_nao_vai_para_a_ingestao():
    ingestor = IngestorFalso()

    with LoopEmSegundoPlano() as loop:
        on_message = criar_on_message(loop, ingestor)
        on_message(
            None,
            None,
            mensagem("dsm/prod/totem/sensor/status", b'{"status": "online"}'),
        )

    assert ingestor.recebidas == []


def test_bytes_que_nao_sao_texto_nao_derrubam_o_callback():
    ingestor = IngestorFalso()

    with LoopEmSegundoPlano() as loop:
        on_message = criar_on_message(loop, ingestor)
        on_message(None, None, mensagem(TOPICO, b"\xff\xfe"))

    assert len(ingestor.recebidas) == 1


def test_fila_cheia_segura_o_callback_ate_abrir_vaga():
    with LoopEmSegundoPlano() as loop:
        liberar = asyncio.Event()
        ingestor = IngestorFalso(liberar)
        on_message = criar_on_message(loop, ingestor)
        chamada = threading.Thread(
            target=on_message, args=(None, None, mensagem(TOPICO, b"{}"))
        )

        chamada.start()
        chamada.join(timeout=0.2)
        segurada = chamada.is_alive()

        loop.call_soon_threadsafe(liberar.set)
        chamada.join(timeout=2)

        assert segurada
        assert not chamada.is_alive()

    assert ingestor.recebidas == [("{}", TOPICO)]
