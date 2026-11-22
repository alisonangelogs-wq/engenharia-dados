
# 01 - Pipeline ETL de Controle de Jornada

## 1. Objetivo

Desenvolver um pipeline de Engenharia de Dados capaz de extrair, validar, transformar e carregar registros de jornada de funcionários em um banco de dados PostgreSQL.

O projeto utiliza dados demonstrativos em CSV e aplica regras de qualidade antes de armazenar as informações.

## 2. Tecnologias utilizadas

- Python 3.13
- Pandas
- PostgreSQL 17
- SQLAlchemy
- Psycopg
- Docker e Docker Compose
- Pytest
- SQL
- Git e GitHub

## 3. Arquitetura ETL

O projeto segue três etapas principais: Extract, Transform e Load.

### Extract — Extração

Arquivo: `src/extract.py`

Responsabilidades:
- Localizar e ler o arquivo CSV.
- Verificar a presença das colunas obrigatórias.
- Identificar a linha de origem de cada registro.
- Retornar os dados para processamento.

### Transform — Transformação

Arquivo: `src/transform.py`

Responsabilidades:
- Validar a identificação do funcionário.
- Validar a data da jornada.
- Validar os horários de entrada e saída.
- Verificar a sequência cronológica dos horários.
- Identificar duplicidades por funcionário e data.
- Calcular as horas trabalhadas, descontando o intervalo.
- Separar registros válidos e rejeitados.

### Load — Carga

Arquivo: `src/load.py`

Responsabilidades:
- Estabelecer conexão com PostgreSQL.
- Executar o script de criação das tabelas.
- Inserir registros válidos.
- Armazenar registros rejeitados e seus motivos.
- Atualizar registros existentes pela chave funcionário/data.

## 4. Estrutura de pastas

```text
01-pipeline-controle-jornada/
├── dados/
│     └── funcionarios.csv
│
├── sql/
│   └── schema.sql
├── src/
│   ├── __init__.py
│   ├── extract.py
│   ├── load.py
│   ├── pipeline.py
│   └── transform.py
├── tests/
│   ├── __init__.py
│   └── test_transform.py
└── README.md
```

## 5. Dados de entrada

Arquivo principal: `dados/funcionarios.csv`

Campos utilizados:

- `employee_id`: identificação do funcionário.
- `work_date`: data da jornada.
- `check_in`: horário de entrada.
- `lunch_out`: saída para intervalo.
- `lunch_in`: retorno do intervalo.
- `check_out`: horário de saída.

Os dados utilizados são demonstrativos.

## 6. Banco de dados

Banco: PostgreSQL

Tabelas:

- `registros_jornada`: armazena as jornadas válidas.
- `registros_rejeitados`: armazena os registros que não passaram pelas validações.

A tabela de jornadas utiliza uma chave composta por funcionário e data, evitando duplicidade para a mesma jornada.

## 7. Configuração do ambiente

Na raiz do repositório:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Crie o arquivo `.env` somente se ele ainda não existir:

```bash
cp -n .env.example .env
```

Configure a variável `POSTGRES_PASSWORD` no arquivo `.env` com a senha cadastrada no PostgreSQL.

O arquivo `.env` não deve ser enviado ao GitHub.

## 8. Inicialização do PostgreSQL

Na raiz do repositório:

```bash
docker compose up -d postgres
```

Verifique o serviço:

```bash
docker compose ps
```

## 9. Execução do pipeline

Entre na pasta do projeto:

```bash
cd projetos/01-pipeline-controle-jornada
```

Execute:

```bash
python -m src.pipeline
```

## 10. Testes automatizados

Execute:

```bash
pytest -v
```

Os testes verificam:

1. Cálculo das horas trabalhadas.
2. Rejeição de horário ausente.
3. Rejeição de sequência inválida.
4. Rejeição de funcionário duplicado.

## 11. Resultados da validação

Execução realizada com os dados demonstrativos:

| Indicador | Resultado |
|---|---:|
| Registros extraídos | 10 |
| Registros válidos | 10 |
| Registros rejeitados | 0 |
| Registros carregados | 10 |
| Testes aprovados | 4 |

A carga foi conferida diretamente no PostgreSQL.

## 12. Autor

Alison Angelo

GitHub: https://github.com/alisonangelogs-wq
