#!/usr/bin/env python3
"""
Genera 12 CSV (y opcionalmente Parquet) con el patrón
   ene-XXXX-<mes_central>-<sufijo>.csv
pero sin el año (p. ej.  ene--02-efm.csv).
Así el código coincide con los nombres originales de INE.
"""

from __future__ import annotations
import pathlib, sys
import pandas as pd

ROOT = pathlib.Path(__file__).parents[1]
PROCESSED = ROOT / "data" / "processed"
SRC = PROCESSED / "ene_totales_trimestre.parquet"
OUT_DIR = PROCESSED / "series_por_mes"
OUT_DIR.mkdir(exist_ok=True)

SUFIJOS = {
    1: "def", 2: "efm", 3: "fma", 4: "mam",
    5: "amj", 6: "mjj", 7: "jja", 8: "jas",
    9: "aso", 10: "son", 11: "ond", 12: "nde",
}

def main() -> None:
    if not SRC.exists():
        raise SystemExit("Ejecute primero totales_trimestre.py para crear el Parquet base.")

    df = pd.read_parquet(SRC, engine="pyarrow")

    for m in sorted(df["mes_central"].unique()):
        suf = SUFIJOS.get(int(m), f"m{int(m):02d}")
        serie = (
            df[df["mes_central"] == m]
              .sort_values("ano_trimestre")
              .reset_index(drop=True)
        )

        stem = f"ene--{int(m):02d}-{suf}"
        csv_path = OUT_DIR / f"{stem}.csv"
        serie.to_csv(csv_path, index=False)

        # Parquet opcional: descomenta la línea siguiente
        # serie.to_parquet(csv_path.with_suffix(".parquet"), index=False)

        print(f"✓ {csv_path.name:18}  {len(serie)} registros")

if __name__ == "__main__":
    sys.exit(main())
