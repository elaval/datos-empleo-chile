#!/usr/bin/env python3
"""
Genera un panel sintético por trimestre con las siguientes reglas:

* ocupacion    = 1-7  → “ocupados”, 8-9 → “desocupados”, otro → “otro”
* nacionalidad = 152  → “Chilena”,  todo lo demás → “Extranjeros”
* edad_de_trabajar = 1 si edad ≥ 15, 0 en otro caso
* Se rellenan NaN en claves numéricas con -1 para agregación; luego se
  restauran a NA (Int64) tras el groupby.
"""

from __future__ import annotations
import pandas as pd, numpy as np, glob, pathlib, yaml, sys

# ──────────────────────────────────────────────────────────── paths / cfg
PROCESSED   = pathlib.Path(__file__).parents[1] / "data" / "processed"
CFG         = yaml.safe_load(open(pathlib.Path(__file__).parents[1] /
                                  "config" / "columns.yml"))

# Dimensiones finales (puedes moverlas a columns.yml si quieres mantener en un sitio)
KEY_DIMS = [
    "ano_trimestre", "mes_central", "ocupacion", "nacionalidad",
    "categoria_ocupacion", "b14_rev4cl_caenes", "b1",
    "ocup_form", "sector", "edad_de_trabajar", "sexo"
]

# Columnas numéricas a las que colocar placeholder -1 para el groupby
INT_COLS = ["categoria_ocupacion", "b14_rev4cl_caenes", "b1",
            "ocup_form", "sector"]

# ────────────────────────────────────────────────────────────── pipeline
def build_panel() -> pd.DataFrame:
    files = glob.glob(str(PROCESSED / "ene-*.parquet"))
    df    = pd.concat(map(pd.read_parquet, files), ignore_index=True)

    # Derivadas
    df["ocupacion"] = np.select(
        [df["cae_especifico"].between(1, 7, inclusive="both"),
         df["cae_especifico"].between(8, 9, inclusive="both")],
        ["ocupados", "desocupados"],
        default="otro"
    )

    df["nacionalidad"] = np.where(df["nacionalidad"] == 152,
                                  "chilena", "extranjeros")

    df["edad_de_trabajar"] = (df["edad"] >= 15).astype(int)

    # Limpieza para groupby: rellenar NaN con -1 en columnas int
    df[INT_COLS] = df[INT_COLS].fillna(-1).astype(int)
    df["sexo"]   = df["sexo"].fillna("otro").astype(str)

    # Agrupación
    agg = (df
        .groupby(KEY_DIMS, dropna=False, observed=False)["fact_cal"]
        .sum()
        .reset_index()
    )

    # Restaurar NaN y dtypes “Int64” que permiten NA
    for col in INT_COLS:
        agg[col] = agg[col].replace(-1, pd.NA).astype("Int64")

    return agg

def main() -> None:
    out_file = PROCESSED / "ene_sintetica.parquet"
    panel = build_panel()
    panel.to_parquet(out_file, index=False)
    print(f"Guardado {out_file}  ({len(panel):,} filas)")

if __name__ == "__main__":
    sys.exit(main())
