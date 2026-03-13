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


# ====== Pipeline =============================================================

def main():
    print("Carregando dados... ", end="", flush=True)
    df = pd.read_parquet(input_path)
    print(f"OK ({len(df):,} registros, {len(df.columns)} colunas)")

    transformacoes = [
        ("Removendo colunas desnecessárias", remover_colunas),
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