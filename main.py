import sys
from pathlib import Path

# Adiciona src/ ao path
sys.path.append(str(Path(__file__).resolve().parent / "src"))

from extract    import main as extract
from transform  import main as transform
from elbow      import main as elbow
from sample     import main as sample
from profiling  import main as profiling
from eda        import main as eda

# ====== Pipeline =============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("PIPELINE — Focos de Queimadas Brasil 2024")
    print("=" * 60)

    etapas = [
        ("1. Extração dos dados",              extract),
     #  ("2. Amostra dos dados brutos",        sample_raw),
        ("2. Transformação dos dados",         transform),
        ("3. Método do Cotovelo (k-means)",    elbow),
        ("4. Amostra estratificada (k-means)", sample),
        ("5. Profiling",                       profiling),
        ("6. Análise exploratória (EDA)",      eda),
    ]

    for descricao, funcao in etapas:
        print(f"\n{descricao}")
        print("-" * 60)
        funcao()

    print("\n" + "=" * 60)
    print("Pipeline concluído com sucesso!")
    print("=" * 60)