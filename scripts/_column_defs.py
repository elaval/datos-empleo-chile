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
    ("o",        "Personas ocupadas (O)"),
    ("do",       "Personas desocupadas (DO)"),
    ("cesantes", "Cesantes"),
    ("busca_trabajo_por_primera_vez", "Buscan trabajo por primera vez (BTPV)"),
    ("fft",      "Fuera de la fuerza de trabajo (FFT)"),
    ("ftp",     "Fuerza de trabajo potencial (FTP)"),
    ("fft_iniciadores", "Iniciadores fuera de la fuerza de trabajo"),
    ("fft_inactivos_habituales",           "Inactivos habituales"),

    # ── Subgrupos especiales ────────────────────────────────────────────
    ("obe",     "Ocupados que buscaron empleo (OBE)"),
    ("id",      "Iniciadores disponibles (ID)"),
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

    # ── Ocupados por categoría ocupacional ──────────────────────────────
    ("categoria_independientes", "Categoría: Independientes"),
    ("categoria_empleador",      "Categoría: Empleador"),
    ("categoria_cuenta_propia",  "Categoría: Cuenta propia"),
    ("categoria_familiar_personal_no_remunerado", "Categoría: Familiar personal no remunerado"),
    ("categoria_dependientes",   "Categoría: Dependientes"),
    ("categoria_asalariados",    "Categoría: Asalariados"),
    ("categoria_asalariado_sector_privado", "Categoría: Asalariado sector privado"),
    ("categoria_asalariado_sector_publico",  "Categoría: Asalariado sector público"),
    ("categoria_servicio_domestico",         "Categoría: Servicio doméstico"),
    ("categoria_serv_domestico_puertas_afuera", "Categoría: Servicio doméstico puertas afuera"),
    ("categoria_serv_domestico_puertas_adentro",  "Categoría: Servicio doméstico puertas adentro"),
    ("categoria_no_corresponde", "Categoría: No corresponde"),


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

       # ── Grupos CIUO ──────────────────────────────────────────────────────
    ("grupo_ciuo_alta",       "CIUO grupo alto (1-3)"),
    ("grupo_ciuo_media_baja", "CIUO grupo medio-bajo (4-9)"),
    ("grupo_ciuo_media",      "CIUO grupo medio (4-8)"),
    ("grupo_ciuo_baja",       "CIUO grupo bajo (9)"),
    ("grupo_ciuo_otras",      "CIUO otros"),

    # ── Educación ────────────────────────────────────────────────────────
    ("o_sin_basica_completa", "Sin educación Básica completa"),
    ("o_ed_basica_completa",  "Educación Básica completa"),
    ("o_ed_media_completa",   "Educación Media completa"),
    ("o_ed_sup_completa",     "Educación Superior completa"),
    ("o_ed_sup_cft",          "Ed. Superior en CFT"),
    ("o_ed_sup_ip",           "Ed. Superior en IP"),
    ("o_ed_sup_univ",         "Ed. Superior universitaria"),


    # ── Ed. Superior × CIUO ─────────────────────────────────────────────
    ("o_ed_sup_ciuo_alta",       "Ed. Superior y grupo CIUO alto (1–3)"),
    ("o_ed_sup_ciuo_media_baja", "Ed. Superior y grupo CIUO medio-bajo (4–9)"),
    ("o_ed_sup_ciuo_no_alta",    "Ed. Superior y grupo CIUO no-alto"),


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
    ("tp_sin_declarar_voluntariedad", "Tiempo parcial sin declarar voluntariedad"),
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
        "label": "Personas ocupadas (O)",
        "description": "Personas en edad de trabajar que, durante la semana de referencia, trabajaron al menos una hora en actividades para producir bienes o servicios a cambio de una remuneración (en dinero o especies), o que estuvieron ausentes temporalmente de su trabajo manteniendo un vínculo laboral. También incluye a quienes trabajan sin remuneración en el negocio de un familiar.",
        "notes": "Definición OIT adoptada por INE. Considera desde 2010-01. Incluye excepciones por ausencia temporal y trabajo no remunerado en negocios familiares.",
        "source": "Glosario ENE 2024, «Ocupado/a (O)»"
    },
    "do": {
        "label": "Personas desocupadas (DO)",
        "description": "Personas en edad de trabajar que no tenían empleo en la semana de referencia, buscaron trabajo activamente en las últimas cuatro semanas y estaban disponibles para trabajar dentro de las próximas dos semanas.",
        "notes": "",
        "source": "Glosario ENE 2024, «Desocupado/a (DO)»"
    },
    "cesantes": {
        "label": "Cesantes",
        "description": "Subconjunto de desocupados/as que tuvieron una ocupación previa de al menos un mes.",
        "notes": "",
        "source": "Glosario ENE 2024, «Cesante»"
    },
    "busca_trabajo_por_primera_vez (BTPV)": {
        "label": "Buscan trabajo por primera vez",
        "description": "Personas desocupadas que nunca han tenido una ocupación anterior.",
        "notes": "",
        "source": "Glosario ENE 2024, «Personas que buscaron trabajo por primera vez»"
    },

    # ------------------------------------------------------------------ FFT
    "fft": {
        "label": "Fuera de la fuerza de trabajo (FFT)",
        "description": (
            "Personas en edad de trabajar que, durante la semana de referencia, "
            "no estaban ocupadas ni desocupadas."
        ),
        "notes": "",
        "source": "Glosario ENE 2024, «Personas fuera de la fuerza de trabajo (FFT)»" 
    },
    "fft_iniciadores": {
        "label": "Iniciadores fuera de la fuerza de trabajo",
        "description": (
            "Personas fuera de la fuerza de trabajo que pronto iniciarán una actividad laboral, "
            "incluyendo tanto a quienes están disponibles para comenzar en ≤2 semanas como a quienes no lo están."
        ),
        "notes": (
            "Corresponden a quienes tienen `cae_general = 6`, incluyendo los códigos específicos 10 (disponibles) y 11 (no disponibles). "
            "Este grupo es parte de la clasificación de la fuerza de trabajo según el INE y se publica como categoría separada en los indicadores principales."
        ),
        "source": "Libro de Códigos ENE 2020, variables cae_general y cae_especifico",
    },

    "fft_inactivos_habituales": {
        "label": "Inactivos habituales",
        "description": (
            "Resto de personas fuera de la fuerza de trabajo que ni buscan trabajo "
            "ni están disponibles para hacerlo en el corto plazo."
        ),
        "notes": "",
        "source": "Clasificación OIT/INE sobre situación en la fuerza de trabajo"  #
    },

    # ------------------------------------------------------------------ Sub-utilización / presión
    "obe": {
        "label": "Ocupados que buscaron empleo (OBE)",
        "description": (
            "Personas ocupadas que realizaron acciones de búsqueda de otro empleo o un empleo adicional durante las últimas cuatro semanas." 
        ),
        "notes": "Componente del numerador de la tasa de presión laboral (TPL).",
        "source": "Separata técnica ENE 2019: se detalla la tasa y su desagregación"  
    },
    "id": {
        "label": "Iniciadores disponibles (ID)",
        "description": (
            "Personas fuera de la fuerza de trabajo que no buscaron trabajo porque iniciarán una actividad laboral pronto, pero están disponibles para comenzar dentro de las próximas dos semanas."
        ),
        "notes": "",
        "source": "Glosario ENE 2024, «Iniciadores/as disponibles (ID)»"  
    },
    "ftp": {
        "label": "Fuerza de trabajo potencial (FTP)",
        "description": (
            "Personas no ocupadas que manifestaron interés en trabajar, pero no buscaron activamente empleo o no estaban disponibles para comenzar a trabajar. "
            "También se les denomina «inactivos/as potencialmente activos/as»."
        ),
        "notes": "",
        "source": "Glosario ENE 2024, «Fuerza de trabajo potencial (FTP)»"
    },
    "fta": {
        "label": "Fuerza de trabajo ajustada (FTA)",
        "description": "Corresponde a la suma de la fuerza de trabajo y la fuerza de trabajo potencial. Se utiliza para calcular indicadores de subutilización laboral",
        "notes": "",
        "source": "Glosario ENE 2024, «Fuerza de trabajo ampliada (FTA)»"
    },
    "deseo_trabajar": {
        "label": "Deseo de trabajar",
        "description": (
            "Personas fuera de la fuerza de trabajo que manifiestan querer "
            "trabajar pero no realizaron búsqueda activa."
        ),
        "notes": "Ítem directo del cuestionario ENE.",
        "source": "Cuestionario ENE 2022, sección ‘Deseo de trabajar’"  #
    },
    # ------------------------------------------------------------------ Ocupados por sexo y nacionalidad
    "o_hombres": {
        "label": "Ocupados hombres",
        "description": (
            "Personas clasificadas como ocupadas (v. definición de «Ocupado/a» "
            "en la ENE) cuyo valor de la variable `sexo` = 1 (hombre) en el "
            "micro-dato."
        ),
        "notes": (
            "Serie íntegra desde 2010-01.  Se construye con la misma regla de "
            "ocupación que la variable general `o`, filtrando solo hombres."
        ),
        "source": (
            "Glosario ENE 2024, entrada «Ocupado/a (O)» "
            "Libro de Códigos ENE 2020, variable SEXO (códigos 1 = Hombre, 2 = Mujer)"
        )
    },
    
    "o_mujeres": {
        "label": "Ocupados mujeres",
        "description": (
            "Personas ocupadas cuyo valor de la variable `sexo` = 2 (mujer)."
        ),
        "notes": (
            "Serie continua 2010-01 en adelante; complemento de `o_hombres`."
        ),
        "source": (
            "Glosario ENE 2024, «Ocupado/a (O)» "
            "Libro de Códigos ENE 2020, variable SEXO"
        )
    },
    
    "o_chile": {
        "label": "Ocupados chilenos",
        "description": (
            "Ocupados/as cuyo código en la variable `nacionalidad` es 152 "
            "(Chile), según clasificación ISO 3166-1 numérica adoptada por el INE."
        ),
        "notes": (
            "Serie disponible desde 2010-01 sin interrupciones.  "
            "Corresponde al subconjunto nacional dentro de `o`."
        ),
        "source": (
            "Libro de Códigos ENE 2020, variable NACIONALIDAD "
            "(código 152 = Chile) "
            "Boletín ENE 2022 (ejemplo de publicación con desagregación por "
            "nacionalidad)"
        )
    },
    
    "o_extranjero": {
        "label": "Ocupados extranjeros",
        "description": (
            "Ocupados/as cuyo valor en `nacionalidad` es distinto de 152, es decir, "
            "personas de nacionalidad extranjera residentes en Chile."
        ),
        "notes": (
            "Se calcula como complemento de `o_chile`.  Serie completa 2010-01."
        ),
        "source": (
            "Libro de Códigos ENE 2020, variable NACIONALIDAD "
            "Boletín ENE 2022 con indicadores por nacionalidad"
        )
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
        "source": "Glosario ENE 2024, ‘Ocupado informal’ (definición inversa) + Nota metodológica informalidad INE 2020"  #
    },
    "o_sector_informal": {
        "label": "Ocupados en sector informal",
        "description": (
            "Ocupados/as cuyo negocio o unidad económica pertenece al sector "
            "informal —sin registro tributario ni contabilidad separada."
        ),
        "notes": "Serie arranca en 2017-08 junto con el módulo de informalidad.",
        "source": "Glosario ENE 2024, ‘Sector informal’"  #
    },

    # ------------------------------------------------------------------ Tasas SU1-SU4
    "su1": {
        "label": "Tasa SU1 (%)",
        "description": (
            "[(Desocupados + Iniciadores disponibles) / (FT + ID)] × 100."
        ),
        "notes": "Subutilización de la fuerza de trabajo – definición OIT (resolución 2013).",
        "source": "Glosario ENE 2024, nota sobre indicadores SU1 a SU4"  #
    },
    "su2": {
        "label": "Tasa SU2 (%)",
        "description": "[(Desocupados + ID + TPI) / (FT + ID)] × 100.",
        "notes": "",
        "source": "Ídem anterior + Resolución OIT 2013"  #0}
    },
    "su3": {
        "label": "Tasa SU3 (%)",
        "description": "[(Desocupados + ID + FTP) / FTA] × 100.",
        "notes": "",
        "source": "Glosario ENE 2024, descripción de FTA y tasas SU3/SU4"  #1}
    },
    "su4": {
        "label": "Tasa SU4 (%)",
        "description": "[(Desocupados + ID + TPI + FTP) / FTA] × 100.",
        "notes": "",
        "source": "Glosario ENE 2024, descripción de FTA y tasas SU3/SU4"  #2}
    },

    # ------------------------------------------------------------------ Horas y tiempo parcial
    "tpv": {
        "label": "Tiempo parcial voluntario (TPV)",
        "description": (
            "Ocupados/as que trabajan ≤ 30 horas habituales y declaran "
            "no querer trabajar más horas."
        ),
        "notes": "",
        "source": "Boletín ENE Nacional 2023: se publica la serie TPV junto a TPI"  #3}
    },
    "tp_sin_declarar_voluntareidad": {
        "label": "Tiempo parcial sin declarar voluntariedad",
        "description": (
            "Ocupados/as ≤ 30 h semanales que no especifican si la reducción "
            "de jornada es voluntaria o involuntaria."
        ),
        "notes": "Cálculo interno; no es indicador oficial INE.",
        "source": "Metodología ENE 2021, anexo de calidad de respuesta horas"  #4}
    },


    "tpi": {
        "label": "Ocupados/as a tiempo parcial involuntario (TPI)",
        "description": "Ocupados/as que trabajan menos de 30 horas habituales a la semana y declaran disponibilidad para trabajar más horas.",
        "notes": "Se considera como parte de la subutilización de la fuerza de trabajo.",
        "source": "Glosario ENE 2024, «Ocupados/as a tiempo parcial involuntario (TPI)»"
    },

    "o_informal": {
        "label": "Ocupados informales",
        "description": "Dependientes sin cotización de salud ni pensión asociada a su empleador; independientes cuyo negocio pertenece al sector informal o familiares no remunerados.",
        "notes": "Disponible desde 2017-08.",
        "source": "Glosario ENE 2019, «Ocupación informal»"
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
        "description": (
            "Año asociado al **mes central** del trimestre móvil. "
            "Cada registro corresponde a un trimestre móvil compuesto por tres meses consecutivos, "
            "pero el año se define según el mes central.\n\n"
            "Por ejemplo, el trimestre Diciembre 2024 – Enero 2025 – Febrero 2025 "
            "tiene mes central = Enero (1), por lo tanto, `ano_trimestre` = 2025."
        ),
        "notes": (
            "El año-trimestre permite identificar de manera unívoca el periodo de referencia "
            "según el criterio adoptado por el INE. Su combinación con `mes_central` es clave "
            "para ordenar cronológicamente la serie."
        ),
        "source": "Metodología ENE 2024 — codificación temporal basada en mes central del trimestre"
    },

    "mes_central": {
        "label": "Mes central",
        "description": (
            "Número del mes (1 a 12) que representa el mes central del trimestre móvil. "
            "Por ejemplo, un trimestre Enero–Febrero–Marzo tiene mes central = 2."
        ),
        "notes": (
            "El mes central se usa como referencia para ordenar, visualizar o filtrar "
            "trimestres móviles. También permite identificar el año del dato cuando se cruza "
            "con `ano_trimestre`."
        ),
        "source": "Metodología ENE 2024 — uso de mes central como indicador de periodo"
    },

    # ------------------------------------------------------------------ Nivel educacional de las personas ocupadas
    "o_sin_basica_completa": {
        "label": "Sin educación Básica completa",
        "description": (
            "Ocupados/as cuyo **nivel educacional más alto** está por debajo de la "
            "enseñanza básica completa.\n\n"
            "Incluye:\n"
            "‒ Personas que declararon 'Nunca estudió', preescolar o básica/primaria "
            "sin haberla finalizado (`nivel` entre 0 y 3, con `termino_nivel` ≠ 1).\n"
            "‒ Casos con códigos fuera del rango 3–14, considerados por el INE como "
            "ausencia de estudios formales."
        ),
        "notes": "Serie continua desde 2010-01.",
        "source": "Libro de Códigos ENE 2010–2019 – variables `nivel` y `termino_nivel`"
    },

    "o_ed_basica_completa": {
        "label": "Educación Básica completa",
        "description": (
            "Ocupados/as que **completaron la enseñanza básica o primaria** "
            "(`nivel` = 3 y `termino_nivel` = 1), o que cursaron enseñanza media "
            "sin terminarla (`nivel` entre 4 y 6 o igual a 14, con `termino_nivel` ≠ 1)."
        ),
        "notes": "Serie continua desde 2010-01.",
        "source": "Libro de Códigos ENE 2010–2019 – variables `nivel` y `termino_nivel`"
    },

    "o_ed_media_completa": {
        "label": "Educación Media completa",
        "description": (
            "Ocupados/as que **terminaron la enseñanza media** (común, técnico-profesional "
            "o humanidades) — `nivel` entre 4 y 6 o igual a 14, con `termino_nivel` = 1 — "
            "o que iniciaron estudios superiores **sin concluirlos** "
            "(`nivel` entre 7 y 9 con `termino_nivel` ≠ 1)."
        ),
        "notes": "Serie continua desde 2010-01.",
        "source": "Libro de Códigos ENE 2010–2019 – variables `nivel` y `termino_nivel`"
    },

    "o_ed_sup_completa": {
        "label": "Educación Superior completa",
        "description": (
            "Ocupados/as con **estudios superiores finalizados**, incluyendo:\n"
            "‒ Carrera técnica de nivel superior en CFT (`nivel` = 7, `termino_nivel` = 1),\n"
            "‒ Título profesional en Instituto Profesional (`nivel` = 8, `termino_nivel` = 1),\n"
            "‒ Estudios universitarios o de posgrado completos (`nivel` entre 9 y 12)."
        ),
        "notes": "Serie continua desde 2010-01.",
        "source": "Libro de Códigos ENE 2010–2019 – variables `nivel` y `termino_nivel`"
    },

    "o_ed_sup_cft": {
        "label": "Ed. Superior en CFT",
        "description": (
            "Ocupados/as con **carrera técnica de nivel superior completada** "
            "(`nivel` = 7 y `termino_nivel` = 1)."
        ),
        "notes": "Disponible en toda la serie.",
        "source": "Libro de Códigos ENE 2010–2019 – código 7 en `nivel`"
    },

    "o_ed_sup_ip": {
        "label": "Ed. Superior en IP",
        "description": (
            "Ocupados/as con **título profesional de Instituto Profesional** "
            "completado (`nivel` = 8 y `termino_nivel` = 1)."
        ),
        "notes": "Disponible en toda la serie.",
        "source": "Libro de Códigos ENE 2010–2019 – código 8 en `nivel`"
    },

    "o_ed_sup_univ": {
        "label": "Ed. Superior universitaria",
        "description": (
            "Ocupados/as con **título universitario o de posgrado completo**:\n"
            "`nivel` = 9 (universitario), 10 (postítulo), 11 (magíster), o 12 (doctorado)."
        ),
        "notes": "Serie continua desde 2010-01.",
        "source": "Libro de Códigos ENE 2010–2019 – códigos 9–12 en `nivel`"
    },


    # ------------------------------------------------------------------ Categorías de ocupación
    "categoria_independientes": {
        "label": "Categoría: Independientes",
        "description": (
            "Ocupados/as clasificados como *empleador/a* (`categoria_ocupacion` = 1), "
            "*trabajador/a por cuenta propia* (`categoria_ocupacion` = 2), o "
            "*familiar personal no remunerado* (`categoria_ocupacion` = 7)."
        ),
        "notes": "Agrupa a todos los que trabajan sin contrato de dependencia.",
        "source": "Glosario ENE 2024, definiciones de Independiente y sus sub-categorías"
    },

    "categoria_empleador": {
        "label": "Categoría: Empleador",
        "description": (
            "Independiente que opera una empresa, negocio o explotación agropecuaria "
            "y contrata al menos a un/a asalariado/a remunerado/a (`categoria_ocupacion` = 1)."
        ),
        "notes": "",
        "source": "INE, Libro de Códigos ENE 2020 — variable `categoria_ocupacion`"
    },

    "categoria_cuenta_propia": {
        "label": "Categoría: Cuenta propia",
        "description": (
            "Persona que trabaja en forma independiente sin contratar asalariados/as "
            "y cuyo ingreso procede directamente de la venta de bienes o servicios "
            "(`categoria_ocupacion` = 2)."
        ),
        "notes": "",
        "source": "Glosario ENE 2024, «Trabajador/a por cuenta propia»"
    },

    "categoria_familiar_personal_no_remunerado": {
        "label": "Categoría: Familiar personal no remunerado",
        "description": (
            "Miembro del hogar que trabaja en la empresa, negocio o finca de un/a "
            "pariente sin percibir remuneración monetaria ni en especie "
            "(`categoria_ocupacion` = 7)."
        ),
        "notes": "",
        "source": "Glosario ENE 2024, «Trabajador/a familiar no remunerado/a»"
    },

    "categoria_dependientes": {
        "label": "Categoría: Dependientes",
        "description": (
            "Trabajadores/as que prestan servicios a un/a empleador/a bajo relación "
            "de subordinación, abarcando asalariados/as del sector privado "
            "(`categoria_ocupacion` = 3), público (4), y servicio doméstico (5 y 6)."
        ),
        "notes": "Complemento del grupo independientes.",
        "source": "Glosario ENE 2024, definición de Dependiente"
    },

    "categoria_asalariados": {
        "label": "Categoría: Asalariados",
        "description": (
            "Dependientes remunerados distintos del servicio doméstico; incluye "
            "asalariados/as del sector privado (`categoria_ocupacion` = 3) y público (4)."
        ),
        "notes": "",
        "source": "Libro de Códigos ENE 2020, `categoria_ocupacion` = 3-4"
    },

    "categoria_asalariado_sector_privado": {
        "label": "Categoría: Asalariado sector privado",
        "description": (
            "Dependiente remunerado cuyo empleador pertenece al sector privado "
            "(`categoria_ocupacion` = 3)."
        ),
        "notes": "",
        "source": "Libro de Códigos ENE 2020, `categoria_ocupacion` = 3"
    },

    "categoria_asalariado_sector_publico": {
        "label": "Categoría: Asalariado sector público",
        "description": (
            "Dependiente remunerado cuyo empleador corresponde al Estado o sus "
            "entidades (`categoria_ocupacion` = 4)."
        ),
        "notes": "",
        "source": "Libro de Códigos ENE 2020, `categoria_ocupacion` = 4"
    },

    "categoria_servicio_domestico": {
        "label": "Categoría: Servicio doméstico",
        "description": (
            "Conjunto de trabajadores/as que realizan labores domésticas remuneradas "
            "en hogares particulares, ya sea viviendo en su propio hogar "
            "(`categoria_ocupacion` = 5) o en el hogar empleador (`categoria_ocupacion` = 6)."
        ),
        "notes": "Subgrupo dentro de Dependientes — desagregado por lugar de pernocta.",
        "source": "Glosario ENE 2019, entrada «Servicio doméstico»"
    },

    "categoria_serv_domestico_puertas_afuera": {
        "label": "Categoría: Servicio doméstico puertas afuera",
        "description": (
            "Trabajador/a de casa particular que vive en su propio hogar y acude a "
            "trabajar durante el día (`categoria_ocupacion` = 5)."
        ),
        "notes": "Denominado también *puertas fuera* en normativa laboral chilena.",
        "source": "Dirección del Trabajo (Chile), ficha “Trabajadoras de casa particular”"
    },

    "categoria_serv_domestico_puertas_adentro": {
        "label": "Categoría: Servicio doméstico puertas adentro",
        "description": (
            "Trabajador/a que reside en el hogar empleador formando parte del "
            "servicio doméstico (`categoria_ocupacion` = 6)."
        ),
        "notes": "",
        "source": "Dirección del Trabajo (Chile), ficha “Trabajadoras de casa particular”"
    },

    "categoria_no_corresponde": {
        "label": "Categoría: No corresponde",
        "description": (
            "Código reservado (`categoria_ocupacion` = 0) para casos sin información "
            "o en los que la categoría ocupacional no aplica al entrevistado/a."
        ),
        "notes": "Valor residual utilizado por INE para editar datos faltantes.",
        "source": "Libro de Códigos ENE 2020, nota al valor 0 en `categoria_ocupacion`"
    },

    # ── Agregados de gran-grupo CIUO ───────────────────────────────────────
    "grupo_ciuo_alta": {
        "label": "CIUO grupo alto (1-3)",
        "description": (
            "Ocupados/as cuyo Gran Grupo CIUO (CIUO-88 hasta 2019-02; CIUO-08 "
            "desde 2017-02) se encuentra en 1, 2 o 3 —Directores/gerentes, "
            "Profesionales científico-intelectuales y Técnicos de nivel medio—, "
            "clasificados como de **alta calificación**."
        ),
        "notes": (
            "Agrupa rangos 1-3 tanto para CIUO-88 como CIUO-08, lo que permite "
            "comparar series a lo largo de la transición metodológica."
        ),
        "source": "CIUO-08 (OIT 2008) y Manual metodológico INE/ENE – anexo clasificación ocupacional"  #
    },

    "grupo_ciuo_media": {
        "label": "CIUO grupo medio (4-8)",
        "description": (
            "Ocupados/as cuyo Gran Grupo CIUO es 4, 5, 6, 7 u 8 —Personal de apoyo "
            "administrativo; Trabajadores de servicios y ventas; Agricultores y "
            "trabajadores agro-forestales; Artesanos/operarios de oficios; y "
            "Operadores de máquinas y ensambladores—, considerados de **calificación media**."
        ),
        "notes": (
            "Excluye el Gran Grupo 9 para diferenciarlo del tramo ‘bajo’. "
            "Cálculo coherente para CIUO-88 y CIUO-08."
        ),
        "source": "ISCO-08 Major Groups 4-8, OIT; tabla INE ENE Gran Grupo CIUO"  #
    },

    "grupo_ciuo_media_baja": {
        "label": "CIUO grupo medio-bajo (4-9)",
        "description": (
            "Agrupación alternativa que junta todos los gran-grupos medios más el "
            "Gran Grupo 9. Incluye 4-9 para medir **calificación media-baja** en sentido amplio."
        ),
        "notes": (
            "Suele usarse para comparar contra el tramo alto (1-3). "
            "Para CIUO-08 y CIUO-88 el mapeo de códigos es equivalente."
        ),
        "source": "Metodología ENE 2024 – desagregación por nivel de calificación ocupacional"  #
    },

    "grupo_ciuo_baja": {
        "label": "CIUO grupo bajo (9)",
        "description": (
            "Ocupados/as clasificados en el **Gran Grupo 9** de CIUO —Ocupaciones "
            "elementales— caracterizadas por tareas simples y rutinarias que "
            "requieren mínima educación formal."
        ),
        "notes": (
            "Serie empalmada: Gran Grupo 9 en CIUO-88 (‘Trabajadores no "
            "calificados’) y Gran Grupo 9 en CIUO-08 (‘Ocupaciones elementales’)."
        ),
        "source": "ISCO-08 Major Group 9; INE Glosario ENE ‘Ocupaciones elementales’"  #
    },

    "grupo_ciuo_otras": {
        "label": "CIUO otros",
        "description": (
            "Ocupados/as cuyo **Gran Grupo CIUO** (versión 88 o 08) **no cae en los rangos 1-9** "
            "utilizados habitualmente para análisis.  Incluye principalmente el "
            "Gran Grupo 10 —*Ocupaciones de las fuerzas armadas / Otros no identificados*— "
            "y registros con código fuera de catálogo o faltante."
        ),
        "notes": (
            "Categoría residual; su tamaño es muy pequeño (<1 % de los ocupados) y puede "
            "variar por cambios de codificación.  No se publica de forma separada en los "
            "boletines del INE, pero se conserva para que la suma de grupos CIUO sea "
            "coherente con el total de ocupados."
        ),
        "source": (
            "CIUO-08 OIT 2008, descripción del **Gran Grupo 10 ‘Ocupaciones de las fuerzas armadas’**"
        )  #
    },

    # ── Educación Superior × CIUO ──────────────────────────────────────────
    "o_ed_sup_ciuo_alta": {
        "label": "Ed. Superior y grupo CIUO alto (1–3)",
        "description": (
            "Ocupados/as con **educación Superior completa** "
            "(niveles 7-12 y `termino_nivel = 1`) cuya ocupación "
            "se ubica en los **Grandes Grupos CIUO 1-3** "
            "(Directivos/gerentes, Profesionales, Técnicos/as)."
        ),
        "notes": (
            "Se construye como la intersección de las reglas "
            "`rule_ed_sup` y `ciuo_gran_grupo ∈ 1-3`. "
            "Para 2010-2019 se usa CIUO-88; desde 2019-12, CIUO-08. "
            "Serie continua, aunque puede haber valores nulos si el gran grupo "
            "no está declarado (NS/NR)."
        ),
        "source": (
            "Glosario ENE 2024, entradas «Nivel educacional» y "
            "«Clasificación CIUO»; "
            "OIT 2008 ISCO-08 Major Groups 1-3"
        )
    },

    "o_ed_sup_ciuo_media_baja": {
        "label": "Ed. Superior y grupo CIUO medio-bajo (4–9)",
        "description": (
            "Ocupados/as con **educación Superior completa** cuya ocupación "
            "pertenece a los **Grandes Grupos CIUO 4-9** "
            "(Apoyo administrativo; Servicios y ventas; "
            "Agricultura y oficios afines; Artesanos/operarios; "
            "Operadores/ensambladores; Ocupaciones elementales)."
        ),
        "notes": (
            "Equivale a `rule_ed_sup & ciuo_gran_grupo ∈ 4-9`. "
            "Agrupa calificaciones medias y bajas; útil para analizar "
            "sobre-educación. Serie válida 2010-01 → presente."
        ),
        "source": (
            "Glosario ENE 2024 y estructura ISCO-08/OIT Grandes Grupos 4-9 "
            
        )
    },

    "o_ed_sup_ciuo_no_alta": {
        "label": "Ed. Superior y CIUO no-alta",
        "description": (
            "Complemento de las dos anteriores: ocupados/as con educación "
            "superior completa **fuera de los Grandes Grupos 1-3**. "
            "Incluye tanto 4-9 como categorías sin clasificación (NS/NR)."
        ),
        "notes": (
            "Implementado como `rule_ed_sup` & `~ciuo_gran_grupo.between(1,3)`. "
            "Útil para medir desajuste educativo. Serie 2010-01 → presente."
        ),
        "source": (
            "Glosario ENE 2024; tabla CIUO-08 grandes grupos; "
            "Metodología ENE 2020, sección desajuste educacional "
            
        )
    },
    # ── Grupos CIUO-08 (2-10 y NS/NR) ─────────────────────────────────────
    "grupo_ciuo08_1": {
        "label": "CIUO08 G1 Directivos y gerentes",
        "description": (
            "Ocupados/as cuyo Gran Grupo CIUO-08 = 1 (Directores, gerentes y "
            "administradores)."
        ),
        "notes": "",
        "source": "CIUO-08 (OIT 2008) — tabla de grandes grupos utilizada por INE"  #5}
    },
    "grupo_ciuo08_2": {
        "label": "CIUO08 G2 Profesionales, científicos e intelectuales",
        "description": (
            "Ocupados/as cuyo Gran Grupo CIUO-08 = 2 (Profesionales, científicos "
            "e intelectuales). Incluye médicos, docentes universitarios, "
            "ingenieros, abogados y otros/as que requieren nivel de cualificación "
            "alto (ISCED 5-8)."
        ),
        "notes": "Serie disponible a partir de 2017-02 (variable `b1`).",
        "source": "Listado oficial de grandes grupos CIUO-08 — OIT / INE Chile"  #
    },
    
    "grupo_ciuo08_3": {
        "label": "CIUO08 G3 Técnicos y profesionales de nivel medio",
        "description": (
            "Ocupados/as con Gran Grupo 3 (Técnicos y profesionales de nivel medio): "
            "por ejemplo técnicos en enfermería, asistentes contables, "
            "paramédicos, programadores de nivel medio."
        ),
        "notes": "Disponible desde 2017-02.",
        "source": "CIUO-08 — definición de Gran Grupo 3"  #
    },
    
    "grupo_ciuo08_4": {
        "label": "CIUO08 G4 Personal de apoyo administrativo",
        "description": (
            "Trabajadores/as clasificados en el Gran Grupo 4 de CIUO-08: "
            "secretarios/as, recepcionistas, oficinistas y otros empleos "
            "de apoyo administrativo."
        ),
        "notes": "Disponible desde 2017-02.",
        "source": "CIUO-08 — Gran Grupo 4"  #
    },
    
    "grupo_ciuo08_5": {
        "label": "CIUO08 G5 Trabajadores de los servicios y comercios",
        "description": (
            "Gran Grupo 5 de CIUO-08: vendedores/as, camareros/as, cuidadores/as, "
            "personal de seguridad, entre otros puestos de servicios y ventas."
        ),
        "notes": "",
        "source": "CIUO-08 — Gran Grupo 5"  #
    },
    
    "grupo_ciuo08_6": {
        "label": "CIUO08 G6 Agricultores y trabajadores agropecuarios / pesqueros",
        "description": (
            "Comprende las ocupaciones agrícolas, ganaderas, forestales y "
            "pesqueras calificadas listadas en el Gran Grupo 6 de CIUO-08."
        ),
        "notes": "",
        "source": "CIUO-08 — Gran Grupo 6"  #
    },
    
    "grupo_ciuo08_7": {
        "label": "CIUO08 G7 Artesanos y operarios de oficios",
        "description": (
            "Ocupados/as del Gran Grupo 7: oficiales, operarios y artesanos de "
            "artes mecánicas, construcción, electricidad, etc."
        ),
        "notes": "",
        "source": "CIUO-08 — Gran Grupo 7"  #
    },
    
    "grupo_ciuo08_8": {
        "label": "CIUO08 G8 Operadores de máquinas y ensambladores",
        "description": (
            "Incluye operadores/as de instalaciones fijas, máquinas industriales, "
            "vehículos y personal de ensamblaje (Gran Grupo 8)."
        ),
        "notes": "",
        "source": "CIUO-08 — Gran Grupo 8"  #
    },
    
    "grupo_ciuo08_9": {
        "label": "CIUO08 G9 Ocupaciones elementales",
        "description": (
            "Trabajos que requieren competencias básicas: limpieza, apoyo manual, "
            "carga y descarga, mensajería, etc. (Gran Grupo 9 de CIUO-08)."
        ),
        "notes": "",
        "source": "CIUO-08 — Gran Grupo 9"  #
    },
    
    "grupo_ciuo08_10": {
        "label": "CIUO08 G10 No identificado",
        "description": (
            "Registros ocupacionales que la ENE no logra codificar en los grandes "
            "grupos 1-9; el INE los etiqueta como ‘Otros no identificados’. "
            "Corresponde al código 10 utilizado en la difusión nacional."
        ),
        "notes": "Categoría exclusiva de la publicación INE; no forma parte del estándar OIT.",
        "source": "Boletines ENE (ej. 2023-12) — notas de pie de cuadro sobre ‘Otros no identificados’"
    },
    
    "grupo_ciuo08_nsnr": {
        "label": "CIUO08 Sin clasificación / NS-NR",
        "description": (
            "Casos sin información suficiente o respuestas ‘No Sabe / No Responde’ "
            "en la codificación CIUO-08."
        ),
        "notes": "",
        "source": "Metodología ENE — tratamiento de códigos NS/NR"
    },
    
    # ── Grupos CIUO-88 (gran grupo 1 a 10 + sin clas.) ────────────────────
    "grupo_ciuo88_1": {
        "label": "CIUO88 G1 Miembros poder ejecutivo y directivos adm. pública/empresas",
        "description": (
            "Ocupados/as cuyo Gran Grupo CIUO-88 = 1: Legisladores, altos funcionarios "
            "gubernamentales, directores corporativos y gerentes generales."
        ),
        "notes": "Serie publicada por INE solo hasta febrero-2019.",
        "source": "ISCO-88, Major Group 1 — Legislators, senior officials and managers"  #
    },
    "grupo_ciuo88_2": {
        "label": "CIUO88 G2 Profesionales científicos e intelectuales",
        "description": (
            "Gran Grupo 2: Profesionales de ciencias físicas, de la salud, docencia y "
            "otras profesiones que requieren formación universitaria completa."
        ),
        "notes": "",
        "source": "ISCO-88, Major Group 2 — Professionals"  #
    },
    "grupo_ciuo88_3": {
        "label": "CIUO88 G3 Técnicos y profesionales de nivel medio",
        "description": (
            "Gran Grupo 3: Técnicos/as, asistentes y profesionales de nivel medio que "
            "apoyan labores científicas, sanitarias, docentes, artísticas o administrativas."
        ),
        "notes": "",
        "source": "ISCO-88, Major Group 3 — Technicians and associate professionals"  #
    },
    "grupo_ciuo88_4": {
        "label": "CIUO88 G4 Empleados de oficina",
        "description": (
            "Gran Grupo 4: Personal de apoyo administrativo — secretarios/as, digitadores, "
            "contables, recepcionistas y otros empleados de oficina y atención al cliente."
        ),
        "notes": "",
        "source": "ISCO-88, Major Group 4 — Clerks"  #
    },
    "grupo_ciuo88_5": {
        "label": "CIUO88 G5 Trabajadores de los servicios y vendedores",
        "description": (
            "Gran Grupo 5: Personal de servicios personales, protección, comercio y venta "
            "al detalle, incluidos meseros/as, peluqueros/as y dependientes de tiendas y mercados."
        ),
        "notes": "",
        "source": "ISCO-88, Major Group 5 — Service workers and shop & market sales workers"  #
    },
    "grupo_ciuo88_6": {
        "label": "CIUO88 G6 Agricultores y trab. agropecuarios/pesqueros",
        "description": (
            "Gran Grupo 6: Trabajadores/as calificados/as de la agricultura, silvicultura, "
            "ganadería y pesca — tanto de mercado como de subsistencia."
        ),
        "notes": "",
        "source": "ISCO-88, Major Group 6 — Skilled agricultural and fishery workers"  #
    },
    "grupo_ciuo88_7": {
        "label": "CIUO88 G7 Oficiales, operarios y artesanos de oficios",
        "description": (
            "Gran Grupo 7: Oficiales, artesanos y operarios de oficios mecánicos, "
            "construcción, imprenta, joyería, textiles y similares."
        ),
        "notes": "",
        "source": "ISCO-88, Major Group 7 — Craft and related trades workers"  #
    },
    "grupo_ciuo88_8": {
        "label": "CIUO88 G8 Operadores de instalaciones y máquinas/montadores",
        "description": (
            "Gran Grupo 8: Operadores/as de plantas industriales, máquinas fijas o móviles, "
            "conductores y ensambladores de equipo."
        ),
        "notes": "",
        "source": "ISCO-88, Major Group 8 — Plant and machine operators and assemblers"  #
    },
    "grupo_ciuo88_9": {
        "label": "CIUO88 G9 Trabajadores no calificados",
        "description": (
            "Gran Grupo 9: Ocupaciones elementales que realizan tareas simples y rutinarias "
            "que requieren poca o ninguna formación formal previa."
        ),
        "notes": "",
        "source": "ISCO-88, Major Group 9 — Elementary occupations"  #
    },
    "grupo_ciuo88_10": {
        "label": "CIUO88 G10 Otros no identificados",
        "description": (
            "Registros de ocupaciones insuficientemente descritas o que no encajan en los "
            "grupos 1-9; se usan como categoría residual en la ENE histórica."
        ),
        "notes": "El INE dejó de publicar esta categoría con la adopción de CIUO-08 (2019).",
        "source": "Metodología ENE 2010 – 2018, adaptación ISCO-88 (categoría residual)"  #
    },
    "grupo_ciuo88_nsnr": {
        "label": "CIUO88 Sin clasificación / NS-NR",
        "description": (
            "Casos en que la ocupación fue declarada como ‘No sabe/No responde’ o no "
            "puede asignarse a ningún gran grupo de la CIUO-88."
        ),
        "notes": "",
        "source": "Cuestionario ENE (apartado de validación de ocupación) + ISCO-88 reglas de codificación"  #0}
    },
    # ── Ramas de actividad (1 a 21) ─────────────────────────────────────────
    "rama_1": {
        "label": "Rama 1: Agricultura, ganadería, silvicultura y pesca",
        "description": (
            "Ocupados/as cuya actividad económica principal se clasifica en la "
            "Sección A de la CIIU Rev.4 (Agricultura, ganadería, silvicultura "
            "y pesca)."
        ),
        "notes": "Serie inicia 2017-08 tras incorporar variable `r_p_rev4cl_caenes`.",
        "source": "CIIU Rev.4 (ONU 2008) adaptada a CAENES Rev.4 CL"  #
    },
    "rama_2": {
        "label": "Rama 2: Explotación de minas y canteras",
        "description": (
            "Ocupados/as clasificados en la Sección B de la CIIU Rev.4 "
            "(Explotación de minas y canteras)."
        ),
        "notes": "Serie inicia 2017-08.",
        "source": "CIIU Rev.4 adaptada a CAENES Rev.4 CL"  #
    },
    "rama_3": {
        "label": "Rama 3: Industrias manufactureras",
    "description": (
        "Ocupados/as cuya actividad principal corresponde a la Sección C "
        "Industrias manufactureras de la CIIU Rev.4."
        ),
        "notes": "Serie inicia 2017-08.",
        "source": "CIIU Rev.4 adaptada a CAENES Rev.4 CL"  #
    },
    "rama_4": {
        "label": "Rama 4: Suministro de electricidad, gas, vapor y aire acondicionado",
        "description": (
            "Sección D de la CIIU Rev.4: producción y distribución de energía "
            "eléctrica y otros suministros energéticos."
        ),
        "notes": "Serie inicia 2017-08.",
        "source": "CIIU Rev.4 adaptada a CAENES Rev.4 CL"  #
    },
    "rama_5": {
        "label": "Rama 5: Suministro de agua; alcantarillado, gestión de residuos",
        "description": (
            "Corresponde a la Sección E de la CIIU Rev.4 (agua, saneamiento "
            "y actividades de descontaminación)."
        ),
        "notes": "Serie inicia 2017-08.",
        "source": "CIIU Rev.4 adaptada a CAENES Rev.4 CL"  #
    },
    "rama_6": {
        "label": "Rama 6: Construcción",
        "description": (
            "Ocupaciones encuadradas en la Sección F Construcción de la "
            "CIIU Rev.4."
        ),
        "notes": "Serie inicia 2017-08.",
        "source": "CIIU Rev.4 adaptada a CAENES Rev.4 CL"  #
    },
    "rama_7": {  # (idéntica a tu ejemplo, incluida aquí para continuidad)
        "label": "Rama 7: Comercio al por mayor y al por menor",
        "description": (
            "Ocupados/as cuya actividad económica principal se clasifica en la "
            "Sección G de la CIIU Rev.4 (Comercio)."
        ),
        "notes": "Serie inicia 2017-08 tras incorporar variable `r_p_rev4cl_caenes`.",
        "source": "CIIU Rev.4 (ONU, 2008) adaptada a CAENES Rev.4 CL"  #
    },
    "rama_8": {
        "label": "Rama 8: Transporte y almacenamiento",
        "description": (
            "Sección H de la CIIU Rev.4: transporte terrestre, acuático, aéreo, "
            "almacenamiento y actividades de apoyo al transporte."
        ),
        "notes": "Serie inicia 2017-08.",
        "source": "CIIU Rev.4 adaptada a CAENES Rev.4 CL"  #
    },
    "rama_9": {
        "label": "Rama 9: Actividades de alojamiento y de servicio de comidas",
        "description": (
            "Sección I de la CIIU Rev.4 (hoteles, restaurantes y servicios de "
            "comidas y bebidas)."
        ),
        "notes": "Serie inicia 2017-08.",
        "source": "CIIU Rev.4 adaptada a CAENES Rev.4 CL"  #
    },
    "rama_10": {
        "label": "Rama 10: Información y comunicaciones",
        "description": (
            "Sección J de la CIIU Rev.4: telecomunicaciones, edición, "
            "programación informática y otros servicios de información."
        ),
        "notes": "Serie inicia 2017-08.",
        "source": "CIIU Rev.4 adaptada a CAENES Rev.4 CL"  #
    },
    "rama_11": {
        "label": "Rama 11: Actividades financieras y de seguros",
        "description": (
            "Sección K de la CIIU Rev.4: intermediación financiera, seguros "
            "y fondos de pensiones."
        ),
        "notes": "Serie inicia 2017-08.",
        "source": "CIIU Rev.4 adaptada a CAENES Rev.4 CL"  #0}
    },
    "rama_12": {
        "label": "Rama 12: Actividades inmobiliarias",
        "description": (
            "Sección L de la CIIU Rev.4: alquiler, compra-venta y gestión de "
            "bienes inmuebles propios o arrendados."
        ),
        "notes": "Serie inicia 2017-08.",
        "source": "CIIU Rev.4 adaptada a CAENES Rev.4 CL"  #1}
    },
    "rama_13": {
        "label": "Rama 13: Actividades profesionales, científicas y técnicas",
        "description": (
            "Sección M de la CIIU Rev.4: servicios jurídicos, contables, "
            "de arquitectura, consultoría, I+D, publicidad, etc."
        ),
        "notes": "Serie inicia 2017-08.",
        "source": "CIIU Rev.4 adaptada a CAENES Rev.4 CL"  #2}
    },
    "rama_14": {
        "label": "Rama 14: Actividades de servicios administrativos y de apoyo",
        "description": (
            "Sección N de la CIIU Rev.4: alquiler de maquinaria, servicios de "
            "empleo, agencias de viaje, limpieza, seguridad y otros apoyos."
        ),
        "notes": "Serie inicia 2017-08.",
        "source": "CIIU Rev.4 adaptada a CAENES Rev.4 CL"  #3}
    },
    "rama_15": {
        "label": "Rama 15: Administración pública y defensa",
        "description": (
            "Sección O de la CIIU Rev.4: administración pública, defensa "
            "y planes de seguridad social obligatorios."
        ),
        "notes": "Serie inicia 2017-08.",
        "source": "CIIU Rev.4 adaptada a CAENES Rev.4 CL"  #4}
    },
    "rama_16": {
        "label": "Rama 16: Enseñanza",
        "description": (
            "Sección P de la CIIU Rev.4 que cubre todos los niveles y tipos "
            "de educación formal."
        ),
        "notes": "Serie inicia 2017-08.",
        "source": "CIIU Rev.4 adaptada a CAENES Rev.4 CL"  #5}
    },
    "rama_17": {
        "label": "Rama 17: Actividades de atención de la salud humana y de asistencia social",
        "description": (
            "Sección Q de la CIIU Rev.4: hospitales, atención ambulatoria, "
            "servicios sociales con y sin alojamiento."
        ),
        "notes": "Serie inicia 2017-08.",
        "source": "CIIU Rev.4 adaptada a CAENES Rev.4 CL"  #6}
    },
    "rama_18": {
        "label": "Rama 18: Actividades artísticas, de entretenimiento y recreativas",
        "description": (
            "Sección R de la CIIU Rev.4: artes escénicas, bibliotecas, "
            "deportes y otras actividades recreativas."
        ),
        "notes": "Serie inicia 2017-08.",
        "source": "CIIU Rev.4 adaptada a CAENES Rev.4 CL"  #7}
    },
    "rama_19": {
        "label": "Rama 19: Otras actividades de servicios",
        "description": (
            "Sección S de la CIIU Rev.4: asociaciones, reparación de "
            "computadores y enseres, servicios personales, etc."
        ),
        "notes": "Serie inicia 2017-08.",
        "source": "CIIU Rev.4 adaptada a CAENES Rev.4 CL"  #8}
    },
    "rama_20": {
        "label": "Rama 20: Actividades de los hogares como empleadores",
        "description": (
            "Sección T de la CIIU Rev.4: hogares que producen bienes o "
            "servicios de uso propio / como empleadores de personal doméstico."
        ),
        "notes": "Serie inicia 2017-08.",
        "source": "CIIU Rev.4 adaptada a CAENES Rev.4 CL"  #9}
    },
    "rama_21": {
        "label": "Rama 21: Actividades de organizaciones y órganos extraterritoriales",
        "description": (
            "Sección U de la CIIU Rev.4: organismos internacionales, "
            "representaciones diplomáticas y otras entidades extraterritoriales."
        ),
        "notes": "Serie inicia 2017-08.",
        "source": "CIIU Rev.4 adaptada a CAENES Rev.4 CL"  #0}
    },

    # ------------------------------------------------------------------ Horas habituales (categorías)
    "horas_1_30": {
        "label": "Horas 1–30",
        "description": (
            "Personas ocupadas cuyo número **habitual** de horas trabajadas a la "
            "semana se encuentra entre 1 y 30, ambas inclusive."
        ),
        "notes": "Corresponde al umbral oficial que usa INE para caracterizar el "
                 "tiempo parcial (≤ 30 h).",
        "source": "Glosario ENE 2024, voz «Horas habitualmente trabajadas»"  #
    },
    "horas_31_44": {
        "label": "Horas 31–44",
        "description": (
            "Ocupados/as con jornada habitual igual o superior a 31 e inferior o "
            "igual a 44 horas semanales."
        ),
        "notes": "Agrupa quienes están por debajo de la jornada legal ordinaria "
                 "chilena (45 h) pero sobre el umbral de trabajo parcial.",
        "source": "INE. Boletín ENE — tabla de distribución de horas habituales"  # 
    },
    "horas_31_39": {
        "label": "Horas 31–39",
        "description": (
            "Sub-conjunto específico dentro de 31-44 h; se utiliza para comparar "
            "con flexibilidad el tramo inmediatamente inferior a 40 h."
        ),
        "notes": "No es indicador oficial; cálculo interno a partir de `habituales`.",
        "source": "Metodología ENE 2021, anexo de calidad de medición de horas"  #
    },
    "horas_40": {
        "label": "Horas 40",
        "description": "Ocupados/as que declaran exactamente 40 horas habituales.",
        "notes": "40 h es la jornada legal vigente a partir de la ley Nº 21 561.",
        "source": "Diario Oficial de Chile, Ley 21 561 (reducción jornada laboral)"  #
    },
    "horas_41_44": {
        "label": "Horas 41–44",
        "description": (
            "Ocupados/as con 41 a 44 horas semanales habituales: tramo de ajuste "
            "entre 40 h y la jornada legal previa de 45 h."
        ),
        "notes": "",
        "source": "INE. Serie histórica de jornada laboral promedio"  # 
    },
    "horas_45": {
        "label": "Horas 45",
        "description": "Ocupados/as que informan exactamente 45 horas habituales.",
        "notes": "45 h fue la jornada legal máxima chilena entre 2005-2024.",
        "source": "Código del Trabajo de Chile, art. 22 (redacción 2005-2024)"  #
    },
    "horas_46_mas": {
        "label": "Horas ≥46",
        "description": (
            "Ocupados/as que declaran 46 horas o más de trabajo habitual por "
            "semana."
        ),
        "notes": "Incluye todas las jornadas extensas (sobre la jornada legal).",
        "source": "Boletín ENE Nacional, cuadro «Distribución de horas habituales»"  # 
    },    

    # ------------------------------------------------------------------ Horas efectivas (tramo alto)
    "horas_efectivas_46_mas": {
        "label": "Horas efectivas ≥46",
        "description": (
            "Personas ocupadas cuya **última semana** registró 46 h o más de "
            "trabajo **efectivo** (excluye ausencias y licencias)."
        ),
        "notes": "Se calcula sobre la variable `efectivas`; 888/999 se recodifican a NA.",
        "source": "INE. Manual de campo ENE, p. 27 (pregunta de horas efectivas)"  # 
    },    

    # ------------------------------------------------------------------ Denominadores y promedios
    "o_declaran_horas": {
        "label": "Ocupados que declaran horas",
        "description": (
            "Total de ocupados/as con respuesta válida en las preguntas de horas "
            "habituales y efectivas (≠ 888/999)."
        ),
        "notes": (
            "Sirve como denominador de los promedios de horas; se almacena como "
            "entero ponderado."
        ),
        "source": "Metodología ENE 2024, sección 5.3 «Tratamiento de no-respuesta»"  #
    },
    "promedio_horas_efectivas_sin_ausentes": {
        "label": "Prom. horas efectivas sin ausentes",
        "description": (
            "Promedio ponderado de horas efectivas trabajadas **solo entre ocupados/as sin ausencias**, "
            "es decir, quienes reportaron horas efectivas mayores a cero en la semana de referencia."
        ),
        "notes": (
            "Excluye a quienes, aun estando ocupados, no trabajaron efectivamente por vacaciones, "
            "licencias médicas, permisos u otras ausencias. \n"
            "Este promedio entrega una medida más precisa del esfuerzo laboral entre quienes efectivamente trabajaron."
        ),
        "source": "Cálculo interno basado en microdatos ENE. No se publica directamente en boletines oficiales del INE."
    },
    "promedio_horas_efectivas_declaran_horas": {
        "label": "Prom. horas efectivas (declaran)",
        "description": (
            "Promedio ponderado de horas efectivas entre quienes **reportaron** "
            "alguna hora trabajada en la semana de referencia."
        ),
        "notes": "Denominador = `o_declaran_horas`. Se presentan 3 decimales.",
        "source": "Boletín ENE Metodológico 2023, sección ‘Horas efectivas’"  # 
    },
    "promedio_horas_habituales": {
        "label": "Prom. horas habituales",
        "description": (
            "Promedio ponderado de horas que los ocupados/as trabajan **habitualmente** "
            "en una semana típica, con redondeo a 3 decimales."
        ),
        "notes": "Denominador = `o_declaran_horas`.",
        "source": "Glosario ENE 2024, voz «Horas habitualmente trabajadas»"  #0}
    },
    # ------------------------------------------------------------------ Tasas complementarias
    "tpl": {
        "label": "Tasa de presión laboral (%)",
        "description": (
            "(DO + ID + OBE) / (FT + ID) × 100. \n"
            "Mide la ‘presión’ sobre el mercado laboral sumando a las personas "
            "desocupadas, a los ocupados que buscaron otro empleo y a los iniciadores "
            "disponibles, respecto de una fuerza de trabajo ampliada que incluye a estos "
            "últimos."
        ),
        "notes": "Indicador complementario OIT-INE; serie continua desde 2010-01.",
        "source": "Libro de Códigos ENE 2020, pág. 193-194 (sección 6.1.4 TPL)"  #
    },

    "toi": {
        "label": "Tasa de empleo informal (%)",
        "description": (
            "OI / O × 100. \n"
            "Porcentaje de ocupados/as clasificados como informales según criterio "
            "de cotización (dependientes) o pertenencia al sector informal "
            "(independientes y familiares no remunerados)."
        ),
        "notes": "Disponible desde 2017-08, cuando la ENE incorporó el módulo de informalidad.",
        "source": "Libro de Códigos ENE 2020, pág. 225 (cálculo TOI)"  #
    },

    "tosi": {
        "label": "Tasa de empleo en sector informal (%)",
        "description": (
            "OSI / O × 100. \n"
            "Proporción de ocupados/as cuya unidad económica pertenece al sector "
            "informal, definida por ausencia de registro tributario o contabilidad "
            "formal separada."
        ),
        "notes": "Serie arranca en 2017-08 junto con la variable `sector` (1 = formal, 2 = informal).",
        "source": "Libro de Códigos ENE 2020, pág. 225-226 (cálculo TOSI)"  #
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