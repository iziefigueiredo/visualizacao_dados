import pandas as pd
from pathlib import Path

# Caminhos
base_dir    = Path(__file__).resolve().parent.parent
input_path  = base_dir / "data" / "raw"     / "focos_br_2024.parquet"
output_path = base_dir / "data" / "interim" / "focos_br_2024_sample.csv"
output_path.parent.mkdir(parents=True, exist_ok=True)

AMOSTRA_TOTAL = 50_000
RANDOM_STATE  = 42

print("Carregando dados... ", end="", flush=True)
df = pd.read_parquet(input_path)
print(f"OK ({len(df):,} registros)")

print("\nDistribuição original por bioma:")
print(df["bioma"].value_counts())

# Amostragem estratificada --> mantém proporção por bioma
df_sample = (
    df.groupby("bioma", group_keys=False)
    .apply(lambda x: x.sample(
        n=round(AMOSTRA_TOTAL * len(x) / len(df)),
        random_state=RANDOM_STATE
    ))
    .reset_index(drop=True)
)

print(f"\nDistribuição da amostra por bioma:")
print(df_sample["bioma"].value_counts())

df_sample.to_csv(output_path, index=False)
print(f"\nAmostra salva em: {output_path}")
print(f"Total de registros: {len(df_sample):,}")