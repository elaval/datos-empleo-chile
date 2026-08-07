"""Genera la CAPA DE CONOCIMIENTO (`conocimiento/`) desde los datos procesados.

Esta capa se ubica entre los datos crudos y los reportes/respuestas. Produce
artefactos que un agente (Claude u otro) puede consumir para construir
conocimiento de orden superior sin re-procesar los datos crudos.

Tres estratos:
  1. Contexto/contrato (estable, AUTORADO a mano): ontologia.md, indicadores.json,
     metodologia.md, README.md.  -> NO los toca este script.
  2. Evidencia (REGENERABLE, este script): hechos computados y verificables.
  3. Hallazgos (curados, AUTORADOS): insights sobre la evidencia.  -> NO los toca.

Este script solo (re)genera el estrato 2 (evidencia/). Re-ejecutar tras cada
publicación del INE:  python -m scripts.generar_conocimiento

Fuentes:
  - Nacional + composición (categoría/sector) : tabla maestra agregada
    (autoritativa, calza con INE, serie completa 2010->hoy, todos los meses).
  - Cortes por sexo / edad / región          : microdatos ponderados por fact_cal,
    usando el archivo del mes central del último release (apila todos los años de
    ese trimestre -> serie anual comparable que controla estacionalidad).
"""
from __future__ import annotations

import datetime
import json
import pathlib

import numpy as np
import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "processed"
MAESTRA = DATA / "agregados" / "integrado" / "ene_trimestre_totales.parquet"
MICRO_DIR = DATA / "microdatos"
OUT = ROOT / "conocimiento" / "evidencia"

# --- Diccionarios de dominio (contrato de codificación de los microdatos) ---
MESES_CENTRALES = {
    1: ("DEF", "diciembre-enero-febrero", "ene-01-def"),
    2: ("EFM", "enero-febrero-marzo", "ene-02-efm"),
    3: ("FMA", "febrero-marzo-abril", "ene-03-fma"),
    4: ("MAM", "marzo-abril-mayo", "ene-04-mam"),
    5: ("AMJ", "abril-mayo-junio", "ene-05-amj"),
    6: ("MJJ", "mayo-junio-julio", "ene-06-mjj"),
    7: ("JJA", "junio-julio-agosto", "ene-07-jja"),
    8: ("JAS", "julio-agosto-septiembre", "ene-08-jas"),
    9: ("ASO", "agosto-septiembre-octubre", "ene-09-aso"),
    10: ("SON", "septiembre-octubre-noviembre", "ene-10-son"),
    11: ("OND", "octubre-noviembre-diciembre", "ene-11-ond"),
    12: ("NDE", "noviembre-diciembre-enero", "ene-12-nde"),
}

SEXO = {1: "Hombre", 2: "Mujer"}

REGION = {
    1: "Tarapacá", 2: "Antofagasta", 3: "Atacama", 4: "Coquimbo",
    5: "Valparaíso", 6: "O'Higgins", 7: "Maule", 8: "Biobío",
    9: "La Araucanía", 10: "Los Lagos", 11: "Aysén", 12: "Magallanes",
    13: "Metropolitana", 14: "Los Ríos", 15: "Arica y Parinacota", 16: "Ñuble",
}

# Grupos etarios construidos desde la variable continua `edad` (población 15+).
GRUPOS_EDAD = [
    (15, 24, "15-24"),
    (25, 34, "25-34"),
    (35, 44, "35-44"),
    (45, 54, "45-54"),
    (55, 64, "55-64"),
    (65, 200, "65 y más"),
]

# Composición de ocupados por categoría ocupacional (columnas de la maestra).
CATEGORIA_COLS = {
    "empleador": "categoria_empleador",
    "cuenta_propia": "categoria_cuenta_propia",
    "asalariado_sector_privado": "categoria_asalariado_sector_privado",
    "asalariado_sector_publico": "categoria_asalariado_sector_publico",
    "servicio_domestico": "categoria_servicio_domestico",
    "familiar_no_remunerado": "categoria_familiar_personal_no_remunerado",
}

# Nivel educacional alcanzado por los ocupados (columnas de la maestra).
# OJO: no suman exactamente el total de ocupados — hay casos sin dato de nivel.
EDUCACION_COLS = {
    "sin_basica_completa": "o_sin_basica_completa",
    "basica_completa": "o_ed_basica_completa",
    "media_completa": "o_ed_media_completa",
    "superior_completa": "o_ed_sup_completa",
}
EDUCACION_SUPERIOR_COLS = {
    "cft": "o_ed_sup_cft",
    "instituto_profesional": "o_ed_sup_ip",
    "universitaria": "o_ed_sup_univ",
}
# Desajuste educativo: ocupados CON educación superior según la calificación del puesto
# que ocupan (CIUO). `no_alta` = trabaja en un puesto que no requiere alta calificación.
DESAJUSTE_COLS = {
    "sup_en_puesto_alta_calificacion": "o_ed_sup_ciuo_alta",
    "sup_en_puesto_no_alta_calificacion": "o_ed_sup_ciuo_no_alta",
    "puestos_alta_calificacion_total": "grupo_ciuo_alta",
}

# Jornada: tramos de horas HABITUALES declaradas por los ocupados.
# Suman `o_declaran_horas` (no el total de ocupados: hay quienes no declaran horas).
# Contexto legal: la Ley 21.561 reduce la jornada máxima de 45 h a 40 h por fases —
# 44 h desde el 26-abr-2024, 42 h desde el 26-abr-2026 y 40 h desde el 26-abr-2028.
JORNADA_COLS = {
    "h_1_30": "horas_1_30",
    "h_31_39": "horas_31_39",
    "h_40": "horas_40",
    "h_41_44": "horas_41_44",
    "h_45": "horas_45",
    "h_46_mas": "horas_46_mas",
}
JORNADA_ETIQUETA = {
    "h_1_30": "1 a 30 h",
    "h_31_39": "31 a 39 h",
    "h_40": "40 h exactas",
    "h_41_44": "41 a 44 h",
    "h_45": "45 h exactas",
    "h_46_mas": "46 h o más",
}

# Grupos ocupacionales CIUO-08 (clasificación vigente).
# ⚠ QUIEBRE DE SERIE: la ENE usó CIUO-88 hasta 2018 y CIUO-08 desde 2017 (2017-2018 traen
# ambas). Las series por grupo ocupacional NO son continuas antes de 2019: por eso este
# bloque solo se emite desde CIUO08_DESDE.
CIUO08_DESDE = 2019
CIUO08_COLS = {
    "g1_directivos_gerentes": "grupo_ciuo08_1",
    "g2_profesionales_cientificos": "grupo_ciuo08_2",
    "g3_tecnicos_nivel_medio": "grupo_ciuo08_3",
    "g4_apoyo_administrativo": "grupo_ciuo08_4",
    "g5_servicios_y_comercio": "grupo_ciuo08_5",
    "g6_agropecuarios_pesqueros": "grupo_ciuo08_6",
    "g7_artesanos_operarios": "grupo_ciuo08_7",
    "g8_operadores_maquinas": "grupo_ciuo08_8",
    "g9_ocupaciones_elementales": "grupo_ciuo08_9",
    "g10_no_identificado": "grupo_ciuo08_10",
    "sin_clasificacion": "grupo_ciuo08_nsnr",
}
CIUO08_ETIQUETA = {
    "g1_directivos_gerentes": "G1 Directivos y gerentes",
    "g2_profesionales_cientificos": "G2 Profesionales y científicos",
    "g3_tecnicos_nivel_medio": "G3 Técnicos de nivel medio",
    "g4_apoyo_administrativo": "G4 Apoyo administrativo",
    "g5_servicios_y_comercio": "G5 Servicios y comercio",
    "g6_agropecuarios_pesqueros": "G6 Agropecuarios y pesqueros",
    "g7_artesanos_operarios": "G7 Artesanos y operarios",
    "g8_operadores_maquinas": "G8 Operadores de máquinas",
    "g9_ocupaciones_elementales": "G9 Ocupaciones elementales",
    "g10_no_identificado": "G10 No identificado",
    "sin_clasificacion": "Sin clasificación / NS-NR",
}
# Los grupos 1-3 componen la "alta calificación" que usa el desajuste educativo.
CIUO08_ALTA = ["g1_directivos_gerentes", "g2_profesionales_cientificos", "g3_tecnicos_nivel_medio"]

CATEGORIA_ETIQUETA = {
    "empleador": "Empleador",
    "cuenta_propia": "Cuenta propia",
    "asalariado_sector_privado": "Asalariado sector privado",
    "asalariado_sector_publico": "Asalariado sector público",
    "servicio_domestico": "Personal de servicio doméstico",
    "familiar_no_remunerado": "Familiar o personal no remunerado",
}


def _round(x, nd=0):
    if x is None or (isinstance(x, float) and np.isnan(x)):
        return None
    return round(float(x), nd)


def core_indicadores(sub: pd.DataFrame) -> dict:
    """Indicadores núcleo (ponderados por fact_cal) para un subconjunto 15+ de microdatos.

    Incluye `n` = tamaño muestral SIN ponderar (nº de personas encuestadas en el grupo).
    Sirve como señal de fragilidad: n bajo ⇒ mayor error muestral (ej. regiones chicas).
    """
    w = sub["fact_cal"]
    pet = w.sum()
    o = w[sub["activ"] == 1].sum()
    do = w[sub["activ"] == 2].sum()
    ft = o + do
    return {
        "n": int(len(sub)),
        "pet": _round(pet),
        "ft": _round(ft),
        "o": _round(o),
        "do": _round(do),
        "td": _round(100 * do / ft, 2) if ft else None,
        "tp": _round(100 * ft / pet, 2) if pet else None,
        "to": _round(100 * o / pet, 2) if pet else None,
    }


def yoy(actual: dict, previo: dict | None) -> dict:
    """Variación interanual (nivel absoluto y % para stocks; puntos porcentuales para tasas)."""
    if previo is None:
        return {}
    d = {}
    for k in ("pet", "ft", "o", "do"):
        if actual.get(k) is not None and previo.get(k) is not None:
            base = previo[k]
            d[f"delta_{k}"] = _round(actual[k] - base)
            d[f"delta_rel_{k}"] = _round(100 * (actual[k] / base - 1), 2) if base else None
    for k in ("td", "tp", "to"):
        if actual.get(k) is not None and previo.get(k) is not None:
            d[f"delta_pp_{k}"] = _round(actual[k] - previo[k], 2)
    return d


# --------------------------------------------------------------------------
# 1. NACIONAL — desde la tabla maestra (serie completa, autoritativa)
# --------------------------------------------------------------------------
def build_nacional(maestra: pd.DataFrame):
    m = maestra.sort_values(["ano_trimestre", "mes_central"]).copy()
    m["ano"] = m["ano_trimestre"].astype(int)
    m["mes_central"] = m["mes_central"].astype(int)

    serie = []
    for _, r in m.iterrows():
        fila = {
            "ano": int(r["ano"]),
            "mes_central": int(r["mes_central"]),
            "trimestre": MESES_CENTRALES[int(r["mes_central"])][0],
            "pet": _round(r["pet"]),
            "ft": _round(r["ft"]),
            "o": _round(r["o"]),
            "do": _round(r["do"]),
            "td": _round(r["td"], 2),
            "tp": _round(r["tp"], 2),
            "to": _round(r["to"], 2),
            "composicion_ocupados": {
                k: _round(r[col]) for k, col in CATEGORIA_COLS.items() if col in m.columns
            },
            "informalidad": {
                "o_formal": _round(r["o_formal"]) if "o_formal" in m.columns else None,
                "o_informal": _round(r["o_informal"]) if "o_informal" in m.columns else None,
                "toi": _round(r["toi"], 2) if "toi" in m.columns else None,
            },
            "sexo_ocupados": {
                "hombres": _round(r["o_hombres"]) if "o_hombres" in m.columns else None,
                "mujeres": _round(r["o_mujeres"]) if "o_mujeres" in m.columns else None,
            },
            "educacion": {
                k: _round(r[col]) for k, col in EDUCACION_COLS.items() if col in m.columns
            },
            "educacion_superior": {
                k: _round(r[col]) for k, col in EDUCACION_SUPERIOR_COLS.items() if col in m.columns
            },
            "desajuste_educativo": {
                k: _round(r[col]) for k, col in DESAJUSTE_COLS.items() if col in m.columns
            },
            # Solo desde 2019: antes la clasificación vigente era CIUO-88 (ver CIUO08_DESDE).
            "ocupacion_ciuo08": (
                {k: _round(r[col]) for k, col in CIUO08_COLS.items() if col in m.columns}
                if int(r["ano"]) >= CIUO08_DESDE else None
            ),
            # Subutilización laboral (OIT). Las tasas dependen de `id` (iniciadores
            # disponibles): ver el quiebre CISO-18 en metodologia.md §3-bis.
            "subutilizacion": {
                "tasas": {k: _round(r[k], 2) for k in ("su1", "su2", "su3", "su4", "tpl")
                          if k in m.columns},
                "componentes": {
                    "desocupados": _round(r["do"]),
                    "iniciadores_disponibles": _round(r["id"]) if "id" in m.columns else None,
                    "parcial_involuntario": _round(r["tpi"]) if "tpi" in m.columns else None,
                    "fuerza_trabajo_potencial": _round(r["ftp"]) if "ftp" in m.columns else None,
                    "ocupados_que_buscaron_empleo": _round(r["obe"]) if "obe" in m.columns else None,
                    "fuerza_trabajo": _round(r["ft"]),
                    "fuerza_trabajo_ampliada": _round(r["fta"]) if "fta" in m.columns else None,
                },
            },
            "jornada": {
                "tramos": {
                    k: _round(r[col]) for k, col in JORNADA_COLS.items() if col in m.columns
                },
                "promedio_horas_habituales": (
                    _round(r["promedio_horas_habituales"], 2)
                    if "promedio_horas_habituales" in m.columns else None
                ),
                "parcial_involuntario": _round(r["tpi"]) if "tpi" in m.columns else None,
                "parcial_voluntario": _round(r["tpv"]) if "tpv" in m.columns else None,
                "o_declaran_horas": (
                    _round(r["o_declaran_horas"]) if "o_declaran_horas" in m.columns else None
                ),
            },
        }
        serie.append(fila)
    return serie


# --------------------------------------------------------------------------
# 2. CORTES — desde microdatos del mes central del último release
# --------------------------------------------------------------------------
def build_cortes(micro: pd.DataFrame):
    m = micro[micro["edad"] >= 15].copy()
    anos = sorted(m["ano_trimestre"].dropna().astype(int).unique())

    def serie_por_grupo(asignar_clave):
        """asignar_clave: fn(df)->Series con la clave de grupo. Devuelve {clave:[filas por año]}."""
        tmp = m.copy()
        tmp["_grupo"] = asignar_clave(tmp)
        salida = {}
        for (ano, grupo), sub in tmp.groupby(["ano_trimestre", "_grupo"]):
            if pd.isna(grupo):
                continue
            salida.setdefault(grupo, {})[int(ano)] = core_indicadores(sub)
        # a lista ordenada por año
        return {
            g: [{"ano": a, **vals} for a, vals in sorted(por_ano.items())]
            for g, por_ano in salida.items()
        }

    def edad_bin(df):
        e = df["edad"]
        out = pd.Series(index=df.index, dtype=object)
        for lo, hi, lab in GRUPOS_EDAD:
            out[(e >= lo) & (e <= hi)] = lab
        return out

    def nacionalidad_bin(df):
        # nacionalidad = código de país ISO (152 = Chile); extranjero = cualquier otro válido.
        return df["nacionalidad"].apply(
            lambda x: "Chileno/a" if x == 152 else ("Extranjero/a" if pd.notna(x) else None)
        )

    cortes = {
        "sexo": {
            "etiqueta_dim": "Sexo",
            "grupos": serie_por_grupo(lambda df: df["sexo"].map(SEXO)),
        },
        "edad": {
            "etiqueta_dim": "Grupo de edad",
            "grupos": serie_por_grupo(edad_bin),
        },
        "region": {
            "etiqueta_dim": "Región",
            "grupos": serie_por_grupo(lambda df: df["region"].map(REGION)),
        },
        "nacionalidad": {
            "etiqueta_dim": "Nacionalidad",
            "grupos": serie_por_grupo(nacionalidad_bin),
        },
    }
    return cortes, anos


# --------------------------------------------------------------------------
# 3. SNAPSHOT + TENDENCIAS
# --------------------------------------------------------------------------
def build_snapshot(serie_nac, cortes, release, generado):
    ult = serie_nac[-1]
    # previo = mismo mes central, año anterior
    prev = next(
        (f for f in reversed(serie_nac[:-1])
         if f["mes_central"] == ult["mes_central"] and f["ano"] == ult["ano"] - 1),
        None,
    )
    nac = {k: ult[k] for k in ("pet", "ft", "o", "do", "td", "tp", "to")}
    nac["delta_yoy"] = yoy(nac, {k: prev[k] for k in nac} if prev else None)

    cortes_snap = {}
    for dim, obj in cortes.items():
        filas = []
        for clave, serie in obj["grupos"].items():
            if not serie:
                continue
            actual = serie[-1]
            previo = next((s for s in reversed(serie[:-1]) if s["ano"] == actual["ano"] - 1), None)
            fila = {"clave": clave, "n": actual.get("n"),
                    **{k: actual.get(k) for k in ("pet", "ft", "o", "do", "td", "tp", "to")}}
            fila["delta_yoy"] = yoy(fila, previo)
            filas.append(fila)
        cortes_snap[dim] = {"etiqueta_dim": obj["etiqueta_dim"], "grupos": filas}

    # S1: composición de ocupados CON variación interanual (mismo mes central, año previo).
    comp_ult = ult["composicion_ocupados"]
    comp_prev = prev["composicion_ocupados"] if prev else None

    def _comp_entry(valor, base):
        e = {"o": valor}
        if base is not None and valor is not None:
            e["delta_o"] = _round(valor - base)
            e["delta_rel_o"] = _round(100 * (valor / base - 1), 2) if base else None
        return e

    composicion = {
        cat: _comp_entry(comp_ult.get(cat), comp_prev.get(cat) if comp_prev else None)
        for cat in comp_ult
    }
    # Agregados de lectura frecuente: asalariados (dependientes) vs. independientes.
    def _suma(cats, d):
        return sum(d[c] for c in cats if d.get(c) is not None) if d else None

    AGG = {
        "asalariados": ["asalariado_sector_privado", "asalariado_sector_publico"],
        "independientes": ["empleador", "cuenta_propia"],
    }
    composicion["_agregados"] = {
        nombre: _comp_entry(_suma(cats, comp_ult), _suma(cats, comp_prev))
        for nombre, cats in AGG.items()
    }

    # Formalidad del empleo (partición de ocupados; serie robusta desde 2017).
    inf_ult = ult["informalidad"]
    inf_prev = prev["informalidad"] if prev else None
    formalidad = {
        "o_formal": _comp_entry(inf_ult.get("o_formal"), inf_prev.get("o_formal") if inf_prev else None),
        "o_informal": _comp_entry(inf_ult.get("o_informal"), inf_prev.get("o_informal") if inf_prev else None),
        "tasa_ocupacion_informal": {"toi": inf_ult.get("toi")},
    }
    if inf_prev and inf_prev.get("toi") is not None and inf_ult.get("toi") is not None:
        formalidad["tasa_ocupacion_informal"]["delta_pp"] = _round(inf_ult["toi"] - inf_prev["toi"], 2)

    # Educación: nivel alcanzado por los ocupados + desglose de superior + desajuste.
    def _bloque(dic_ult, dic_prev):
        return {k: _comp_entry(v, (dic_prev or {}).get(k)) for k, v in dic_ult.items()}

    educacion = {
        "por_nivel": _bloque(ult["educacion"], prev["educacion"] if prev else None),
        "superior_por_tipo": _bloque(ult["educacion_superior"],
                                     prev["educacion_superior"] if prev else None),
        "desajuste": _bloque(ult["desajuste_educativo"],
                             prev["desajuste_educativo"] if prev else None),
    }
    # % de ocupados con educación superior que trabaja en un puesto NO de alta calificación.
    def _tasa_desajuste(d):
        sup = d.get("sup_en_puesto_alta_calificacion")
        noa = d.get("sup_en_puesto_no_alta_calificacion")
        return 100 * noa / (sup + noa) if sup and noa else None

    t_act = _tasa_desajuste(ult["desajuste_educativo"])
    t_prev = _tasa_desajuste(prev["desajuste_educativo"]) if prev else None
    educacion["tasa_desajuste"] = {
        "definicion": "% de los ocupados con educación superior completa que trabaja en un "
                      "puesto que NO es de alta calificación (CIUO).",
        "valor": _round(t_act, 2),
        "delta_pp": _round(t_act - t_prev, 2) if (t_act and t_prev) else None,
    }
    # Los niveles no cierran contra el total: se explicita el residuo sin dato.
    suma_niv = sum(v for v in ult["educacion"].values() if v is not None)
    residuo = ult["o"] - suma_niv
    residuo_prev = None
    if prev:
        residuo_prev = prev["o"] - sum(v for v in prev["educacion"].values() if v is not None)
    educacion["_cobertura"] = {
        "suma_niveles": _round(suma_niv),
        "ocupados": _round(ult["o"]),
        "sin_dato_de_nivel": _round(residuo),
        # Se expone el residuo del año previo y su variación para que la suma de las
        # variaciones por nivel se pueda cuadrar exactamente con la variación nacional.
        "sin_dato_de_nivel_previo": _round(residuo_prev),
        "delta_sin_dato_de_nivel": _round(residuo - residuo_prev) if residuo_prev is not None else None,
    }

    # Jornada: distribución de horas habituales + jornada parcial.
    j_ult, j_prev = ult["jornada"], (prev["jornada"] if prev else None)
    jornada = {
        "tramos": {
            k: _comp_entry(v, (j_prev or {}).get("tramos", {}).get(k))
            for k, v in j_ult["tramos"].items()
        },
        "promedio_horas_habituales": {
            "valor": j_ult["promedio_horas_habituales"],
            "delta": (_round(j_ult["promedio_horas_habituales"]
                             - j_prev["promedio_horas_habituales"], 2)
                      if j_prev and j_prev["promedio_horas_habituales"] else None),
        },
        "parcial": {
            "involuntario": _comp_entry(j_ult["parcial_involuntario"],
                                        j_prev["parcial_involuntario"] if j_prev else None),
            "voluntario": _comp_entry(j_ult["parcial_voluntario"],
                                      j_prev["parcial_voluntario"] if j_prev else None),
        },
        "contexto_legal": {
            "ley": "Ley 21.561 (2023): reduce la jornada máxima de 45 h a 40 h por fases.",
            "fases": {"44_h": "2024-04-26", "42_h": "2026-04-26", "40_h": "2028-04-26"},
            "nota": "El trimestre AMJ 2026 capta solo parcialmente la fase de 42 h, vigente "
                    "desde el 26 de abril de 2026: dos de sus tres meses son posteriores.",
        },
    }
    suma_tramos = sum(v for v in j_ult["tramos"].values() if v is not None)
    no_declaran = ult["o"] - (j_ult["o_declaran_horas"] or 0)
    no_declaran_prev = (prev["o"] - (j_prev["o_declaran_horas"] or 0)) if j_prev else None
    jornada["_cobertura"] = {
        "suma_tramos": _round(suma_tramos),
        "o_declaran_horas": j_ult["o_declaran_horas"],
        "ocupados": _round(ult["o"]),
        "no_declaran_horas": _round(no_declaran),
        "no_declaran_horas_previo": _round(no_declaran_prev),
        "delta_no_declaran_horas": (_round(no_declaran - no_declaran_prev)
                                    if no_declaran_prev is not None else None),
    }

    # Subutilización: tasas con su Δ en pp + componentes con su Δ absoluta.
    s_ult = ult["subutilizacion"]
    s_prev = prev["subutilizacion"] if prev else None
    ETIQ_SU = {
        "su1": "SU1 · desocupación (incl. iniciadores disponibles)",
        "su2": "SU2 · SU1 + subempleo por horas",
        "su3": "SU3 · SU1 + fuerza de trabajo potencial",
        "su4": "SU4 · SU1 + subempleo por horas + potencial",
        "tpl": "Presión laboral · SU1 + ocupados que buscan otro empleo",
    }
    subutilizacion = {
        "nota": "Indicadores OIT de subutilización. SU1 es la desocupación ampliada con "
                "iniciadores disponibles, por lo que es algo mayor que la TD. Cada nivel "
                "agrega un grupo distinto de personas subutilizadas.",
        "tasas": {
            k: {
                "etiqueta": ETIQ_SU.get(k, k),
                "valor": v,
                "delta_pp": (_round(v - s_prev["tasas"][k], 2)
                             if s_prev and s_prev["tasas"].get(k) is not None else None),
            }
            for k, v in s_ult["tasas"].items()
        },
        "componentes": {
            k: _comp_entry(v, (s_prev or {}).get("componentes", {}).get(k))
            for k, v in s_ult["componentes"].items() if v is not None
        },
        "referencia_td": {"valor": nac["td"], "delta_pp": nac["delta_yoy"].get("delta_pp_td")},
    }

    # Ocupación por grupo CIUO-08.
    ocupacion = None
    if ult.get("ocupacion_ciuo08"):
        o_ult = ult["ocupacion_ciuo08"]
        o_prev = prev.get("ocupacion_ciuo08") if prev else None
        ocupacion = {
            "clasificacion": "CIUO-08",
            "serie_valida_desde": CIUO08_DESDE,
            "nota_quiebre": "La ENE usó CIUO-88 hasta 2018 y CIUO-08 desde 2017. Las series "
                            "por grupo ocupacional NO son comparables a través de ese corte; "
                            f"este bloque solo se emite desde {CIUO08_DESDE}.",
            "grupos": {
                k: {"etiqueta": CIUO08_ETIQUETA[k],
                    **_comp_entry(v, (o_prev or {}).get(k))}
                for k, v in o_ult.items()
            },
        }
        alta_a = sum(o_ult[k] for k in CIUO08_ALTA if o_ult.get(k) is not None)
        alta_p = (sum(o_prev[k] for k in CIUO08_ALTA if o_prev.get(k) is not None)
                  if o_prev else None)
        ocupacion["_agregados"] = {
            "alta_calificacion_g1_g3": {
                "nota": "Suma de G1-G3: es el mismo agregado que usa el desajuste educativo.",
                **_comp_entry(alta_a, alta_p),
            }
        }

    return {
        "release": release,
        "generado": generado,
        "fuente_metodologia": "conocimiento/metodologia.md",
        "periodo": {
            "ano": ult["ano"],
            "mes_central": ult["mes_central"],
            "trimestre": ult["trimestre"],
            "etiqueta": f"{MESES_CENTRALES[ult['mes_central']][1]} {ult['ano']}",
            "comparacion": f"{MESES_CENTRALES[ult['mes_central']][0]} {ult['ano'] - 1}",
        },
        "nacional": nac,
        "composicion_ocupados": composicion,
        "formalidad": formalidad,
        "educacion": educacion,
        "subutilizacion": subutilizacion,
        "jornada": jornada,
        "ocupacion_ciuo08": ocupacion,
        "cortes": cortes_snap,
    }


TASAS = {"td", "tp", "to"}
INDS_TENDENCIA = ("td", "tp", "to", "o", "ft", "do")


def descriptor_serie(vals):
    """Descriptor de tendencia de una serie [(ano, valor), ...] ya ordenada y sin None.

    Incluye referencias (primero/último/hace 1 y 5 años/máximo/mínimo), la dirección del
    último año, y el cambio de largo plazo (primer → último año), en pp para tasas o en
    absoluto + % para stocks. `es_tasa` se infiere del nombre del indicador afuera.
    """
    if len(vals) < 2:
        return None
    anos, xs = zip(*vals)
    imax, imin = int(np.argmax(xs)), int(np.argmin(xs))
    return {
        "primero": {"ano": anos[0], "valor": xs[0]},
        "ultimo": {"ano": anos[-1], "valor": xs[-1]},
        "hace_1_ano": {"ano": anos[-2], "valor": xs[-2]},
        "hace_5_anos": ({"ano": anos[-6], "valor": xs[-6]} if len(xs) >= 6 else None),
        "maximo": {"ano": anos[imax], "valor": xs[imax]},
        "minimo": {"ano": anos[imin], "valor": xs[imin]},
        "direccion_1_ano": ("sube" if xs[-1] > xs[-2] else "baja" if xs[-1] < xs[-2] else "estable"),
        "_anos": (anos[0], anos[-1], xs[0], xs[-1]),
    }


def _con_cambio_largo_plazo(desc, es_tasa):
    a0, a1, x0, x1 = desc.pop("_anos")
    clp = {"desde": a0, "hasta": a1}
    if es_tasa:
        clp["delta_pp"] = _round(x1 - x0, 2)
    else:
        clp["delta"] = _round(x1 - x0)
        clp["delta_rel"] = _round(100 * (x1 / x0 - 1), 2) if x0 else None
    desc["cambio_largo_plazo"] = clp
    return desc


def _descriptores_de(serie_dicts):
    """Aplica descriptor_serie a cada indicador de una lista de dicts {ano, td, tp, ...}."""
    out = {}
    for ind in INDS_TENDENCIA:
        vals = [(d["ano"], d[ind]) for d in serie_dicts if d.get(ind) is not None]
        desc = descriptor_serie(vals)
        if desc:
            out[ind] = _con_cambio_largo_plazo(desc, ind in TASAS)
    return out


def build_tendencias(serie_nac):
    """Descriptores de tendencia de la serie nacional para el mes central del último release."""
    mc = serie_nac[-1]["mes_central"]
    serie = [f for f in serie_nac if f["mes_central"] == mc]
    return {
        "nota": f"Serie nacional del mes central {mc} ({MESES_CENTRALES[mc][0]}), año contra año.",
        "mes_central": mc,
        "indicadores": _descriptores_de(serie),
    }


def build_tendencias_cortes(cortes):
    """Descriptores de tendencia por grupo de cada corte (sexo/edad/región/nacionalidad)."""
    out = {}
    for dim, obj in cortes.items():
        grupos = {clave: _descriptores_de(serie) for clave, serie in obj["grupos"].items()}
        out[dim] = {"etiqueta_dim": obj["etiqueta_dim"], "grupos": grupos}
    return out


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    generado = datetime.date.today().isoformat()

    maestra = pd.read_parquet(MAESTRA)
    serie_nac = build_nacional(maestra)
    ult = serie_nac[-1]
    mc = ult["mes_central"]
    release = f"{ult['ano']}-{mc:02d}-{MESES_CENTRALES[mc][0].lower()}"

    micro_path = MICRO_DIR / f"{MESES_CENTRALES[mc][2]}.parquet"
    micro = pd.read_parquet(
        micro_path,
        columns=["ano_trimestre", "edad", "sexo", "region", "nacionalidad", "activ", "fact_cal"],
    )
    cortes, anos_cortes = build_cortes(micro)

    snapshot = build_snapshot(serie_nac, cortes, release, generado)
    tendencias = build_tendencias(serie_nac)
    tendencias_cortes = build_tendencias_cortes(cortes)

    meta = {
        "release": release,
        "generado": generado,
        "generador": "scripts/generar_conocimiento.py",
        "fuentes": {
            "nacional": str(MAESTRA.relative_to(ROOT)),
            "cortes": str(micro_path.relative_to(ROOT)),
        },
        "cobertura_nacional": {
            "desde": f"{serie_nac[0]['ano']}-{serie_nac[0]['mes_central']:02d}",
            "hasta": f"{ult['ano']}-{mc:02d}",
            "periodos": len(serie_nac),
        },
        "cortes_mes_central": mc,
        "cortes_anos": [int(a) for a in anos_cortes],
    }

    def write(nombre, obj):
        (OUT / nombre).write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"  ✓ conocimiento/evidencia/{nombre}")

    print(f"Generando capa de conocimiento — release {release} (generado {generado})")
    write("_meta.json", meta)
    write("snapshot.json", snapshot)
    write("series-nacional.json", {"release": release, "serie": serie_nac})
    write("series-cortes.json", {"release": release, "mes_central": mc, "cortes": cortes})
    write("tendencias.json", {"release": release, **tendencias})
    write("tendencias-cortes.json", {
        "release": release,
        "mes_central": mc,
        "nota": f"Descriptores de tendencia por grupo de cada corte, sobre la serie anual "
                f"comparable del mes central {mc} ({MESES_CENTRALES[mc][0]}), año contra año. "
                f"Fuente: series-cortes.json. Tasas (td/tp/to) en 0-100; cambio_largo_plazo en "
                f"pp para tasas, absoluto + % para stocks.",
        "cortes": tendencias_cortes,
    })
    print("Listo.")


if __name__ == "__main__":
    main()
