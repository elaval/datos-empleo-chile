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

    # ── Grupos CIUO-08 (1 a 10) ─────────────────────────────────────────
    #("grupo_ciuo08_1",   "Grupo CIUO08 1: Directores y gerentes"),
    #("grupo_ciuo08_2",   "Grupo CIUO08 2: Profesionales científicos e intelectuales"),
    #("grupo_ciuo08_3",   "Grupo CIUO08 3: Técnicos y profesionales de nivel medio"),
    #("grupo_ciuo08_4",   "Grupo CIUO08 4: Personal de apoyo administrativo"),
    #("grupo_ciuo08_5",   "Grupo CIUO08 5: Trabajadores de los servicios y vendedores de comercios y mercados"),
    #("grupo_ciuo08_6",   "Grupo CIUO08 6: Agricultores y trabajadores calificados agropecuarios, forestales y pesqueros"),
    #("grupo_ciuo08_7",   "Grupo CIUO08 7: Oficiales, operarios y artesanos de artes mecánicas y de otros oficios"),
    #("grupo_ciuo08_8",   "Grupo CIUO08 8: Operadores de instalaciones y máquinas y ensambladores"),
    #("grupo_ciuo08_9",   "Grupo CIUO08 9: Ocupaciones elementales"),
    #("grupo_ciuo08_10",  "Grupo CIUO08 10: Otros no identificados"),
    #("grupo_ciuo08_nsnr","CIUO08 NS/NR"),

    # ── Grupos CIUO-88 (1 a 10) ─────────────────────────────────────────
    #("grupo_ciuo88_1",   "Grupo CIUO88 1: Miembros del poder ejecutivo y de los cuerpos legislativos y personal directivo de la administración pública y de empresas"),
    #("grupo_ciuo88_2",   "Grupo CIUO88 2: Profesionales científicos e intelectuales"),
    #("grupo_ciuo88_3",   "Grupo CIUO88 3: Técnicos profesionales de nivel medio"),
    #("grupo_ciuo88_4",   "Grupo CIUO88 4: Empleados de oficina"),
    #("grupo_ciuo88_5",   "Grupo CIUO88 5: Trabajadores de los servicios y vendedores de comercios y mercados"),
    #("grupo_ciuo88_6",   "Grupo CIUO88 6: Agricultores y trabajadores calificados agropecuarios y pesqueros"),
    #("grupo_ciuo88_7",   "Grupo CIUO88 7: Oficiales, operarios y artesanos de artes mecánicas y de otros oficios"),
    #("grupo_ciuo88_8",   "Grupo CIUO88 8: Operadores de instalaciones y máquinas y montadores"),
    #("grupo_ciuo88_9",   "Grupo CIUO88 9: Trabajadores no calificados"),
    #("grupo_ciuo88_10",  "Grupo CIUO88 10: Otros no clasificados"),
    #("grupo_ciuo88_nsnr","CIUO88 NS/NR"),

    # ── Grupos CIUO-08 (rótulos INE) ─────────────────────────────────────
    ("grupo_ciuo08_1",   "CIUO08 G1 Directivos y gerentes"),
    ("grupo_ciuo08_2",   "CIUO08 G2 Profesionales, científicos e intelectuales"),
    ("grupo_ciuo08_3",   "CIUO08 G3 Técnicos y profesionales de nivel medio"),
    ("grupo_ciuo08_4",   "CIUO08 G4 Personal de apoyo administrativo"),
    ("grupo_ciuo08_5",   "CIUO08 G5 Trabajadores de los servicios y comercios"),
    ("grupo_ciuo08_6",   "CIUO08 G6 Agricultores, trab. agropecuarios y pesqueros"),
    ("grupo_ciuo08_7",   "CIUO08 G7 Artesanos y operarios de oficios"),
    ("grupo_ciuo08_8",   "CIUO08 G8 Operadores de máquinas y ensambladores"),
    ("grupo_ciuo08_9",   "CIUO08 G9 Ocupaciones elementales"),
    ("grupo_ciuo08_10",  "CIUO08 G10 No identificado"),
    ("grupo_ciuo08_nsnr","CIUO08 Sin clasificación / NS-NR"),

    # ── Grupos CIUO-88 (rótulos INE históricos) ─────────────────────────
    ("grupo_ciuo88_1",   "CIUO88 G1 Miembros poder ejecutivo y directivos adm. pública/empresas"),
    ("grupo_ciuo88_2",   "CIUO88 G2 Profesionales científicos e intelectuales"),
    ("grupo_ciuo88_3",   "CIUO88 G3 Técnicos y profesionales de nivel medio"),
    ("grupo_ciuo88_4",   "CIUO88 G4 Empleados de oficina"),
    ("grupo_ciuo88_5",   "CIUO88 G5 Trabajadores de los servicios y vendedores"),
    ("grupo_ciuo88_6",   "CIUO88 G6 Agricultores y trab. agropecuarios/pesqueros"),
    ("grupo_ciuo88_7",   "CIUO88 G7 Oficiales, operarios y artesanos de oficios"),
    ("grupo_ciuo88_8",   "CIUO88 G8 Operadores de instalaciones y máquinas/montadores"),
    ("grupo_ciuo88_9",   "CIUO88 G9 Trabajadores no calificados"),
    ("grupo_ciuo88_10",  "CIUO88 G10 Otros no identificados"),
    ("grupo_ciuo88_nsnr","CIUO88 Sin clasificación / NS-NR"),


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

VARIABLE_META = {
    "pet": {
        "label": "Población en edad de trabajar (PET)",
        "description": (
            "Todas las personas de 15 años o más residentes en Chile, sin "
            "límite superior de edad. Sirve de universo para calcular tasas "
            "de participación y ocupación."
        ),
        "notes": "Disponible desde 2010-01 con periodicidad mensual.",
        "source": "Glosario ENE 2024, entrada «Población en edad de trabajar»"  # :contentReference[oaicite:0]{index=0}
    },

    "ft": {
        "label": "Fuerza de trabajo (FT)",
        "description": (
            "Personas en edad de trabajar que, en la semana de referencia, "
            "estaban ocupadas o desocupadas."
        ),
        "notes": "Serie continua desde 2010-01.",
        "source": "Glosario ENE 2024, «Fuerza de trabajo (FT)»"  # :contentReference[oaicite:1]{index=1}
    },

    "o": {
        "label": "Personas ocupadas",
        "description": (
            "Quienes trabajaron ≥ 1 hora la semana de referencia o se ausentaron "
            "temporalmente de su empleo manteniendo vínculo o remuneración."
        ),
        "notes": "Definición OIT adoptada por INE; serie completa 2010-01.",
        "source": "Glosario ENE 2024, «Ocupado/a (O)»"  # :contentReference[oaicite:2]{index=2}
    },

    "do": {
        "label": "Personas desocupadas",
        "description": (
            "Personas sin trabajo que buscaron activamente empleo en las últimas "
            "4 semanas y están disponibles para comenzar en las próximas 2."
        ),
        "notes": "",
        "source": "Glosario ENE 2024, «Desocupado/a (DO)»"  # :contentReference[oaicite:3]{index=3}
    },

    "cesantes": {
        "label": "Cesantes",
        "description": (
            "Subconjunto de desocupados/as que tuvieron una ocupación previa de "
            "al menos un mes."
        ),
        "notes": "",
        "source": "Glosario ENE 2024, «Cesante»"  # :contentReference[oaicite:4]{index=4}
    },

    "busca_trabajo_por_primera_vez": {
        "label": "Buscan trabajo por primera vez",
        "description": (
            "Desocupados/as sin experiencia laboral previa —no han tenido nunca "
            "una ocupación remunerada."
        ),
        "notes": "",
        "source": "Glosario ENE 2024, «Personas que buscaron trabajo por primera vez»"  # :contentReference[oaicite:5]{index=5}
    },

    "tpi": {
        "label": "Tiempo parcial involuntario (TPI)",
        "description": (
            "Ocupados/as que trabajan ≤ 30 h habituales y declaran estar "
            "disponibles para trabajar más horas inmediatamente o en 15 días."
        ),
        "notes": "",
        "source": "Glosario ENE 2024, «Ocupados/as a tiempo parcial involuntario»"  # :contentReference[oaicite:6]{index=6}
    },

    "o_informal": {
        "label": "Ocupados informales",
        "description": (
            "Dependientes sin cotización de salud ni pensión asociada a su "
            "empleador; independientes cuyo negocio pertenece al sector informal "
            "o familiares no remunerados."
        ),
        "notes": "Disponible desde 2017-08.",
        "source": "Glosario ENE 2019, «Ocupación informal»"  # :contentReference[oaicite:7]{index=7}
    },

    "ftp": {
        "label": "Fuerza de trabajo potencial (FTP)",
        "description": (
            "Personas no ocupadas que quieren trabajar pero su búsqueda activa "
            "y/o disponibilidad no cumple los criterios para ser desocupadas."
        ),
        "notes": "",
        "source": "Glosario ENE 2024, «Fuerza de trabajo potencial (FTP)»"  # :contentReference[oaicite:8]{index=8}
    },

    "fta": {
        "label": "Fuerza de trabajo ajustada (FTA)",
        "description": (
            "Suma de la fuerza de trabajo (ocupados + desocupados) más la fuerza "
            "de trabajo potencial; se usa como denominador en tasas SU3 y SU4."
        ),
        "notes": "",
        "source": "Glosario ENE 2024, «Fuerza de trabajo ampliada (FTA)»"  # :contentReference[oaicite:9]{index=9}
    },

    "td": {
        "label": "Tasa de desocupación (%)",
        "description": "Desocupados / Fuerza de trabajo × 100, redondeada a 3 decimales.",
        "notes": "",
        "source": "Glosario ENE 2019, «Tasa de desocupación»"  # :contentReference[oaicite:10]{index=10}
    },

    "tp": {
        "label": "Tasa de participación (%)",
        "description": "Fuerza de trabajo / PET × 100, redondeada a 3 decimales.",
        "notes": "",
        "source": "Glosario ENE 2019, «Tasa de participación»"  # :contentReference[oaicite:11]{index=11}
    },

    "to": {
        "label": "Tasa de ocupación (%)",
        "description": "Ocupados / PET × 100, redondeada a 3 decimales.",
        "notes": "",
        "source": "Glosario ENE 2019, «Tasa de ocupación»"  # :contentReference[oaicite:12]{index=12}
    }
}


# Diccionario: variable → fecha de arranque
START_DATES = {
    "o_formal": "2017-08",
    "o_informal": "2017-08",
    "o_sector_informal": "2017-08",
    "toi": "2017-08",
    "tosi":   "2017-08",
    "deseo_trabajar": "2020-02",
    "grupo_ciuo_nsnr": "2019-12",
    "rama_1": "2017-08",
    "rama_2": "2017-08",
    "rama_3": "2017-08",
    "rama_4": "2017-08",
    "rama_5": "2017-08",
    "rama_6": "2017-08",
    "rama_7": "2017-08",
    "rama_8": "2017-08",
    "rama_9": "2017-08",
    "rama_10": "2017-08",
    "rama_11": "2017-08",
    "rama_12": "2017-08",
    "rama_13": "2017-08",
    "rama_14": "2017-08",
    "rama_15": "2017-08",
    "rama_16": "2017-08",
    "rama_17": "2017-08",
    "rama_18": "2017-08",
    "rama_19": "2017-08",
    "rama_20": "2017-08",
    "rama_21": "2017-08",
    "grupo_ciuo08_1": "2017-02",
    "grupo_ciuo08_2": "2017-02",
    "grupo_ciuo08_3": "2017-02",
    "grupo_ciuo08_4": "2017-02",
    "grupo_ciuo08_5": "2017-02",
    "grupo_ciuo08_6": "2017-02",
    "grupo_ciuo08_7": "2017-02",
    "grupo_ciuo08_8": "2017-02",
    "grupo_ciuo08_9": "2017-02",
    "grupo_ciuo08_10": "2017-02",
    "grupo_ciuo08_nsnr": "2017-02",

}

# Diccionario: variable → fecha de arranque
END_DATES = {

    "grupo_ciuo88_1": "2019-02",
    "grupo_ciuo88_2": "2019-02",
    "grupo_ciuo88_3": "2019-02",
    "grupo_ciuo88_4": "2019-02",
    "grupo_ciuo88_5": "2019-02",
    "grupo_ciuo88_6": "2019-02",
    "grupo_ciuo88_7": "2019-02",
    "grupo_ciuo88_8": "2019-02",
    "grupo_ciuo88_9": "2019-02",
    "grupo_ciuo88_10": "2019-02",
    "grupo_ciuo88_nsnr": "2019-02",

}