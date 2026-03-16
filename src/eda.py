import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path


def main():
    # ====== Caminhos =========================================================

    base_dir   = Path(__file__).resolve().parent.parent
    input_path = base_dir / "data" / "processed" / "focos_br_2024_sample.csv"
    output_dir = base_dir / "reports"
    output_dir.mkdir(parents=True, exist_ok=True)

    # ====== Carregamento =====================================================

    print("Carregando dados... ", end="", flush=True)
    df = pd.read_csv(input_path)
    print(f"OK ({len(df):,} registros)")

    cores = {
        "Amazônia": "steelblue",
        "Cerrado":  "darkorange",
        "Pantanal": "seagreen"
    }

    meses_label = {
        1: "Jan", 2: "Fev", 3: "Mar", 4: "Abr",
        5: "Mai", 6: "Jun", 7: "Jul", 8: "Ago",
        9: "Set", 10: "Out", 11: "Nov", 12: "Dez"
    }

    # ====== Boxplot: Risco de Fogo por Faixa de Precipitação =================

    print("Gerando boxplot chuva x fogo... ", end="", flush=True)
    df_plot = df[df["precipitacao"] <= df["precipitacao"].quantile(0.99)].copy()
    prec_max = df_plot["precipitacao"].max()
    bins     = [0, 1, 10, 30, 60, 100, prec_max + 1]
    labels   = ["0", "1-10", "10-30", "30-60", "60-100", ">100"]
    bins     = sorted(set(b for b in bins if b <= prec_max + 1))
    labels   = labels[:len(bins) - 1]
    df_plot["faixa_precipitacao"] = pd.cut(df_plot["precipitacao"], bins=bins, labels=labels, include_lowest=True)
    fig, ax = plt.subplots(figsize=(9, 6))
    df_plot.boxplot(column="risco_fogo", by="faixa_precipitacao", ax=ax, patch_artist=True,
        boxprops=dict(facecolor="steelblue", alpha=0.6),
        medianprops=dict(color="red", linewidth=2),
        flierprops=dict(marker="o", markersize=2, alpha=0.3))
    ax.set_title("Risco de Fogo por Faixa de Precipitação — Brasil 2024", fontsize=13)
    ax.set_xlabel("Faixa de Precipitação (mm)")
    ax.set_ylabel("Risco de Fogo (0-1)")
    plt.suptitle("")
    ax.grid(True, linestyle="--", alpha=0.4)
    plt.tight_layout()
    plt.savefig(output_dir / "boxplot_chuva_fogo.png", dpi=150)
    plt.close()
    print("OK")

    # ====== Boxplot: Risco de Fogo por Mês ===================================

    print("Gerando boxplot risco de fogo por mês... ", end="", flush=True)
    df["mes_label"] = df["mes"].map(meses_label)
    df_mes = df.copy()
    df_mes["mes_label"] = pd.Categorical(df_mes["mes_label"], categories=[meses_label[m] for m in range(1, 13)], ordered=True)
    df_mes.sort_values("mes_label", inplace=True)
    fig, ax = plt.subplots(figsize=(12, 6))
    df_mes.boxplot(column="risco_fogo", by="mes_label", ax=ax, patch_artist=True,
        boxprops=dict(facecolor="steelblue", alpha=0.6),
        medianprops=dict(color="red", linewidth=2),
        flierprops=dict(marker="o", markersize=1, alpha=0.2))
    ax.set_title("Risco de Fogo por Mês — Brasil 2024", fontsize=13)
    ax.set_xlabel("Mês")
    ax.set_ylabel("Risco de Fogo (0-1)")
    plt.suptitle("")
    ax.grid(True, linestyle="--", alpha=0.4)
    plt.tight_layout()
    plt.savefig(output_dir / "boxplot_risco_mes.png", dpi=150)
    plt.close()
    print("OK")

    # ====== Heatmap: Focos por Estado e Mês ==================================

    print("Gerando heatmap focos por estado e mês... ", end="", flush=True)
    pivot = df.groupby(["estado", "mes"]).size().unstack(fill_value=0)
    meses_disponiveis = [meses_label[m] for m in sorted(pivot.columns)]
    pivot.columns = meses_disponiveis
    pivot = pivot.loc[pivot.sum(axis=1).sort_values(ascending=False).head(20).index]
    fig, ax = plt.subplots(figsize=(14, 8))
    im = ax.imshow(pivot.values, aspect="auto", cmap="YlOrRd")
    plt.colorbar(im, ax=ax, label="Número de Focos")
    ax.set_xticks(range(len(meses_disponiveis)))
    ax.set_xticklabels(meses_disponiveis)
    ax.set_yticks(range(len(pivot)))
    ax.set_yticklabels(pivot.index)
    ax.set_title("Focos de Queimadas por Estado e Mês — Brasil 2024", fontsize=13)
    ax.set_xlabel("Mês")
    ax.set_ylabel("Estado")
    plt.tight_layout()
    plt.savefig(output_dir / "heatmap_focos_estado_mes.png", dpi=150)
    plt.close()
    print("OK")

    # ====== Área Empilhada: Focos por Bioma ao longo dos Meses ===============

    print("Gerando área empilhada focos por bioma e mês... ", end="", flush=True)
    focos_bioma_mes = df.groupby(["mes", "bioma"]).size().unstack(fill_value=0)
    focos_bioma_mes.index = [meses_label[m] for m in focos_bioma_mes.index]
    # Ordem: menor volume na base, maior no topo
    ordem = ["Pantanal", "Cerrado", "Amazônia"]
    ordem_disponivel = [b for b in ordem if b in focos_bioma_mes.columns]
    focos_bioma_mes = focos_bioma_mes[ordem_disponivel]
    fig, ax = plt.subplots(figsize=(12, 6))
    focos_bioma_mes.plot.area(ax=ax, color=[cores.get(b, "gray") for b in focos_bioma_mes.columns], alpha=0.7)
    ax.set_title("Distribuição de Focos por Bioma ao Longo dos Meses — Brasil 2024", fontsize=13)
    ax.set_xlabel("Mês")
    ax.set_ylabel("Número de Focos")
    ax.legend(title="Bioma")
    ax.grid(True, linestyle="--", alpha=0.4)
    plt.tight_layout()
    plt.savefig(output_dir / "area_focos_bioma_mes.png", dpi=150)
    plt.close()
    print("OK")

    # ====== Linha: FRP Médio por Bioma e Mês =================================

    print("Gerando FRP médio por bioma e mês... ", end="", flush=True)
    frp_bioma_mes = df.groupby(["mes", "bioma"])["frp"].mean().unstack(fill_value=0)
    frp_bioma_mes.index = [meses_label[m] for m in frp_bioma_mes.index]
    fig, ax = plt.subplots(figsize=(12, 6))
    for bioma in frp_bioma_mes.columns:
        ax.plot(frp_bioma_mes.index, frp_bioma_mes[bioma], marker="o", label=bioma, color=cores.get(bioma, "gray"), linewidth=2)
    ax.set_title("FRP Médio por Bioma ao Longo dos Meses — Brasil 2024", fontsize=13)
    ax.set_xlabel("Mês")
    ax.set_ylabel("FRP Médio (Fire Radiative Power)")
    ax.legend(title="Bioma")
    ax.grid(True, linestyle="--", alpha=0.4)
    plt.tight_layout()
    plt.savefig(output_dir / "linha_frp_bioma_mes.png", dpi=150)
    plt.close()
    print("OK")

    # ====== Linha: Média de Dias sem Chuva por Bioma e Mês ===================

    print("Gerando linha média dias sem chuva por bioma e mês... ", end="", flush=True)
    dias_bioma_mes = df.groupby(["mes", "bioma"])["numero_dias_sem_chuva"].mean().unstack(fill_value=0)
    dias_bioma_mes.index = [meses_label[m] for m in dias_bioma_mes.index]
    fig, ax = plt.subplots(figsize=(12, 6))
    for bioma in dias_bioma_mes.columns:
        ax.plot(dias_bioma_mes.index, dias_bioma_mes[bioma], marker="o", label=bioma, color=cores.get(bioma, "gray"), linewidth=2)
    ax.set_title("Média de Dias sem Chuva por Bioma ao Longo dos Meses — Brasil 2024", fontsize=13)
    ax.set_xlabel("Mês")
    ax.set_ylabel("Média de Dias sem Chuva")
    ax.legend(title="Bioma")
    ax.grid(True, linestyle="--", alpha=0.4)
    plt.tight_layout()
    plt.savefig(output_dir / "linha_dias_sem_chuva_bioma_mes.png", dpi=150)
    plt.close()
    print("OK")

    # ====== Barras: Focos por Hora do Dia por Bioma ==========================

    print("Gerando barras focos por hora do dia por bioma... ", end="", flush=True)
    focos_hora_bioma = df.groupby(["hora", "bioma"]).size().unstack(fill_value=0)
    biomas = focos_hora_bioma.columns.tolist()
    horas  = focos_hora_bioma.index.tolist()
    x      = np.arange(len(horas))
    width  = 0.25
    fig, ax = plt.subplots(figsize=(14, 6))
    for i, bioma in enumerate(biomas):
        ax.bar(x + i * width, focos_hora_bioma[bioma], width=width, label=bioma, color=cores.get(bioma, "gray"), alpha=0.8)
    ax.set_title("Focos de Queimadas por Hora do Dia e Bioma — Brasil 2024", fontsize=13)
    ax.set_xlabel("Hora do Dia (GMT)")
    ax.set_ylabel("Número de Focos")
    ax.set_xticks(x + width)
    ax.set_xticklabels(horas)
    ax.legend(title="Bioma")
    ax.grid(True, linestyle="--", alpha=0.4, axis="y")
    plt.tight_layout()
    plt.savefig(output_dir / "barras_focos_hora_bioma.png", dpi=150)
    plt.close()
    print("OK")

    print(f"\nGráficos salvos em: {output_dir}")


if __name__ == "__main__":
    main()