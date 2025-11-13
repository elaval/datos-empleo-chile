# datos-empleo-chile


## Script
python -m scripts.generar_documentacion_variables

python -m scripts.descargar_csv_raw

python -m scripts.construir_panel_microdatos



python -m scripts.generar_totales_trimestrales
python -m scripts.generar_series_mensuales_simplificadas

## A PArtir de los microdatos se generan resumenes agrupando variables de reportes comunes
# - resumenes_locales: genera un "cubo" para agregar personas en distintas categorias
# - totales con delta: genera tabla simplificada con columnas para distintas variable re reporte común
python -m scripts.generar_resumenes_locales
python -m scripts.generar_totales_con_deltas



