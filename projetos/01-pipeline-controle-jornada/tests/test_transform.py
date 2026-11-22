import pandas as pd

from src.transform import transform_data


def criar_registro(
    employee_id="001",
    check_in="08:00",
    lunch_out="12:00",
    lunch_in="13:00",
    check_out="17:00",
    source_row=2,
):
    return {
        "employee_id": employee_id,
        "work_date": "2026-11-09",
        "check_in": check_in,
        "lunch_out": lunch_out,
        "lunch_in": lunch_in,
        "check_out": check_out,
        "source_row": source_row,
    }


def test_calculo_horas_trabalhadas():
    df = pd.DataFrame([criar_registro()])

    validos, rejeitados = transform_data(df)

    assert len(validos) == 1
    assert len(rejeitados) == 0
    assert validos[0]["work_hours"] == 8.0


def test_rejeitar_horario_ausente():
    df = pd.DataFrame([
        criar_registro(check_out="")
    ])

    validos, rejeitados = transform_data(df)

    assert len(validos) == 0
    assert len(rejeitados) == 1
    assert "check_out ausente ou inválido" in (
        rejeitados[0]["rejection_reason"]
    )


def test_rejeitar_sequencia_invalida():
    df = pd.DataFrame([
        criar_registro(
            check_in="12:00",
            lunch_out="11:00",
            lunch_in="12:00",
            check_out="16:00",
        )
    ])

    validos, rejeitados = transform_data(df)

    assert len(validos) == 0
    assert len(rejeitados) == 1
    assert "sequência cronológica inválida" in (
        rejeitados[0]["rejection_reason"]
    )


def test_rejeitar_funcionario_duplicado():
    df = pd.DataFrame([
        criar_registro(source_row=2),
        criar_registro(source_row=3),
    ])

    validos, rejeitados = transform_data(df)

    assert len(validos) == 0
    assert len(rejeitados) == 2
    assert all(
        "duplicado" in registro["rejection_reason"]
        for registro in rejeitados
    )
