import csv
import json
import uuid

from carga_sintetica import CAMPOS_CSV, NAMESPACE_EVENTOS, gerar_csv


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
