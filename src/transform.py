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
    colunas_remover = ["id", "pais", "pais_id", "municipio_id", "estado_id", "satelite"]
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


def tratar_risco_fogo(df: pd.DataFrame) -> pd.DataFrame:
    """Substitui valores negativos por NaN em risco_fogo.
    Valores válidos vão de 0 a 1.
    """
    import numpy as np
    df["risco_fogo"] = df["risco_fogo"].where(df["risco_fogo"] >= 0, np.nan)
    return df


def dropar_nulos(df: pd.DataFrame) -> pd.DataFrame:
    """Remove registros com NaN nas colunas essenciais para análise."""
    colunas = ["numero_dias_sem_chuva", "precipitacao", "risco_fogo", "frp"]
    antes = len(df)
    df = df.dropna(subset=colunas)
    depois = len(df)
    print(f"({antes - depois:,} registros removidos)", end=" ")
    return df

def remover_negativos(df: pd.DataFrame) -> pd.DataFrame:
    """Remove registros com valores negativos em colunas que não admitem negativos."""
    colunas = ["frp", "precipitacao", "numero_dias_sem_chuva", "risco_fogo"]
    antes = len(df)
    for col in colunas:
        df = df[df[col] >= 0]
    depois = len(df)
    print(f"({antes - depois:,} registros removidos)", end=" ")
    return df


def tratar_data_hora(df: pd.DataFrame) -> pd.DataFrame:
    """Quebra data_hora_gmt em três colunas: data, hora e mes."""
    df["data_hora_gmt"] = pd.to_datetime(df["data_hora_gmt"])
    df["data"] = df["data_hora_gmt"].dt.strftime("%Y-%m-%d")
    df["mes"]  = df["data_hora_gmt"].dt.month
    df = df.drop(columns=["data_hora_gmt"])
    return df


def remover_duplicados(df: pd.DataFrame) -> pd.DataFrame:
    """Remove registros duplicados gerados na concatenação dos meses."""
    antes = len(df)
    df = df.drop_duplicates()
    depois = len(df)
    print(f"({antes - depois:,} duplicados removidos)", end=" ")
    return df

def normalizar_frp(df: pd.DataFrame) -> pd.DataFrame:
    """Normaliza FRP para escala 0-1 usando min-max."""
    df["frp"] = (df["frp"] - df["frp"].min()) / (df["frp"].max() - df["frp"].min())
    return df


# ====== Pipeline =============================================================

def main():
    print("Carregando dados... ", end="", flush=True)
    df = pd.read_parquet(input_path)
    print(f"OK ({len(df):,} registros, {len(df.columns)} colunas)")

    transformacoes = [
        ("Removendo colunas desnecessárias", remover_colunas),
        ("Tratando dias sem chuva",          tratar_dias_sem_chuva),
        ("Tratando risco de fogo",           tratar_risco_fogo),
        ("Quebrando data e hora",            tratar_data_hora),
        ("Removendo duplicados",             remover_duplicados),
        ("Dropando nulos",                   dropar_nulos),
        ("Normalizando FRP",                 normalizar_frp),
        ("Removendo negativos",              remover_negativos),
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