import pandas as pd
from ydata_profiling import ProfileReport
from pathlib import Path

# Caminhos
base_dir     = Path(__file__).resolve().parent.parent
input_path   = base_dir / "data" / "interim" / "focos_br_2024_sample.csv"
output_dir   = base_dir / "reports"
output_dir.mkdir(parents=True, exist_ok=True)
output_path  = output_dir / "focos_br_2024_sample_profile.html"

print("Carregando dados... ", end="", flush=True)
df = pd.read_csv(input_path)
print(f"OK ({len(df):,} registros, {len(df.columns)} colunas)")

print("Gerando relatório de profiling (pode demorar alguns minutos)...")
profile = ProfileReport(
    df,
    title="Focos de Queimadas e Incêndios — Brasil 2024 (amostra 300k)",
    explorative=True,
)

profile.to_file(output_path)
print(f"Relatório salvo em: {output_path}")