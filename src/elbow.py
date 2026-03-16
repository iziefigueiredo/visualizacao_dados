import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from pathlib import Path

# ====== Configurações ========================================================

COLUNAS_KMEANS = ["lat", "lon", "numero_dias_sem_chuva", "precipitacao", "frp"]
K_MIN          = 2
K_MAX          = 11
RANDOM_STATE   = 42
AMOSTRA        = None  # None = usa todos os registros

# ====== Função principal =====================================================

def main():
    base_dir    = Path(__file__).resolve().parent.parent
    input_path  = base_dir / "data" / "interim" / "focos_br_2024.parquet"
    output_dir  = base_dir / "reports"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "elbow.png"

    print("Carregando dados... ", end="", flush=True)
    df = pd.read_parquet(input_path)
    print(f"OK ({len(df):,} registros)")

    df_clean = df[COLUNAS_KMEANS].dropna()
    print(f"Registros sem NaN nas colunas do k-means: {len(df_clean):,}")

    if AMOSTRA:
        df_sample = df_clean.sample(n=min(AMOSTRA, len(df_clean)), random_state=RANDOM_STATE)
        print(f"Amostra para elbow: {len(df_sample):,} registros")
    else:
        df_sample = df_clean
        print(f"Usando todos os registros: {len(df_sample):,}")

    scaler   = StandardScaler()
    X_scaled = scaler.fit_transform(df_sample)

    print(f"\nCalculando inércia para k={K_MIN} até k={K_MAX-1}...")
    inercias = []
    for k in range(K_MIN, K_MAX):
        print(f"  k={k}... ", end="", flush=True)
        kmeans = KMeans(n_clusters=k, random_state=RANDOM_STATE, n_init=10)
        kmeans.fit(X_scaled)
        inercias.append(kmeans.inertia_)
        print(f"inércia={kmeans.inertia_:.2f}")

    plt.figure(figsize=(8, 5))
    plt.plot(range(K_MIN, K_MAX), inercias, marker="o", color="steelblue", linewidth=2)
    plt.title("Método Elbow — Focos de Queimadas Brasil 2024", fontsize=13)
    plt.xlabel("Número de clusters (k)")
    plt.ylabel("Inércia")
    plt.xticks(range(K_MIN, K_MAX))
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    print(f"\nGráfico salvo em: {output_path}")


if __name__ == "__main__":
    main()