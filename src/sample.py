import pandas as pd
import sys
from pathlib import Path

# Adiciona src/ ao path para importar kmeans
sys.path.append(str(Path(__file__).resolve().parent))
from kmeans import treinar_kmeans, atribuir_clusters

# ====== Caminhos =============================================================

base_dir    = Path(__file__).resolve().parent.parent
input_path  = base_dir / "data" / "interim"   / "focos_br_2024.parquet"
output_path = base_dir / "data" / "processed" / "focos_br_2024_sample.csv"
output_path.parent.mkdir(parents=True, exist_ok=True)

# ====== Configurações ========================================================

AMOSTRA_TOTAL = 500_000
RANDOM_STATE  = 42

# ====== Carregamento =========================================================

print("Carregando dados... ", end="", flush=True)
df = pd.read_parquet(input_path)
print(f"OK ({len(df):,} registros)")

# ====== Clusterização ========================================================

print("Treinando k-means... ", end="", flush=True)
kmeans, scaler = treinar_kmeans(df)
print("OK")

print("Atribuindo clusters... ", end="", flush=True)
df = atribuir_clusters(df, kmeans, scaler)
print("OK")
print(f"Distribuição por cluster:\n{df['cluster'].value_counts().sort_index()}")

# ====== Amostragem estratificada por cluster =================================

print(f"\nAmostrando {AMOSTRA_TOTAL:,} registros estratificados por cluster...")
df_sample = (
    df.groupby("cluster", group_keys=False)
    .apply(lambda x: x.sample(
        n=round(AMOSTRA_TOTAL * len(x) / len(df)),
        random_state=RANDOM_STATE
    ))
    .reset_index(drop=True)
)

# ====== Salvamento ===========================================================

df_sample.to_csv(output_path, index=False)
print(f"\nAmostra salva em: {output_path}")
print(f"Total de registros: {len(df_sample):,}")
print(f"Distribuição por cluster:\n{df_sample['cluster'].value_counts().sort_index()}")