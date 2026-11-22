from src.extract import extract_data
from src.transform import transform_data
from src.load import load_data


def run_pipeline():
    print("=" * 55)
    print("PIPELINE ETL - CONTROLE DE JORNADA")
    print("=" * 55)

    # 1. Extração
    print("\n[1/3] Extraindo dados do CSV...")
    dados_extraidos = extract_data()
    print(f"Registros extraídos: {len(dados_extraidos)}")

    # 2. Transformação
    print("\n[2/3] Validando e transformando dados...")
    dados_validos, dados_rejeitados = transform_data(dados_extraidos)

    print(f"Registros válidos: {len(dados_validos)}")
    print(f"Registros rejeitados: {len(dados_rejeitados)}")

    # 3. Carga
    print("\n[3/3] Carregando dados no PostgreSQL...")
    load_data(dados_validos, dados_rejeitados)

    print("\nPipeline ETL finalizado.")
    print("=" * 55)


if __name__ == "__main__":
    run_pipeline()
