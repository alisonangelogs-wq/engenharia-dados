from collections import Counter
from datetime import datetime


COLUNAS_HORARIOS = [
    "check_in",
    "lunch_out",
    "lunch_in",
    "check_out",
]


def transform_data(df):
    """
    Valida os registros de jornada.
    Retorna dois DataFrames: registros válidos e rejeitados.
    """

    registros_validos = []
    registros_rejeitados = []
    registros_processados = []

    for registro in df.to_dict(orient="records"):
        employee_id = str(registro.get("employee_id", "")).strip()
        motivos = []

        if not employee_id or employee_id.lower() == "nan":
            motivos.append("employee_id ausente")

        # Validação da data.
        try:
            work_date = datetime.strptime(
                str(registro["work_date"]).strip(),
                "%Y-%m-%d"
            ).date()
        except (ValueError, TypeError):
            work_date = None
            motivos.append("data inválida")

        # Validação dos horários.
        horarios = {}

        for coluna in COLUNAS_HORARIOS:
            valor = registro.get(coluna)

            try:
                if valor is None or str(valor).strip() == "":
                    raise ValueError

                horarios[coluna] = datetime.strptime(
                    str(valor).strip(),
                    "%H:%M"
                ).time()

            except (ValueError, TypeError):
                horarios[coluna] = None
                motivos.append(f"{coluna} ausente ou inválido")

        # Verificação da sequência cronológica.
        if all(horarios.values()):
            sequencia = [horarios[coluna] for coluna in COLUNAS_HORARIOS]

            if sequencia != sorted(sequencia):
                motivos.append("sequência cronológica inválida")

        registros_processados.append({
            "employee_id": employee_id,
            "work_date": work_date,
            "horarios": horarios,
            "source_row": registro.get("source_row"),
            "raw_record": registro,
            "motivos": motivos,
        })

    # Identificação de registros duplicados.
    chaves = [
        (item["employee_id"], item["work_date"])
        for item in registros_processados
        if item["employee_id"] and item["work_date"] is not None
    ]

    contagem = Counter(chaves)

    for item in registros_processados:
        chave = (item["employee_id"], item["work_date"])

        if item["work_date"] is not None and contagem[chave] > 1:
            item["motivos"].append(
                "registro duplicado para funcionário e data"
            )

        if item["motivos"]:
            registros_rejeitados.append({
                "employee_id": item["employee_id"] or None,
                "work_date": item["work_date"],
                "source_row": item["source_row"],
                "rejection_reason": "; ".join(item["motivos"]),
                "raw_record": item["raw_record"],
            })
            continue

        horarios = item["horarios"]

        minutos_manha = (
            horarios["lunch_out"].hour * 60
            + horarios["lunch_out"].minute
            - horarios["check_in"].hour * 60
            - horarios["check_in"].minute
        )

        minutos_tarde = (
            horarios["check_out"].hour * 60
            + horarios["check_out"].minute
            - horarios["lunch_in"].hour * 60
            - horarios["lunch_in"].minute
        )

        work_hours = round(
            (minutos_manha + minutos_tarde) / 60,
            2
        )

        registros_validos.append({
            "employee_id": item["employee_id"],
            "work_date": item["work_date"],
            **horarios,
            "work_hours": work_hours,
            "source_row": item["source_row"],
        })

    return registros_validos, registros_rejeitados
