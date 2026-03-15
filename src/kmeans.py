import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# ====== Configurações ========================================================

COLUNAS_KMEANS = ["lat", "lon", "numero_dias_sem_chuva", "precipitacao", "frp", "hora", "mes"]
K              = 6
RANDOM_STATE   = 42

# ====== Funções ==============================================================

def treinar_kmeans(df: pd.DataFrame) -> tuple:
    """Treina o k-means e retorna o modelo e o scaler ajustados."""
    df_clean = df[COLUNAS_KMEANS].dropna()

    scaler   = StandardScaler()
    X_scaled = scaler.fit_transform(df_clean)

    kmeans = KMeans(n_clusters=K, random_state=RANDOM_STATE, n_init=10)
    kmeans.fit(X_scaled)

    return kmeans, scaler


def atribuir_clusters(df: pd.DataFrame, kmeans: KMeans, scaler: StandardScaler) -> pd.DataFrame:
    """Atribui o cluster a cada registro do dataframe."""
    df_clean  = df[COLUNAS_KMEANS].dropna()
    X_scaled  = scaler.transform(df_clean)
    labels    = kmeans.predict(X_scaled)

    df["cluster"] = np.nan
    df.loc[df_clean.index, "cluster"] = labels
    df["cluster"] = df["cluster"].astype("Int64")

    return df

if __name__ == "__main__":
    main()