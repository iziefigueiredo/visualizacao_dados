import pandas as pd
from ydata_profiling import ProfileReport
from pathlib import Path


def main():
    # ====== Caminhos =========================================================

    base_dir   = Path(__file__).resolve().parent.parent
    output_dir = base_dir / "reports"
    output_dir.mkdir(parents=True, exist_ok=True)

    perfis = [
        {
            "input":   base_dir / "data" / "raw" / "focos_br_2024.parquet",
            "output":  output_dir / "profile_raw.html",
            "title":   "Focos de Queimadas — Brasil 2024 (dados brutos)",
            "minimal": True,
            "formato": "parquet"
        },
        {
            "input":   base_dir / "data" / "processed" / "focos_br_2024_sample.csv",
            "output":  output_dir / "profile_sample_tratado.html",
            "title":   "Focos de Queimadas — Brasil 2024 (amostra tratada)",
            "minimal": False,
            "formato": "csv"
        },
    ]

    # ====== Geração dos profiles =============================================

    for perfil in perfis:
        print(f"\nCarregando {perfil['input'].name}... ", end="", flush=True)

        if perfil["formato"] == "parquet":
            df = pd.read_parquet(perfil["input"])
        else:
            df = pd.read_csv(perfil["input"])

        print(f"OK ({len(df):,} registros, {len(df.columns)} colunas)")

        print("Gerando relatório de profiling (pode demorar alguns minutos)...")
        profile = ProfileReport(
            df,
            title=perfil["title"],
            minimal=perfil["minimal"],
            explorative=not perfil["minimal"],
        )

        profile.to_file(perfil["output"])
        print(f"Relatório salvo em: {perfil['output']}")


if __name__ == "__main__":
    main()