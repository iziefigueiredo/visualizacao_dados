import pandas as pd
from pathlib import Path

# ====== Configurações ========================================================

AMOSTRA_TOTAL = 500_000
RANDOM_STATE  = 42

# ====== Função principal =====================================================

def main():
    base_dir    = Path(__file__).resolve().parent.parent
    input_path  = base_dir / "data" / "raw"     / "focos_br_2024.parquet"
    output_path = base_dir / "data" / "interim" / "focos_br_2024_sample_raw.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    print("Carregando dados brutos... ", end="", flush=True)
    df = pd.read_parquet(input_path)
    print(f"OK ({len(df):,} registros)")

    print("Amostrando estratificado por bioma... ", end="", flush=True)
    df_sample = (
        df.groupby("bioma", group_keys=False)
        .apply(lambda x: x.sample(
            n=min(round(AMOSTRA_TOTAL * len(x) / len(df)), len(x)),
            random_state=RANDOM_STATE
        ), include_groups=True)
        .reset_index(drop=True)
    )
    print("OK")

    df_sample.to_csv(output_path, index=False)
    print(f"\nAmostra salva em: {output_path}")
    print(f"Total de registros: {len(df_sample):,}")
    print(f"Distribuição por bioma:\n{df_sample['bioma'].value_counts()}")


if __name__ == "__main__":
    main()