# DSM Conecta

Aplicativo multiplataforma de divulgação do curso de **Desenvolvimento de Software Multiplataforma (DSM)**.

Além de divulgar o curso, o sistema coleta dados anônimos de navegação (telemetria) para medir o interesse nas ações de divulgação.

## Tecnologias

- **Flutter** — aplicativo (Android, Web e Desktop)
- **Python + FastAPI** — API e serviço de ingestão de dados
- **Eclipse Mosquitto** — broker MQTT que transporta as telemetrias
- **PostgreSQL + TimescaleDB** — banco de dados
- **Docker Compose** — sobe o Mosquitto e o banco de dados no ambiente local

## Pré-requisitos

- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [Git](https://git-scm.com/)

## Ambiente local com Docker

O arquivo `docker-compose.yml` sobe dois serviços:

| Serviço | Container | Portas |
| :--- | :--- | :--- |
| Mosquitto (MQTT) | `mosquitto` | `1883` (MQTT), `9001` (WebSocket) |
| PostgreSQL/TimescaleDB | `dsm_conecta_db` | `5432` |

### 1. Criar o arquivo `.env`

Na raiz do projeto, crie um arquivo `.env` com as credenciais do banco. Ele não é versionado (está no `.gitignore`).

```
POSTGRES_USER=seu_usuario
POSTGRES_PASSWORD=sua_senha
POSTGRES_DB=nome_do_banco
```

### 2. Subir os containers

```bash
docker compose up -d
```

Na primeira vez o Docker baixa as imagens; depois é só iniciar. O `-d` deixa rodando em segundo plano.

### 3. Conferir se subiu

```bash
docker compose ps
```

Os dois containers devem aparecer com status `Up`.

### 4. Testar

**Mosquitto** — entre no container e publique/assine uma mensagem:

```bash
docker exec -it mosquitto sh
```

Dentro do container:

```sh
mosquitto_sub -t teste -v &
mosquitto_pub -t teste -m "funcionou"
```

Se aparecer `teste funcionou`, o broker está OK. Digite `exit` para sair.

**PostgreSQL** — entre no container e rode uma query:

```bash
docker exec -it dsm_conecta_db psql -U seu_usuario -d nome_do_banco
```

Dentro do `psql`:

```sql
SELECT version();
```

Deve mostrar a versão do PostgreSQL com TimescaleDB. Digite `\q` para sair.

### Comandos úteis

| Ação | Comando |
| :--- | :--- |
| Ver logs | `docker compose logs -f` |
| Parar (mantém os dados) | `docker compose stop` |
| Iniciar de novo | `docker compose start` |
| Remover os containers | `docker compose down` |
| Remover containers e apagar os dados | `docker compose down -v` |

> Os dados do banco e do Mosquitto ficam nas pastas `postgres/data/` e `infra/mosquitto/`, então continuam existindo mesmo depois de `docker compose down`. Só `down -v` apaga tudo.

## Testes do backend

Os testes do módulo de validação de mensagens ficam em `backend/tests/` e usam o [pytest](https://docs.pytest.org/). É necessário ter o Python 3 instalado.

### 1. Instalar as dependências

```bash
cd backend
pip install -r requirements.txt
```

### 2. Rodar os testes

Dentro de `backend/`:

```bash
python -m pytest
```

Para ver também a cobertura de testes (a meta do projeto é no mínimo 70%):

```bash
python -m pytest --cov=ingestor
```

Também funciona rodando da raiz do repositório com `python -m pytest backend/tests`, que é como o CI executa.

> O desenvolvimento segue TDD: o teste é commitado antes do código que o faz passar, e o CI (GitHub Actions) roda a suíte a cada push e pull request.

## Estrutura do projeto

```
DSM_Conecta/
├── docker-compose.yml       # Sobe o Mosquitto e o banco
├── .env                     # Credenciais do banco (não versionado)
├── infra/mosquitto/         # Configuração e dados do Mosquitto
├── postgres/                # Dados e scripts de init do banco
├── backend/                 # Código Python (FastAPI + ingestor)
└── app/                     # Código Flutter
```

## Próximos passos

- [ ] Serviço Python para consumir as mensagens MQTT
- [ ] API FastAPI para as consultas
- [ ] App Flutter
- [ ] Scripts SQL das tabelas de telemetria
