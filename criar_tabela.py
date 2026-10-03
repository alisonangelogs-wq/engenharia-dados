from sqlalchemy import create_engine, text

engine = create_engine(
    "postgresql+psycopg2://airflow:airflow@localhost:5432/engenharia_dados"
)

sql = """
CREATE TABLE IF NOT EXISTS funcionarios (
    employee_id INTEGER PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    departamento VARCHAR(100),
    cargo VARCHAR(100)
);
"""

with engine.begin() as conn:
    conn.execute(text(sql))

print("Tabela funcionarios criada com sucesso!")
