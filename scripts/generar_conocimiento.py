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

# CISO-18 (segundo nivel). El INE publica ciso1/ciso2 en las bases trimestrales
# solo desde AMJ 2026: antes de esa fecha las columnas vienen NA (no hay serie
# retropolable desde microdatos públicos; ver ADR-0002). NO comparable con
# CATEGORIA_COLS (CISE-93): fusiona servicio doméstico, mueve familiares no
# remunerados a dependientes y separa contratistas dependientes.
CISO18_COLS = {
    "empleador": "ciso_empleador",
    "cuenta_propia": "ciso_cuenta_propia",
    "contratista_dependiente": "ciso_contratistas_dependientes",
    "asalariado_sector_privado": "ciso_asalariado_sector_privado",
    "asalariado_sector_publico": "ciso_asalariado_sector_publico",
    "servicio_domestico": "ciso_servicio_domestico",
    "familiar_no_remunerado": "ciso_familiar_no_remunerado",
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

# Fases de la Ley 21.561, por fecha de entrada en vigencia.
LEY_JORNADA_FASES = (
    (datetime.date(2024, 4, 26), 44),
    (datetime.date(2026, 4, 26), 42),
    (datetime.date(2028, 4, 26), 40),
)
LEY_JORNADA_PREVIA = 45  # jornada máxima antes de la primera fase
MES_NOMBRE = ("enero", "febrero", "marzo", "abril", "mayo", "junio", "julio",
              "agosto", "septiembre", "octubre", "noviembre", "diciembre")


def _meses_del_trimestre(ano: int, mes_central: int) -> list[tuple[int, int]]:
    """Los tres meses (año, mes) que componen el trimestre móvil de ese mes central."""
    idx = ano * 12 + (mes_central - 1)
    return [((k // 12), (k % 12) + 1) for k in (idx - 1, idx, idx + 1)]


def _fase_jornada(ano: int, mes: int):
    """La fase de la Ley 21.561 vigente al EMPEZAR ese mes, o None si es anterior a todas.

    Un mes cuenta dentro de una fase solo si empieza en o después de su fecha de
    vigencia. Como cada fase entra a regir un 26 de abril, el abril correspondiente
    queda siempre del lado anterior: lo capta a medias y no se le atribuye.
    """
    inicio = datetime.date(ano, mes, 1)
    vigente = None
    for fecha, horas in LEY_JORNADA_FASES:
        if inicio >= fecha:
            vigente = (fecha, horas)
    return vigente


def _nota_jornada_legal(ano: int, mes_central: int) -> str:
    """Describe cómo se sitúa el trimestre móvil frente a las fases de la Ley 21.561.

    Se CALCULA, no se escribe a mano: un texto fijo queda falso en cuanto avanza el
    release. La versión anterior afirmaba «el trimestre AMJ 2026 capta solo
    parcialmente la fase de 42 h» y siguió diciéndolo en JJA y JAS 2026, cuando ya
    era falso.
    """
    etiqueta = f"{MESES_CENTRALES[mes_central][0]} {ano}"
    meses = _meses_del_trimestre(ano, mes_central)
    fases = [_fase_jornada(a, m) for a, m in meses]

    def legible(fase):
        fecha, _ = fase
        return f"{fecha.day} de {MES_NOMBRE[fecha.month - 1]} de {fecha.year}"

    if len(set(fases)) == 1:
        fase = fases[0]
        if fase is None:
            primera_fecha, primera_horas = LEY_JORNADA_FASES[0]
            return (f"El trimestre {etiqueta} es anterior a la primera fase de la Ley "
                    f"21.561 ({primera_horas} h desde el "
                    f"{primera_fecha.day} de {MES_NOMBRE[primera_fecha.month - 1]} de "
                    f"{primera_fecha.year}): la jornada máxima legal de sus tres meses "
                    f"es {LEY_JORNADA_PREVIA} h.")
        return (f"El trimestre {etiqueta} está enteramente dentro de la fase de "
                f"{fase[1]} h, vigente desde el {legible(fase)}.")

    ultima = fases[-1]
    posteriores = sum(1 for f in fases if f == ultima)
    cuenta = {1: "uno de sus tres meses es posterior",
              2: "dos de sus tres meses son posteriores"}[posteriores]
    return (f"El trimestre {etiqueta} cae en la transición a la fase de {ultima[1]} h, "
            f"vigente desde el {legible(ultima)}: {cuenta}.")

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

# Composición de la desocupación. Partición EXACTA de `do`: quien perdió un empleo
# (cesante) y quien busca por primera vez. Serie completa desde 2010-02.
DESOCUPADOS_COLS = {
    "cesantes": "cesantes",
    "busca_trabajo_primera_vez": "busca_trabajo_por_primera_vez",
}
DESOCUPADOS_ETIQUETA = {
    "cesantes": "Cesantes (tuvieron empleo antes)",
    "busca_trabajo_primera_vez": "Buscan trabajo por primera vez",
}

# Rama de actividad económica del empleo principal: CAENES rev. 4, 21 secciones.
# Se construye desde `b14_rev4cl_caenes` (ver el comentario de las reglas en
# generar_totales_trimestrales.py: `r_p_rev4cl_caenes` es otra variable y no
# reproduce el boletín del INE).
# ⚠ El INE publica esta clasificación desde JAS 2017. Antes la vigente
# era CIIU rev. 3, que NO es empalmable con esta a nivel de sección: los trimestres
# anteriores salen en NA y el bloque del snapshot no se emite.
# ⚠ Las 21 secciones NO suman el total de ocupados: hay casos sin rama declarada.
# El residuo se expone en `_cobertura` (igual que en educación y jornada).
RAMA_COLS = {f"r{i:02d}": f"rama_{i}" for i in range(1, 22)}
RAMA_ETIQUETA = {
    "r01": "Agricultura, ganadería, silvicultura y pesca",
    "r02": "Explotación de minas y canteras",
    "r03": "Industrias manufactureras",
    "r04": "Suministro de electricidad, gas, vapor y aire acondicionado",
    "r05": "Suministro de agua, alcantarillado y gestión de residuos",
    "r06": "Construcción",
    "r07": "Comercio al por mayor y al por menor",
    "r08": "Transporte y almacenamiento",
    "r09": "Alojamiento y servicio de comidas",
    "r10": "Información y comunicaciones",
    "r11": "Actividades financieras y de seguros",
    "r12": "Actividades inmobiliarias",
    "r13": "Actividades profesionales, científicas y técnicas",
    "r14": "Servicios administrativos y de apoyo",
    "r15": "Administración pública y defensa",
    "r16": "Enseñanza",
    "r17": "Salud humana y asistencia social",
    "r18": "Actividades artísticas, de entretenimiento y recreativas",
    "r19": "Otras actividades de servicios",
    "r20": "Hogares como empleadores",
    "r21": "Organizaciones y órganos extraterritoriales",
}

# Tipo de vínculo contractual de los dependientes (asalariados privados y públicos +
# servicio doméstico): categoria_ocupacion 3-6, que es exactamente el universo que
# responde b8/b9 en la ENE. Serie completa desde 2010-02.
#
# ⚠ DOS DENOMINADORES DISTINTOS, y confundirlos infla la cifra:
#   · «% con contrato escrito» se calcula sobre los dependientes (b8);
#   · «% indefinido» TAMBIÉN se calcula sobre los dependientes, no sobre los que tienen
#     contrato escrito, porque b9 pregunta por la duración del «contrato O ACUERDO de
#     trabajo» y se le hace a todos los dependientes, con contrato escrito o sin él.
#
# Identificación de las variables verificada contra una cifra publicada por el INE
# (ver ADR-0004 y el comentario de las reglas en generar_totales_trimestrales.py).
CONTRATO_COLS = {
    "con_contrato_escrito": "dep_contrato_escrito",
    "sin_contrato_escrito": "dep_sin_contrato_escrito",
    "plazo_indefinido": "dep_plazo_indefinido",
    "plazo_definido": "dep_plazo_definido",
}
CONTRATO_DEFINIDO_COLS = {
    "temporada": "dep_definido_temporada",
    "obra_o_proyecto": "dep_definido_obra",
    "menos_de_3_meses": "dep_definido_menos_3_meses",
    "renovable_anual": "dep_definido_renovable_anual",
    "reemplazo": "dep_definido_reemplazo",
}
CONTRATO_VIA_COLS = {
    "directo_con_la_empresa": "dep_contratado_directamente",
    "contratista_o_subcontratista": "dep_subcontratado",
    "empresa_de_servicios_temporales": "dep_servicios_temporales",
    "enganchador_agricola": "dep_enganchador",
}
CONTRATO_ETIQUETA = {
    "con_contrato_escrito": "Con contrato escrito",
    "sin_contrato_escrito": "Sin contrato escrito (acuerdo de palabra)",
    "plazo_indefinido": "Contrato o acuerdo indefinido",
    "plazo_definido": "Contrato o acuerdo de plazo definido",
    "temporada": "Limitado a la temporada",
    "obra_o_proyecto": "Por obra, proyecto o faena",
    "menos_de_3_meses": "Menos de tres meses (prueba o práctica)",
    "renovable_anual": "Renovable una vez al año",
    "reemplazo": "Por reemplazo",
    "directo_con_la_empresa": "Directamente con la empresa donde trabaja",
    "contratista_o_subcontratista": "Con un contratista o subcontratista",
    "empresa_de_servicios_temporales": "Con una empresa de servicios temporales",
    "enganchador_agricola": "Con un enganchador (contratista agrícola)",
}

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
            # NA antes de AMJ 2026 (inicio de publicación CISO-18; ver ADR-0002)
            "ciso18": {
                k: _round(r[col]) for k, col in CISO18_COLS.items() if col in m.columns
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
            # Partición exacta de los desocupados; serie completa desde 2010-02.
            "composicion_desocupados": {
                k: _round(r[col]) for k, col in DESOCUPADOS_COLS.items() if col in m.columns
            },
            # NA antes de JAS 2017 (inicio de CAENES rev. 4 en la ENE).
            "rama_actividad": {
                k: _round(r[col]) for k, col in RAMA_COLS.items() if col in m.columns
            },
            # Vínculo contractual de los dependientes; serie completa desde 2010-02.
            "vinculo_contractual": {
                "dependientes": (_round(r["categoria_dependientes"])
                                 if "categoria_dependientes" in m.columns else None),
                **{k: _round(r[col]) for k, col in CONTRATO_COLS.items() if col in m.columns},
                "plazo_definido_por_tipo": {
                    k: _round(r[col]) for k, col in CONTRATO_DEFINIDO_COLS.items()
                    if col in m.columns
                },
                "via_de_contratacion": {
                    k: _round(r[col]) for k, col in CONTRATO_VIA_COLS.items() if col in m.columns
                },
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

    # CISO-18: solo si el release tiene datos (desde AMJ 2026). Sin serie previa
    # en microdatos públicos, el delta interanual existirá recién cuando el año
    # anterior también traiga la clasificación (AMJ 2027 en adelante).
    ciso_ult = ult.get("ciso18") or {}
    ciso_prev = (prev.get("ciso18") or {}) if prev else {}
    total_o = nac.get("o")
    ciso18 = None
    if any(v is not None for v in ciso_ult.values()):
        ciso18 = {
            "nota": (
                "Clasificación CISO-18 (segundo nivel). Publicada por el INE en las bases "
                "trimestrales desde AMJ 2026: no hay serie previa reproducible desde microdatos "
                "públicos, y NO es comparable con composicion_ocupados (CISE-93). Ver ADR-0002."
            ),
            "categorias": {
                cat: {
                    "o": v,
                    "pct_ocupados": _round(100 * v / total_o, 2) if total_o else None,
                    **(
                        {
                            "delta_o": _round(v - ciso_prev[cat]),
                            "delta_rel_o": _round(100 * (v / ciso_prev[cat] - 1), 2),
                        }
                        if ciso_prev.get(cat) is not None else {}
                    ),
                }
                for cat, v in ciso_ult.items() if v is not None
            },
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

    # Composición de la desocupación: cesantía vs. primera búsqueda. Partición exacta
    # de `do`, así que el residuo de `_cobertura` debe ser 0.
    des_ult = ult["composicion_desocupados"]
    des_prev = prev["composicion_desocupados"] if prev else None
    total_do = nac.get("do")
    desocupados = {
        "nota": "Partición exacta de los desocupados: cesantes son quienes tuvieron un "
                "empleo antes y lo perdieron; el resto busca trabajo por primera vez. "
                "La distinción separa destrucción de empleo de dificultad de entrada.",
        "grupos": {
            k: {
                "etiqueta": DESOCUPADOS_ETIQUETA[k],
                "pct_desocupados": _round(100 * v / total_do, 2) if (v and total_do) else None,
                **_comp_entry(v, (des_prev or {}).get(k)),
            }
            for k, v in des_ult.items()
        },
    }
    suma_des = sum(v for v in des_ult.values() if v is not None)
    desocupados["_cobertura"] = {
        "suma_grupos": _round(suma_des),
        "desocupados": _round(total_do),
        "residuo": _round(total_do - suma_des) if total_do is not None else None,
    }

    # Vínculo contractual de los dependientes. Las dos proporciones que importan van con
    # su denominador escrito al lado, porque son distintas de lo que el lector supone:
    # el «% indefinido» se calcula sobre todos los dependientes, no sobre los que tienen
    # contrato escrito (b9 pregunta por «contrato o acuerdo», ver CONTRATO_COLS).
    vc_ult = ult.get("vinculo_contractual") or {}
    vc_prev = (prev.get("vinculo_contractual") or {}) if prev else {}
    contrato = None
    if vc_ult.get("dependientes"):
        dep, dep_prev = vc_ult["dependientes"], vc_prev.get("dependientes")

        def _prop(clave):
            v, vp = vc_ult.get(clave), vc_prev.get(clave)
            e = {"etiqueta": CONTRATO_ETIQUETA[clave], "personas": v,
                 "pct_dependientes": _round(100 * v / dep, 2) if (v and dep) else None}
            if v is not None and vp is not None:
                e["delta_personas"] = _round(v - vp)
                if dep_prev:
                    e["delta_pp"] = _round(100 * v / dep - 100 * vp / dep_prev, 2)
            return e

        contrato = {
            "nota": ("Vínculo contractual de los dependientes (asalariados privados y "
                     "públicos más servicio doméstico), que son quienes la ENE pregunta. "
                     "Empleadores, cuenta propia y familiares no remunerados quedan fuera "
                     "del universo, no en cero."),
            "denominador": {"dependientes": dep,
                            "delta_dependientes": (_round(dep - dep_prev) if dep_prev else None)},
            "contrato_escrito": {k: _prop(k) for k in
                                 ("con_contrato_escrito", "sin_contrato_escrito")},
            "duracion": {k: _prop(k) for k in ("plazo_indefinido", "plazo_definido")},
            "plazo_definido_por_tipo": {
                k: {"etiqueta": CONTRATO_ETIQUETA[k],
                    **_comp_entry(v, (vc_prev.get("plazo_definido_por_tipo") or {}).get(k))}
                for k, v in (vc_ult.get("plazo_definido_por_tipo") or {}).items()
            },
            "via_de_contratacion": {
                k: {"etiqueta": CONTRATO_ETIQUETA[k],
                    "pct_dependientes": _round(100 * v / dep, 2) if (v and dep) else None,
                    **_comp_entry(v, (vc_prev.get("via_de_contratacion") or {}).get(k))}
                for k, v in (vc_ult.get("via_de_contratacion") or {}).items()
            },
        }
        esc = (vc_ult.get("con_contrato_escrito") or 0) + (vc_ult.get("sin_contrato_escrito") or 0)
        dur = (vc_ult.get("plazo_indefinido") or 0) + (vc_ult.get("plazo_definido") or 0)
        tipos = sum(v for v in (vc_ult.get("plazo_definido_por_tipo") or {}).values() if v)
        definido = vc_ult.get("plazo_definido") or 0
        contrato["_cobertura"] = {
            "nota": "El residuo son dependientes que no saben o no responden la pregunta.",
            "dependientes": dep,
            "responden_contrato_escrito": _round(esc),
            "sin_dato_contrato_escrito": _round(dep - esc),
            "responden_duracion": _round(dur),
            "sin_dato_duracion": _round(dep - dur),
            # b10 se pregunta SOLO a quien declara plazo definido, y tiene sus propios
            # códigos de no sabe / no responde: los tipos no cierran contra el total.
            "suma_tipos_de_plazo": _round(tipos),
            "plazo_definido": _round(definido),
            "sin_dato_tipo_de_plazo": _round(definido - tipos),
        }

    # Rama de actividad económica (CAENES rev. 4). Solo si el release la trae.
    rama = None
    ram_ult = ult.get("rama_actividad") or {}
    if any(v is not None for v in ram_ult.values()):
        ram_prev = (prev.get("rama_actividad") or {}) if prev else {}
        rama = {
            "clasificacion": "CAENES rev. 4 (21 secciones)",
            "nota_quiebre": "La ENE clasifica la rama con CAENES rev. 4 desde JAS 2017. Antes "
                            "usaba CIIU rev. 3, que no es empalmable a nivel de sección: no "
                            "existe serie de rama anterior a ese trimestre.",
            "ramas": {
                k: {
                    "etiqueta": RAMA_ETIQUETA[k],
                    "pct_ocupados": _round(100 * v / total_o, 2) if (v and total_o) else None,
                    **_comp_entry(v, ram_prev.get(k)),
                }
                for k, v in ram_ult.items() if v is not None
            },
        }
        suma_ram = sum(v for v in ram_ult.values() if v is not None)
        suma_ram_prev = (sum(v for v in ram_prev.values() if v is not None)
                         if ram_prev else None)
        sin_rama = total_o - suma_ram if total_o is not None else None
        sin_rama_prev = (prev["o"] - suma_ram_prev
                         if (prev and suma_ram_prev) else None)
        rama["_cobertura"] = {
            "nota": "Las 21 secciones no suman el total de ocupados: hay casos sin rama "
                    "declarada. Para cuadrar la variación por rama con la nacional hay que "
                    "incluir la variación del residuo.",
            "suma_ramas": _round(suma_ram),
            "ocupados": _round(total_o),
            "sin_rama_declarada": _round(sin_rama),
            "sin_rama_declarada_previo": _round(sin_rama_prev),
            "delta_sin_rama_declarada": (_round(sin_rama - sin_rama_prev)
                                         if sin_rama_prev is not None else None),
        }

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
            "nota": _nota_jornada_legal(ult["ano"], ult["mes_central"]),
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
    # Cada etiqueta declara sobre qué se construye la tasa. SU1 NO es la TD: le suma los
    # iniciadores disponibles (al numerador y al denominador), por eso es algo mayor.
    ETIQ_SU = {
        "su1": "SU1 · TD + iniciadores disponibles",
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
        "ciso18": ciso18,
        "composicion_desocupados": desocupados,
        "vinculo_contractual": contrato,
        "rama_actividad": rama,
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


# --------------------------------------------------------------------------
# 5. DESCOMPOSICIÓN COMPOSICIÓN / INTRA-GRUPO (shift-share)
# --------------------------------------------------------------------------
# Una tasa nacional es el promedio ponderado de las tasas de sus grupos, con pesos
# iguales a la participación de cada grupo en el denominador. Cuando la tasa nacional
# se mueve, hay dos razones posibles y conviene no confundirlas:
#
#   · CAMBIÓ QUIÉN COMPONE la población (más adultos mayores, más población extranjera);
#   · CAMBIÓ LA SITUACIÓN DENTRO de cada grupo.
#
# Se usa la descomposición simétrica (pesos y tasas promediados entre los dos años), que
# es EXACTA: composición + intra = variación total, sin residuo. Demostración:
#   Σ Δw·(r₀+r₁)/2 + Σ (w₀+w₁)/2·Δr = Σ w₁r₁ − Σ w₀r₀
# La alternativa asimétrica (pesos del año base) deja un término de interacción que hay
# que repartir a mano, y repartirlo es una decisión que nadie podría auditar después.
#
# ⚠ Los cortes son de UNA dimensión. La descomposición por edad no controla por sexo ni al
# revés: son lentes alternativos sobre el mismo cambio, no sumandos de una partición común.
TASAS_DESCOMPONIBLES = {
    # tasa: (numerador, denominador, qué es el ponderador)
    "td": ("do", "ft", "participación del grupo en la fuerza de trabajo"),
    "tp": ("ft", "pet", "participación del grupo en la población en edad de trabajar"),
    "to": ("o", "pet", "participación del grupo en la población en edad de trabajar"),
}


def _descomponer(grupos: dict, ano0: int, ano1: int, num: str, den: str):
    """Shift-share simétrico de una tasa entre dos años. Devuelve None si falta un año."""
    filas = {}
    for clave, serie in grupos.items():
        f0 = next((x for x in serie if x["ano"] == ano0), None)
        f1 = next((x for x in serie if x["ano"] == ano1), None)
        if not f0 or not f1 or not f0.get(den) or not f1.get(den):
            return None
        filas[clave] = (f0, f1)

    tot0 = sum(f0[den] for f0, _ in filas.values())
    tot1 = sum(f1[den] for _, f1 in filas.values())
    if not tot0 or not tot1:
        return None

    tasa0 = 100 * sum(f0[num] for f0, _ in filas.values()) / tot0
    tasa1 = 100 * sum(f1[num] for _, f1 in filas.values()) / tot1
    # Tasa nacional promedio de los dos años: CENTRA el aporte de composición de cada grupo.
    # Sin centrar, el aporte por grupo es Δpeso × tasa del grupo, y eso NO se puede leer solo:
    # como los pesos suman 1 en los dos años, Σ Δpeso = 0, y el signo de cada término queda
    # dictado por el nivel de la tasa del grupo en vez de por su posición respecto del país.
    # El caso que lo delató: entre 2010 y 2026 los jóvenes 15-24 pasan de 21,67 % a 15,19 % de
    # la PET y su tasa de ocupación es la más baja de todas; sin centrar su aporte sale −1,69 pp,
    # que leído solo dice «la caída del peso juvenil bajó la ocupación nacional», y es al revés.
    # Centrado da +1,91 pp: menos peso en el grupo de tasa más baja EMPUJA la tasa nacional
    # hacia arriba. El total no cambia — Σ Δpeso × tasa_media_nacional = 0 — así que centrar
    # arregla la lectura por grupo sin tocar la aritmética del agregado.
    tasa_media = (tasa0 + tasa1) / 2

    comp_total, intra_total, detalle = 0.0, 0.0, []
    for clave, (f0, f1) in filas.items():
        w0, w1 = f0[den] / tot0, f1[den] / tot1
        r0, r1 = 100 * f0[num] / f0[den], 100 * f1[num] / f1[den]
        comp = (w1 - w0) * ((r0 + r1) / 2 - tasa_media)
        intra = (w0 + w1) / 2 * (r1 - r0)
        comp_total += comp
        intra_total += intra
        detalle.append({
            "clave": clave,
            "peso_desde_pct": _round(100 * w0, 2),
            "peso_hasta_pct": _round(100 * w1, 2),
            "tasa_desde": _round(r0, 2),
            "tasa_hasta": _round(r1, 2),
            "aporte_composicion_pp": _round(comp, 3),
            "aporte_intra_pp": _round(intra, 3),
        })
    detalle.sort(key=lambda d: abs(d["aporte_intra_pp"] + d["aporte_composicion_pp"]), reverse=True)
    return {
        "tasa_desde": _round(tasa0, 2),
        "tasa_hasta": _round(tasa1, 2),
        "delta_pp": _round(tasa1 - tasa0, 2),
        "efecto_composicion_pp": _round(comp_total, 3),
        "efecto_intra_pp": _round(intra_total, 3),
        "residuo_pp": _round((tasa1 - tasa0) - (comp_total + intra_total), 6),
        "grupos": detalle,
    }


def build_descomposicion(cortes: dict, serie_nac: list, mes_central: int):
    ult = serie_nac[-1]["ano"]
    horizontes = [
        (ult - 1, ult, "último año"),
        (2019, ult, "contra el último trimestre previo a la pandemia"),
        (serie_nac[0]["ano"], ult, "toda la serie"),
    ]
    salida = []
    for ano0, ano1, etiqueta in horizontes:
        if ano0 >= ano1:
            continue
        tasas = {}
        for tasa, (num, den, pond) in TASAS_DESCOMPONIBLES.items():
            dims = {}
            for dim, obj in cortes.items():
                d = _descomponer(obj["grupos"], ano0, ano1, num, den)
                if d:
                    dims[dim] = {"etiqueta_dim": obj["etiqueta_dim"], **d}
            if dims:
                tasas[tasa] = {"ponderador": pond, "dimensiones": dims}
        if tasas:
            salida.append({"desde": ano0, "hasta": ano1, "etiqueta": etiqueta, "tasas": tasas})
    return {
        "mes_central": mes_central,
        "nota": (
            "Separa cuánto del movimiento de una tasa nacional viene de que cambió la "
            "composición de la población y cuánto de que cambió la situación dentro de cada "
            "grupo. Es aritmética exacta sobre los cortes publicados: composición + intra = "
            "variación total, con residuo 0. No establece causas."
        ),
        "metodo": (
            "Descomposición simétrica (shift-share): el aporte de composición de cada grupo es "
            "Δpeso × (tasa promedio del grupo − tasa promedio nacional), y el aporte intra-grupo "
            "es peso promedio × Δtasa del grupo. La suma sobre los grupos reproduce exactamente "
            "la variación de la tasa nacional. El aporte de composición va CENTRADO en la tasa "
            "nacional: sin centrar, el signo de cada grupo lo dicta el nivel de su tasa y no su "
            "posición respecto del país, y el número por grupo se lee al revés (los pesos suman "
            "1 en los dos años, así que Σ Δpeso = 0 y centrar no altera el total)."
        ),
        "advertencias": [
            "Los cortes son de UNA dimensión: la descomposición por edad no controla por sexo "
            "ni al revés. Cada dimensión es un lente alternativo sobre el mismo cambio, no un "
            "sumando de una partición común.",
            "Un aporte grande de composición no dice que la composición sea la causa: dice que, "
            "con las tasas de cada grupo congeladas, el solo cambio de pesos habría movido la "
            "tasa nacional en esa magnitud.",
            "Los grupos con n muestral chico (ver `n` en series-cortes.json) aportan aritmética "
            "frágil: el error muestral de su tasa viaja al aporte.",
        ],
        "horizontes": salida,
    }


# --------------------------------------------------------------------------
# 6. FLUJOS — la misma persona doce meses después
# --------------------------------------------------------------------------
# `idrph` identifica a la misma persona entre trimestres, así que el panel rotativo
# de la ENE permite seguirla. Comprobado, no supuesto: en el enlace JAS 2025 → JAS
# 2026 coinciden el sexo en 99,75 % de los casos, la región en 99,98 % y la edad
# avanza 0 a 2 años en 98,69 %. Y los pares comparten TODOS el mes de entrevista,
# así que el intervalo es exactamente doce meses, no «alrededor de un año».
#
# ESTO NO ES UNA ESTIMACIÓN POBLACIONAL Y NO PUEDE PRESENTARSE COMO TAL:
#   · `fact_cal` es un ponderador transversal, diseñado para representar a la
#     población en UN trimestre, no para la submuestra que permanece doce meses.
#     Se publican las dos versiones —sin ponderar y ponderando por el factor del
#     año base— para que la distancia entre ambas quede a la vista.
#   · la permanencia es de ~26 % y NO es aleatoria: el bloque `sesgo_de_permanencia`
#     mide su dirección comparando los indicadores del año base en la submuestra
#     enlazada contra la muestra completa del mismo año. El sesgo tiene signo
#     constante en los dieciséis pares: la submuestra SUBESTIMA la desocupación.
#     Esa es la corrección que el lector tiene que tener en mente, y por eso va
#     pegada a cada par en vez de en una nota al pie.
#   · el par 2019-2020 NO es enlazable: 3 personas de 86.031. La pandemia cortó el
#     panel. No hay transición que cruce el shock y se declara en `no_derivable`.
ESTADOS = {1: "ocupado", 2: "desocupado", 3: "fuera_de_la_fuerza_de_trabajo"}
MIN_ENLACES = 1000  # bajo este umbral no se publica matriz: el error la haría ilegible


def _transiciones(par, col_peso=None):
    """Matriz de transición: proporciones por fila (estado de origen)."""
    out = {}
    for cod, nombre in ESTADOS.items():
        fila = par[par.activ0 == cod]
        if not len(fila):
            continue
        n = len(fila)
        w = fila[col_peso].sum() if col_peso else n
        destinos = {}
        for cod1, nombre1 in ESTADOS.items():
            sel = fila[fila.activ1 == cod1]
            destinos[f"a_{nombre1}"] = _round(
                100 * ((sel[col_peso].sum() if col_peso else len(sel)) / w), 2) if w else None
        out[nombre] = {"n": n, **destinos}
    return out


def build_flujos(micro, mes_central: int):
    m = micro[micro["edad"] >= 15].copy()
    m["ano_trimestre"] = m["ano_trimestre"].astype(int)
    anos = sorted(int(x) for x in m["ano_trimestre"].unique())
    pares, no_derivable = [], {}

    for y0, y1 in zip(anos, anos[1:]):
        a = m[m.ano_trimestre == y0]
        b = m[m.ano_trimestre == y1]
        par = a.merge(b, on="idrph", suffixes=("0", "1"))
        n_base, n_enl = len(a), len(par)

        def _ind(d, suf="", peso=None):
            w = d[peso] if peso else pd.Series(1.0, index=d.index)
            pet = w.sum()
            o = w[d["activ" + suf] == 1].sum()
            do = w[d["activ" + suf] == 2].sum()
            ft = o + do
            return (_round(100 * o / pet, 2) if pet else None,
                    _round(100 * do / ft, 2) if ft else None)

        to_f, td_f = _ind(a)
        enlace = {
            "n_muestra_base": n_base,
            "n_enlazados": n_enl,
            "pct_permanencia": _round(100 * n_enl / n_base, 1) if n_base else None,
            "intervalo": "exactamente 12 meses (todos los pares comparten mes de entrevista)",
        }
        if n_enl < MIN_ENLACES:
            no_derivable[f"{y0}-{y1}"] = (
                f"No enlazable: {n_enl} personas de {n_base:,} en la muestra base. Sin "
                f"transiciones para este par.".replace(",", ".")
            )
            pares.append({"desde": y0, "hasta": y1, "enlace": enlace,
                          "sesgo_de_permanencia": None, "transiciones": None})
            continue

        to_e, td_e = _ind(par, "0")
        pares.append({
            "desde": y0,
            "hasta": y1,
            "enlace": enlace,
            "sesgo_de_permanencia": {
                "nota": ("Indicadores del AÑO BASE calculados sobre la submuestra que "
                         "permanece, contra la muestra completa del mismo año. La diferencia "
                         "es la dirección del sesgo de permanencia, no una corrección "
                         "aplicable: no se puede restar de las transiciones."),
                "to_muestra_completa": to_f, "to_enlazados": to_e,
                "sesgo_to_pp": _round(to_e - to_f, 2) if (to_e and to_f) else None,
                "td_muestra_completa": td_f, "td_enlazados": td_e,
                "sesgo_td_pp": _round(td_e - td_f, 2) if (td_e and td_f) else None,
            },
            "transiciones": {
                "nota": ("Proporciones por fila dentro de la submuestra enlazada. NO son "
                         "estimaciones poblacionales."),
                "sin_ponderar": _transiciones(par),
                "ponderado_por_factor_del_ano_base": _transiciones(par, "fact_cal0"),
            },
            "entre_los_que_siguen_ocupados": _sigue_ocupado(par),
        })

    return {
        "mes_central": mes_central,
        "nota": ("Transiciones de la MISMA persona a doce meses, enlazada por `idrph` en el "
                 "panel rotativo de la ENE. Mide flujos de personas, no diferencias entre dos "
                 "fotos agregadas. No es una estimación poblacional: ver advertencias."),
        "metodo": ("Para cada par de años consecutivos del mes central, se enlazan por `idrph` "
                   "las personas de 15 años o más presentes en los dos años y se tabula el "
                   "estado de actividad en t contra t+12. Todos los pares comparten mes de "
                   "entrevista, así que el intervalo es exactamente doce meses."),
        "advertencias": [
            "`fact_cal` es un ponderador TRANSVERSAL: representa a la población en un "
            "trimestre, no a la submuestra que permanece doce meses. Por eso las matrices se "
            "publican sin ponderar y ponderadas, y ninguna de las dos es un nivel poblacional.",
            "La permanencia ronda el 26 % y no es aleatoria. El bloque `sesgo_de_permanencia` "
            "lo mide: la submuestra enlazada SUBESTIMA la desocupación del año base en todos "
            "los pares. Cualquier lectura de las transiciones tiene que cargar con eso.",
            "Las transiciones describen qué pasó con esas personas, no por qué. Un flujo de "
            "ocupado a fuera de la fuerza de trabajo no dice si fue desaliento, estudio, "
            "cuidado o jubilación: eso no es derivable de esta capa.",
            "El enlace se verificó por coherencia de sexo, región y edad (99,75 %, 99,98 % y "
            "98,69 % en el par más reciente). Un residuo de enlaces falsos es inevitable.",
        ],
        "no_derivable": no_derivable,
        "pares": pares,
    }


def _sigue_ocupado(par):
    """Qué cambió para quienes están ocupados en los dos años."""
    oo = par[(par.activ0 == 1) & (par.activ1 == 1)]
    if not len(oo):
        return None
    out = {"n": len(oo)}
    if "categoria_ocupacion0" in oo.columns:
        cambio = (oo.categoria_ocupacion0 != oo.categoria_ocupacion1) & \
                 oo.categoria_ocupacion0.notna() & oo.categoria_ocupacion1.notna()
        base = (oo.categoria_ocupacion0.notna() & oo.categoria_ocupacion1.notna()).sum()
        out["cambio_de_categoria_ocupacional_pct"] = (
            _round(100 * cambio.sum() / base, 2) if base else None)
    if "ocup_form0" in oo.columns:
        val = oo[oo.ocup_form0.isin([1, 2]) & oo.ocup_form1.isin([1, 2])]
        if len(val):
            out["formalidad"] = {
                "n": len(val),
                "formal_a_informal_pct": _round(
                    100 * len(val[(val.ocup_form0 == 1) & (val.ocup_form1 == 2)]) / len(val), 2),
                "informal_a_formal_pct": _round(
                    100 * len(val[(val.ocup_form0 == 2) & (val.ocup_form1 == 1)]) / len(val), 2),
                "sigue_informal_pct": _round(
                    100 * len(val[(val.ocup_form0 == 2) & (val.ocup_form1 == 2)]) / len(val), 2),
            }
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
        columns=["ano_trimestre", "edad", "sexo", "region", "nacionalidad", "activ", "fact_cal",
                 "idrph", "categoria_ocupacion", "ocup_form"],
    )
    cortes, anos_cortes = build_cortes(micro)

    snapshot = build_snapshot(serie_nac, cortes, release, generado)
    tendencias = build_tendencias(serie_nac)
    tendencias_cortes = build_tendencias_cortes(cortes)
    descomposicion = build_descomposicion(cortes, serie_nac, mc)
    flujos = build_flujos(micro, mc)

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
    write("descomposicion.json", {"release": release, **descomposicion})
    write("flujos.json", {"release": release, **flujos})
    print("Listo.")


if __name__ == "__main__":
    main()
