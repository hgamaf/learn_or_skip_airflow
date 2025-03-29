# Learn or Skip Airflow

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110.0-green.svg)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.32.2-red.svg)](https://streamlit.io/)
[![Plotly](https://img.shields.io/badge/Plotly-5.19.0-blue.svg)](https://plotly.com/)
[![Pandas](https://img.shields.io/badge/Pandas-2.2.1-green.svg)](https://pandas.pydata.org/)
[![SQLite](https://img.shields.io/badge/SQLite-3-blue.svg)](https://www.sqlite.org/)
[![Airflow](https://img.shields.io/badge/Airflow-2.7.0-orange.svg)](https://airflow.apache.org/)

Aplicação web para ajudar a decidir se vale a pena aprender Apache Airflow.

## Fluxo do Projeto

```mermaid
graph TB
    subgraph Airflow ["Apache Airflow"]
        A[DAG: Gerar Transações] -->|"Executa<br/>00:00 UTC"| B[Gerar Dados Aleatórios]
        B -->|"Salva<br/>transactions.csv"| C[("/data/transactions.csv")]
        D[DAG: Salvar no Banco] -->|"Executa<br/>01:00 UTC"| E[Ler CSV]
        E -->|"Processa<br/>e Salva"| F[("SQLite DB<br/>/data/transactions.db")]
    end

    subgraph API ["FastAPI API"]
        H["/start-dashboard"] -->|"Inicia"| G
        I["/stop-dashboard"] -->|"Para"| G
        J["/dashboard-status"] -->|"Monitora"| G
    end

    subgraph Dashboard ["Dashboard Streamlit"]
        G[Dashboard] -->|"Lê Dados"| F
        G -->|"Gera"| K[Métricas]
        G -->|"Gera"| L[Gráficos]
        G -->|"Gera"| M[Tabela de Dados]
    end

    style Airflow fill:#f9d5e5,stroke:#333,stroke-width:2px
    style API fill:#eeeeee,stroke:#333,stroke-width:2px
    style Dashboard fill:#d5e8d4,stroke:#333,stroke-width:2px
    
    classDef storage fill:#fff,stroke:#333,stroke-width:2px,stroke-dasharray: 5 5
    class C,F storage
```

## Pré-requisitos

- Python 3.8+
- [uv](https://github.com/astral-sh/uv) - Gerenciador de pacotes Python mais rápido
- [Astro CLI](https://docs.astronomer.io/astro/cli/install-cli) - CLI do Astronomer

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/learn-or-skip-airflow.git
cd learn-or-skip-airflow
```

2. Inicialize o ambiente virtual Python com uv:
```bash
uv init
uv venv
source .venv/bin/activate  # No Linux/Mac
# ou
.venv\Scripts\activate  # No Windows
```

3. Instale as dependências:
```bash
# Opção 1: Instalar todas as dependências do pyproject.toml
uv pip install

# Opção 2: Instalar dependências individualmente
uv add pandas==2.2.1
uv add streamlit==1.32.2
uv add plotly==5.19.0
uv add numpy==1.26.4
uv add python-dateutil==2.8.2
uv add pytz==2024.1
uv add typing-extensions==4.9.0
uv add tenacity==8.2.3
uv add rich==13.7.0
uv add click==8.1.7
uv add watchdog==4.0.0
uv add altair==5.2.0
uv add toolz==0.12.1
uv add fastapi==0.110.0
uv add uvicorn==0.27.1
```

## Iniciando o Projeto

### 1. Iniciar o Ambiente Airflow

```bash
# Inicia o ambiente Airflow local
astro dev start

# Aguarde até que todos os serviços estejam prontos
# O Airflow estará disponível em http://localhost:8080
# Credenciais padrão: admin/admin
```

### 2. Iniciar a API FastAPI

```bash
python main.py
```

A API estará disponível em `http://localhost:8000`

### 3. Gerenciar o Dashboard

Use os seguintes endpoints da API:

- **Iniciar o Dashboard**:
```bash
curl -X POST http://localhost:8000/start-dashboard
```

- **Parar o Dashboard**:
```bash
curl -X POST http://localhost:8000/stop-dashboard
```

- **Verificar Status**:
```bash
curl http://localhost:8000/dashboard-status
```

### 4. Acessar o Dashboard

Após iniciar o dashboard, acesse:
- Dashboard: `http://localhost:8501`
- Documentação da API: `http://localhost:8000/docs`
- Airflow UI: `http://localhost:8080`

## Estrutura do Projeto

```
learn_or_skip_airflow/
├── .astro/                     # Configurações do Astronomer
├── dags/                       # DAGs do Airflow
│   ├── generate_transactions_dag.py  # DAG para gerar transações
│   └── save_to_database_dag.py      # DAG para salvar no banco
├── data/                      # Dados gerados e banco
│   ├── transactions.csv       # Arquivo CSV com transações
│   └── transactions.db        # Banco de dados SQLite
├── src/                       # Código fonte do projeto
│   ├── data_generators/       # Geradores de dados
│   │   ├── __init__.py
│   │   └── generate_transactions.py  # Gerador de transações
│   ├── database/             # Gerenciamento do banco
│   │   ├── __init__.py
│   │   └── db_manager.py     # Classe DatabaseManager
│   ├── dashboard/            # Dashboard Streamlit
│   │   ├── __init__.py
│   │   └── app.py           # Aplicação Streamlit
│   ├── models/              # Modelos de dados
│   │   ├── __init__.py
│   │   └── transaction.py   # Classe Transaction
│   └── utils/               # Utilitários
│       ├── __init__.py
│       └── constants.py     # Constantes do projeto
├── .env                     # Variáveis de ambiente
├── .gitignore              # Arquivos ignorados pelo Git
├── main.py                 # API FastAPI
├── pyproject.toml          # Dependências do projeto
└── README.md              # Documentação
```

### Descrição dos Componentes

#### DAGs
- `generate_transactions_dag.py`: Gera transações diariamente às 00:00 UTC
- `save_to_database_dag.py`: Salva transações no banco às 01:00 UTC

#### Dados
- `transactions.csv`: Arquivo temporário com transações geradas
- `transactions.db`: Banco SQLite com histórico de transações

#### Código Fonte
- **Data Generators**: Scripts para gerar dados simulados
- **Database**: Gerenciamento do banco de dados SQLite
- **Dashboard**: Interface visual com Streamlit
- **Models**: Classes e tipos de dados
- **Utils**: Funções e constantes compartilhadas

#### API e Configuração
- `main.py`: API FastAPI para controle do dashboard
- `pyproject.toml`: Dependências e metadados do projeto
- `.env`: Configurações de ambiente (não versionado)

## Funcionalidades

### Dashboard
- Filtro por período de datas
- Métricas principais (total, valor médio, etc.)
- Gráficos interativos:
  - Linha temporal de transações
  - Distribuição por categoria
  - Total por tipo de transação
- Tabela detalhada de transações

### DAGs
- Geração diária de dados
- Armazenamento automático no banco
- Tratamento de erros e retries

### API
- Gerenciamento do dashboard
- Status em tempo real
- Documentação automática (Swagger/ReDoc)

## Desenvolvimento

### Gerar Dados Manualmente
```bash
python src/generate_bank_transactions.py
```

### Salvar no Banco
```bash
python src/save_to_database.py
```

### Executar Dashboard Diretamente
```bash
streamlit run src/dashboard/app.py
```

### Comandos Úteis do Airflow

```bash
# Iniciar o ambiente Airflow
astro dev start

# Parar o ambiente Airflow
astro dev stop

# Reiniciar o ambiente Airflow
astro dev restart

# Ver logs
astro dev logs
```

## Licença

MIT
