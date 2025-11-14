# datos-empleo-chile


## Script
python -m scripts.generar_documentacion_variables

# Descarga datos raw (.csv) del INE que se almacenados en un tar.gz como un asset del release
python -m scripts.descargar_csv_raw

# Para nuevos updates, hacer una descarga manual del los archivos .cs publicados por el INE en data/raw/ine

# Construir archivos por mes con datos granulares (microdatos)
python -m scripts.construir_panel_microdatos

# Construir datos procesados con los totales srimestrales
python -m scripts.generar_totales_trimestrales
python -m scripts.generar_series_mensuales_simplificadas

## A PArtir de los microdatos se generan resumenes agrupando variables de reportes comunes
# - resumenes_locales: genera un "cubo" para agregar personas en distintas categorias
# - totales con delta: genera tabla simplificada con columnas para distintas variable re reporte común
python -m scripts.generar_resumenes_locales
python -m scripts.generar_totales_con_deltas



