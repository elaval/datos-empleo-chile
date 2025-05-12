#!/usr/bin/env python3
"""
construir_panel_encuestados.py
================================
Lee los CSV raw publicados por el INE y los agrupa por trimestre móvil
(con mes central), creando un archivo Parquet con microdatos por trimestre.

Cada archivo se guarda en data/processed/microdatos/ene-<MM>-<sufijo>.parquet
"""

import warnings
# Silenciar el único FutureWarning ruidoso
warnings.filterwarnings(
    "ignore",
    message="The behavior of DataFrame concatenation with empty or all-NA entries is deprecated",
    category=FutureWarning,
)

import pathlib
import pandas as pd
import yaml
import sys

# Rutas
BASE_DIR       = pathlib.Path(__file__).resolve().parents[1]
RAW            = BASE_DIR / "data" / "raw" / "ine"
PROCESSED      = BASE_DIR / "data" / "processed"
MICRODATA_DIR  = PROCESSED / "microdatos"
CONFIG_PATH    = BASE_DIR / "config" / "columns.yml"

# Definición de columnas a leer (subset_columns) y orden en el YAML
CFG = yaml.safe_load(open(CONFIG_PATH, encoding="utf-8"))

def trimester_code(filename: str) -> str:
    """
    Dada una filename tipo 'ene-2025-02-efm.csv', devuelve '02-efm'
    """
    parts = filename.split("-")[2:4]
    return "-".join(parts).split(".")[0]

def preprocess(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normaliza fact_cal: reemplaza coma por punto y a float.
    """
    if "fact_cal" in df.columns:
        df["fact_cal"] = (
            df["fact_cal"]
              .astype(str)
              .str.replace(",", ".", regex=False)
              .astype(float)
        )
    return df

def main() -> None:
    # Crear carpeta de microdatos si no existe
    MICRODATA_DIR.mkdir(parents=True, exist_ok=True)

    # Agrupar DataFrames por código de trimestre
    buckets: dict[str, list[pd.DataFrame]] = {}

    for csv_path in RAW.glob("*.csv"):
        tri = trimester_code(csv_path.name)
        # Leer solo columnas que existan
        df = pd.read_csv(
            csv_path,
            sep=";",
            encoding="latin-1",
            low_memory=False,
            usecols=lambda c: c in CFG["subset_columns"]
        )
        # Asegurar que todas las columnas del YAML estén presentes
        missing = set(CFG["subset_columns"]) - set(df.columns)
        for col in missing:
            df[col] = pd.Series(pd.NA, index=df.index, dtype="string")
        # Reordenar
        df = df.reindex(columns=CFG["subset_columns"])
        # Preprocesar fact_cal
        df = preprocess(df)
        # Acumular en bucket
        buckets.setdefault(tri, []).append(df)

    # Concatenar y guardar un Parquet por cada trimestre móvil
    for tri, frames in buckets.items():
        out = pd.concat(frames, ignore_index=True)
        output_path = MICRODATA_DIR / f"ene-{tri}.parquet"
        out.to_parquet(output_path, index=False, engine="pyarrow")
        print(f"✔ Guardado microdatos: {output_path.relative_to(PROCESSED)}  ({len(out):,} filas)")

if __name__ == "__main__":
    sys.exit(main())
