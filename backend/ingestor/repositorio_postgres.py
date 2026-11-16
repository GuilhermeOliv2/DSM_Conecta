import json
from datetime import datetime

SQL_INSERIR_EVENTO = """
INSERT INTO telemetry_event (
    event_id, session_id, category, origin, topic,
    schema_version, occurred_at, payload
)
VALUES ($1, $2, $3, $4, $5, $6, $7, $8::jsonb)
ON CONFLICT (event_id, occurred_at) DO NOTHING
RETURNING event_id
"""


def evento_para_linha(evento, topico):
    return (
        evento["event_id"],
        evento["session_id"],
        evento["category"],
        evento["origin"],
        topico,
        evento["schema_version"],
        datetime.fromisoformat(evento["timestamp"].replace("Z", "+00:00")),
        json.dumps(evento["payload"]),
    )


class RepositorioPostgres:
    def __init__(self, pool):
        self._pool = pool

    async def salvar(self, evento, topico):
        linha = evento_para_linha(evento, topico)
        inserido = await self._pool.fetchval(SQL_INSERIR_EVENTO, *linha)
        return inserido is not None
