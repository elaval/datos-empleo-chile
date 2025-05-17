#!/usr/bin/env python3
"""
generar_totales_trimestrales.py
================================
Lee los Parquet granulares de microdatos (ene-*.parquet) y construye un resumen
con una sola fila por año-trimestre. Todas las reglas de filtrado están en el
diccionario RULES, de modo que añadir o ajustar categorías futuras sea sencillo.

Además calcula promedios de horas ponderadas y exporta:
 - Parquet técnico:  agregados/integrado/ene_trimestre_totales.parquet
 - CSV técnico:      agregados/integrado/ene_trimestre_totales.csv
 - CSV simplificado: agregados/integrado/ene_trimestre_totales_simplificados.csv
"""
from __future__ import annotations
import pathlib, glob, sys
import pandas as pd
import pyarrow.parquet as pq
from scripts._column_defs import PUBLIC_COLS, SUFIJOS

# Columnas en el orden en que queremos exportar el resumen
FINAL_COLS = [
    "ano_trimestre",
    "mes_central",

    "pet",
    "ft",
    "o",
    "do",
    "cesantes",
    "busca_trabajo_por_primera_vez",
    "fft",
    "fft_iniciadores",
    "fft_inactivos_potencialmente_activos",
    "fft_inactivos_habituales",

    "obe",
    "id",
    "ftp",
    "fta",
    "deseo_trabajar",

    "o_hombres",
    "o_mujeres",
    "o_chile",
    "o_extranjero",
    "o_formal",
    "o_informal",
    "o_sector_informal",
    "o_sin_basica_completa",
    "o_ed_basica_completa",
    "o_ed_media_completa",
    "o_ed_sup_completa",
    "o_ed_sup_cft",
    "o_ed_sup_ip",
    "o_ed_sup_univ",

    "o_ed_sup_ciuo_alta",
    "o_ed_sup_ciuo_media_baja",
    "o_ed_sup_ciuo_no_alta",
    
    "categoria_independientes",
    "categoria_empleador",
    "categoria_cuenta_propia",
    "categoria_familiar_personal_no_remunerado",
    "categoria_dependientes",
    "categoria_asalariados",
    "categoria_asalariado_sector_privado",
    "categoria_asalariado_sector_publico",
    "categoria_servicio_domestico",
    "categoria_serv_domestico_puertas_afuera",
    "categoria_serv_domestico_puertas_adentro",

    "grupo_ciuo_alta",
    "grupo_ciuo_media_baja",
    "grupo_ciuo_media",
    "grupo_ciuo_baja",
    "grupo_ciuo_otras",
    "grupo_ciuo_1",
    "grupo_ciuo_2",
    "grupo_ciuo_3",
    "grupo_ciuo_4",
    "grupo_ciuo_5",
    "grupo_ciuo_6",
    "grupo_ciuo_7",
    "grupo_ciuo_8",
    "grupo_ciuo_9",
    "grupo_ciuo_10",
    "grupo_ciuo_nsnr",

    "rama_1",
    "rama_2",
    "rama_3",
    "rama_4",
    "rama_5",
    "rama_6",
    "rama_7",
    "rama_8",
    "rama_9",
    "rama_10",
    "rama_11",
    "rama_12",
    "rama_13",
    "rama_14",
    "rama_15",
    "rama_16",
    "rama_17",
    "rama_18",
    "rama_19",
    "rama_20",
    "rama_21",

    "horas_1_30",
    "tpi",
    "tpv",
    "tp_sin_declarar_voluntareidad",
    "horas_31_44",
    "horas_31_39",
    "horas_40",
    "horas_41_44",
    "horas_45",
    "horas_46_mas",
    "horas_efectivas_46_mas",
    "o_declaran_horas",

    "promedio_horas_efectivas_sin_ausentes",
    "promedio_horas_efectivas_declaran_horas",
    "promedio_horas_habituales",

    "td",
    "to",
    "tp",
    # resto de tasas y campos…
    "tpl",
    "su1", 
    "su2", 
    "su3", 
    "su4",
    "toi",
    "tosi",
]

# rutas base
ROOT                 = pathlib.Path(__file__).resolve().parents[1]
PROCESSED            = ROOT / "data" / "processed"
MICRODATA_DIR        = PROCESSED / "microdatos"          # aquí van los Parquet de microdatos

AGREGADOS_DIR        = PROCESSED / "agregados"
INTEGRADO_DIR        = AGREGADOS_DIR / "integrado"
INTEGRADO_DIR.mkdir(parents=True, exist_ok=True)

OUTFILE_BASE         = INTEGRADO_DIR / "ene_trimestre_totales"
OUTFILE_PARQUET      = OUTFILE_BASE.with_suffix(".parquet")
OUTFILE_CSV          = OUTFILE_BASE.with_suffix(".csv")
OUTFILE_SIMPLIFICADO = INTEGRADO_DIR / "ene_trimestre_totales_simplificados.csv"


def read_frames() -> list[pd.DataFrame]:
    """Lee todos los Parquet de microdatos y devuelve una lista de DataFrames."""
    pattern = str(MICRODATA_DIR / "ene-*.parquet")
    files = sorted(glob.glob(pattern))
    if not files:
        raise SystemExit(f"No se encuentran Parquet en {MICRODATA_DIR}")

    base_cols = [
        "ano_trimestre", "mes_central", "fact_cal",
        "cae_especifico","cae_general", "nacionalidad", "edad", "sexo",
        "ocup_form","sector", "tpi", "categoria_ocupacion",
        "nivel", "termino_nivel",
        "b1", "b1_ciuo88",
        "obe", "id", "ftp", "deseo_trabajar", "habituales", "efectivas", "activ",
        "c10", "c11",
        "r_p_rev4cl_caenes",

    ]

    frames: list[pd.DataFrame] = []
    for fpath in files:
        schema = pq.read_schema(fpath)
        available = set(schema.names)
        cols_to_read = [c for c in base_cols if c in available]
        df = pd.read_parquet(fpath, columns=cols_to_read, engine="pyarrow")

        # unificar ciuo_gran_grupo
        ciuo = pd.Series(pd.NA, index=df.index, dtype="Int64")
        if "b1_ciuo88" in df:
            ciuo = pd.to_numeric(df["b1_ciuo88"], errors="coerce").astype("Int64")
        if "b1" in df:
            tmp = pd.to_numeric(df["b1"], errors="coerce").astype("Int64")
            ciuo = tmp.combine_first(ciuo)
        df["ciuo_gran_grupo"] = ciuo

        # sexo → Int64
        if df["sexo"].dtype != "Int64":
            df["sexo"] = pd.to_numeric(df["sexo"], errors="coerce").astype("Int64")

        frames.append(df)
    return frames


# ───────────────────────────── rule helpers
def rule_fuerza_de_trabajo(df): return df["cae_especifico"].between(1, 9)
def rule_edad_trabajar(df):     return df["edad"] >= 15
def rule_ocupados(df):          return df["cae_especifico"].between(1, 7)

def rule_desocupados(df):       return df["cae_especifico"].between(8, 9)
def rule_cesantes(df):          return df["cae_especifico"] == 8
def rule_busca_trabajo_por_primera_vez(df): return df["cae_especifico"] == 9

def rule_fuera_fuerza_de_trabajo(df): return df["activ"] == 3
def rule_fft_iniciadores(df): return df["cae_general"] == 6
def rule_fft_inactivos_potencialmente_activos(df): return df["cae_general"].between(7, 8)
def rule_fft_inactivos_habituales(df): return df["cae_general"] == 9

def rule_obe(df):       return df["obe"] == 1
def rule_id(df):        return df["id"] == 1
def rule_ftp(df):       return df["ftp"] == 1
def rule_deseo_trabajar(df):       return df["deseo_trabajar"] == 1

def rule_categoria_independientes(df):  return rule_ocupados(df) & df["categoria_ocupacion"].isin([1, 2, 7])
def rule_categoria_empleador(df):    return rule_ocupados(df) & (df["categoria_ocupacion"] == 1)
def rule_categoria_cuenta_propia(df):    return rule_ocupados(df) & (df["categoria_ocupacion"] == 2)
def rule_categoria_dependientes(df):    return rule_ocupados(df) & (df["categoria_ocupacion"].between(3, 6))
def rule_categoria_asalariados(df):    return rule_ocupados(df) & (df["categoria_ocupacion"].between(3, 4))
def rule_categoria_asalariado_sector_privado(df):    return rule_ocupados(df) & (df["categoria_ocupacion"] == 3)
def rule_categoria_asalariado_sector_publico(df):    return rule_ocupados(df) & (df["categoria_ocupacion"] == 4)
def rule_categoria_servicio_domestico(df):    return rule_ocupados(df) & (df["categoria_ocupacion"].between(5, 6))
def rule_categoria_serv_domestico_puertas_afuera(df):    return rule_ocupados(df) & (df["categoria_ocupacion"] == 5)
def rule_categoria_serv_domestico_puertas_adentro(df):    return rule_ocupados(df) & (df["categoria_ocupacion"] == 6)
def rule_categoria_familiar_personal_no_remunerado(df):    return rule_ocupados(df) & (df["categoria_ocupacion"] == 7)
def rule_categoria_no_corresponde(df):    return rule_ocupados(df) & (df["categoria_ocupacion"] == 0)

def rule_grupo_ciuo_1(df):    return rule_ocupados(df) & (df["ciuo_gran_grupo"] == 1)
def rule_grupo_ciuo_2(df):    return rule_ocupados(df) & (df["ciuo_gran_grupo"] == 2)
def rule_grupo_ciuo_3(df):    return rule_ocupados(df) & (df["ciuo_gran_grupo"] == 3)
def rule_grupo_ciuo_4(df):    return rule_ocupados(df) & (df["ciuo_gran_grupo"] == 4)
def rule_grupo_ciuo_5(df):    return rule_ocupados(df) & (df["ciuo_gran_grupo"] == 5)
def rule_grupo_ciuo_6(df):    return rule_ocupados(df) & (df["ciuo_gran_grupo"] == 6)
def rule_grupo_ciuo_7(df):    return rule_ocupados(df) & (df["ciuo_gran_grupo"] == 7)
def rule_grupo_ciuo_8(df):    return rule_ocupados(df) & (df["ciuo_gran_grupo"] == 8)
def rule_grupo_ciuo_9(df):    return rule_ocupados(df) & (df["ciuo_gran_grupo"] == 9)
def rule_grupo_ciuo_10(df):   return rule_ocupados(df) & (df["ciuo_gran_grupo"] == 10)
def rule_grupo_ciuo_nsnr(df):   return rule_ocupados(df) & (~df["ciuo_gran_grupo"].between(1,10))

def rule_hombres(df):           return rule_ocupados(df) & (df["sexo"] == 1)
def rule_mujeres(df):           return rule_ocupados(df) & (df["sexo"] == 2)
def rule_chile(df):             return rule_ocupados(df) & (df["nacionalidad"] == 152)
def rule_extranjero(df):        return rule_ocupados(df) & (df["nacionalidad"] != 152)
def rule_formal(df):            return rule_ocupados(df) & (df["ocup_form"] == 1)
def rule_informal(df):          return rule_ocupados(df) & (df["ocup_form"] == 2)
def rule_sector_informal(df):          return rule_ocupados(df) & (df["sector"] == 2)

def rule_tpi(df):               return rule_ocupados(df) & (df["tpi"] == 1)
def rule_tp_sin_declarar_voluntareidad(df):    return rule_ocupados(df) & df["habituales"].between(1, 30) & ((df["c10"] > 2) | ((df["c10"] == 1) & (df["c11"] > 4)))
def rule_tpv(df):
    return (
        rule_ocupados(df)
        & (df["habituales"] <= 30)
        & (
            df["c10"].eq(2)
            | (df["c10"].eq(1) & df["c11"].between(3, 4))
        )
    )


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



def rule_habituales(df):
    return rule_ocupados(df) & (df["habituales_clean"] > 0)

def rule_horas_1_30(df):
    #  1 ≤ x ≤ 30
    return rule_ocupados(df) & df["habituales_clean"].between(1, 30, inclusive="both")

def rule_horas_31_44(df):
    # 31 ≤ x ≤ 44
    return rule_ocupados(df) & df["habituales_clean"].between(31, 44, inclusive="both")

def rule_horas_31_39(df):
    # 31 ≤ x ≤ 39
    return rule_ocupados(df) & df["habituales_clean"].between(31, 39, inclusive="both")

def rule_horas_40(df):
    # exactly 40
    return rule_ocupados(df) & (df["habituales_clean"] == 40)

def rule_horas_41_44(df):
    # 41 ≤ x ≤ 44
    return rule_ocupados(df) & df["habituales_clean"].between(41, 44, inclusive="both")

def rule_horas_45(df):
    # exactly 45
    return rule_ocupados(df) & (df["habituales_clean"] == 45)

def rule_horas_46_mas(df):
    # x ≥ 46
    return rule_ocupados(df) & (df["habituales_clean"] >= 46)

def rule_horas_efectivas_46_mas(df):
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

def rule_rama_1(df):
    return rule_ocupados(df) & (df["r_p_rev4cl_caenes"] == 1)

def rule_rama_2(df):
    return rule_ocupados(df) & (df["r_p_rev4cl_caenes"] == 2)

def rule_rama_3(df):    
    return rule_ocupados(df) & (df["r_p_rev4cl_caenes"] == 3)

def rule_rama_4(df):
    return rule_ocupados(df) & (df["r_p_rev4cl_caenes"] == 4)

def rule_rama_5(df):
    return rule_ocupados(df) & (df["r_p_rev4cl_caenes"] == 5)

def rule_rama_6(df):
    return rule_ocupados(df) & (df["r_p_rev4cl_caenes"] == 6)

def rule_rama_7(df):
    return rule_ocupados(df) & (df["r_p_rev4cl_caenes"] == 7)

def rule_rama_8(df):
    return rule_ocupados(df) & (df["r_p_rev4cl_caenes"] == 8)

def rule_rama_9(df):
    return rule_ocupados(df) & (df["r_p_rev4cl_caenes"] == 9)

def rule_rama_10(df):
    return rule_ocupados(df) & (df["r_p_rev4cl_caenes"] == 10)

def rule_rama_11(df):
    return rule_ocupados(df) & (df["r_p_rev4cl_caenes"] == 11)

def rule_rama_12(df):
    return rule_ocupados(df) & (df["r_p_rev4cl_caenes"] == 12)

def rule_rama_13(df):
    return rule_ocupados(df) & (df["r_p_rev4cl_caenes"] == 13)

def rule_rama_14(df):
    return rule_ocupados(df) & (df["r_p_rev4cl_caenes"] == 14)

def rule_rama_15(df):
    return rule_ocupados(df) & (df["r_p_rev4cl_caenes"] == 15)

def rule_rama_16(df):
    return rule_ocupados(df) & (df["r_p_rev4cl_caenes"] == 16)

def rule_rama_17(df):
    return rule_ocupados(df) & (df["r_p_rev4cl_caenes"] == 17)

def rule_rama_18(df):
    return rule_ocupados(df) & (df["r_p_rev4cl_caenes"] == 18)

def rule_rama_19(df):
    return rule_ocupados(df) & (df["r_p_rev4cl_caenes"] == 19)

def rule_rama_20(df):
    return rule_ocupados(df) & (df["r_p_rev4cl_caenes"] == 20)

def rule_rama_21(df):
    return rule_ocupados(df) & (df["r_p_rev4cl_caenes"] == 21)


RULES: dict[str, callable] = {
    "pet": rule_edad_trabajar,
    "ft": rule_fuerza_de_trabajo,
    "o": rule_ocupados,
    "do": rule_desocupados,
    "cesantes": rule_cesantes,
    "busca_trabajo_por_primera_vez": rule_busca_trabajo_por_primera_vez,
    "fft": rule_fuera_fuerza_de_trabajo,
    "fft_iniciadores": rule_fft_iniciadores,
    "fft_inactivos_potencialmente_activos": rule_fft_inactivos_potencialmente_activos,
    "fft_inactivos_habituales": rule_fft_inactivos_habituales,

    "obe": rule_obe,
    "tpi": rule_tpi,
    "id": rule_id,
    "ftp": rule_ftp,
    "deseo_trabajar": rule_deseo_trabajar,
 
    "categoria_independientes": rule_categoria_independientes,
    "categoria_empleador": rule_categoria_empleador,
    "categoria_familiar_personal_no_remunerado": rule_categoria_familiar_personal_no_remunerado,
    "categoria_dependientes": rule_categoria_dependientes,
    "categoria_asalariados": rule_categoria_asalariados,
    "categoria_cuenta_propia": rule_categoria_cuenta_propia,
    "categoria_asalariado_sector_privado": rule_categoria_asalariado_sector_privado,
    "categoria_asalariado_sector_publico": rule_categoria_asalariado_sector_publico,
    "categoria_servicio_domestico": rule_categoria_servicio_domestico,
    "categoria_serv_domestico_puertas_afuera": rule_categoria_serv_domestico_puertas_afuera,
    "categoria_serv_domestico_puertas_adentro": rule_categoria_serv_domestico_puertas_adentro,
    "categoria_no_corresponde": rule_categoria_no_corresponde,

    "grupo_ciuo_1": rule_grupo_ciuo_1,
    "grupo_ciuo_2": rule_grupo_ciuo_2,
    "grupo_ciuo_3": rule_grupo_ciuo_3,
    "grupo_ciuo_4": rule_grupo_ciuo_4,
    "grupo_ciuo_5": rule_grupo_ciuo_5,
    "grupo_ciuo_6": rule_grupo_ciuo_6,
    "grupo_ciuo_7": rule_grupo_ciuo_7,
    "grupo_ciuo_8": rule_grupo_ciuo_8,
    "grupo_ciuo_9": rule_grupo_ciuo_9,
    "grupo_ciuo_10": rule_grupo_ciuo_10,
    "grupo_ciuo_nsnr": rule_grupo_ciuo_nsnr,

    "o_hombres": rule_hombres,
    "o_mujeres": rule_mujeres,

    "o_chile": rule_chile,
    "o_extranjero": rule_extranjero,

    "o_formal": rule_formal,
    "o_informal": rule_informal,

    "o_sector_informal": rule_sector_informal,

    "o_sin_basica_completa": rule_sin_basica,
    "o_ed_basica_completa": rule_ed_basica,
    "o_ed_media_completa": rule_ed_media,
    "o_ed_sup_completa": rule_ed_sup,
    "o_ed_sup_cft": rule_ed_sup_cft,
    "o_ed_sup_ip": rule_ed_sup_ip,
    "o_ed_sup_univ": rule_ed_sup_univ,

    "o_ed_sup_ciuo_alta": rule_ed_sup_ciuo_alta,
    "o_ed_sup_ciuo_media_baja": rule_ed_sup_ciuo_media_baja,
    "o_ed_sup_ciuo_no_alta": rule_ed_sup_ciuo_no_alta,

    "grupo_ciuo_alta": rule_ciuo_alta,
    "grupo_ciuo_media_baja": rule_ciuo_media_baja,
    "grupo_ciuo_media": rule_ciuo_media,
    "grupo_ciuo_baja": rule_ciuo_baja,
    "grupo_ciuo_otras": rule_ciuo_otras,

    "oc_hab": rule_habituales,

    "tpv": rule_tpv,
    "tp_sin_declarar_voluntareidad": rule_tp_sin_declarar_voluntareidad,
    "horas_1_30":    rule_horas_1_30,
    "horas_31_44":   rule_horas_31_44,
    "horas_31_39":   rule_horas_31_39,
    "horas_40":      rule_horas_40,
    "horas_41_44":   rule_horas_41_44,
    "horas_45":      rule_horas_45,
    "horas_46_mas":  rule_horas_46_mas,
    "horas_efectivas_46_mas": rule_horas_efectivas_46_mas,

    "oc_edad_15_24": rule_edad_15_24,
    "oc_edad_25_34": rule_edad_25_34,
    "oc_edad_35_44": rule_edad_35_44,
    "oc_edad_45_54": rule_edad_45_54,
    "oc_edad_55_64": rule_edad_55_64,
    "oc_edad_65_mas": rule_edad_65_mas,

    "rama_1": rule_rama_1,
    "rama_2": rule_rama_2,
    "rama_3": rule_rama_3,
    "rama_4": rule_rama_4,
    "rama_5": rule_rama_5,
    "rama_6": rule_rama_6,
    "rama_7": rule_rama_7,
    "rama_8": rule_rama_8,
    "rama_9": rule_rama_9,
    "rama_10": rule_rama_10,
    "rama_11": rule_rama_11,
    "rama_12": rule_rama_12,
    "rama_13": rule_rama_13,
    "rama_14": rule_rama_14,
    "rama_15": rule_rama_15,
    "rama_16": rule_rama_16,
    "rama_17": rule_rama_17,
    "rama_18": rule_rama_18,
    "rama_19": rule_rama_19,
    "rama_20": rule_rama_20,
    "rama_21": rule_rama_21,

}


def aggregate(df: pd.DataFrame) -> pd.DataFrame:
    masks = {name: fn(df) for name, fn in RULES.items()}
    agg_dict = {
        key: ("fact_cal", lambda s, m=mask: s[m.loc[s.index]].sum())
        for key, mask in masks.items()
    }
    return (
        df.groupby(["ano_trimestre", "mes_central"], dropna=False, observed=True)
          .agg(**agg_dict)
          .reset_index()
          .sort_values(["ano_trimestre", "mes_central"])
    )


def main() -> int:
    # 1) Leo microdatos
    frames = read_frames()
    df = pd.concat(frames, ignore_index=True)

    # 2) Preparo horas limpias
    df["efectivas_clean"]  = df["efectivas"].replace({888: 0, 999: 0})
    df["habituales_clean"] = df["habituales"].replace({888: 0, 999: 0}).fillna(0)

    # 3) Agrego todos los indicadores
    resumen = aggregate(df)

    # 4) Promedios ponderados corregidos
    # Definimos las dos máscaras:
    mask_o_declaran_horas = (df["activ"] == 1) & (~df["efectivas"].isin([888, 999]))    
    mask_sin_ausentes = mask_o_declaran_horas & df["efectivas_clean"].between(1, 168, inclusive="both")

    # Calculamos horas ponderadas y pesos
    df["efe1_horas_pond"] = df["efectivas_clean"].where(mask_o_declaran_horas, 0) * df["fact_cal"]
    df["efe2_horas_pond"] = df["efectivas_clean"].where(mask_sin_ausentes, 0) * df["fact_cal"]
    df["hab_horas_pond"]  = df["habituales_clean"] * df["fact_cal"]
    df["o_declaran_horas_pond"]   = df["fact_cal"].where(mask_o_declaran_horas, 0)
    df["oc_sin_ausentes_pond"]   = df["fact_cal"].where(mask_sin_ausentes, 0)

    # 5) Agrupamos totales y conteos de pesos por trimestre
    horas = (
        df.groupby(["ano_trimestre", "mes_central"])
          .agg(
            efe1_total = ("efe1_horas_pond", "sum"),
            efe2_total = ("efe2_horas_pond", "sum"),
            hab_total  = ("hab_horas_pond",  "sum"),
            o_declaran_horas   = ("o_declaran_horas_pond",   "sum"),
            oc_sin_ausentes   = ("oc_sin_ausentes_pond",   "sum"),
          )
          .reset_index()
    )

    # 6) Unimos con el resto de indicadores
    resumen = resumen.merge(horas, on=["ano_trimestre", "mes_central"])

    # 7) Renombra y calcula columnas derivadas
    resumen.rename(columns={
        "oc_efe1": "efe1",
        "oc_efe2": "efe2",
        "oc_hab":  "habituales_sum"
    }, inplace=True)

    resumen["oi"]  = resumen["o_informal"]
    resumen["osi"] = resumen["o_sector_informal"]
    resumen["fta"] = resumen["ft"] + resumen["id"] + resumen["ftp"]

    # 8) Tasas originales (en porcentaje con 3 decimales)
    def safe_div(n, d):
        return (n / d * 100).round(3)

    resumen["td"]   = safe_div(resumen["do"],  resumen["ft"])
    resumen["to"]   = safe_div(resumen["o"],   resumen["pet"])
    resumen["tp"]   = safe_div(resumen["ft"],  resumen["pet"])
    resumen["tpl"]  = safe_div(resumen["id"] + resumen["obe"] + resumen["do"],
                                resumen["ft"] + resumen["id"])
    resumen["su1"]  = safe_div(resumen["do"] + resumen["id"],
                                resumen["ft"] + resumen["id"])
    resumen["su2"]  = safe_div(resumen["do"] + resumen["id"] + resumen["tpi"],
                                resumen["ft"] + resumen["id"])
    resumen["su3"]  = safe_div(resumen["do"] + resumen["id"] + resumen["ftp"],
                                resumen["fta"])
    resumen["su4"]  = safe_div(resumen["do"] + resumen["id"] + resumen["tpi"] + resumen["ftp"],
                                resumen["fta"])
    resumen["toi"]  = safe_div(resumen["oi"],   resumen["o"])
    resumen["tosi"] = safe_div(resumen["osi"],  resumen["o"])

    # 9) Promedios reales de horas (3 decimales)
    resumen["promedio_horas_efectivas_sin_ausentes"] = (
        resumen["efe1_total"] / resumen["oc_sin_ausentes"]
    ).round(3)

    resumen["promedio_horas_efectivas_declaran_horas"] = (
        resumen["efe2_total"] / resumen["o_declaran_horas"]
    ).round(3)

    resumen["promedio_horas_habituales"] = (
        resumen["hab_total"] / resumen["o_declaran_horas"]
    ).round(3)


    # 10) Eliminar columnas intermedias antes de exportar
    resumen.drop(columns=[
        "efe1_total", "efe2_total", "hab_total",
    #    "o_declaran_horas", "oc_sin_ausentes"
    ], inplace=True)


    # Reordeno según la constante FINAL_COLS
    resumen = resumen[FINAL_COLS]

    # 11) Export técn ico
    resumen.to_parquet(OUTFILE_PARQUET, index=False)
    resumen.to_csv(OUTFILE_CSV, index=False)
    print(f"✔ Guardado técnico: {OUTFILE_PARQUET} (+ CSV)  [{len(resumen)} filas]")

    # 12) Genero CSV simplificado
    lite = resumen.copy()
    orig = set(lite.columns)
    for old, new in PUBLIC_COLS:
        if old in orig:
            lite.rename(columns={old: new}, inplace=True)
    cols_order = [new for old, new in PUBLIC_COLS if old in orig]
    lite = lite[cols_order]

    # Redondeo enteros
    mask_counts = (
        ~lite.columns.isin(["Año-Trimestre", "Mes central"]) &
        ~lite.columns.str.startswith(("Tasa", "Promedio", "Prom."))
    )
    lite.loc[:, mask_counts] = lite.loc[:, mask_counts].round(0).astype("Int64")

    lite.to_csv(
        OUTFILE_SIMPLIFICADO,
        index=False,
        encoding="utf-8-sig"   # UTF-8 con BOM
    )   
    print(f"✔ Guardado público: {OUTFILE_SIMPLIFICADO}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
