import pandas as pd
from ydata_profiling import ProfileReport
from pathlib import Path

# Caminhos relativos ao local do script (src/../data/)
base_dir = Path(__file__).resolve().parent.parent
input_path = base_dir / "data" / "raw" / "focos_mensal_br_202401.csv"
output_path = base_dir / "data" / "focos_mensal_br_202401_profile.html"

print("Carregando dados... ", end="", flush=True)
df = pd.read_csv(input_path)
print(f"OK ({len(df):,} registros, {len(df.columns)} colunas)")

print("Gerando relatório de profiling (pode demorar alguns minutos)...")
profile = ProfileReport(
    df,
    title="Focos de Queimadas e Incêndios — Brasil, Janeiro 2024",
    explorative=True,
)

profile.to_file(output_path)
print(f"Relatório salvo em: {output_path}")