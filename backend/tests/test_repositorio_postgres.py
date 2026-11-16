import asyncio
import json
from datetime import datetime, timezone

from ingestor.repositorio_postgres import RepositorioPostgres, evento_para_linha

TOPICO = "dsm/prod/app/interacao/tela"


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


class PoolFalso:
    def __init__(self, resposta):
        self.resposta = resposta
        self.chamadas = []

    async def fetchval(self, sql, *argumentos):
        self.chamadas.append((sql, argumentos))
        return self.resposta


def test_linha_segue_a_ordem_das_colunas_do_insert():
    linha = evento_para_linha(mensagem_valida(), TOPICO)

    assert linha[:6] == (
        "9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d",
        "sess_a8b9c7",
        "interacao",
        "app",
        TOPICO,
        "1.0",
    )


def test_timestamp_com_z_vira_data_hora_em_utc():
    linha = evento_para_linha(mensagem_valida(), TOPICO)

    assert linha[6] == datetime(2026, 9, 25, 10, 0, tzinfo=timezone.utc)


def test_timestamp_com_fuso_vira_o_mesmo_instante():
    msg = mensagem_valida()
    msg["timestamp"] = "2026-09-25T07:00:00-03:00"

    linha = evento_para_linha(msg, TOPICO)

    assert linha[6] == datetime(2026, 9, 25, 10, 0, tzinfo=timezone.utc)
    assert linha[6].utcoffset() is not None


def test_payload_vira_texto_json():
    linha = evento_para_linha(mensagem_valida(), TOPICO)

    assert isinstance(linha[7], str)
    assert json.loads(linha[7]) == {"tela": "matriz_curricular"}


def test_salvar_devolve_true_quando_o_banco_inseriu():
    repo = RepositorioPostgres(PoolFalso(resposta="9b1deb4d"))

    gravou = asyncio.run(repo.salvar(mensagem_valida(), TOPICO))

    assert gravou is True


def test_salvar_devolve_false_quando_o_banco_recusou_a_repetida():
    repo = RepositorioPostgres(PoolFalso(resposta=None))

    gravou = asyncio.run(repo.salvar(mensagem_valida(), TOPICO))

    assert gravou is False


def test_salvar_envia_a_linha_ao_banco():
    pool = PoolFalso(resposta="9b1deb4d")
    repo = RepositorioPostgres(pool)

    asyncio.run(repo.salvar(mensagem_valida(), TOPICO))

    assert pool.chamadas[0][1] == evento_para_linha(mensagem_valida(), TOPICO)


def test_insert_deixa_o_banco_barrar_a_repetida():
    pool = PoolFalso(resposta="9b1deb4d")
    repo = RepositorioPostgres(pool)

    asyncio.run(repo.salvar(mensagem_valida(), TOPICO))

    sql = " ".join(pool.chamadas[0][0].split()).upper()
    assert "INSERT INTO TELEMETRY_EVENT" in sql
    assert "ON CONFLICT (EVENT_ID, OCCURRED_AT) DO NOTHING" in sql
    assert "RETURNING EVENT_ID" in sql
