
# Projeto 02 — Data Warehouse de Vendas

## 1. Visão geral

Desenvolvimento de um Data Warehouse para consolidar dados de clientes, produtos e vendas de uma empresa fictícia.

O projeto implementa um processo ETL utilizando Python e Pandas para extração, validação e transformação dos dados, PostgreSQL para armazenamento e SQL para consultas analíticas.

A solução utiliza modelagem dimensional no formato Star Schema, organizando os dados em dimensões e uma tabela fato para facilitar análises de negócio.

## 2. Objetivos técnicos

- Construir um processo ETL com Python.
- Extrair dados de diferentes arquivos CSV.
- Aplicar regras de validação e qualidade dos dados.
- Identificar valores ausentes e registros duplicados.
- Validar relacionamentos entre clientes, produtos e vendas.
- Implementar modelagem dimensional.
- Criar tabelas de dimensão e tabela fato.
- Armazenar dados no PostgreSQL.
- Desenvolver consultas SQL analíticas.
- Implementar testes automatizados com Pytest.

## 3. Tecnologias utilizadas

| Tecnologia | Aplicação |
|---|---|
| Python | Desenvolvimento do ETL |
| Pandas | Manipulação e transformação dos dados |
| PostgreSQL | Banco de dados do Data Warehouse |
| SQL | Modelagem e consultas analíticas |
| SQLAlchemy | Conexão com PostgreSQL |
| Docker | Ambiente do banco de dados |
| Pytest | Testes automatizados |
| Git | Controle de versão |
| GitHub | Hospedagem do código |

## 4. Arquitetura do projeto

O processo segue o fluxo ETL:

**Extract → Transform → Load**

1. **Extract:** leitura dos arquivos CSV de clientes, produtos e vendas.
2. **Transform:** validação dos dados, verificação dos relacionamentos, conversão de datas e cálculo do valor total das vendas.
3. **Load:** carregamento das dimensões e da tabela fato no PostgreSQL.

A arquitetura utiliza o modelo estrela (Star Schema).

### Estrutura dimensional

**Dimensões:**
- `dim_clientes`
- `dim_produtos`
- `dim_tempo`

**Tabela fato:**
- `fato_vendas`

A tabela fato utiliza chaves estrangeiras para relacionar os registros às dimensões.

O detalhamento da arquitetura está disponível em [`docs/arquitetura.md`](docs/arquitetura.md).

## 5. Estrutura de diretórios

```text
02-data-warehouse/
│
├── dados/
│   ├── clientes.csv
│   ├── produtos.csv
│   └── vendas.csv
│
├── docs/
│   └── arquitetura.md
│
├── sql/
│   ├── 02_create_dimensions.sql
│   ├── 03_create_fact_table.sql
│   └── 04_analytics_queries.sql
│
├── src/
│   ├── extract.py
│   ├── transform.py
│   ├── database.py
│   ├── load_dimensions.py
│   ├── __init__.py
│   ├── load_fact.py
│   └── pipeline.py
│
├── tests/
│   ├── test_transform.py
│   └── test_pipeline.py
│
└── README.md
```

## 6. Resultados obtidos

O processamento dos dados de origem produziu os seguintes indicadores:

| Indicador | Resultado |
|---|---:|
| Clientes cadastrados | 10 |
| Produtos cadastrados | 10 |
| Vendas processadas | 15 |
| Unidades vendidas | 25 |
| Faturamento total | R$ 16.870,00 |
| Ticket médio | R$ 1.124,67 |

### Consultas analíticas desenvolvidas

- Indicadores gerais de vendas.
- Faturamento por categoria.
- Faturamento por cliente.
- Desempenho por produto.
- Faturamento por mês.
- Faturamento por cidade.

## 7. Testes automatizados

O projeto utiliza Pytest para verificar as regras de transformação e o funcionamento do pipeline.

Os testes contemplam:

- Valores ausentes.
- Identificadores duplicados.
- Preços e custos inválidos.
- Quantidades e valores unitários inválidos.
- Relacionamentos inconsistentes.
- Conversão de datas.
- Cálculo do valor total.
- Execução integrada do pipeline com funções simuladas.

**Resultado: 17 testes aprovados.**

O teste de integração do pipeline utiliza mocks, sem realizar operações reais no banco de dados.

## 8. Como executar

### Pré-requisitos

- Python instalado.
- Docker instalado e em execução.
- PostgreSQL configurado conforme o projeto.
- Dependências Python instaladas.
- Arquivo `.env` configurado na raiz do repositório principal.

### Executar o pipeline

Com o ambiente virtual ativado, entre na pasta do projeto e execute:

```bash
python -m src.pipeline
```

### Executar os testes

```bash
python -m pytest -v
```

### Executar as consultas SQL

Na pasta do projeto:

```bash
docker exec -i portfolio_postgres psql -U engenharia -d engenharia_dados < sql/04_analytics_queries.sql
```

## 9. Aprendizados técnicos

Durante o desenvolvimento foram aplicados conceitos de:

- Engenharia de Dados e processos ETL.
- Manipulação de dados com Pandas.
- Validação e qualidade de dados.
- Modelagem dimensional e Star Schema.
- Chaves substitutas e integridade referencial.
- Integração Python e PostgreSQL.
- Consultas SQL analíticas.
- Testes automatizados e mocks.
- Organização de projetos e controle de versão com Git.

## 10. Autor

**Alison Angelo**

Projeto desenvolvido para fins de aprendizado prático e construção de portfólio na área de Engenharia de Dados.
