# Datos de Empleo Chile ‑ ENE

> Repositorio con los micro‑datos originales de la Encuesta Nacional de Empleo (INE) más series agregadas listas para análisis reproducible.

## 1 | Estructura del repo

```text
├─ data/
│  ├─ raw/ine/                # 181 CSV originales (NO versionados, descargan vía release)
│  ├─ processed/
│  │   ├─ ene-*.parquet        # 52 archivos granulares por trimestre móvil
│  │   ├─ ene_totales_trimestre.parquet  # panel anual‑trimestral agregado
│  │   ├─ ene_totales_trimestre.csv
│  │   └─ series_por_mes/serie_mesNN.csv # 12 series ‘mes central’ comparables inter‑anual
├─ scripts/                   # ETL reproducible
└─ notebooks/                 # exploración
```

## 2 | Descarga rápida en Python

```python
import pandas as pd
url = (
    "https://raw.githubusercontent.com/elaval/datos-empleo-chile/main/"
    "data/processed/ene_totales_trimestre.parquet"
)
df = pd.read_parquet(url)
```

## 3 | Diccionario de datos (nivel trimestre móvil)
## Diccionario de variables
👉 Consulte la lista completa en [`../docs/variables.md`](../docs/variables.md)                 |

## 4 | Reproducibilidad

1. `python -m venv .venv && pip install -r requirements.txt`
2. `python scripts/get_raw_release.py`  → descarga CSV originales.
3. `python scripts/build_trimester_panels.py`  → Parquet granulares.
4. `python scripts/totales_trimestre.py`   → panel + CSV + series mes.

Acciones de GitHub automatizan los pasos 3‑4 a cada push o calendario. 

Actualización de datos desde repositorio local:
$ python update_raw_release.py 2025-04

## 5 | Licencia y citación

* **Código**: MIT License.
* **Datos INE**: dominio público chileno (Ley 19.628), citar como: “Instituto Nacional de Estadísticas (INE). Encuesta Nacional de Empleo, varias oleadas 2010‑2025, [https://www.ine.gob.cl”](https://www.ine.gob.cl”).

---

**Mantenedor:** @elaval · Última actualización automática: {{FECHA\_BUILD}}

