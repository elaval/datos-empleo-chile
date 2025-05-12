#!/usr/bin/env python3
import warnings
# ── silenciar *una vez* el único FutureWarning ruidoso ────────────────
warnings.filterwarnings(
    "ignore",
    message="The behavior of DataFrame concatenation with empty or all-NA entries is deprecated",
    category=FutureWarning,
)

import pathlib, pandas as pd
import yaml, re, sys

RAW     = pathlib.Path(__file__).parents[1] / "data" / "raw" / "ine"
PROCESSED = pathlib.Path(__file__).parents[1] / "data" / "processed"
CFG     = yaml.safe_load(open(pathlib.Path(__file__).parents[1] / "config" / "columns.yml"))

def trimester_code(filename: str) -> str:
    # ene-2025-02-efm.csv → "02-efm"
    parts = filename.split("-")[2:4]
    return "-".join(parts).split(".")[0]

def preprocess(df: pd.DataFrame) -> pd.DataFrame:
    if "fact_cal" in df.columns:
        df["fact_cal"] = (
            df["fact_cal"].astype(str).str.replace(",", ".", regex=False).astype(float)
        )
    return df

def main():
    PROCESSED.mkdir(parents=True, exist_ok=True)
    buckets = dict()

    for csv in RAW.glob("*.csv"):
        tri = trimester_code(csv.name)
        df = pd.read_csv(
            csv,
            sep=";",
            encoding="latin-1",
            low_memory=False,
            usecols=lambda c: c in CFG["subset_columns"]      # ← lee sólo las que existan
        )
        # ❶ aseguramos que TODAS las columnas de la lista aparezcan
        missing = set(CFG["subset_columns"]) - set(df.columns)
        for col in missing:
            df[col] = pd.Series(pd.NA, index=df.index, dtype="string")
 
        # ❷ reordenamos en el orden del YAML
        df = df.reindex(columns=CFG["subset_columns"])

        df  = preprocess(df)
        buckets.setdefault(tri, []).append(df)

    for tri, frames in buckets.items():
        out = pd.concat(frames, ignore_index=True)
        out.to_parquet(PROCESSED / f"ene-{tri}.parquet")
        print(f"Wrote {tri}: {len(out):,} filas")

if __name__ == "__main__":
    sys.exit(main())
