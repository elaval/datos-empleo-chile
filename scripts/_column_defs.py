# scripts/_column_defs.py
from collections import OrderedDict

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
    # ------------------------------------------------------------------ FFT
    "fft": {
        "label": "Fuera de la fuerza de trabajo (FFT)",
        "description": (
            "Personas en edad de trabajar que, durante la semana de referencia, "
            "no estaban ocupadas ni desocupadas."
        ),
        "notes": "",
        "source": "Glosario ENE 2024, «Personas fuera de la fuerza de trabajo (FFT)»"  # :contentReference[oaicite:0]{index=0}
    },
    "fft_iniciadores": {
        "label": "Iniciadores fuera de la fuerza de trabajo",
        "description": (
            "Personas fuera de la fuerza de trabajo que pronto iniciarán "
            "una actividad laboral y declararon disponibilidad para comenzar en ≤2 semanas."
        ),
        "notes": "",
        "source": "Glosario ENE 2024, «Iniciadores/as disponibles (ID)» —se usa la misma lógica de clasificación"  # :contentReference[oaicite:1]{index=1}
    },
    "fft_inactivos_potencialmente_activos": {
        "label": "Inactivos potencialmente activos",
        "description": (
            "Personas no ocupadas que expresaron interés en trabajar pero cuya "
            "búsqueda activa y/o disponibilidad no cumplió los criterios de desocupación."
        ),
        "notes": "Equivalen a la Fuerza de trabajo potencial (FTP).",
        "source": "Glosario ENE 2024, «Fuerza de trabajo potencial (FTP)»"  # :contentReference[oaicite:2]{index=2}
    },
    "fft_inactivos_habituales": {
        "label": "Inactivos habituales",
        "description": (
            "Resto de personas fuera de la fuerza de trabajo que ni buscan trabajo "
            "ni están disponibles para hacerlo en el corto plazo."
        ),
        "notes": "",
        "source": "Clasificación OIT/INE sobre situación en la fuerza de trabajo"  # :contentReference[oaicite:3]{index=3}
    },

    # ------------------------------------------------------------------ Sub-utilización / presión
    "obe": {
        "label": "Ocupados que buscaron empleo (OBE)",
        "description": (
            "Ocupados/as que, aun teniendo trabajo, realizaron búsqueda activa "
            "de otro empleo en las últimas 4 semanas."  # definición abreviada
        ),
        "notes": "Componente del numerador de la tasa de presión laboral (TPL).",
        "source": "Separata técnica ENE 2019: se detalla la tasa y su desagregación"  # :contentReference[oaicite:4]{index=4}
    },
    "id": {
        "label": "Iniciadores disponibles (ID)",
        "description": (
            "Personas fuera de la fuerza de trabajo que no buscaron empleo porque "
            "comenzarán pronto una ocupación y están disponibles para trabajar "
            "en ≤2 semanas."
        ),
        "notes": "",
        "source": "Glosario ENE 2024, «Iniciadores/as disponibles (ID)»"  # :contentReference[oaicite:5]{index=5}
    },
    "deseo_trabajar": {
        "label": "Deseo de trabajar",
        "description": (
            "Personas fuera de la fuerza de trabajo que manifiestan querer "
            "trabajar pero no realizaron búsqueda activa."
        ),
        "notes": "Ítem directo del cuestionario ENE.",
        "source": "Cuestionario ENE 2022, sección ‘Deseo de trabajar’"  # :contentReference[oaicite:6]{index=6}
    },

    # ------------------------------------------------------------------ Formalidad e informalidad
    "o_formal": {
        "label": "Ocupados formales",
        "description": (
            "Ocupados/as cuyo vínculo laboral incluye cotizaciones de salud "
            "y pensión pagadas por el empleador o, para independientes, "
            "empresas con contabilidad formal inscrita en SII."
        ),
        "notes": "Estimación vigente desde 2017-08 (cambio de módulo de informalidad).",
        "source": "Glosario ENE 2024, ‘Ocupado informal’ (definición inversa) + Nota metodológica informalidad INE 2020"  # :contentReference[oaicite:7]{index=7}
    },
    "o_sector_informal": {
        "label": "Ocupados en sector informal",
        "description": (
            "Ocupados/as cuyo negocio o unidad económica pertenece al sector "
            "informal —sin registro tributario ni contabilidad separada."
        ),
        "notes": "Serie arranca en 2017-08 junto con el módulo de informalidad.",
        "source": "Glosario ENE 2024, ‘Sector informal’"  # :contentReference[oaicite:8]{index=8}
    },

    # ------------------------------------------------------------------ Tasas SU1-SU4
    "su1": {
        "label": "Tasa SU1 (%)",
        "description": (
            "[(Desocupados + Iniciadores disponibles) / (FT + ID)] × 100."
        ),
        "notes": "Subutilización de la fuerza de trabajo – definición OIT (resolución 2013).",
        "source": "Glosario ENE 2024, nota sobre indicadores SU1 a SU4"  # :contentReference[oaicite:9]{index=9}
    },
    "su2": {
        "label": "Tasa SU2 (%)",
        "description": "[(Desocupados + ID + TPI) / (FT + ID)] × 100.",
        "notes": "",
        "source": "Ídem anterior + Resolución OIT 2013"  # :contentReference[oaicite:10]{index=10}
    },
    "su3": {
        "label": "Tasa SU3 (%)",
        "description": "[(Desocupados + ID + FTP) / FTA] × 100.",
        "notes": "",
        "source": "Glosario ENE 2024, descripción de FTA y tasas SU3/SU4"  # :contentReference[oaicite:11]{index=11}
    },
    "su4": {
        "label": "Tasa SU4 (%)",
        "description": "[(Desocupados + ID + TPI + FTP) / FTA] × 100.",
        "notes": "",
        "source": "Glosario ENE 2024, descripción de FTA y tasas SU3/SU4"  # :contentReference[oaicite:12]{index=12}
    },

    # ------------------------------------------------------------------ Horas y tiempo parcial
    "tpv": {
        "label": "Tiempo parcial voluntario (TPV)",
        "description": (
            "Ocupados/as que trabajan ≤ 30 horas habituales y declaran "
            "no querer trabajar más horas."
        ),
        "notes": "",
        "source": "Boletín ENE Nacional 2023: se publica la serie TPV junto a TPI"  # :contentReference[oaicite:13]{index=13}
    },
    "tp_sin_declarar_voluntareidad": {
        "label": "Tiempo parcial sin declarar voluntariedad",
        "description": (
            "Ocupados/as ≤ 30 h semanales que no especifican si la reducción "
            "de jornada es voluntaria o involuntaria."
        ),
        "notes": "Cálculo interno; no es indicador oficial INE.",
        "source": "Metodología ENE 2021, anexo de calidad de respuesta horas"  # :contentReference[oaicite:14]{index=14}
    },

    # ------------------------------------------------------------------ Ejemplo genérico de grupos CIUO y ramas
    "grupo_ciuo08_1": {
        "label": "CIUO08 G1 Directivos y gerentes",
        "description": (
            "Ocupados/as cuyo Gran Grupo CIUO-08 = 1 (Directores, gerentes y "
            "administradores)."
        ),
        "notes": "",
        "source": "CIUO-08 (OIT 2008) — tabla de grandes grupos utilizada por INE"  # :contentReference[oaicite:15]{index=15}
    },
    # … (repetir patrón para CIUO-08_2-10 y CIUO-88_1-10) …

    "rama_7": {
        "label": "Rama 7: Comercio al por mayor y al por menor",
        "description": (
            "Ocupados/as cuya actividad económica principal se clasifica en la "
            "Sección G de la CIIU Rev.4 (Comercio)."
        ),
        "notes": "Serie inicia 2017-08 tras incorporar variable `r_p_rev4cl_caenes`.",
        "source": "CIIU Rev.4 (ONU, 2008) adaptada a CAENES Rev.4 CL"  # :contentReference[oaicite:16]{index=16}
    },
    # … idem ramas 1-21 …

    # ------------------------------------------------------------------ Promedios de horas
    "promedio_horas_efectivas_sin_ausentes": {
        "label": "Prom. horas efectivas sin ausentes",
        "description": (
            "Promedio ponderado de horas efectivas trabajadas por los ocupados "
            "presentes (excluye ausencias), con redondeo a 3 decimales."
        ),
        "notes": "Denominador = `oc_sin_ausentes`.",
        "source": "Metodología de horas ENE 2024, sección medición de tiempo de trabajo"  # :contentReference[oaicite:17]{index=17}
    },
    "pet": {
        "label": "Población en edad de trabajar (PET)",
        "description": "Todas las personas de 15 años o más residentes en Chile, sin límite superior de edad. Sirve de universo para calcular tasas de participación y ocupación.",
        "notes": "Disponible desde 2010-01 con periodicidad mensual.",
        "source": "Glosario ENE 2024, entrada «Población en edad de trabajar»"
    },
    "ft": {
        "label": "Fuerza de trabajo (FT)",
        "description": "Personas en edad de trabajar que, en la semana de referencia, estaban ocupadas o desocupadas.",
        "notes": "Serie continua desde 2010-01.",
        "source": "Glosario ENE 2024, «Fuerza de trabajo (FT)»"
    },
    "o": {
        "label": "Personas ocupadas",
        "description": "Quienes trabajaron ≥ 1 hora la semana de referencia o se ausentaron temporalmente de su empleo manteniendo vínculo o remuneración.",
        "notes": "Definición OIT adoptada por INE; serie completa 2010-01.",
        "source": "Glosario ENE 2024, «Ocupado/a (O)»"
    },
    "do": {
        "label": "Personas desocupadas",
        "description": "Personas sin trabajo que buscaron activamente empleo en las últimas 4 semanas y están disponibles para comenzar en las próximas 2.",
        "notes": "",
        "source": "Glosario ENE 2024, «Desocupado/a (DO)»"
    },
    "cesantes": {
        "label": "Cesantes",
        "description": "Subconjunto de desocupados/as que tuvieron una ocupación previa de al menos un mes.",
        "notes": "",
        "source": "Glosario ENE 2024, «Cesante»"
    },
    "busca_trabajo_por_primera_vez": {
        "label": "Buscan trabajo por primera vez",
        "description": "Desocupados/as sin experiencia laboral previa —no han tenido nunca una ocupación remunerada.",
        "notes": "",
        "source": "Glosario ENE 2024, «Personas que buscaron trabajo por primera vez»"
    },
    "tpi": {
        "label": "Tiempo parcial involuntario (TPI)",
        "description": "Ocupados/as que trabajan ≤ 30 h habituales y declaran estar disponibles para trabajar más horas inmediatamente o en 15 días.",
        "notes": "",
        "source": "Glosario ENE 2024, «Ocupados/as a tiempo parcial involuntario»"
    },
    "o_informal": {
        "label": "Ocupados informales",
        "description": "Dependientes sin cotización de salud ni pensión asociada a su empleador; independientes cuyo negocio pertenece al sector informal o familiares no remunerados.",
        "notes": "Disponible desde 2017-08.",
        "source": "Glosario ENE 2019, «Ocupación informal»"
    },
    "ftp": {
        "label": "Fuerza de trabajo potencial (FTP)",
        "description": "Personas no ocupadas que quieren trabajar pero su búsqueda activa y/o disponibilidad no cumple los criterios para ser desocupadas.",
        "notes": "",
        "source": "Glosario ENE 2024, «Fuerza de trabajo potencial (FTP)»"
    },
    "fta": {
        "label": "Fuerza de trabajo ajustada (FTA)",
        "description": "Suma de la fuerza de trabajo (ocupados + desocupados) más la fuerza de trabajo potencial; se usa como denominador en tasas SU3 y SU4.",
        "notes": "",
        "source": "Glosario ENE 2024, «Fuerza de trabajo ampliada (FTA)»"
    },
    "td": {
        "label": "Tasa de desocupación (%)",
        "description": "Desocupados / Fuerza de trabajo × 100, redondeada a 3 decimales.",
        "notes": "",
        "source": "Glosario ENE 2019, «Tasa de desocupación»"
    },
    "tp": {
        "label": "Tasa de participación (%)",
        "description": "Fuerza de trabajo / PET × 100, redondeada a 3 decimales.",
        "notes": "",
        "source": "Glosario ENE 2019, «Tasa de participación»"
    },
    "to": {
        "label": "Tasa de ocupación (%)",
        "description": "Ocupados / PET × 100, redondeada a 3 decimales.",
        "notes": "",
        "source": "Glosario ENE 2019, «Tasa de ocupación»"
    },
    "ano_trimestre": {
        "label": "Año-Trimestre",
        "description": "",
        "notes": "",
        "source": ""
    },
    "mes_central": {
        "label": "Mes central",
        "description": "",
        "notes": "",
        "source": ""
    },
    "o_hombres": {
        "label": "Ocupados hombres",
        "description": "",
        "notes": "",
        "source": ""
    },
    "o_mujeres": {
        "label": "Ocupados mujeres",
        "description": "",
        "notes": "",
        "source": ""
    },
    "o_chile": {
        "label": "Ocupados chilenos",
        "description": "",
        "notes": "",
        "source": ""
    },
    "o_extranjero": {
        "label": "Ocupados extranjeros",
        "description": "",
        "notes": "",
        "source": ""
    },
    "o_sin_basica_completa": {
        "label": "Sin educación básica completa",
        "description": "",
        "notes": "",
        "source": ""
    },
    "o_ed_basica_completa": {
        "label": "Educación básica completa",
        "description": "",
        "notes": "",
        "source": ""
    },
    "o_ed_media_completa": {
        "label": "Educación media completa",
        "description": "",
        "notes": "",
        "source": ""
    },
    "o_ed_sup_completa": {
        "label": "Educación superior completa",
        "description": "",
        "notes": "",
        "source": ""
    },
    "o_ed_sup_cft": {
        "label": "Edu. superior en CFT",
        "description": "",
        "notes": "",
        "source": ""
    },
    "o_ed_sup_ip": {
        "label": "Edu. superior en IP",
        "description": "",
        "notes": "",
        "source": ""
    },
    "o_ed_sup_univ": {
        "label": "Edu. superior universitaria",
        "description": "",
        "notes": "",
        "source": ""
    },
    "categoria_independientes": {
        "label": "Independientes",
        "description": "",
        "notes": "",
        "source": ""
    },
    "categoria_empleador": {
        "label": "Empleador",
        "description": "",
        "notes": "",
        "source": ""
    },
    "categoria_familiar_personal_no_remunerado": {
        "label": "Familiar personal no remunerado",
        "description": "",
        "notes": "",
        "source": ""
    },
    "categoria_dependientes": {
        "label": "Dependientes",
        "description": "",
        "notes": "",
        "source": ""
    },
    "categoria_asalariados": {
        "label": "Asalariados",
        "description": "",
        "notes": "",
        "source": ""
    },
    "categoria_cuenta_propia": {
        "label": "Cuenta propia",
        "description": "",
        "notes": "",
        "source": ""
    },
    "categoria_asalariado_sector_privado": {
        "label": "Asalariado sector privado",
        "description": "",
        "notes": "",
        "source": ""
    },
    "categoria_asalariado_sector_publico": {
        "label": "Asalariado sector público",
        "description": "",
        "notes": "",
        "source": ""
    },
    "categoria_servicio_domestico": {
        "label": "Servicio doméstico",
        "description": "",
        "notes": "",
        "source": ""
    },
    "categoria_serv_domestico_puertas_afuera": {
        "label": "Servicio doméstico puertas afuera",
        "description": "",
        "notes": "",
        "source": ""
    },
    "categoria_serv_domestico_puertas_adentro": {
        "label": "Servicio doméstico puertas adentro",
        "description": "",
        "notes": "",
        "source": ""
    },
    "categoria_no_corresponde": {
        "label": "No corresponde",
        "description": "",
        "notes": "",
        "source": ""
    },
    "grupo_ciuo_alta": {
        "label": "CIUO grupo alto (1-3)",
        "description": "",
        "notes": "",
        "source": ""
    },
    "grupo_ciuo_media_baja": {
        "label": "CIUO grupo medio-bajo (4-9)",
        "description": "",
        "notes": "",
        "source": ""
    },
    "grupo_ciuo_media": {
        "label": "CIUO grupo medio (4-8)",
        "description": "",
        "notes": "",
        "source": ""
    },
    "grupo_ciuo_baja": {
        "label": "CIUO grupo bajo (9)",
        "description": "",
        "notes": "",
        "source": ""
    },
    "grupo_ciuo_otras": {
        "label": "CIUO otros",
        "description": "",
        "notes": "",
        "source": ""
    },
    "o_ed_sup_ciuo_alta": {
        "label": "Ed Supuerior y Grupo CIUO alto",
        "description": "",
        "notes": "",
        "source": ""
    },
    "o_ed_sup_ciuo_media_baja": {
        "label": "Ed Supuerior y Grupo CIUO medio-bajo",
        "description": "",
        "notes": "",
        "source": ""
    },
    "o_ed_sup_ciuo_no_alta": {
        "label": "Ed Supuerior y Grupo CIUO bajo",
        "description": "",
        "notes": "",
        "source": ""
    },
    "grupo_ciuo08_2": {
        "label": "CIUO08 G2 Profesionales, científicos e intelectuales",
        "description": "",
        "notes": "",
        "source": ""
    },
    "grupo_ciuo08_3": {
        "label": "CIUO08 G3 Técnicos y profesionales de nivel medio",
        "description": "",
        "notes": "",
        "source": ""
    },
    "grupo_ciuo08_4": {
        "label": "CIUO08 G4 Personal de apoyo administrativo",
        "description": "",
        "notes": "",
        "source": ""
    },
    "grupo_ciuo08_5": {
        "label": "CIUO08 G5 Trabajadores de los servicios y comercios",
        "description": "",
        "notes": "",
        "source": ""
    },
    "grupo_ciuo08_6": {
        "label": "CIUO08 G6 Agricultores, trab. agropecuarios y pesqueros",
        "description": "",
        "notes": "",
        "source": ""
    },
    "grupo_ciuo08_7": {
        "label": "CIUO08 G7 Artesanos y operarios de oficios",
        "description": "",
        "notes": "",
        "source": ""
    },
    "grupo_ciuo08_8": {
        "label": "CIUO08 G8 Operadores de máquinas y ensambladores",
        "description": "",
        "notes": "",
        "source": ""
    },
    "grupo_ciuo08_9": {
        "label": "CIUO08 G9 Ocupaciones elementales",
        "description": "",
        "notes": "",
        "source": ""
    },
    "grupo_ciuo08_10": {
        "label": "CIUO08 G10 No identificado",
        "description": "",
        "notes": "",
        "source": ""
    },
    "grupo_ciuo08_nsnr": {
        "label": "CIUO08 Sin clasificación / NS-NR",
        "description": "",
        "notes": "",
        "source": ""
    },
    "grupo_ciuo88_1": {
        "label": "CIUO88 G1 Miembros poder ejecutivo y directivos adm. pública/empresas",
        "description": "",
        "notes": "",
        "source": ""
    },
    "grupo_ciuo88_2": {
        "label": "CIUO88 G2 Profesionales científicos e intelectuales",
        "description": "",
        "notes": "",
        "source": ""
    },
    "grupo_ciuo88_3": {
        "label": "CIUO88 G3 Técnicos y profesionales de nivel medio",
        "description": "",
        "notes": "",
        "source": ""
    },
    "grupo_ciuo88_4": {
        "label": "CIUO88 G4 Empleados de oficina",
        "description": "",
        "notes": "",
        "source": ""
    },
    "grupo_ciuo88_5": {
        "label": "CIUO88 G5 Trabajadores de los servicios y vendedores",
        "description": "",
        "notes": "",
        "source": ""
    },
    "grupo_ciuo88_6": {
        "label": "CIUO88 G6 Agricultores y trab. agropecuarios/pesqueros",
        "description": "",
        "notes": "",
        "source": ""
    },
    "grupo_ciuo88_7": {
        "label": "CIUO88 G7 Oficiales, operarios y artesanos de oficios",
        "description": "",
        "notes": "",
        "source": ""
    },
    "grupo_ciuo88_8": {
        "label": "CIUO88 G8 Operadores de instalaciones y máquinas/montadores",
        "description": "",
        "notes": "",
        "source": ""
    },
    "grupo_ciuo88_9": {
        "label": "CIUO88 G9 Trabajadores no calificados",
        "description": "",
        "notes": "",
        "source": ""
    },
    "grupo_ciuo88_10": {
        "label": "CIUO88 G10 Otros no identificados",
        "description": "",
        "notes": "",
        "source": ""
    },
    "grupo_ciuo88_nsnr": {
        "label": "CIUO88 Sin clasificación / NS-NR",
        "description": "",
        "notes": "",
        "source": ""
    },
    "rama_1": {
        "label": "Rama 1: Agricultura, ganadería, silvicultura y pesca",
        "description": "",
        "notes": "",
        "source": ""
    },
    "rama_2": {
        "label": "Rama 2: Explotación de minas y canteras",
        "description": "",
        "notes": "",
        "source": ""
    },
    "rama_3": {
        "label": "Rama 3: Industrias manufactureras",
        "description": "",
        "notes": "",
        "source": ""
    },
    "rama_4": {
        "label": "Rama 4: Suministro de electricidad, gas, vapor y aire acondicionado",
        "description": "",
        "notes": "",
        "source": ""
    },
    "rama_5": {
        "label": "Rama 5: Suministro de agua",
        "description": "",
        "notes": "",
        "source": ""
    },
    "rama_6": {
        "label": "Rama 6: Construcción",
        "description": "",
        "notes": "",
        "source": ""
    },
    "rama_8": {
        "label": "Rama 8: Transporte y almacenamiento",
        "description": "",
        "notes": "",
        "source": ""
    },
    "rama_9": {
        "label": "Rama 9: Actividades de alojamiento y de servicio de comidas",
        "description": "",
        "notes": "",
        "source": ""
    },
    "rama_10": {
        "label": "Rama 10: Información y comunicaciones",
        "description": "",
        "notes": "",
        "source": ""
    },
    "rama_11": {
        "label": "Rama 11: Actividades financieras y de seguros",
        "description": "",
        "notes": "",
        "source": ""
    },
    "rama_12": {
        "label": "Rama 12: Actividades inmobiliarias",
        "description": "",
        "notes": "",
        "source": ""
    },
    "rama_13": {
        "label": "Rama 13: Actividades profesionales, científicas y técnicas",
        "description": "",
        "notes": "",
        "source": ""
    },
    "rama_14": {
        "label": "Rama 14: Actividades de servicios administrativos y de apoyo",
        "description": "",
        "notes": "",
        "source": ""
    },
    "rama_15": {
        "label": "Rama 15: Administración pública y defensa",
        "description": "",
        "notes": "",
        "source": ""
    },
    "rama_16": {
        "label": "Rama 16: Enseñanza",
        "description": "",
        "notes": "",
        "source": ""
    },
    "rama_17": {
        "label": "Rama 17: Actividades de atención de la salud humana y de asistencia social",
        "description": "",
        "notes": "",
        "source": ""
    },
    "rama_18": {
        "label": "Rama 18: Actividades artísticas, de entretenimiento y recreativas",
        "description": "",
        "notes": "",
        "source": ""
    },
    "rama_19": {
        "label": "Rama 19: Otras actividades de servicios",
        "description": "",
        "notes": "",
        "source": ""
    },
    "rama_20": {
        "label": "Rama 20: Actividades de los hogares como empleadores",
        "description": "",
        "notes": "",
        "source": ""
    },
    "rama_21": {
        "label": "Rama 21: Actividades de organizaciones y órganos extraterritoriales",
        "description": "",
        "notes": "",
        "source": ""
    },
    "horas_1_30": {
        "label": "Horas 1–30",
        "description": "",
        "notes": "",
        "source": ""
    },
    "horas_31_44": {
        "label": "Horas 31–44",
        "description": "",
        "notes": "",
        "source": ""
    },
    "horas_31_39": {
        "label": "Horas 31–39",
        "description": "",
        "notes": "",
        "source": ""
    },
    "horas_40": {
        "label": "Horas 40",
        "description": "",
        "notes": "",
        "source": ""
    },
    "horas_41_44": {
        "label": "Horas 41–44",
        "description": "",
        "notes": "",
        "source": ""
    },
    "horas_45": {
        "label": "Horas 45",
        "description": "",
        "notes": "",
        "source": ""
    },
    "horas_46_mas": {
        "label": "Horas ≥46",
        "description": "",
        "notes": "",
        "source": ""
    },
    "horas_efectivas_46_mas": {
        "label": "Horas efectivas ≥46",
        "description": "",
        "notes": "",
        "source": ""
    },
    "o_declaran_horas": {
        "label": "Ocupados que declaran horas",
        "description": "",
        "notes": "",
        "source": ""
    },
    "promedio_horas_efectivas_declaran_horas": {
        "label": "Prom. horas efectivas (declaran)",
        "description": "",
        "notes": "",
        "source": ""
    },
    "promedio_horas_habituales": {
        "label": "Prom. horas habituales",
        "description": "",
        "notes": "",
        "source": ""
    },
    "tpl": {
        "label": "Tasa de presión laboral (%)",
        "description": "",
        "notes": "",
        "source": ""
    },
    "toi": {
        "label": "Tasa de empleo informal (%)",
        "description": "",
        "notes": "",
        "source": ""
    },
    "tosi": {
        "label": "Tasa de empleo en sector informal (%)",
        "description": "",
        "notes": "",
        "source": ""
    },

    
}

# ---------------------------------------------------------------------
# Re-ordena VARIABLE_META según PUBLIC_COLS (lo que no esté en la lista
# se agrega manteniendo su orden de aparición original)


_PUBLIC_ORDER = [code for code, _ in PUBLIC_COLS]          # 1) orden oficial
_VARIABLE_REST = [k for k in VARIABLE_META if k not in _PUBLIC_ORDER]

ORDERED_VARIABLE_META = OrderedDict()
for code in _PUBLIC_ORDER + _VARIABLE_REST:
    if code in VARIABLE_META:
        ORDERED_VARIABLE_META[code] = VARIABLE_META[code]

# Sustituye el diccionario original por el ordenado
VARIABLE_META = ORDERED_VARIABLE_META

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