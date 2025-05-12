#!/usr/bin/env python3
"""
aggregate_quarter_totals_raw.py
================================
Lee los Parquet granulares (ene-*.parquet) y construye un resumen con una sola
fila por año-trimestre.  Todas las reglas de filtrado se definen en un único
diccionario `RULES`, de modo que añadir o ajustar categorías futuras sea
sencillo y consistente.

Además calcula promedios de horas ponderadas.
"""

from __future__ import annotations
import pathlib, glob, sys
import pandas as pd, numpy as np
import pyarrow.parquet as pq    
from _column_defs import PUBLIC_COLS, SUFIJOS


ROOT       = pathlib.Path(__file__).resolve().parents[1]
PROCESSED  = ROOT / "data" / "processed"
# base para los totales
OUTFILE_BASE = PROCESSED / "ene_trimestre_totales"

# archivo parquet + su CSV “completo”
OUTFILE_PARQUET = OUTFILE_BASE.with_suffix(".parquet")
OUTFILE_CSV     = OUTFILE_BASE.with_suffix(".csv")

# CSV simplificado para público general
OUTFILE_SIMPLIFICADO = PROCESSED / "ene_trimestre_totales_simplificados.csv"


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
        "obe","id","ftp","habituales","efectivas","activ",
    ]

    frames = []
    for f in files:
        available = set(pq.read_schema(f).names)
        cols_to_read = [c for c in base_cols if c in available]
        df = pd.read_parquet(f, columns=cols_to_read, engine="pyarrow")

        # unificar ciuo_gran_grupo
        ciuo = pd.Series(pd.NA, index=df.index, dtype="Int64")
        if "b1_ciuo88" in df.columns:
            ciuo = pd.to_numeric(df["b1_ciuo88"], errors="coerce").astype("Int64")
        if "b1" in df.columns:
            new = pd.to_numeric(df["b1"], errors="coerce").astype("Int64")
            ciuo = new.combine_first(ciuo)
        df["ciuo_gran_grupo"] = ciuo

        # sexo a Int64
        if df["sexo"].dtype != "Int64":
            df["sexo"] = pd.to_numeric(df["sexo"], errors="coerce").astype("Int64")

        frames.append(df)
    return frames

# ───────────────────────────── rule helpers
def rule_ocupados(df):          return df["cae_especifico"].between(1, 7)
def rule_desocupados(df):       return df["cae_especifico"].between(8, 9)
def rule_edad_trabajar(df):     return df["edad"] >= 15
def rule_hombres(df):           return rule_ocupados(df) & (df["sexo"] == 1)
def rule_mujeres(df):           return rule_ocupados(df) & (df["sexo"] == 2)
def rule_chile(df):             return rule_ocupados(df) & (df["nacionalidad"] == 152)
def rule_extranjero(df):        return rule_ocupados(df) & (df["nacionalidad"] != 152)
def rule_formal(df):            return rule_ocupados(df) & (df["ocup_form"] == 1)
def rule_informal(df):          return rule_ocupados(df) & (df["ocup_form"] == 2)
def rule_tpi(df):               return rule_ocupados(df) & (df["tpi"] == 1)
def rule_sector_publico(df):    return rule_ocupados(df) & (df["categoria_ocupacion"] == 4)
def rule_no_sector_publico(df): return rule_ocupados(df) & (df["categoria_ocupacion"] != 4)

def _mask_sin_basica(df):
    n,t = df["nivel"], df["termino_nivel"]
    return ((n == 3)&(t != 1)) | (~n.between(3,14))
def _mask_ed_basica(df):
    n,t = df["nivel"], df["termino_nivel"]
    return ((n == 3)&(t == 1)) | (n.isin([4,5,6,14])&(t != 1))
def _mask_ed_media(df):
    n,t = df["nivel"], df["termino_nivel"]
    return ((n.between(4,6)|(n==14))&(t==1)) | (n.between(7,9)&(t !=1))
def _mask_ed_sup(df):
    n,t = df["nivel"], df["termino_nivel"]
    return (n.between(7,9)&(t==1)) | n.between(10,12)

def rule_sin_basica(df):      return rule_ocupados(df) & _mask_sin_basica(df)
def rule_ed_basica(df):       return rule_ocupados(df) & _mask_ed_basica(df)
def rule_ed_media(df):        return rule_ocupados(df) & _mask_ed_media(df)
def rule_ed_sup(df):          return rule_ocupados(df) & _mask_ed_sup(df)
def rule_ed_sup_cft(df):      return rule_ocupados(df) & (df["nivel"]==7)&(df["termino_nivel"]==1)
def rule_ed_sup_ip(df):       return rule_ocupados(df) & (df["nivel"]==8)&(df["termino_nivel"]==1)
def rule_ed_sup_univ(df):     return rule_ocupados(df) & (((df["nivel"]==9)&(df["termino_nivel"]==1))|df["nivel"].between(10,12))

def rule_ciuo_alta(df):       return rule_ocupados(df) & df["ciuo_gran_grupo"].between(1,3)
def rule_ciuo_media_baja(df): return rule_ocupados(df) & df["ciuo_gran_grupo"].between(4,9)
def rule_ciuo_media(df):      return rule_ocupados(df) & df["ciuo_gran_grupo"].between(4,8)
def rule_ciuo_baja(df):       return rule_ocupados(df) & (df["ciuo_gran_grupo"]==9)
def rule_ciuo_otras(df):      return rule_ocupados(df) & ~df["ciuo_gran_grupo"].between(1,9)

def rule_ed_sup_ciuo_alta(df):       return _mask_ed_sup(df) & df["ciuo_gran_grupo"].between(1,3)
def rule_ed_sup_ciuo_media_baja(df): return _mask_ed_sup(df) & df["ciuo_gran_grupo"].between(4,9)
def rule_ed_sup_ciuo_no_alta(df):    return _mask_ed_sup(df) & ~df["ciuo_gran_grupo"].between(1,3)

def rule_obe(df):       return df["obe"] == 1
def rule_id(df):        return df["id"] == 1
def rule_ftp(df):       return df["ftp"] == 1

def rule_habituales(df): return df.get("habituales",0) > 0
def rule_efe1(df):      return df.get("efectivas",0).between(1,168)&(df.get("activ",0)==1)
def rule_efe2(df):      return df.get("efectivas",0) > 0

def rule_horas_1_30(df):
    #  1 ≤ x ≤ 30
    return rule_ocupados(df) & df["efectivas_clean"].between(1, 30, inclusive="both")

def rule_horas_31_44(df):
    # 31 ≤ x ≤ 44
    return rule_ocupados(df) & df["efectivas_clean"].between(31, 44, inclusive="both")

def rule_horas_31_39(df):
    # 31 ≤ x ≤ 39
    return rule_ocupados(df) & df["efectivas_clean"].between(31, 39, inclusive="both")

def rule_horas_40(df):
    # exactly 40
    return rule_ocupados(df) & (df["efectivas_clean"] == 40)

def rule_horas_41_44(df):
    # 41 ≤ x ≤ 44
    return rule_ocupados(df) & df["efectivas_clean"].between(41, 44, inclusive="both")

def rule_horas_45(df):
    # exactly 45
    return rule_ocupados(df) & (df["efectivas_clean"] == 45)

def rule_horas_46_mas(df):
    # x ≥ 46
    return rule_ocupados(df) & (df["efectivas_clean"] >= 46)

def rule_edad_15_24(df):
    # 15 ≤ edad ≤ 24
    return rule_ocupados(df) & df["edad"].between(15, 24, inclusive="both")

def rule_edad_25_34(df):
    # 25 ≤ edad ≤ 34
    return rule_ocupados(df) & df["edad"].between(25, 34, inclusive="both")

def rule_edad_35_44(df):
    return rule_ocupados(df) & df["edad"].between(35, 44, inclusive="both")

def rule_edad_45_54(df):
    return rule_ocupados(df) & df["edad"].between(45, 54, inclusive="both")

def rule_edad_55_64(df):
    return rule_ocupados(df) & df["edad"].between(55, 64, inclusive="both")

def rule_edad_65_mas(df):
    # edad ≥ 65
    return rule_ocupados(df) & (df["edad"] >= 65)


RULES: dict[str, callable] = {
    "personas_ocupadas": rule_ocupados,
    "personas_desocupadas": rule_desocupados,
    "personas_edad_trabajar": rule_edad_trabajar,
    "oc_hombres": rule_hombres,
    "oc_mujeres": rule_mujeres,
    "oc_chile": rule_chile,
    "oc_extranjero": rule_extranjero,
    "oc_formal": rule_formal,
    "oc_informal": rule_informal,
    "oc_tpi": rule_tpi,
    "oc_sector_publico": rule_sector_publico,
    "oc_no_sector_publico": rule_no_sector_publico,
    "oc_sin_basica_completa": rule_sin_basica,
    "oc_ed_basica_complet": rule_ed_basica,
    "oc_ed_media_completa": rule_ed_media,
    "oc_ed_sup_completa": rule_ed_sup,
    "oc_ed_sup_cft": rule_ed_sup_cft,
    "oc_ed_sup_ip": rule_ed_sup_ip,
    "oc_ed_sup_univ": rule_ed_sup_univ,
    "oc_ciuo_alta": rule_ciuo_alta,
    "oc_ciuo_media_baja": rule_ciuo_media_baja,
    "oc_ciuo_media": rule_ciuo_media,
    "oc_ciuo_baja": rule_ciuo_baja,
    "oc_ciuo_otras": rule_ciuo_otras,
    "oc_ed_sup_ciuo_alta": rule_ed_sup_ciuo_alta,
    "oc_ed_sup_ciuo_media_baja": rule_ed_sup_ciuo_media_baja,
    "oc_ed_sup_ciuo_no_alta": rule_ed_sup_ciuo_no_alta,
    "oc_obe": rule_obe,
    "oc_id": rule_id,
    "oc_ftp": rule_ftp,
    "oc_hab": rule_habituales,
    "oc_efe1": rule_efe1,
    "oc_efe2": rule_efe2,
    "horas_1_30":    rule_horas_1_30,
    "horas_31_44":   rule_horas_31_44,
    "horas_31_39":   rule_horas_31_39,
    "horas_40":      rule_horas_40,
    "horas_41_44":   rule_horas_41_44,
    "horas_45":      rule_horas_45,
    "horas_46_mas":  rule_horas_46_mas,
    "oc_edad_15_24": rule_edad_15_24,
    "oc_edad_25_34": rule_edad_25_34,
    "oc_edad_35_44": rule_edad_35_44,
    "oc_edad_45_54": rule_edad_45_54,
    "oc_edad_55_64": rule_edad_55_64,
    "oc_edad_65_mas": rule_edad_65_mas,

}

def aggregate(df: pd.DataFrame) -> pd.DataFrame:
    masks = {k: fn(df) for k, fn in RULES.items()}
    agg_dict = {
        name: ("fact_cal", lambda s, m=mask: s[m.loc[s.index]].sum())
        for name, mask in masks.items()
    }
    return (
        df.groupby(["ano_trimestre", "mes_central"], dropna=False, observed=True)
          .agg(**agg_dict)
          .reset_index()
          .sort_values(["ano_trimestre", "mes_central"])
    )

def main() -> None:
    frames = read_frames()
    df = pd.concat(frames, ignore_index=True)
    # Cálculos de horas ponderadas
    # limpiar códigos especiales
    df["efectivas_clean"] = df["efectivas"].replace({888: 0, 999: 0})

    resumen = aggregate(df)
    
    # efe1
    mask1 = df["efectivas_clean"].between(1,168)&(df["activ"]==1)
    df["efe1_horas_pond"] = df["efectivas_clean"].where(mask1,0)*df["fact_cal"]
    # efe2
    mask2 = df["efectivas_clean"]>0
    df["efe2_horas_pond"] = df["efectivas_clean"].where(mask2,0)*df["fact_cal"]
    # habituales
    df["hab_horas_pond"] = df["habituales"].fillna(0)*df["fact_cal"]

    horas = (
        df.groupby(["ano_trimestre","mes_central"])
          .agg(
            efe1_total = ("efe1_horas_pond","sum"),
            efe2_total = ("efe2_horas_pond","sum"),
            hab_total  = ("hab_horas_pond","sum"),
          )
          .reset_index()
    )

    resumen = resumen.merge(horas, on=["ano_trimestre","mes_central"])

    # renombra conteos
    resumen["pet"] = resumen["personas_edad_trabajar"]
    resumen["fdt"] = resumen["personas_ocupadas"] + resumen["personas_desocupadas"]
    resumen["fft"] = resumen["personas_edad_trabajar"] - resumen["fdt"]

    resumen["oc"]  = resumen["personas_ocupadas"]
    resumen["des"] = resumen["personas_desocupadas"]
    resumen.rename(columns={
        "oc_id":"id", "oc_obe":"obe", "oc_ftp":"ftp",
        "oc_efe1":"efe1","oc_efe2":"efe2","oc_hab":"habituales_sum"
    }, inplace=True)
    resumen["tpi"] = resumen["oc_tpi"]
    resumen["oi"]  = resumen["oc_informal"]
    resumen["osi"] = resumen["oc_sector_publico"]
    resumen["fta"] = resumen["fdt"] + resumen["id"] + resumen["ftp"]

    # Tasas
    def safe_div(n,d): return (n/d*100).round(2)
    resumen["td"]  = safe_div(resumen["des"],resumen["fdt"])
    resumen["to"]  = safe_div(resumen["oc"],resumen["pet"])
    resumen["tp"]  = safe_div(resumen["fdt"],resumen["pet"])
    resumen["tpl"] = safe_div(resumen["id"]+resumen["obe"]+resumen["des"],resumen["fdt"]+resumen["id"])
    resumen["su1"] = safe_div(resumen["des"]+resumen["id"],resumen["fdt"]+resumen["id"])
    resumen["su2"] = safe_div(resumen["des"]+resumen["id"]+resumen["tpi"],resumen["fdt"]+resumen["id"])
    resumen["su3"] = safe_div(resumen["des"]+resumen["id"]+resumen["ftp"],resumen["fta"])
    resumen["su4"] = safe_div(resumen["des"]+resumen["id"]+resumen["tpi"]+resumen["ftp"],resumen["fta"])
    resumen["toi"]  = safe_div(resumen["oi"],resumen["oc"])
    resumen["tosi"] = safe_div(resumen["osi"],resumen["oc"])

    # Promedios reales de horas
    resumen["promedio_horas_efectivas_presente"] = (resumen["efe1_total"]/resumen["oc"]).round(1)
    resumen["promedio_horas_efectivas_total"]   = (resumen["efe2_total"]/resumen["oc"]).round(1)
    resumen["promedio_horas_habituales"]        = (resumen["hab_total"]/resumen["oc"]).round(1)

    # eliminar intermedias
    resumen.drop(columns=["efe1_total","efe2_total","hab_total"], inplace=True)

    # Exportar
    resumen.to_parquet(OUTFILE_PARQUET, index=False, engine="pyarrow")
    resumen.to_csv(   OUTFILE_CSV,     index=False)
    print(f"✔ Guardado {OUTFILE_PARQUET} y {OUTFILE_CSV}  ({len(resumen)} filas)")

    lite = resumen.copy()
    orig = set(lite.columns)

    # Rename & reorder
    for old, new in PUBLIC_COLS:
        if old in orig:
            lite.rename(columns={old: new}, inplace=True)
    cols_final = [new for old, new in PUBLIC_COLS if old in orig]
    lite = lite[cols_final]

    # 1) pick out the count columns
    cols = lite.columns
    mask_counts = (
        ~cols.isin(["ano_trimestre", "mes_central"]) &
        ~cols.str.startswith(("tasa_", "promedio_"))
    )
    count_cols = cols[mask_counts]

    # 2) round and cast to Int64
    lite.loc[:, count_cols] = (
        lite[count_cols]
        .round(0)
        .astype("Int64")
    )

    # 3) write it out
    lite.to_csv(OUTFILE_SIMPLIFICADO, index=False)
    print(f"✔ CSV público listo: {OUTFILE_SIMPLIFICADO.name}")

    # -- 4) Generar series por mes (reutilizando lite ya renombrado)
    serie_dir = PROCESSED / "series_por_mes"
    serie_dir.mkdir(exist_ok=True)

    for m in sorted(lite["mes_central"].unique()):
        suf  = SUFIJOS[int(m)]
        dfm  = lite[lite["mes_central"] == m]

        # ---- CORRECCIÓN: uso de los nombres "new" para reordenar
        cols_final = [ new for _old,new in PUBLIC_COLS if new in dfm.columns ]
        dfm = dfm[cols_final]

        nombre   = f"ene-{int(m):02d}-{suf}.csv"
        path_csv = serie_dir / nombre
        dfm.to_csv(path_csv, index=False)
        print(f"✓ {nombre:18} → {len(dfm)} filas")

if __name__ == "__main__":
    sys.exit(main())
