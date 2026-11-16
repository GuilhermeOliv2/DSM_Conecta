import argparse
import csv
import json
import os
import random
import sys
import tempfile
import time
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOTAL_REGISTROS_PADRAO = 1_000_000
NAMESPACE_EVENTOS = uuid.UUID("cc292aab-6744-4c72-9622-3bc250d953ee")
CAMPOS_CSV = (
    "event_id",
    "session_id",
    "category",
    "origin",
    "event_timestamp",
    "schema_version",
    "payload",
)


def gerar_csv(caminho, quantidade, seed=42):
    aleatorio = random.Random(seed)
    instante = datetime.now(timezone.utc) - timedelta(days=30)
    total_visitantes = 0

    with Path(caminho).open("w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.writer(arquivo)
        escritor.writerow(CAMPOS_CSV)

        for numero in range(1, quantidade + 1):
            novos_visitantes = aleatorio.randint(0, 3)
            total_visitantes += novos_visitantes
            payload = {
                "sensor_id": "totem-01",
                "novos_visitantes": novos_visitantes,
                "total_visitantes": total_visitantes,
            }
            escritor.writerow(
                (
                    uuid.uuid5(NAMESPACE_EVENTOS, str(numero)),
                    "sensor",
                    "sensor",
                    "totem",
                    instante.isoformat(),
                    "1.0",
                    json.dumps(payload, separators=(",", ":")),
                )
            )
            instante += timedelta(seconds=2)


def criar_tabela_eventos_sinteticos(configuracao_banco):
    import psycopg2

    with psycopg2.connect(**configuracao_banco) as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS eventos_sinteticos (
                    event_id UUID PRIMARY KEY,
                    session_id TEXT NOT NULL,
                    category TEXT NOT NULL CHECK (category = 'sensor'),
                    origin TEXT NOT NULL CHECK (origin = 'totem'),
                    event_timestamp TIMESTAMPTZ NOT NULL,
                    schema_version TEXT NOT NULL,
                    payload JSONB NOT NULL,
                    is_synthetic BOOLEAN NOT NULL DEFAULT TRUE
                )
                """
            )
            cursor.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_eventos_sinteticos_timestamp
                    ON eventos_sinteticos (event_timestamp)
                """
            )


def carregar_csv(caminho, configuracao_banco):
    import psycopg2

    with psycopg2.connect(**configuracao_banco) as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(
                """
                CREATE TEMP TABLE carga_sintetica_stage (
                    LIKE eventos_sinteticos INCLUDING DEFAULTS
                ) ON COMMIT DROP
                """
            )
            with Path(caminho).open("r", newline="", encoding="utf-8") as arquivo:
                leitor = csv.DictReader(arquivo)
                if tuple(leitor.fieldnames or ()) != CAMPOS_CSV:
                    raise ValueError("O cabeçalho do CSV da carga não é válido.")
                arquivo.seek(0)
                cursor.copy_expert(
                    """
                    COPY carga_sintetica_stage (
                        event_id, session_id, category, origin,
                        event_timestamp, schema_version, payload
                    ) FROM STDIN WITH (FORMAT CSV, HEADER TRUE)
                    """,
                    arquivo,
                )
            cursor.execute(
                """
                INSERT INTO eventos_sinteticos (
                    event_id, session_id, category, origin, event_timestamp,
                    schema_version, payload, is_synthetic
                )
                SELECT
                    event_id, session_id, category, origin, event_timestamp,
                    schema_version, payload, TRUE
                FROM carga_sintetica_stage
                ON CONFLICT (event_id) DO NOTHING
                """
            )
            inseridos = cursor.rowcount
            cursor.execute(
                """
                SELECT COUNT(*)
                FROM eventos_sinteticos
                WHERE is_synthetic = TRUE
                """
            )
            total = cursor.fetchone()[0]

    return inseridos, total


def carregar_configuracao_banco():
    valores = {}
    arquivo_env = ROOT / ".env"
    if arquivo_env.exists():
        for linha in arquivo_env.read_text(encoding="utf-8").splitlines():
            linha = linha.strip()
            if not linha or linha.startswith("#") or "=" not in linha:
                continue
            chave, valor = linha.split("=", 1)
            valores[chave.strip()] = valor.strip().strip("\"'")

    def obter(nome, padrao=None):
        return os.environ.get(nome) or valores.get(nome) or padrao

    configuracao = {
        "dbname": obter("POSTGRES_DB"),
        "user": obter("POSTGRES_USER"),
        "password": obter("POSTGRES_PASSWORD"),
        "host": obter("POSTGRES_HOST", "127.0.0.1"),
        "port": obter("POSTGRES_PORT", "5432"),
    }
    ausentes = [
        nome
        for nome in ("dbname", "user", "password")
        if not configuracao[nome]
    ]
    if ausentes:
        raise ValueError(
            "Configure POSTGRES_DB, POSTGRES_USER e POSTGRES_PASSWORD "
            "no arquivo .env ou nas variáveis de ambiente."
        )
    return configuracao


def main():
    parser = argparse.ArgumentParser(
        description="Gera e carrega eventos sintéticos no PostgreSQL."
    )
    parser.add_argument(
        "--registros",
        type=int,
        default=TOTAL_REGISTROS_PADRAO,
        help="quantidade de eventos a gerar (padrão: 1000000)",
    )
    parser.add_argument(
        "--csv",
        type=Path,
        help="caminho opcional para manter o CSV gerado",
    )
    argumentos = parser.parse_args()
    if argumentos.registros < 1:
        parser.error("--registros deve ser maior que zero.")

    try:
        configuracao_banco = carregar_configuracao_banco()
    except ValueError as erro:
        parser.error(str(erro))

    inicio_execucao = time.perf_counter()
    criar_tabela_eventos_sinteticos(configuracao_banco)
    if argumentos.csv:
        caminho_csv = argumentos.csv.resolve()
        caminho_csv.parent.mkdir(parents=True, exist_ok=True)
        gerar_csv(caminho_csv, argumentos.registros)
        inseridos, total = carregar_csv(caminho_csv, configuracao_banco)
    else:
        with tempfile.TemporaryDirectory(prefix="dsm-carga-") as diretorio:
            caminho_csv = Path(diretorio) / "carga_sintetica.csv"
            gerar_csv(caminho_csv, argumentos.registros)
            inseridos, total = carregar_csv(caminho_csv, configuracao_banco)
    tempo_execucao = time.perf_counter() - inicio_execucao

    print(f"Novos registros inseridos: {inseridos}")
    print(f"Total de registros sintéticos na tabela: {total}")
    print(f"Tempo total de execução da carga sintética: {tempo_execucao:.2f} s")
    if total < argumentos.registros:
        print(
            "A quantidade persistida ficou abaixo do solicitado.",
            file=sys.stderr,
        )
        return 1
    print("Carga sintética concluída e verificada.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
