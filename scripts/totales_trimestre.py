#!/usr/bin/env python3
"""
aggregate_quarter_totals_raw.py
================================
Lee los Parquet granulares (ene-*.parquet) y construye un resumen con una sola
fila por año-trimestre.  Todas las reglas de filtrado se definen en un único
diccionario `RULES`, de modo que añadir o ajustar categorías futuras sea
sencillo y consistente.

Indicadores generados
---------------------
personas_ocupadas
personas_desocupadas
personas_fuera_fuerza_trabajo
personas_edad_trabajar
oc_hombres, oc_mujeres, oc_chile, oc_extranjero
oc_formal, oc_informal, oc_tpi
oc_sector_publico, oc_no_sector_publico
oc_ed_sup, oc_ed_media, oc_ed_basica, oc_sin_ed_basica
"""

from __future__ import annotations
import pathlib, glob, sys
import pandas as pd, numpy as np
import pyarrow.parquet as pq     

ROOT       = pathlib.Path(__file__).resolve().parents[1]
PROCESSED  = ROOT / "data" / "processed"
OUTFILE    = PROCESSED / "ene_totales_trimestre.parquet"

def read_frames() -> list[pd.DataFrame]:
    pattern = str(PROCESSED / "ene-*.parquet")
    files   = sorted(glob.glob(pattern))
    if not files:
        raise SystemExit("No se encuentran Parquet granulares.")

    base_cols = [
        "ano_trimestre", "mes_central", "fact_cal",
        "cae_especifico", "nacionalidad", "edad", "sexo",
        "ocup_form", "tpi", "categoria_ocupacion",
        "nivel", "termino_nivel",
        "b1", "b1_ciuo88",
    ]

    frames = []
    for f in files:
        # ── 1 · obtener sólo los nombres de columna (sin leer datos) ──
        available = set(pq.read_schema(f).names)

        cols_to_read = [c for c in base_cols if c in available]
        df = pd.read_parquet(f, columns=cols_to_read, engine="pyarrow")

        # ── unificar b1_int ───────────────────────────────────────────────
        if "b1" in df.columns and df["b1"].notna().any():
            df["b1_int"] = pd.to_numeric(df["b1"], errors="coerce").astype("Int64")

        elif "b1_ciuo88" in df.columns and df["b1_ciuo88"].notna().any():
            df["b1_int"] = pd.to_numeric(df["b1_ciuo88"], errors="coerce").astype("Int64")

        else:
            df["b1_int"] = pd.Series(pd.NA, index=df.index, dtype="Int64")
        # ─────────────────────────────────────────────────────────────────

        # sexo a entero por si viene como string
        if df["sexo"].dtype != "Int64":
            df["sexo"] = pd.to_numeric(df["sexo"], errors="coerce").astype("Int64")

        frames.append(df)

    return frames

# ───────────────────────────── rule helpers
def rule_ocupados(df):          # 1 – 7
    return df["cae_especifico"].between(1, 7)

def rule_desocupados(df):       # 8 – 9
    return df["cae_especifico"].between(8, 9)

def rule_fuera_fuerza(df):
    return ~(df["cae_especifico"].between(1, 9))

def rule_edad_trabajar(df):
    return df["edad"] >= 15

def rule_hombres(df):
    return rule_ocupados(df) & (df["sexo"] == 1)

def rule_mujeres(df):
    return rule_ocupados(df) & (df["sexo"] == 2)

def rule_chile(df):
    return rule_ocupados(df) & (df["nacionalidad"] == 152)

def rule_extranjero(df):
    return rule_ocupados(df) & (df["nacionalidad"] != 152)

def rule_formal(df):
    return rule_ocupados(df) & (df["ocup_form"] == 1)

def rule_informal(df):
    return rule_ocupados(df) & (df["ocup_form"] == 2)

def rule_tpi(df):
    return rule_ocupados(df) & (df["tpi"] == 1)

def rule_sector_publico(df):
    return rule_ocupados(df) & (df["categoria_ocupacion"] == 4)

def rule_no_sector_publico(df):
    return rule_ocupados(df) & (df["categoria_ocupacion"] != 4)

# ── educación
def _mask_sin_basica(df):
    n, t = df["nivel"], df["termino_nivel"]
    return ((n == 3) & (t != 1)) | (~n.between(3, 14))

def _mask_ed_basica(df):
    n, t = df["nivel"], df["termino_nivel"]
    return (((n == 3) & (t == 1)) |
            (n.isin([4, 5, 6, 14]) & (t != 1)))

def _mask_ed_media(df):
    n, t = df["nivel"], df["termino_nivel"]
    return (((n.between(4, 6) | (n == 14)) & (t == 1)) |
            (n.between(7, 9) & (t != 1)))

def _mask_ed_sup(df):
    n, t = df["nivel"], df["termino_nivel"]
    return ((n.between(7, 9) & (t == 1)) | n.between(10, 12))

def _mask_ed_sup_cft(df):
    n, t = df["nivel"], df["termino_nivel"]
    return ((n ==7) & (t == 1)) 

def _mask_ed_sup_ip(df):
    n, t = df["nivel"], df["termino_nivel"]
    return ((n ==8) & (t == 1)) 

def _mask_ed_sup_univ(df):
    n, t = df["nivel"], df["termino_nivel"]
    return ((n ==9) & (t == 1)) | n.between(10, 12)

def rule_sin_basica(df):
    return rule_ocupados(df) & _mask_sin_basica(df)

def rule_ed_basica(df):
    return rule_ocupados(df) & _mask_ed_basica(df)

def rule_ed_media(df):
    return rule_ocupados(df) & _mask_ed_media(df)

def rule_ed_sup(df):
    return rule_ocupados(df) & _mask_ed_sup(df)

def rule_ed_sup_cft(df):
    return rule_ocupados(df) & _mask_ed_sup_cft(df)

def rule_ed_sup_ip(df):
    return rule_ocupados(df) & _mask_ed_sup_ip(df)

def rule_ed_sup_univ(df):
    return rule_ocupados(df) & _mask_ed_sup_univ(df)

# ─── Calificación ocupacional (siempre entre personas ocupadas) ────────
def rule_alta_calificacion(df):
    return rule_ocupados(df) & df["b1_int"].between(1, 3)

def rule_calif_media_baja(df):
    return rule_ocupados(df) & df["b1_int"].between(4, 9)

def rule_calif_media(df):
    return rule_ocupados(df) & df["b1_int"].between(4, 8)

def rule_calif_baja(df):
    return rule_ocupados(df) & (df["b1_int"] == 9)

def rule_otra_calificacion(df):
    return rule_ocupados(df) & ~df["b1_int"].between(1, 9)

# ─── Educación superior completa + calificación ────────────────────────
_mask_ed_sup = _mask_ed_sup  # ya estaba definido arriba

def rule_ed_sup_compet_alta(df):
    return _mask_ed_sup(df) & rule_alta_calificacion(df)

def rule_ed_sup_compet_media_baja(df):
    return _mask_ed_sup(df) & df["b1_int"].between(4, 9)

def rule_ed_sup_compet_no_alta(df):
    return _mask_ed_sup(df) & ~df["b1_int"].between(1, 3)

def rule_test_b1_ciuo88(df):
    return _mask_ed_sup(df) & ~df["b1_ciuo88"].between(1, 3)


# ───────────────────────────── rule registry
RULES: dict[str, callable] = {
    # población total
    "personas_ocupadas"             : rule_ocupados,
    "personas_desocupadas"          : rule_desocupados,
    "personas_fuera_fuerza_trabajo" : rule_fuera_fuerza,
    "personas_edad_trabajar"        : rule_edad_trabajar,
    # ocupados sexo / país
    "oc_hombres"            : rule_hombres,
    "oc_mujeres"            : rule_mujeres,
    "oc_chile"              : rule_chile,
    "oc_extranjero"         : rule_extranjero,
    # formalidad, TPI, sector
    "oc_formal"             : rule_formal,
    "oc_informal"           : rule_informal,
    "oc_tpi"                : rule_tpi,
    "oc_sector_publico"     : rule_sector_publico,
    "oc_no_sector_publico"  : rule_no_sector_publico,
    # educación
    "oc_sin_ed_basica"      : rule_sin_basica,
    "oc_ed_basica"          : rule_ed_basica,
    "oc_ed_media"           : rule_ed_media,
    "oc_ed_sup"             : rule_ed_sup,
    "oc_ed_sup_cft"         : rule_ed_sup_cft,
    "oc_ed_sup_ip"          : rule_ed_sup_ip,
    "oc_ed_sup_univ"        : rule_ed_sup_univ,

    # calificación de la ocupación
    "oc_calif_alta"          : rule_alta_calificacion,
    "oc_calif_media_baja"    : rule_calif_media_baja,
    "oc_calif_media"         : rule_calif_media,
    "oc_calif_baja"          : rule_calif_baja,
    "oc_otra_calificacion"   : rule_otra_calificacion,

    # educación sup + calificación
    "oc_ed_sup_compet_alta"       : rule_ed_sup_compet_alta,
    "oc_ed_sup_compet_media_baja" : rule_ed_sup_compet_media_baja,
    "oc_ed_sup_compet_no_alta"    : rule_ed_sup_compet_no_alta,

    # test b1_ciuo88
    "oc_test_b1_ciuo88"           : rule_test_b1_ciuo88,
}

# ───────────────────────────── aggregation
def aggregate(df: pd.DataFrame) -> pd.DataFrame:
    # calcula todas las máscaras una sola vez
    masks = {k: fn(df) for k, fn in RULES.items()}

    agg_dict = {
        name: ("fact_cal", lambda s, m=mask: s[m.loc[s.index]].sum())
        for name, mask in masks.items()
    }

    grouped = (
        df.groupby(["ano_trimestre", "mes_central"], dropna=False, observed=True)
          .agg(**agg_dict)
          .reset_index()
          .sort_values(["ano_trimestre", "mes_central"])
    )
    return grouped


# ───────────────────────────── main
def main() -> None:
    frames   = read_frames()
    df       = pd.concat(frames, ignore_index=True)
    resumen  = aggregate(df)

    # redondeo + Int64
    count_cols = [c for c in resumen.columns if c.startswith(("personas_", "oc_"))]
    resumen[count_cols] = (
        resumen[count_cols]
        .round(0)
        .astype("Int64")
    )

    resumen.to_parquet(OUTFILE, index=False, engine="pyarrow")

    # ─── extra: CSV copy ──────────────────────────────────────────────
    csv_path = OUTFILE.with_suffix(".csv")          # ene_totales_trimestre.csv
    resumen.to_csv(csv_path, index=False)
    # -----------------------------------------------------------------

    print(
        f"✔ Guardado {OUTFILE} y {csv_path}  "
        f"({len(resumen)} filas)"
    )


if __name__ == "__main__":
    sys.exit(main())
