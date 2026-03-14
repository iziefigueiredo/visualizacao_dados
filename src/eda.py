import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# ====== Caminhos =============================================================

base_dir    = Path(__file__).resolve().parent.parent
input_path  = base_dir / "data" / "processed" / "focos_br_2024_sample.csv"
output_dir  = base_dir / "reports"
output_dir.mkdir(parents=True, exist_ok=True)

# ====== Carregamento =========================================================

print("Carregando dados... ", end="", flush=True)
df = pd.read_csv(input_path)
print(f"OK ({len(df):,} registros)")

# Remove outliers extremos de precipitacao para melhor visualização
df_plot = df[df["precipitacao"] <= df["precipitacao"].quantile(0.99)]

# ====== Hexbin ===============================================================

print("Gerando hexbin... ", end="", flush=True)
fig, ax = plt.subplots(figsize=(9, 6))

hb = ax.hexbin(
    df_plot["precipitacao"],
    df_plot["risco_fogo"],
    gridsize=50,
    cmap="YlOrRd",
    mincnt=1
)

plt.colorbar(hb, ax=ax, label="Número de focos")
ax.set_title("Precipitação vs Risco de Fogo — Brasil 2024", fontsize=13)
ax.set_xlabel("Precipitação (mm)")
ax.set_ylabel("Risco de Fogo (0-1)")
ax.grid(True, linestyle="--", alpha=0.4)
plt.tight_layout()
plt.savefig(output_dir / "eda_hexbin_chuva_fogo.png", dpi=150)
plt.close()
print("OK")

# ====== Boxplot ==============================================================

print("Gerando boxplot... ", end="", flush=True)

# Cria faixas de precipitação
bins   = [0, 1, 10, 30, 60, 100, df_plot["precipitacao"].max()]
labels = ["0", "1-10", "10-30", "30-60", "60-100", ">100"]
df_plot = df_plot.copy()
df_plot["faixa_precipitacao"] = pd.cut(
    df_plot["precipitacao"], bins=bins, labels=labels, include_lowest=True
)

fig, ax = plt.subplots(figsize=(9, 6))

df_plot.boxplot(
    column="risco_fogo",
    by="faixa_precipitacao",
    ax=ax,
    patch_artist=True,
    boxprops=dict(facecolor="steelblue", alpha=0.6),
    medianprops=dict(color="red", linewidth=2),
    flierprops=dict(marker="o", markersize=2, alpha=0.3)
)

ax.set_title("Risco de Fogo por Faixa de Precipitação — Brasil 2024", fontsize=13)
ax.set_xlabel("Faixa de Precipitação (mm)")
ax.set_ylabel("Risco de Fogo (0-1)")
plt.suptitle("")
ax.grid(True, linestyle="--", alpha=0.4)
plt.tight_layout()
plt.savefig(output_dir / "eda_boxplot_chuva_fogo.png", dpi=150)
plt.close()
print("OK")

print(f"\nGráficos salvos em: {output_dir}")