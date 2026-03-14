import pandas as pd
from pathlib import Path

# Caminhos
base_dir     = Path(__file__).resolve().parent.parent
input_path   = base_dir / "data" / "raw"     / "focos_br_2024.parquet"
output_path  = base_dir / "data" / "interim" / "focos_br_2024.parquet"
output_path.parent.mkdir(parents=True, exist_ok=True)


# ====== Funções de transformação =============================================

def remover_colunas(df: pd.DataFrame) -> pd.DataFrame:
    """Remove colunas que não agregam análise."""
    colunas_remover = ["id", "pais", "pais_id", "municipio_id", "estado_id"]
    return df.drop(columns=colunas_remover)


def tratar_dias_sem_chuva(df: pd.DataFrame) -> pd.DataFrame:
    """Substitui valores negativos por NaN em numero_dias_sem_chuva.
    Zeros reais são mantidos — indicam que choveu no dia.
    """
    import numpy as np
    df["numero_dias_sem_chuva"] = df["numero_dias_sem_chuva"].where(
        df["numero_dias_sem_chuva"] >= 0, np.nan
    )
    return df


def tratar_data_hora(df: pd.DataFrame) -> pd.DataFrame:
    """Quebra data_hora_gmt em duas colunas: data e hora."""
    df["data_hora_gmt"] = pd.to_datetime(df["data_hora_gmt"])
    df["data"] = df["data_hora_gmt"].dt.date
    df["hora"] = df["data_hora_gmt"].dt.hour
    df = df.drop(columns=["data_hora_gmt"])
    return df


# ====== Pipeline =============================================================

def main():
    print("Carregando dados... ", end="", flush=True)
    df = pd.read_parquet(input_path)
    print(f"OK ({len(df):,} registros, {len(df.columns)} colunas)")

    transformacoes = [
        ("Removendo colunas desnecessárias", remover_colunas),
        ("Tratando dias sem chuva",          tratar_dias_sem_chuva),
        ("Quebrando data e hora",            tratar_data_hora),
    ]

    for descricao, funcao in transformacoes:
        print(f"{descricao}... ", end="", flush=True)
        df = funcao(df)
        print("OK")

    df.to_parquet(output_path, index=False)
    print(f"\nArquivo salvo em: {output_path}")
    print(f"Total de registros: {len(df):,}")
    print(f"Colunas finais: {list(df.columns)}")


if __name__ == "__main__":
    main()