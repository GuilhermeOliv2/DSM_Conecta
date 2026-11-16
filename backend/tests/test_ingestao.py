import asyncio
import json

import pytest

from ingestor.ingestao import DUPLICADA, ERRO, GRAVADA, INVALIDA, Ingestor


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


class RepositorioFalso:
    def __init__(self, falhar=False):
        self.gravadas = []
        self.falhar = falhar

    async def salvar(self, evento):
        if self.falhar:
            raise RuntimeError("banco indisponivel")
        if any(g["event_id"] == evento["event_id"] for g in self.gravadas):
            return False
        self.gravadas.append(evento)
        return True


def test_mensagem_nova_e_gravada():
    repo = RepositorioFalso()
    ingestor = Ingestor(repo)

    resultado = asyncio.run(ingestor.processar(json.dumps(mensagem_valida())))

    assert resultado == GRAVADA
    assert len(repo.gravadas) == 1


def test_mensagem_repetida_nao_e_gravada_de_novo():
    repo = RepositorioFalso()
    ingestor = Ingestor(repo)
    texto = json.dumps(mensagem_valida())

    async def cenario():
        primeira = await ingestor.processar(texto)
        segunda = await ingestor.processar(texto)
        return primeira, segunda

    primeira, segunda = asyncio.run(cenario())

    assert (primeira, segunda) == (GRAVADA, DUPLICADA)
    assert len(repo.gravadas) == 1


def test_repetida_e_registrada_em_log(caplog):
    ingestor = Ingestor(RepositorioFalso())
    texto = json.dumps(mensagem_valida())

    async def cenario():
        await ingestor.processar(texto)
        await ingestor.processar(texto)

    with caplog.at_level("INFO"):
        asyncio.run(cenario())

    assert "Mensagem duplicada descartada" in caplog.text


def test_mensagem_invalida_nao_chega_ao_repositorio():
    repo = RepositorioFalso()
    ingestor = Ingestor(repo)

    resultado = asyncio.run(ingestor.processar("{isso nao e json"))

    assert resultado == INVALIDA
    assert repo.gravadas == []


def test_falha_do_banco_nao_derruba_o_fluxo(caplog):
    ingestor = Ingestor(RepositorioFalso(falhar=True))

    with caplog.at_level("ERROR"):
        resultado = asyncio.run(ingestor.processar(json.dumps(mensagem_valida())))

    assert resultado == ERRO
    assert "Falha ao gravar mensagem" in caplog.text


def test_fila_cheia_segura_quem_publica():
    async def cenario():
        ingestor = Ingestor(RepositorioFalso(), tamanho_fila=1)
        texto = json.dumps(mensagem_valida())

        await ingestor.publicar(texto)

        with pytest.raises(asyncio.TimeoutError):
            await asyncio.wait_for(ingestor.publicar(texto), timeout=0.05)

    asyncio.run(cenario())


def test_trabalhadores_gravam_o_que_esta_na_fila():
    repo = RepositorioFalso()

    async def cenario():
        ingestor = Ingestor(repo, tamanho_fila=10)
        for i in range(3):
            msg = mensagem_valida()
            msg["event_id"] = f"evt-{i}"
            await ingestor.publicar(json.dumps(msg))

        await ingestor.iniciar(trabalhadores=2)
        await ingestor.aguardar_fila_vazia()
        await ingestor.parar()

    asyncio.run(cenario())

    assert len(repo.gravadas) == 3
