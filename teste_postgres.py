import pandas as pd
from sqlalchemy import create_engine

# Conexão com PostgreSQL
engine = create_engine(
    "postgresql+psycopg2://airflow:airflow@localhost:5432/engenharia_dados"
)

# Teste de conexão
with engine.connect() as conn:
    print("CONEXÃO COM POSTGRES OK")

# Lista as tabelas existentes
tabelas = pd.read_sql(
    """
    SELECT table_name
    FROM information_schema.tables
    WHERE table_schema = 'public'
    ORDER BY table_name;
    """,
    engine
)

print("\nTABELAS DO BANCO:")
print(tabelas)
