import os
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine

# Localiza a raiz do repositório
DIRETORIO_RAIZ = Path(__file__).resolve().parents[3]

# Carrega as configurações do arquivo .env
load_dotenv(DIRETORIO_RAIZ / ".env")

# Recupera as configurações do PostgreSQL
POSTGRES_USER = os.getenv("POSTGRES_USER", "engenharia")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5433")
POSTGRES_DB = os.getenv("POSTGRES_DB", "engenharia_dados")

# Verifica se a senha foi encontrada
if not POSTGRES_PASSWORD:
    raise ValueError("POSTGRES_PASSWORD não foi encontrada no arquivo .env")

# Monta a URL de conexão
DATABASE_URL = (
    f"postgresql+psycopg://{POSTGRES_USER}:"
    f"{POSTGRES_PASSWORD}@{POSTGRES_HOST}:"
    f"{POSTGRES_PORT}/{POSTGRES_DB}"
)

# Cria o mecanismo de conexão
engine = create_engine(DATABASE_URL)

# Testa a conexão com o banco
def testar_conexao():
    with engine.connect() as conexao:
        resultado = conexao.exec_driver_sql("SELECT version();")
        print("Conexão com PostgreSQL estabelecida.")
        print(resultado.scalar())