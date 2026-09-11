# Moodle API

Base de uma API em FastAPI que consome os web services REST do Moodle.

- **Dev**: roda com venv, direto no host, apontando pro `moodle-docker` local.
- **Prod**: roda com Docker, apontando pro Moodle de produção.

## Estrutura

```
├── .env.example          # Modelo de variáveis de ambiente (copiar pra .env)
├── .gitignore            # Arquivos ignorados pelo git
├── Dockerfile            # Imagem de produção
├── docker-compose.yml    # Sobe a imagem de produção
├── requirements.txt      # Dependências Python
│
└── app/
    ├── __init__.py
    ├── main.py           # Cria o FastAPI e registra as rotas
    ├── config.py         # Lê as configurações do .env (pydantic-settings)
    ├── moodle_client.py  # Função genérica pra chamar qualquer wsfunction do Moodle
    └── routers/
        ├── __init__.py
        └── moodle.py     # GET /moodle/site-info e GET /moodle/courses (exemplos)
```

Como uma requisição percorre o código:

1. `main.py` recebe a requisição e despacha pro router certo (`routers/`)
2. o router chama `moodle_client.call_moodle_function(...)`, passando o nome
   da função do Moodle que quer usar
3. `moodle_client.py` monta a chamada REST (usando `MOODLE_BASE_URL` e
   `MOODLE_TOKEN` que vêm de `config.py`) e devolve o JSON já decodificado
4. o router devolve isso (ou o que quiser derivar disso) como resposta

Pra adicionar um endpoint novo: cria uma função em algum arquivo de
`routers/` (ou um router novo) chamando `call_moodle_function("nome_da_funcao_do_moodle", **params)`,
igual os dois exemplos em `app/routers/moodle.py`. Não precisa mexer no
`moodle_client.py` a não ser que precise de algo diferente de uma chamada
REST simples.

## Dev: rodando com venv

Pré-requisito: ter o [`moodle-docker`](../moodle-docker) rodando local
(`docker compose up -d --build` lá).

Copia o `.env.example` pra `.env`:

**Windows (cmd)**
```bat
copy .env.example .env
```

**Linux / macOS**
```bash
cp .env.example .env
```

Edita o `.env`:
- `MOODLE_BASE_URL=http://localhost:8080` (ou a porta que você configurou no `moodle-docker`)
- `MOODLE_TOKEN`: pega com `docker compose exec moodle cat /var/www/moodledata/webservice_token.txt` (rodando de dentro da pasta do `moodle-docker`)

Cria o venv, instala as dependências e sobe a API:

**Windows (cmd)**
```bat
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**Windows (PowerShell)**, se der erro de permissão no `activate`, roda uma vez
(como administrador) `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`:
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**Linux / macOS**
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Abra `http://localhost:8000/docs` pra ver a documentação interativa (Swagger)
gerada automaticamente pelo FastAPI, e testar os endpoints por ali.

## Prod: rodando com Docker

Copia o `.env.example` pra `.env` (`copy .env.example .env` no Windows,
`cp .env.example .env` no Linux/macOS) e edita com a URL e o token do Moodle
de produção. Depois sobe (comando igual nos dois sistemas, já que quem roda
é o Docker):

```bash
docker compose up -d --build
```

## Parar

```bash
docker compose down
```
