# scripts/_column_defs.py

# mapeo común (old_name, new_name)
PUBLIC_COLS = [
    # ── Identificadores temporales ─────────────────────────────────────
    ("ano_trimestre",               "ano_trimestre"),
    ("mes_central",                 "mes_central"),

    # ── Totales de población (miles de personas) ───────────────────────
    ("personas_ocupadas",           "ocupados"),
    ("personas_desocupadas",        "desocupados"),
    ("personas_edad_trabajar",      "poblacion_en_edad_de_trabajar"),
    ("fdt",                         "fuerza_de_trabajo"),
    ("fft",                         "personas_inactivas"),
   

    # ── Ocupados por sexo y nacionalidad ────────────────────────────────
    ("oc_hombres",                  "ocupados_hombres"),
    ("oc_mujeres",                  "ocupados_mujeres"),
    ("oc_chile",                    "ocupados_chilenos"),
    ("oc_extranjero",               "ocupados_extranjeros"),

    # ── Formalidad, TPI y sector ─────────────────────────────────────────
    ("oc_formal",                   "ocupados_formales"),
    ("oc_informal",                 "ocupados_informales"),
    ("oc_tpi",                      "ocupados_tiempo_parcial_involuntario"),
    ("oc_sector_publico",           "ocupados_sector_publico"),
    ("oc_no_sector_publico",        "ocupados_sector_no_publico"),

    # ── Nivel educacional de ocupados ───────────────────────────────────
    ("oc_sin_ed_basica",            "ocupados_sin_educ_basica_completa"),
    ("oc_ed_basica",                "ocupados_educ_basica_completa"),
    ("oc_ed_media",                 "ocupados_educ_media_completa"),
    ("oc_ed_sup",                   "ocupados_educ_superior_completa"),
    ("oc_ed_sup_cft",               "ocupados_educ_superior_cft"),
    ("oc_ed_sup_ip",                "ocupados_educ_superior_ip"),
    ("oc_ed_sup_univ",              "ocupados_educ_superior_universitaria"),

    # ── Calificación ocupacional (CIUO) ─────────────────────────────────
    ("oc_ciuo_alta",                "ocupados_ciuo_grupo_1_3"),
    ("oc_ciuo_media_baja",          "ocupados_ciuo_grupo_4_9"),
    ("oc_ciuo_media",               "ocupados_ciuo_grupo_4_8"),
    ("oc_ciuo_baja",                "ocupados_ciuo_grupo_9"),
    ("oc_ciuo_otras",               "ocupados_ciuo_grupo_otros"),

    # ── Educación superior × CIUO ────────────────────────────────────────
    ("oc_ed_sup_ciuo_alta",         "sup_completa_ciuo_alta"),
    ("oc_ed_sup_ciuo_media_baja",   "sup_completa_ciuo_media_baja"),
    ("oc_ed_sup_ciuo_no_alta",      "sup_completa_ciuo_no_alta"),

    # ── Tasas oficiales del INE (%) ─────────────────────────────────────
    ("tp",                          "tasa_participacion"),
    ("to",                          "tasa_ocupacion"),
    ("td",                          "tasa_desocupacion"),
    ("toi",                         "tasa_informalidad_ocupacional"),
    ("tpl",                         "tasa_presion_laboral"),
    ("su1",                         "tasa_su1"),
    ("su2",                         "tasa_su2"),
    ("su3",                         "tasa_su3"),
    ("su4",                         "tasa_su4"),

    ("horas_1_30",   "ocupados_horas_1_30"),
    ("horas_31_44",  "ocupados_horas_31_44"),
    ("horas_31_39",  "ocupados_horas_31_39"),
    ("horas_40",     "ocupados_horas_40"),
    ("horas_41_44",  "ocupados_horas_41_44"),
    ("horas_45",     "ocupados_horas_45"),
    ("horas_46_mas", "ocupados_horas_46_o_más"),

    # ── Promedios de horas ───────────────────────────────────────────────
    ("promedio_horas_habituales",             "promedio_horas_habituales"),
    ("promedio_horas_efectivas_presente",     "promedio_horas_efectivas_presente"),
    ("promedio_horas_efectivas_total",        "promedio_horas_efectivas_total"),
]

# sufijos para cada mes
SUFIJOS = {
    1: "def",  2: "efm",  3: "fma", 4: "mam",
    5: "amj",  6: "mjj",  7: "jja", 8: "jas",
    9: "aso", 10: "son", 11: "ond", 12: "nde",
}
