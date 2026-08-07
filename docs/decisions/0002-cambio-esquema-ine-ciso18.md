# ADR-0002 — Cambio de esquema del INE en AMJ 2026 (adopción CISO-18)

- **Estado:** Aceptada
- **Fecha:** 2026-08-06
- **Ámbito:** `config/columns.yml` + `scripts/construir_panel_microdatos.py`
- **Decide sobre:** cómo absorber cambios de esquema en los CSV crudos del INE sin romper
  la continuidad interna del pipeline ni de las series publicadas.

---

## Contexto

Con la publicación del trimestre **abril–junio 2026** (`ene-2026-05-amj.csv`), el INE adoptó
la **CISO-18** (Clasificación Internacional de la Situación en la Ocupación, OIT 2018, que
reemplaza a la CISE-93) y cambió el esquema del CSV público: de **185 a 222 columnas**.
Referencias: *Documento Metodológico Adopción CISO-18* y *Libro de Códigos ENE*, ambos
INE, julio 2026.

El cambio tiene tres componentes de naturaleza distinta:

1. **38 columnas nuevas**: la clasificación derivada (`ciso1`, `ciso2`, `ciso3_a`,
   `ciso3_b`, `cd`, `cdi`, `cdd` — incluye la categoría nueva de **contratistas
   dependientes**, ~7,4% de los ocupados), las preguntas de insumo que el cuestionario
   aplica desde 2020 pero que recién ahora se publican (`do_1`–`do_4`, `de_1a`–`de_3b`,
   `re1`–`re6`), variables intermedias de dependencia (`dep_*`, `riesgo_economico`, etc.)
   y flags analíticos antes implícitos (`pet`, `ft`, `fta`, `inhab`).
2. **1 renombre silencioso**: `id` ("Iniciador/a disponible") pasó a llamarse `idisp`.
3. **Continuidad**: `categoria_ocupacion` (CISE-93) se mantiene intacta.

El renombre produjo un **bug silencioso**: `construir_panel_microdatos.py` rellena columnas
ausentes con NA en lugar de fallar, por lo que `id` quedó NA para AMJ 2026 y los
iniciadores disponibles contaron 0 en `generar_totales_trimestrales.py` /
`generar_agregados.py`, distorsionando la fuerza de trabajo ampliada (`fta`) y las tasas de
subutilización (TPL, SU1–SU4) de ese trimestre (~141 casos muestrales, ~27 mil personas
expandidas). La cifra publicada era plausible pero fabricada — el peor tipo de error.

## Decisión

### 1. Nombres internos estables + normalización en la capa de ingesta

El pipeline conserva los **nombres históricos** como contrato interno. Los renombres del
INE se absorben en un único punto — el diccionario `RENAMES` de
`construir_panel_microdatos.py` — que traduce nombres nuevos a históricos al leer cada CSV
(`idisp` → `id`, extensible a futuros renombres).

**Por qué:** los parquet por trimestre apilan filas 2010–2026 y deben tener esquema
uniforme; y `id` se usa en `generar_totales_trimestrales.py`, `generar_agregados.py` y
`_column_defs.py`. Migrar todo el pipeline a `idisp` tocaba más superficie con cero
beneficio analítico. *(Principio: contrato vs. juicio — el esquema interno es contrato
fijo; el mapeo desde la fuente es lo configurable.)*

### 2. Incorporar la dimensión CISO-18 al subset de microdatos

Se agregan a `config/columns.yml`: `ciso1`, `ciso2`, `ciso3_b`, `cd`. Quedan pobladas
desde AMJ 2026 y NA hacia atrás. Se excluyen por ahora `ciso3_a`, `cdi`, `cdd` y las
preguntas de insumo (derivables/redundantes para el consumo actual; agregarlas es trivial
si un análisis las pide). *(Principio: la granularidad sigue al consumo.)*

### 3. Regla de series: CISE-93 y CISO-18 no se mezclan

- La serie histórica de categoría en la ocupación sigue siendo `categoria_ocupacion`
  (CISE-93), sin quiebre.
- La serie CISO-18 **parte en AMJ 2026** en este repo. No es comparable 1:1 con CISE-93:
  en 2025, ~3,3 pp de asalariados privados y ~2,7 pp de cuenta propia migran a
  contratistas dependientes; el servicio doméstico se fusiona (puertas adentro/afuera) y
  los familiares no remunerados pasan del grupo independiente al dependiente.
- La serie CISO-18 2020–2025 **no es derivable de los microdatos públicos** (las preguntas
  de insumo no se publicaron antes de AMJ 2026). Existe solo como agregados oficiales en
  los anexos G/H del documento metodológico, calculados por el INE sobre su **Base Anual**
  (promedio anual, `fact_anual`) — transcrita a `conocimiento/referencia-ine-ciso18.json`
  como evidencia externa anual, no comparable con trimestres móviles.
  *(Principio: evidencia ≠ hallazgo — ante lo no disponible, decir "no derivable".)*

## Consecuencias

**Positivas**
- AMJ 2026 corregido y verificado: `id` = 141 casos muestrales (serie: 201 en 2023, 161 en
  2024, 148 en 2025); `ciso2` poblado en 42.473 filas; `cd` = 3.341 contratistas
  dependientes — cifras que calzan con el CSV crudo.
- Futuros renombres del INE se resuelven con una línea en `RENAMES`.
- La dimensión contratistas dependientes queda disponible en microdatos para análisis y
  para la capa de conocimiento.

**Límites / deuda asumida**
- Los scripts de agregados aún no explotan las columnas CISO (solo viajan en microdatos).
- La detección del cambio fue reactiva: el rellenado silencioso con NA sigue vigente para
  cualquier otra columna que el INE renombre o elimine a futuro. Mitigación pendiente: un
  chequeo en `construir_panel_microdatos.py` que alerte cuando una columna esperada falta
  en un CSV nuevo (en vez de rellenar NA sin avisar).
- `ciso3_b` distingue 19 categorías con celdas chicas (ej. servicio doméstico de corta
  duración ≈ 9,5 mil personas a nivel nacional): usar con `n` a la vista.

## Alternativas consideradas

- **Migrar el pipeline a `idisp` (nombre nuevo del INE).** Rechazada: toca 3+ scripts y
  rompe la uniformidad de esquema dentro de cada parquet apilado; el nombre interno es
  contrato del pipeline, no de la fuente.
- **Duplicar ambas columnas (`id` e `idisp`).** Rechazada: dos nombres para el mismo hecho
  invita a inconsistencia.
- **No incorporar CISO-18 todavía.** Rechazada: el costo marginal es casi nulo (4 columnas
  en un YAML) y la categoría de contratistas dependientes es la principal novedad analítica
  de la ENE desde la medición de informalidad (2017).

## Referencias

- INE (2026), *Documento Metodológico: Adopción de la CISO-18 en la ENE*, julio 2026
  (esp. §4 construcción, §5.2 impacto CISE-93 vs CISO-18, anexos B–F código R, anexos G/H
  serie anual 2020–2025).
- INE (2026), *Libro de Códigos Base de Datos ENE*, 31 de julio de 2026 (esp. §5.4
  variables analíticas: definiciones de `ciso*`, `cd*`, `idisp`).
- [ADR-0001](0001-capa-de-conocimiento.md) — capa de conocimiento (regla evidencia ≠
  hallazgo aplicada aquí a la serie 2020–2025).
