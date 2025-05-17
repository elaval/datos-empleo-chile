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
            "Glosario ENE 2024, entrada «Ocupado/a (O)» :contentReference[oaicite:0]{index=0}; "
            "Libro de Códigos ENE 2020, variable SEXO (códigos 1 = Hombre, 2 = Mujer) :contentReference[oaicite:1]{index=1}"
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
            "Glosario ENE 2024, «Ocupado/a (O)» :contentReference[oaicite:2]{index=2}; "
            "Libro de Códigos ENE 2020, variable SEXO :contentReference[oaicite:3]{index=3}"
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
            "(código 152 = Chile) :contentReference[oaicite:4]{index=4}; "
            "Boletín ENE 2022 (ejemplo de publicación con desagregación por "
            "nacionalidad) :contentReference[oaicite:5]{index=5}"
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
            "Libro de Códigos ENE 2020, variable NACIONALIDAD :contentReference[oaicite:6]{index=6}; "
            "Boletín ENE 2022 con indicadores por nacionalidad :contentReference[oaicite:7]{index=7}"
        )
    },
    # ------------------------------------------------------------------ Nivel educacional de las personas ocupadas
    "o_sin_basica_completa": {
        "label": "Sin educación básica completa",
        "description": (
            "Ocupados/as cuyo **nivel educacional más alto (variable `nivel`) se "
            "encuentra por debajo de la enseñanza básica completa**. \n\n"
            "Se incluyen:\n"
            "‒ Quienes declararon “Nunca estudió”, pre-escolar o básica/primaria "
            "pero **no** la finalizaron (`nivel` = 0-3 **y** `termino_nivel` ≠ 1), y\n"
            "‒ Cualquier otro código fuera del rango 3-14, que el INE clasifica como "
            "sin estudios formales. :contentReference[oaicite:0]{index=0}"
        ),
        "notes": "Serie continua desde 2010-01; construida con `_mask_sin_basica`.",
        "source": "Libro de Códigos ENE 2010-2019 – definición de `nivel`/`termino_nivel` :contentReference[oaicite:1]{index=1}"
    },    

    "o_ed_basica_completa": {
        "label": "Educación básica completa",
        "description": (
            "Ocupados/as que **finalizaron la básica/primaria** "
            "(`nivel` = 3 y `termino_nivel` = 1) **o** que cursaron enseñanza media "
            "pero **no la concluyeron** (`nivel` ∈ 4-6, 14 y `termino_nivel` ≠ 1). "
            "Corresponde al *_mask_ed_basica_* definido en el script. :contentReference[oaicite:2]{index=2}"
        ),
        "notes": "Continuidad 2010-01 ↔ presente; categoría mutuamente excluyente.",
        "source": "Libro de Códigos ENE 2010-2019 – códigos 3-6, 14 :contentReference[oaicite:3]{index=3}"
    },    

    "o_ed_media_completa": {
        "label": "Educación media completa",
        "description": (
            "Ocupados/as que **terminaron la enseñanza media (común o TP) "
            "o humanidades** (`nivel` = 4-6, 14 **y** `termino_nivel` = 1) "
            "o que iniciaron estudios superiores **sin concluirlos** "
            "(`nivel` = 7-9 y `termino_nivel` ≠ 1). "
            "Implementa la lógica de *_mask_ed_media_*. :contentReference[oaicite:4]{index=4}"
        ),
        "notes": "",
        "source": "Libro de Códigos ENE 2010-2019 – códigos 4-9, 14 :contentReference[oaicite:5]{index=5}"
    },    

    "o_ed_sup_completa": {
        "label": "Educación superior completa",
        "description": (
            "Ocupados/as con **estudios superiores finalizados**:\n"
            "‒ Técnico de nivel superior/CFT (`nivel` = 7, `termino_nivel` = 1),\n"
            "‒ Profesional/IP (`nivel` = 8, `termino_nivel` = 1),\n"
            "‒ Universitario u otros de pos-grado (`nivel` = 9-12). "
            "Equivale al *_mask_ed_sup_* del script. :contentReference[oaicite:6]{index=6}"
        ),
        "notes": "",
        "source": "Libro de Códigos ENE 2010-2019 – códigos 7-12 :contentReference[oaicite:7]{index=7}"
    },    

    "o_ed_sup_cft": {
        "label": "Edu. superior en CFT",
        "description": (
            "Sub-conjunto de ocupados/as con **Carrera Técnica de nivel superior** "
            "terminada (`nivel` = 7 & `termino_nivel` = 1). :contentReference[oaicite:8]{index=8}"
        ),
        "notes": "Disponible en toda la serie; regla `rule_ed_sup_cft`.",
        "source": "Libro de Códigos ENE 2010-2019 – código 7 :contentReference[oaicite:9]{index=9}"
    },    

    "o_ed_sup_ip": {
        "label": "Edu. superior en IP",
        "description": (
            "Ocupados/as con **título profesional de Instituto Profesional** "
            "terminado (`nivel` = 8 & `termino_nivel` = 1). :contentReference[oaicite:10]{index=10}"
        ),
        "notes": "",
        "source": "Libro de Códigos ENE 2010-2019 – código 8 :contentReference[oaicite:11]{index=11}"
    },    

    "o_ed_sup_univ": {
        "label": "Edu. superior universitaria",
        "description": (
            "Agrupa ocupados/as con **título universitario o pos-grado** "
            "completo: `nivel` = 9 (universitario) o 10-12 "
            "(post-título, magíster, doctorado). :contentReference[oaicite:12]{index=12}"
        ),
        "notes": "",
        "source": "Libro de Códigos ENE 2010-2019 – códigos 9-12 :contentReference[oaicite:13]{index=13}"
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
    # ── Grupos CIUO-08 (2-10 y NS/NR) ─────────────────────────────────────
    "grupo_ciuo08_1": {
        "label": "CIUO08 G1 Directivos y gerentes",
        "description": (
            "Ocupados/as cuyo Gran Grupo CIUO-08 = 1 (Directores, gerentes y "
            "administradores)."
        ),
        "notes": "",
        "source": "CIUO-08 (OIT 2008) — tabla de grandes grupos utilizada por INE"  # :contentReference[oaicite:15]{index=15}
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
        "source": "Listado oficial de grandes grupos CIUO-08 — OIT / INE Chile"  # :contentReference[oaicite:0]{index=0}
    },
    
    "grupo_ciuo08_3": {
        "label": "CIUO08 G3 Técnicos y profesionales de nivel medio",
        "description": (
            "Ocupados/as con Gran Grupo 3 (Técnicos y profesionales de nivel medio): "
            "por ejemplo técnicos en enfermería, asistentes contables, "
            "paramédicos, programadores de nivel medio."
        ),
        "notes": "Disponible desde 2017-02.",
        "source": "CIUO-08 — definición de Gran Grupo 3"  # :contentReference[oaicite:1]{index=1}
    },
    
    "grupo_ciuo08_4": {
        "label": "CIUO08 G4 Personal de apoyo administrativo",
        "description": (
            "Trabajadores/as clasificados en el Gran Grupo 4 de CIUO-08: "
            "secretarios/as, recepcionistas, oficinistas y otros empleos "
            "de apoyo administrativo."
        ),
        "notes": "Disponible desde 2017-02.",
        "source": "CIUO-08 — Gran Grupo 4"  # :contentReference[oaicite:2]{index=2}
    },
    
    "grupo_ciuo08_5": {
        "label": "CIUO08 G5 Trabajadores de los servicios y comercios",
        "description": (
            "Gran Grupo 5 de CIUO-08: vendedores/as, camareros/as, cuidadores/as, "
            "personal de seguridad, entre otros puestos de servicios y ventas."
        ),
        "notes": "",
        "source": "CIUO-08 — Gran Grupo 5"  # :contentReference[oaicite:3]{index=3}
    },
    
    "grupo_ciuo08_6": {
        "label": "CIUO08 G6 Agricultores y trabajadores agropecuarios / pesqueros",
        "description": (
            "Comprende las ocupaciones agrícolas, ganaderas, forestales y "
            "pesqueras calificadas listadas en el Gran Grupo 6 de CIUO-08."
        ),
        "notes": "",
        "source": "CIUO-08 — Gran Grupo 6"  # :contentReference[oaicite:4]{index=4}
    },
    
    "grupo_ciuo08_7": {
        "label": "CIUO08 G7 Artesanos y operarios de oficios",
        "description": (
            "Ocupados/as del Gran Grupo 7: oficiales, operarios y artesanos de "
            "artes mecánicas, construcción, electricidad, etc."
        ),
        "notes": "",
        "source": "CIUO-08 — Gran Grupo 7"  # :contentReference[oaicite:5]{index=5}
    },
    
    "grupo_ciuo08_8": {
        "label": "CIUO08 G8 Operadores de máquinas y ensambladores",
        "description": (
            "Incluye operadores/as de instalaciones fijas, máquinas industriales, "
            "vehículos y personal de ensamblaje (Gran Grupo 8)."
        ),
        "notes": "",
        "source": "CIUO-08 — Gran Grupo 8"  # :contentReference[oaicite:6]{index=6}
    },
    
    "grupo_ciuo08_9": {
        "label": "CIUO08 G9 Ocupaciones elementales",
        "description": (
            "Trabajos que requieren competencias básicas: limpieza, apoyo manual, "
            "carga y descarga, mensajería, etc. (Gran Grupo 9 de CIUO-08)."
        ),
        "notes": "",
        "source": "CIUO-08 — Gran Grupo 9"  # :contentReference[oaicite:7]{index=7}
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
        "source": "ISCO-88, Major Group 1 — Legislators, senior officials and managers"  # :contentReference[oaicite:0]{index=0}
    },
    "grupo_ciuo88_2": {
        "label": "CIUO88 G2 Profesionales científicos e intelectuales",
        "description": (
            "Gran Grupo 2: Profesionales de ciencias físicas, de la salud, docencia y "
            "otras profesiones que requieren formación universitaria completa."
        ),
        "notes": "",
        "source": "ISCO-88, Major Group 2 — Professionals"  # :contentReference[oaicite:1]{index=1}
    },
    "grupo_ciuo88_3": {
        "label": "CIUO88 G3 Técnicos y profesionales de nivel medio",
        "description": (
            "Gran Grupo 3: Técnicos/as, asistentes y profesionales de nivel medio que "
            "apoyan labores científicas, sanitarias, docentes, artísticas o administrativas."
        ),
        "notes": "",
        "source": "ISCO-88, Major Group 3 — Technicians and associate professionals"  # :contentReference[oaicite:2]{index=2}
    },
    "grupo_ciuo88_4": {
        "label": "CIUO88 G4 Empleados de oficina",
        "description": (
            "Gran Grupo 4: Personal de apoyo administrativo — secretarios/as, digitadores, "
            "contables, recepcionistas y otros empleados de oficina y atención al cliente."
        ),
        "notes": "",
        "source": "ISCO-88, Major Group 4 — Clerks"  # :contentReference[oaicite:3]{index=3}
    },
    "grupo_ciuo88_5": {
        "label": "CIUO88 G5 Trabajadores de los servicios y vendedores",
        "description": (
            "Gran Grupo 5: Personal de servicios personales, protección, comercio y venta "
            "al detalle, incluidos meseros/as, peluqueros/as y dependientes de tiendas y mercados."
        ),
        "notes": "",
        "source": "ISCO-88, Major Group 5 — Service workers and shop & market sales workers"  # :contentReference[oaicite:4]{index=4}
    },
    "grupo_ciuo88_6": {
        "label": "CIUO88 G6 Agricultores y trab. agropecuarios/pesqueros",
        "description": (
            "Gran Grupo 6: Trabajadores/as calificados/as de la agricultura, silvicultura, "
            "ganadería y pesca — tanto de mercado como de subsistencia."
        ),
        "notes": "",
        "source": "ISCO-88, Major Group 6 — Skilled agricultural and fishery workers"  # :contentReference[oaicite:5]{index=5}
    },
    "grupo_ciuo88_7": {
        "label": "CIUO88 G7 Oficiales, operarios y artesanos de oficios",
        "description": (
            "Gran Grupo 7: Oficiales, artesanos y operarios de oficios mecánicos, "
            "construcción, imprenta, joyería, textiles y similares."
        ),
        "notes": "",
        "source": "ISCO-88, Major Group 7 — Craft and related trades workers"  # :contentReference[oaicite:6]{index=6}
    },
    "grupo_ciuo88_8": {
        "label": "CIUO88 G8 Operadores de instalaciones y máquinas/montadores",
        "description": (
            "Gran Grupo 8: Operadores/as de plantas industriales, máquinas fijas o móviles, "
            "conductores y ensambladores de equipo."
        ),
        "notes": "",
        "source": "ISCO-88, Major Group 8 — Plant and machine operators and assemblers"  # :contentReference[oaicite:7]{index=7}
    },
    "grupo_ciuo88_9": {
        "label": "CIUO88 G9 Trabajadores no calificados",
        "description": (
            "Gran Grupo 9: Ocupaciones elementales que realizan tareas simples y rutinarias "
            "que requieren poca o ninguna formación formal previa."
        ),
        "notes": "",
        "source": "ISCO-88, Major Group 9 — Elementary occupations"  # :contentReference[oaicite:8]{index=8}
    },
    "grupo_ciuo88_10": {
        "label": "CIUO88 G10 Otros no identificados",
        "description": (
            "Registros de ocupaciones insuficientemente descritas o que no encajan en los "
            "grupos 1-9; se usan como categoría residual en la ENE histórica."
        ),
        "notes": "El INE dejó de publicar esta categoría con la adopción de CIUO-08 (2019).",
        "source": "Metodología ENE 2010 – 2018, adaptación ISCO-88 (categoría residual)"  # :contentReference[oaicite:9]{index=9}
    },
    "grupo_ciuo88_nsnr": {
        "label": "CIUO88 Sin clasificación / NS-NR",
        "description": (
            "Casos en que la ocupación fue declarada como ‘No sabe/No responde’ o no "
            "puede asignarse a ningún gran grupo de la CIUO-88."
        ),
        "notes": "",
        "source": "Cuestionario ENE (apartado de validación de ocupación) + ISCO-88 reglas de codificación"  # :contentReference[oaicite:10]{index=10}
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
        "source": "CIIU Rev.4 (ONU 2008) adaptada a CAENES Rev.4 CL"  # :contentReference[oaicite:0]{index=0}
    },
    "rama_2": {
        "label": "Rama 2: Explotación de minas y canteras",
        "description": (
            "Ocupados/as clasificados en la Sección B de la CIIU Rev.4 "
            "(Explotación de minas y canteras)."
        ),
        "notes": "Serie inicia 2017-08.",
        "source": "CIIU Rev.4 adaptada a CAENES Rev.4 CL"  # :contentReference[oaicite:1]{index=1}
    },
    "rama_3": {
        "label": "Rama 3: Industrias manufactureras",
    "description": (
        "Ocupados/as cuya actividad principal corresponde a la Sección C "
        "Industrias manufactureras de la CIIU Rev.4."
        ),
        "notes": "Serie inicia 2017-08.",
        "source": "CIIU Rev.4 adaptada a CAENES Rev.4 CL"  # :contentReference[oaicite:2]{index=2}
    },
    "rama_4": {
        "label": "Rama 4: Suministro de electricidad, gas, vapor y aire acondicionado",
        "description": (
            "Sección D de la CIIU Rev.4: producción y distribución de energía "
            "eléctrica y otros suministros energéticos."
        ),
        "notes": "Serie inicia 2017-08.",
        "source": "CIIU Rev.4 adaptada a CAENES Rev.4 CL"  # :contentReference[oaicite:3]{index=3}
    },
    "rama_5": {
        "label": "Rama 5: Suministro de agua; alcantarillado, gestión de residuos",
        "description": (
            "Corresponde a la Sección E de la CIIU Rev.4 (agua, saneamiento "
            "y actividades de descontaminación)."
        ),
        "notes": "Serie inicia 2017-08.",
        "source": "CIIU Rev.4 adaptada a CAENES Rev.4 CL"  # :contentReference[oaicite:4]{index=4}
    },
    "rama_6": {
        "label": "Rama 6: Construcción",
        "description": (
            "Ocupaciones encuadradas en la Sección F Construcción de la "
            "CIIU Rev.4."
        ),
        "notes": "Serie inicia 2017-08.",
        "source": "CIIU Rev.4 adaptada a CAENES Rev.4 CL"  # :contentReference[oaicite:5]{index=5}
    },
    "rama_7": {  # (idéntica a tu ejemplo, incluida aquí para continuidad)
        "label": "Rama 7: Comercio al por mayor y al por menor",
        "description": (
            "Ocupados/as cuya actividad económica principal se clasifica en la "
            "Sección G de la CIIU Rev.4 (Comercio)."
        ),
        "notes": "Serie inicia 2017-08 tras incorporar variable `r_p_rev4cl_caenes`.",
        "source": "CIIU Rev.4 (ONU, 2008) adaptada a CAENES Rev.4 CL"  # :contentReference[oaicite:6]{index=6}
    },
    "rama_8": {
        "label": "Rama 8: Transporte y almacenamiento",
        "description": (
            "Sección H de la CIIU Rev.4: transporte terrestre, acuático, aéreo, "
            "almacenamiento y actividades de apoyo al transporte."
        ),
        "notes": "Serie inicia 2017-08.",
        "source": "CIIU Rev.4 adaptada a CAENES Rev.4 CL"  # :contentReference[oaicite:7]{index=7}
    },
    "rama_9": {
        "label": "Rama 9: Actividades de alojamiento y de servicio de comidas",
        "description": (
            "Sección I de la CIIU Rev.4 (hoteles, restaurantes y servicios de "
            "comidas y bebidas)."
        ),
        "notes": "Serie inicia 2017-08.",
        "source": "CIIU Rev.4 adaptada a CAENES Rev.4 CL"  # :contentReference[oaicite:8]{index=8}
    },
    "rama_10": {
        "label": "Rama 10: Información y comunicaciones",
        "description": (
            "Sección J de la CIIU Rev.4: telecomunicaciones, edición, "
            "programación informática y otros servicios de información."
        ),
        "notes": "Serie inicia 2017-08.",
        "source": "CIIU Rev.4 adaptada a CAENES Rev.4 CL"  # :contentReference[oaicite:9]{index=9}
    },
    "rama_11": {
        "label": "Rama 11: Actividades financieras y de seguros",
        "description": (
            "Sección K de la CIIU Rev.4: intermediación financiera, seguros "
            "y fondos de pensiones."
        ),
        "notes": "Serie inicia 2017-08.",
        "source": "CIIU Rev.4 adaptada a CAENES Rev.4 CL"  # :contentReference[oaicite:10]{index=10}
    },
    "rama_12": {
        "label": "Rama 12: Actividades inmobiliarias",
        "description": (
            "Sección L de la CIIU Rev.4: alquiler, compra-venta y gestión de "
            "bienes inmuebles propios o arrendados."
        ),
        "notes": "Serie inicia 2017-08.",
        "source": "CIIU Rev.4 adaptada a CAENES Rev.4 CL"  # :contentReference[oaicite:11]{index=11}
    },
    "rama_13": {
        "label": "Rama 13: Actividades profesionales, científicas y técnicas",
        "description": (
            "Sección M de la CIIU Rev.4: servicios jurídicos, contables, "
            "de arquitectura, consultoría, I+D, publicidad, etc."
        ),
        "notes": "Serie inicia 2017-08.",
        "source": "CIIU Rev.4 adaptada a CAENES Rev.4 CL"  # :contentReference[oaicite:12]{index=12}
    },
    "rama_14": {
        "label": "Rama 14: Actividades de servicios administrativos y de apoyo",
        "description": (
            "Sección N de la CIIU Rev.4: alquiler de maquinaria, servicios de "
            "empleo, agencias de viaje, limpieza, seguridad y otros apoyos."
        ),
        "notes": "Serie inicia 2017-08.",
        "source": "CIIU Rev.4 adaptada a CAENES Rev.4 CL"  # :contentReference[oaicite:13]{index=13}
    },
    "rama_15": {
        "label": "Rama 15: Administración pública y defensa",
        "description": (
            "Sección O de la CIIU Rev.4: administración pública, defensa "
            "y planes de seguridad social obligatorios."
        ),
        "notes": "Serie inicia 2017-08.",
        "source": "CIIU Rev.4 adaptada a CAENES Rev.4 CL"  # :contentReference[oaicite:14]{index=14}
    },
    "rama_16": {
        "label": "Rama 16: Enseñanza",
        "description": (
            "Sección P de la CIIU Rev.4 que cubre todos los niveles y tipos "
            "de educación formal."
        ),
        "notes": "Serie inicia 2017-08.",
        "source": "CIIU Rev.4 adaptada a CAENES Rev.4 CL"  # :contentReference[oaicite:15]{index=15}
    },
    "rama_17": {
        "label": "Rama 17: Actividades de atención de la salud humana y de asistencia social",
        "description": (
            "Sección Q de la CIIU Rev.4: hospitales, atención ambulatoria, "
            "servicios sociales con y sin alojamiento."
        ),
        "notes": "Serie inicia 2017-08.",
        "source": "CIIU Rev.4 adaptada a CAENES Rev.4 CL"  # :contentReference[oaicite:16]{index=16}
    },
    "rama_18": {
        "label": "Rama 18: Actividades artísticas, de entretenimiento y recreativas",
        "description": (
            "Sección R de la CIIU Rev.4: artes escénicas, bibliotecas, "
            "deportes y otras actividades recreativas."
        ),
        "notes": "Serie inicia 2017-08.",
        "source": "CIIU Rev.4 adaptada a CAENES Rev.4 CL"  # :contentReference[oaicite:17]{index=17}
    },
    "rama_19": {
        "label": "Rama 19: Otras actividades de servicios",
        "description": (
            "Sección S de la CIIU Rev.4: asociaciones, reparación de "
            "computadores y enseres, servicios personales, etc."
        ),
        "notes": "Serie inicia 2017-08.",
        "source": "CIIU Rev.4 adaptada a CAENES Rev.4 CL"  # :contentReference[oaicite:18]{index=18}
    },
    "rama_20": {
        "label": "Rama 20: Actividades de los hogares como empleadores",
        "description": (
            "Sección T de la CIIU Rev.4: hogares que producen bienes o "
            "servicios de uso propio / como empleadores de personal doméstico."
        ),
        "notes": "Serie inicia 2017-08.",
        "source": "CIIU Rev.4 adaptada a CAENES Rev.4 CL"  # :contentReference[oaicite:19]{index=19}
    },
    "rama_21": {
        "label": "Rama 21: Actividades de organizaciones y órganos extraterritoriales",
        "description": (
            "Sección U de la CIIU Rev.4: organismos internacionales, "
            "representaciones diplomáticas y otras entidades extraterritoriales."
        ),
        "notes": "Serie inicia 2017-08.",
        "source": "CIIU Rev.4 adaptada a CAENES Rev.4 CL"  # :contentReference[oaicite:20]{index=20}
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