# generar_series_mensuales_simplificadas.py
#!/usr/bin/env python3
"""
generar_series_mensuales_simplificadas.py
========================================
Lee el CSV simplificado integrado y crea un CSV por cada mes central,
facilitando comparaciones año a año.
"""

import pathlib, sys
import pandas as pd
from scripts._column_defs import PUBLIC_COLS, SUFIJOS

# rutas base
ROOT = pathlib.Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"
AGREGADOS_INTEGRADO = PROCESSED / "agregados" / "integrado"
OUT_DIR = PROCESSED / "agregados" / "por_mes_simplificado"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# archivo simplificado integrado
SIMPL_CSV = AGREGADOS_INTEGRADO / "ene_trimestre_totales_simplificados.csv"

def main() -> None:
    df = pd.read_csv(SIMPL_CSV)
    for m in sorted(df["mes_central"].unique()):
        suf = SUFIJOS[int(m)]
        dfm = df[df["mes_central"] == m].reset_index(drop=True)
        # reordenar columnas según PUBLIC_COLS
        cols_final = [new for old, new in PUBLIC_COLS if new in dfm.columns]
        dfm = dfm[cols_final]
        fname = f"ene-{int(m):02d}-{suf}.csv"
        path = OUT_DIR / fname
        dfm.to_csv(path, index=False)
        print(f"✓ {fname:18} → {len(dfm)} filas")

if __name__ == "__main__":
    sys.exit(main())