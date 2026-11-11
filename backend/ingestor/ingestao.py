import asyncio
import logging

from ingestor.validador_mensagens import MensagemInvalida, validar_mensagem

logger = logging.getLogger(__name__)

GRAVADA = "gravada"
DUPLICADA = "duplicada"
INVALIDA = "invalida"
ERRO = "erro"


class Ingestor:
    def __init__(self, repositorio, tamanho_fila=1000):
        self._repositorio = repositorio
        self._fila = asyncio.Queue(maxsize=tamanho_fila)
        self._trabalhadores = []

    async def processar(self, texto, topico=None):
        try:
            evento = validar_mensagem(texto, topico=topico)
        except MensagemInvalida:
            return INVALIDA

        try:
            gravou = await self._repositorio.salvar(evento)
        except Exception:
            logger.exception("Falha ao gravar mensagem %s", evento["event_id"])
            return ERRO

        if not gravou:
            logger.info("Mensagem duplicada descartada: %s", evento["event_id"])
            return DUPLICADA
        return GRAVADA

    async def publicar(self, texto, topico=None):
        await self._fila.put((texto, topico))

    async def iniciar(self, trabalhadores=1):
        for _ in range(trabalhadores):
            self._trabalhadores.append(asyncio.create_task(self._trabalhar()))

    async def aguardar_fila_vazia(self):
        await self._fila.join()

    async def parar(self):
        for tarefa in self._trabalhadores:
            tarefa.cancel()
        await asyncio.gather(*self._trabalhadores, return_exceptions=True)
        self._trabalhadores.clear()

    async def _trabalhar(self):
        while True:
            texto, topico = await self._fila.get()
            try:
                await self.processar(texto, topico)
            finally:
                self._fila.task_done()
