import requests
import pandas as pd
from io import StringIO
from pathlib import Path
import time

# ====== Configurações ========================================================

base_url   = "https://dataserver-coids.inpe.br/queimadas/queimadas/focos/csv/mensal/Brasil/"
BIOMAS     = ["Amazônia", "Cerrado", "Pantanal"]

# ====== Função principal =====================================================

def main():
    output_dir = Path(__file__).resolve().parent.parent / "data" / "raw"
    output_dir.mkdir(parents=True, exist_ok=True)

    dfs = []

    for mes in range(1, 13):
        url = f"{base_url}focos_mensal_br_2024{mes:02d}.csv"
        print(f"Baixando mês {mes:02d}/2024... ", end="", flush=True)

        try:
            response = requests.get(url, timeout=60)
            response.raise_for_status()

            df = pd.read_csv(StringIO(response.text))
            df_filtrado = df[df["bioma"].isin(BIOMAS)]
            dfs.append(df_filtrado)
            print(f"OK ({len(df):,} registros → {len(df_filtrado):,} após filtro)")

        except requests.exceptions.Timeout:
            print(f"TIMEOUT — pulando mês {mes:02d}")
        except requests.exceptions.HTTPError as e:
            print(f"ERRO HTTP: {e} — pulando mês {mes:02d}")
        except Exception as e:
            print(f"ERRO: {e} — pulando mês {mes:02d}")

        time.sleep(1)

    if dfs:
        df_final = pd.concat(dfs, ignore_index=True)
        output_path = output_dir / "focos_br_2024.parquet"
        df_final.to_parquet(output_path, index=False)

        print(f"\nArquivo salvo em: {output_path}")
        print(f"Total de registros: {len(df_final):,}")
        print(f"Biomas incluídos: {BIOMAS}")
        print(f"Distribuição por bioma:\n{df_final['bioma'].value_counts()}")
    else:
        print("\nNenhum dado foi baixado. Verifique sua conexão.")


if __name__ == "__main__":
    main()