import requests
import pandas as pd
from io import StringIO
from pathlib import Path

base_url = "https://dataserver-coids.inpe.br/queimadas/queimadas/focos/csv/mensal/Brasil/"

# Pasta de destino relativa ao local do script (src/../data/raw)
output_dir = Path(__file__).resolve().parent.parent / "data" / "raw"
output_dir.mkdir(parents=True, exist_ok=True)

mes = 1
url = f"{base_url}focos_mensal_br_202401.csv"
print(f"Baixando mês {mes:02d}/2024... ", end="", flush=True)

try:
    response = requests.get(url, timeout=60)
    response.raise_for_status()

    df = pd.read_csv(StringIO(response.text))

    output_path = output_dir / "focos_mensal_br_202401.csv"
    df.to_csv(output_path, index=False)

    print(f"OK ({len(df):,} registros)")
    print(f"Arquivo salvo em: {output_path}")

except requests.exceptions.Timeout:
    print("TIMEOUT — verifique sua conexão e tente novamente.")
except requests.exceptions.HTTPError as e:
    print(f"ERRO HTTP: {e}")
except Exception as e:
    print(f"ERRO: {e}")