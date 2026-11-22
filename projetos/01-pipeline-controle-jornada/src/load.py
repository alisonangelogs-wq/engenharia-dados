import json
import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL


ROOT_DIR = Path(__file__).resolve().parents[3]


def load_data(dados_validos, dados_rejeitados):
    """Cria as tabelas e grava os dados no PostgreSQL."""

    load_dotenv(ROOT_DIR / ".env")

    senha = os.getenv("POSTGRES_PASSWORD")

    if not senha:
        raise RuntimeError(
            "POSTGRES_PASSWORD não encontrada no arquivo .env"
        )

    url = URL.create(
        drivername="postgresql+psycopg",
        username="engenharia",
        password=senha,
        host="localhost",
        port=5433,
        database="engenharia_dados",
    )

    engine = create_engine(url)

    schema_path = (
        Path(__file__).resolve().parents[1] / "sql" / "schema.sql"
    )

    schema_sql = schema_path.read_text(encoding="utf-8")

    try:
        with engine.begin() as conexao:

            # Criação das tabelas.
            for comando in schema_sql.split(";"):
                if comando.strip():
                    conexao.exec_driver_sql(comando)

            # Inserção e atualização dos registros válidos.
            sql_validos = text("""
                INSERT INTO registros_jornada (
                    employee_id, work_date,
                    check_in, lunch_out,
                    lunch_in, check_out,
                    work_hours, source_row
                )
                VALUES (
                    :employee_id, :work_date,
                    :check_in, :lunch_out,
                    :lunch_in, :check_out,
                    :work_hours, :source_row
                )
                ON CONFLICT (employee_id, work_date)
                DO UPDATE SET
                    check_in = EXCLUDED.check_in,
                    lunch_out = EXCLUDED.lunch_out,
                    lunch_in = EXCLUDED.lunch_in,
                    check_out = EXCLUDED.check_out,
                    work_hours = EXCLUDED.work_hours,
                    source_row = EXCLUDED.source_row,
                    loaded_at = CURRENT_TIMESTAMP
            """)

            for registro in dados_validos:
                conexao.execute(sql_validos, registro)

            # Histórico de registros rejeitados.
            sql_rejeitados = text("""
                INSERT INTO registros_rejeitados (
                    employee_id,
                    work_date,
                    source_row,
                    rejection_reason,
                    raw_record
                )
                VALUES (
                    :employee_id,
                    :work_date,
                    :source_row,
                    :rejection_reason,
                    CAST(:raw_record AS JSONB)
                )
            """)

            for registro in dados_rejeitados:
                parametros = registro.copy()
                parametros["raw_record"] = json.dumps(
                    registro["raw_record"],
                    default=str,
                    ensure_ascii=False,
                )

                conexao.execute(sql_rejeitados, parametros)

        print("Carga no PostgreSQL concluída.")

    finally:
        engine.dispose()
