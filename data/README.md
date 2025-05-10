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

| Columna                                                                          | Tipo       | Descripción / cálculo                                                                                     |
| -------------------------------------------------------------------------------- | ---------- | --------------------------------------------------------------------------------------------------------- |
| `ano_trimestre`                                                                  | int        | Año de la ventana móvil (2025, 2024, …). Corresponde al año del último mes del trimestre.                 |
| `mes_central`                                                                    | int (1‑12) | Mes central de la ventana móvil (01 = DEF, 02 = EFM, … 12 = NDE).                                         |
| `personas_ocupadas`                                                              | Int64      | Σ `fact_cal` donde `cae_especifico` ∈ 1‑7.                                                                |
| `personas_desocupadas`                                                           | Int64      | Σ `fact_cal` donde `cae_especifico` ∈ 8‑9.                                                                |
| `personas_fuera_fuerza_trabajo`                                                  | Int64      | Σ `fact_cal` resto de categorías.                                                                         |
| `personas_edad_trabajar`                                                         | Int64      | Σ `fact_cal` con `edad ≥ 15 años`.                                                                        |
| `oc_hombres` / `oc_mujeres`                                                      | Int64      | Ocupados (`cae_especifico` 1‑7) por sexo (1, 2).                                                          |
| `oc_formal` / `oc_informal`                                                      | Int64      | Ocupados con `ocup_form` = 1 (formal) o 2 (informal).                                                     |
| `oc_tpi`                                                                         | Int64      | Ocupados con `tpi` = 1 (trabajo a plazo indef.).                                                          |
| `oc_sector_publico` / `oc_no_sector_publico`                                     | Int64      | Ocupados con `categoria_ocupacion` = 4 (adm. pública) o distinto de 4.                                    |
| `oc_calif_alta`                                                                  | Int64      | Ocupados con `b1_int` ∈ 1‑3 (Ciuo OIT 88/CL 2012 “directores, profesionales”).                            |
| `oc_calif_media`, `oc_calif_media_baja`, `oc_calif_baja`, `oc_otra_calificacion` | Int64      | Ver reglas en `scripts/totales_trimestre.py` según rangos de `b1_int`.                                    |
| `oc_ed_sup`, `oc_ed_media`, `oc_ed_basica`, `oc_sin_ed_basica`                   | Int64      | Ocupados por máximo nivel completado (`nivel`, `termino_nivel`).                                          |
| `oc_ed_sup_cft` / `oc_ed_sup_ip` / `oc_ed_sup_univ`                              | Int64      | Ocupados con educación superior completa de tipo CFT (nivel 7), IP (8) o universitaria /postgrado (9‑12). |
| `oc_ed_sup_compet_alta` / `media_baja` / `no_alta`                               | Int64      | Cruce de `oc_ed_sup` con calificación ocupacional (alta 1‑3, media‑baja 4‑9).                             |
| `fact_cal` *(solo en parquet granular)*                                          | float      | Factor de expansión original de INE (pesa cada registro).                                                 |
| `b1_int` *(solo en parquet granular)*                                            | Int64      | Código unificado de ocupación (CIUO‑88 → 1‑9) : usa `b1` (≥2018) o `b1_ciuo88` (<2018).                   |

## 4 | Reproducibilidad

1. `python -m venv .venv && pip install -r requirements.txt`
2. `python scripts/get_raw_release.py`  → descarga CSV originales.
3. `python scripts/build_trimester_panels.py`  → Parquet granulares.
4. `python scripts/totales_trimestre.py`   → panel + CSV + series mes.

Acciones de GitHub automatizan los pasos 3‑4 a cada push o calendario. 

## 5 | Licencia y citación

* **Código**: MIT License.
* **Datos INE**: dominio público chileno (Ley 19.628), citar como: “Instituto Nacional de Estadísticas (INE). Encuesta Nacional de Empleo, varias oleadas 2010‑2025, [https://www.ine.gob.cl”](https://www.ine.gob.cl”).

---

**Mantenedor:** @elaval · Última actualización automática: {{FECHA\_BUILD}}

