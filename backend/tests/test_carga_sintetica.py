import csv
import io
import json
import sys
import uuid
from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

import carga_sintetica
from carga_sintetica import (
    CAMPOS_CSV,
    NAMESPACE_EVENTOS,
    carregar_csv,
    criar_tabela_eventos_sinteticos,
    gerar_csv,
)


def _configurar_banco_falso(monkeypatch, inseridos=1, total=1):
    conectar = MagicMock()
    conexao = MagicMock()
    cursor = MagicMock()
    conectar.return_value = conexao
    conexao.__enter__.return_value = conexao
    conexao.cursor.return_value = cursor
    cursor.__enter__.return_value = cursor
    cursor.rowcount = inseridos
    cursor.fetchone.return_value = (total,)
    monkeypatch.setitem(
        sys.modules, "psycopg2", SimpleNamespace(connect=conectar)
    )
    return conectar, cursor


def _escrever_csv(caminho, campos=CAMPOS_CSV):
    with caminho.open("w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.writer(arquivo)
        escritor.writerow(campos)
        escritor.writerow(
            (
                str(uuid.uuid5(NAMESPACE_EVENTOS, "1")),
                "sensor",
                "sensor",
                "totem",
                "2026-01-01T00:00:00+00:00",
                "1.0",
                '{"sensor_id":"totem-01"}',
            )
        )


def test_gerar_csv_produz_eventos_validos_e_ids_estaveis(tmp_path):
    caminho = tmp_path / "carga.csv"

    gerar_csv(caminho, 3)

    with caminho.open("r", newline="", encoding="utf-8") as arquivo:
        leitor = csv.DictReader(arquivo)
        linhas = list(leitor)

    assert tuple(leitor.fieldnames) == CAMPOS_CSV
    assert len(linhas) == 3
    assert len({linha["event_id"] for linha in linhas}) == 3
    assert linhas[0]["event_id"] == str(uuid.uuid5(NAMESPACE_EVENTOS, "1"))
    assert all(linha["category"] == "sensor" for linha in linhas)
    assert all(linha["origin"] == "totem" for linha in linhas)
    assert all(json.loads(linha["payload"])["sensor_id"] == "totem-01" for linha in linhas)


def test_gerar_csv_preserva_total_acumulado_de_visitantes(tmp_path):
    caminho = tmp_path / "carga.csv"

    gerar_csv(caminho, 5)

    with caminho.open("r", newline="", encoding="utf-8") as arquivo:
        linhas = list(csv.DictReader(arquivo))

    totais = [
        json.loads(linha["payload"])["total_visitantes"] for linha in linhas
    ]
    novos = [
        json.loads(linha["payload"])["novos_visitantes"] for linha in linhas
    ]

    assert totais == sorted(totais)
    assert totais[-1] == sum(novos)


def test_criar_tabela_eventos_sinteticos_prepara_tabela_e_indice(monkeypatch):
    conectar, cursor = _configurar_banco_falso(monkeypatch)
    configuracao = {"dbname": "test_db", "user": "test_user"}

    criar_tabela_eventos_sinteticos(configuracao)

    conectar.assert_called_once_with(**configuracao)
    comandos = "\n".join(
        chamada.args[0] for chamada in cursor.execute.call_args_list
    )
    assert "CREATE TABLE IF NOT EXISTS eventos_sinteticos" in comandos
    assert (
        "CREATE INDEX IF NOT EXISTS idx_eventos_sinteticos_timestamp"
        in comandos
    )


def test_carregar_csv_copia_registros_e_retorna_contagens(
    tmp_path, monkeypatch
):
    caminho = tmp_path / "carga.csv"
    _escrever_csv(caminho)
    conectar, cursor = _configurar_banco_falso(
        monkeypatch, inseridos=1, total=4
    )
    dados_copiados = []

    def capturar_copia(comando, arquivo):
        dados_copiados.append((comando, arquivo.read()))

    cursor.copy_expert.side_effect = capturar_copia
    configuracao = {"dbname": "test_db", "user": "test_user"}

    resultado = carregar_csv(caminho, configuracao)

    assert resultado == (1, 4)
    conectar.assert_called_once_with(**configuracao)
    assert cursor.copy_expert.call_count == 1
    assert "COPY carga_sintetica_stage" in dados_copiados[0][0]
    linhas_copiadas = list(csv.reader(io.StringIO(dados_copiados[0][1])))
    assert tuple(linhas_copiadas[0]) == CAMPOS_CSV
    assert len(linhas_copiadas) == 2
    assert linhas_copiadas[1][0] == str(uuid.uuid5(NAMESPACE_EVENTOS, "1"))
    comandos = "\n".join(chamada.args[0] for chamada in cursor.execute.call_args_list)
    assert "CREATE TABLE IF NOT EXISTS eventos_sinteticos" not in comandos
    assert "ON CONFLICT (event_id) DO NOTHING" in comandos
    assert "SELECT COUNT(*)" in comandos


def test_carregar_csv_rejeita_cabecalho_invalido(tmp_path, monkeypatch):
    caminho = tmp_path / "carga.csv"
    campos_invalidos = ("session_id",) + CAMPOS_CSV[1:]
    _escrever_csv(caminho, campos_invalidos)
    _, cursor = _configurar_banco_falso(monkeypatch)

    with pytest.raises(ValueError, match="cabeçalho do CSV"):
        carregar_csv(caminho, {"dbname": "test_db"})

    cursor.copy_expert.assert_not_called()


def test_main_exibe_relatorio_de_desempenho(tmp_path, monkeypatch, capsys):
    caminho = tmp_path / "carga.csv"
    etapas = []

    def registrar_etapa(nome):
        etapas.append(nome)

    def carregar(*_args):
        registrar_etapa("carregar")
        return 2, 2

    monkeypatch.setattr(
        sys,
        "argv",
        ["carga_sintetica.py", "--registros", "2", "--csv", str(caminho)],
    )
    monkeypatch.setattr(
        carga_sintetica, "carregar_configuracao_banco", lambda: {}
    )
    monkeypatch.setattr(
        carga_sintetica,
        "criar_tabela_eventos_sinteticos",
        lambda *_args: registrar_etapa("preparar"),
    )
    monkeypatch.setattr(
        carga_sintetica,
        "gerar_csv",
        lambda *_args: registrar_etapa("gerar"),
    )
    monkeypatch.setattr(
        carga_sintetica, "carregar_csv", carregar
    )
    tempos = iter((10.0, 20.0, 23.0, 24.0, 28.0, 30.0, 36.0, 40.0))
    monkeypatch.setattr(carga_sintetica.time, "perf_counter", lambda: next(tempos))

    assert carga_sintetica.main() == 0

    saida = capsys.readouterr().out
    assert "Tempo de preparação do banco: 3.00 s" in saida
    assert "Tempo de geração do CSV: 4.00 s" in saida
    assert "Tempo de carga no PostgreSQL: 6.00 s" in saida
    assert "Tempo total: 30.00 s" in saida
    assert "Taxa de geração: 0.50 registros/s" in saida
    assert "Taxa de inserção: 0.33 registros/s" in saida
    assert etapas == ["preparar", "gerar", "carregar"]
