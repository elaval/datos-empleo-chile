# scripts/_column_defs.py

# mapeo común (old_name, new_name)
PUBLIC_COLS = [
    # ── Identificadores temporales ─────────────────────────────────────
    ("ano_trimestre", "Año-Trimestre"),
    ("mes_central",   "Mes central"),

    # ── Totales de población ─────────────────────────────────────────────
    ("pet",      "Población en edad de trabajar (PET)"),
    ("ft",       "Fuerza de trabajo (FT)"),
    ("o",        "Personas ocupadas"),
    ("do",       "Personas desocupadas"),
    ("cesantes", "Cesantes"),
    ("busca_trabajo_por_primera_vez", "Buscan trabajo por primera vez"),
    ("fft",      "Fuera de la fuerza de trabajo (FFT)"),
    ("fft_iniciadores", "Iniciadores fuera de la fuerza de trabajo"),
    ("fft_inactivos_potencialmente_activos", "Inactivos potencialmente activos"),
    ("fft_inactivos_habituales",           "Inactivos habituales"),

    # ── Subgrupos especiales ────────────────────────────────────────────
    ("obe",     "Ocupados que buscaron empleo (OBE)"),
    ("id",      "Iniciadores disponibles (ID)"),
    ("ftp",     "Fuerza de trabajo potencial (FTP)"),
    ("fta",     "Fuerza de trabajo ajustada (FTA)"),
    ("deseo_trabajar", "Deseo de trabajar"),

    # ── Ocupados por sexo y origen ──────────────────────────────────────
    ("o_hombres",    "Ocupados hombres"),
    ("o_mujeres",    "Ocupados mujeres"),
    ("o_chile",      "Ocupados chilenos"),
    ("o_extranjero", "Ocupados extranjeros"),

    # ── Formalidad y sector ─────────────────────────────────────────────
    ("o_formal",          "Ocupados formales"),
    ("o_informal",        "Ocupados informales"),
    ("o_sector_informal", "Ocupados en sector informal"),

    # ── Educación ────────────────────────────────────────────────────────
    ("o_sin_basica_completa", "Sin educación básica completa"),
    ("o_ed_basica_completa",  "Educación básica completa"),
    ("o_ed_media_completa",   "Educación media completa"),
    ("o_ed_sup_completa",     "Educación superior completa"),
    ("o_ed_sup_cft",          "Edu. superior en CFT"),
    ("o_ed_sup_ip",           "Edu. superior en IP"),
    ("o_ed_sup_univ",         "Edu. superior universitaria"),

    ("categoria_independientes", "Independientes"),
    ("categoria_empleador",      "Empleador"),
    ("categoria_familiar_personal_no_remunerado", "Familiar personal no remunerado"),
    ("categoria_dependientes",   "Dependientes"),
    ("categoria_asalariados",    "Asalariados"),
    ("categoria_cuenta_propia",  "Cuenta propia"),
    ("categoria_asalariado_sector_privado", "Asalariado sector privado"),
    ("categoria_asalariado_sector_publico",  "Asalariado sector público"),
    ("categoria_servicio_domestico",         "Servicio doméstico"),
    ("categoria_serv_domestico_puertas_afuera", "Servicio doméstico puertas afuera"),
    ("categoria_serv_domestico_puertas_adentro",  "Servicio doméstico puertas adentro"),
    ("categoria_no_corresponde", "No corresponde"),


   # ── Grupos CIUO ──────────────────────────────────────────────────────
    ("grupo_ciuo_alta",       "CIUO grupo alto (1-3)"),
    ("grupo_ciuo_media_baja", "CIUO grupo medio-bajo (4-9)"),
    ("grupo_ciuo_media",      "CIUO grupo medio (4-8)"),
    ("grupo_ciuo_baja",       "CIUO grupo bajo (9)"),
    ("grupo_ciuo_otras",      "CIUO otros"),

    # ── Edu. superior × CIUO ─────────────────────────────────────────────
    ("o_ed_sup_ciuo_alta",       "Ed Supuerior y Grupo CIUO alto"),
    ("o_ed_sup_ciuo_media_baja", "Ed Supuerior y Grupo CIUO medio-bajo"),
    ("o_ed_sup_ciuo_no_alta",    "Ed Supuerior y Grupo CIUO bajo"),

    # ── Grupos CIUO (1 a 10) ────────────────────────────────────────────
    ("grupo_ciuo_1",  "Grupo 1: Directores, gerentes y administradores"),
    ("grupo_ciuo_2",  "Grupo 2: Profesionales, científicos e intelectuales"),
    ("grupo_ciuo_3",  "Grupo 3: Técnicos y profesionales de nivel medio"),
    ("grupo_ciuo_4",  "Grupo 4: Personal de apoyo administrativo"),
    ("grupo_ciuo_5",  "Grupo 5: Trabajadores de servicios y vendedores de comercios y mercados"),
    ("grupo_ciuo_6",  "Grupo 6: Agricultores y trabajadores calif. agropecuarios, forestales y pesqueros"),
    ("grupo_ciuo_7",  "Grupo 7: Artesanos y operarios de oficios"),
    ("grupo_ciuo_8",  "Grupo 8: Operadores de instalaciones, máquinas y ensambladores"),
    ("grupo_ciuo_9",  "Grupo 9: Ocupaciones elementales"),
    ("grupo_ciuo_10", "Grupo 10: Otros no identificados"),
    ("grupo_ciuo_nsnr", "CIUO NS/NR"),

    # ── Ramas de actividad (1 a 21) ──────────────────────────────────────
    ("rama_1",  "Rama 1: Agricultura, ganadería, silvicultura y pesca"),
    ("rama_2",  "Rama 2: Explotación de minas y canteras"),
    ("rama_3",  "Rama 3: Industrias manufactureras"),
    ("rama_4",  "Rama 4: Suministro de electricidad, gas, vapor y aire acondicionado"),
    ("rama_5",  "Rama 5: Suministro de agua"),
    ("rama_6",  "Rama 6: Construcción"),
    ("rama_7",  "Rama 7: Comercio al por mayor y al por menor"),
    ("rama_8",  "Rama 8: Transporte y almacenamiento"),
    ("rama_9",  "Rama 9: Actividades de alojamiento y de servicio de comidas"),
    ("rama_10", "Rama 10: Información y comunicaciones"),
    ("rama_11", "Rama 11: Actividades financieras y de seguros"),
    ("rama_12", "Rama 12: Actividades inmobiliarias"),
    ("rama_13", "Rama 13: Actividades profesionales, científicas y técnicas"),
    ("rama_14", "Rama 14: Actividades de servicios administrativos y de apoyo"),
    ("rama_15", "Rama 15: Administración pública y defensa"),
    ("rama_16", "Rama 16: Enseñanza"),
    ("rama_17", "Rama 17: Actividades de atención de la salud humana y de asistencia social"),
    ("rama_18", "Rama 18: Actividades artísticas, de entretenimiento y recreativas"),
    ("rama_19", "Rama 19: Otras actividades de servicios"),
    ("rama_20", "Rama 20: Actividades de los hogares como empleadores"),
    ("rama_21", "Rama 21: Actividades de organizaciones y órganos extraterritoriales"),

    # ── Horas trabajadas ────────────────────────────────────────────────
    ("horas_1_30", "Horas 1–30"),
    ("tpi",        "Tiempo parcial involuntario (TPI)"),
    ("tpv",        "Tiempo parcial voluntario (TPV)"),
    ("tp_sin_declarar_voluntareidad", "Tiempo parcial sin declarar voluntariedad"),
    ("horas_31_44", "Horas 31–44"),
    ("horas_31_39", "Horas 31–39"),
    ("horas_40",    "Horas 40"),
    ("horas_41_44", "Horas 41–44"),
    ("horas_45",    "Horas 45"),
    ("horas_46_mas","Horas ≥46"),
    ("horas_efectivas_46_mas", "Horas efectivas ≥46"),
    ("o_declaran_horas",      "Ocupados que declaran horas"),

    # ── Promedios de horas ───────────────────────────────────────────────
    ("promedio_horas_efectivas_sin_ausentes",  "Prom. horas efectivas sin ausentes"),
    ("promedio_horas_efectivas_declaran_horas","Prom. horas efectivas (declaran)"),
    ("promedio_horas_habituales",              "Prom. horas habituales"),

    # ── Tasas (%) ────────────────────────────────────────────────────────
    ("td",   "Tasa de desocupación (%)"),
    ("to",   "Tasa de ocupación (%)"),
    ("tp",   "Tasa de participación (%)"),
    ("tpl",  "Tasa de presión laboral (%)"),
    ("su1",  "Tasa SU1 (%)"),
    ("su2",  "Tasa SU2 (%)"),
    ("su3",  "Tasa SU3 (%)"),
    ("su4",  "Tasa SU4 (%)"),
    ("toi",  "Tasa de empleo informal (%)"),
    ("tosi", "Tasa de empleo en sector informal (%)"),
]


# sufijos para cada mes
SUFIJOS = {
    1: "def",  2: "efm",  3: "fma", 4: "mam",
    5: "amj",  6: "mjj",  7: "jja", 8: "jas",
    9: "aso", 10: "son", 11: "ond", 12: "nde",
}
