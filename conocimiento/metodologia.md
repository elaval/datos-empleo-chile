# Metodología y advertencias — capa de conocimiento

Este documento es la **capa de rigor**. Todo agente que use la evidencia o los
hallazgos debe conocer estas reglas antes de afirmar nada. Es la contraparte de
`conocimiento/indicadores.json` (el contrato de *qué* mide cada cosa); aquí está el
*cómo* y el *cuánto confiar*.

Referencia canónica de las fuentes crudas: `../DATOS.md` (o, en el proyecto de
análisis, `DATOS.md`).

---

## 1. Unidad de observación: el trimestre móvil

La ENE publica **trimestres móviles** (medias móviles de 3 meses), identificados por
su **mes central**. Ejemplo: mes central 5 = trimestre **abril-mayo-junio (AMJ)**.

- Una cifra es una media de tres meses, no un dato puntual del mes central.
- **Comparar siempre contra el mismo mes central de años anteriores** (variación
  interanual). El empleo tiene estacionalidad fuerte; la comparación entre trimestres
  consecutivos la confunde. Toda la evidencia de cortes usa esta lógica año-contra-año.

## 2. Ponderación: `fact_cal`

Los agregados de microdatos se calculan **siempre** ponderando por `fact_cal` (factor
de expansión calibrado), nunca contando filas. La población en edad de trabajar (PET)
son las personas de **15 años o más** (`edad >= 15`).

## 3. ⚠️ Recalibración: las cifras NO coinciden con los boletines originales del INE

**El hallazgo metodológico más importante de esta base.** El INE re-expandió los
microdatos históricos con **proyecciones de población actualizadas** (posteriores al
Censo 2017). Los microdatos antiguos traían dos factores:

| Factor | Qué es | Ejemplo FMA 2010 |
|---|---|---|
| `fact` | Original de la época — reproduce el boletín publicado entonces | TD 8,63 %, FT 7.625.805 (= boletín ENE Nº 139: 8,6 %) |
| `fact_cal` | Recalibrado — **es el que usa toda esta base** | TD 8,84 %, FT 7.896.518 |

- Efecto: ~**+0,2 a +0,3 pp** en la TD histórica y ~**+2 pp** en participación, parejo
  entre años. La **forma y el ranking de la serie se conservan**; cambia el nivel absoluto.
- Los microdatos **desde 2022** ya solo traen `fact_cal`.
- **Implicancia para un agente:** las comparaciones *internas* a esta base son
  homogéneas (todos los años en base `fact_cal`) y válidas. Pero **al citar una cifra
  histórica no la contrastes con un boletín antiguo sin advertir la recalibración**.
  Cuando publiques niveles históricos, agrega la nota de método.

## 3-bis. ⚠️ Quiebres de clasificación: no todas las series son continuas

Además de la recalibración, hay **cambios de clasificación** que parten series en dos. No son
errores: son cambios de estándar internacional que el INE adopta.

| Clasificación | Qué clasifica | Corte |
|---|---|---|
| **CIUO-88 → CIUO-08** | La *ocupación* (qué tarea hace la persona) | CIUO-88 hasta 2018, CIUO-08 desde 2017. En microdatos, `b1_ciuo88` viene **vacío desde 2019**. |
| **CISE-93 → CISO-18** | La *situación en la ocupación* (relación laboral) | El INE adopta CISO-18 en AMJ 2026. `categoria_ocupacion` (CISE-93) se mantiene intacta. Ver ADR-0002. |

**Reglas prácticas:**

- El bloque `ocupacion_ciuo08` de la evidencia **solo se emite desde 2019**, para que nadie
  construya sin querer una serie que cruce el corte. No mezclar CIUO-88 con CIUO-08.
- El agregado `grupo_ciuo_alta` (G1–G3), que usa la tasa de desajuste educativo, **sí** tiene
  serie larga en la maestra; pero su composición interna cambia de clasificación en el corte:
  la tendencia larga es utilizable, el desglose por grupo hacia atrás no.
- Un salto brusco en una categoría residual (`G10 No identificado`, `NS-NR`) suele indicar
  cambio de codificación, no un fenómeno real. Verificar antes de interpretarlo.
- **Un renombre puede romper un indicador sin que se note.** Con CISO-18 el INE renombró
  `id` (iniciadores disponibles) a `idisp`; el pipeline rellenaba con NA en vez de fallar, y
  las tasas de subutilización (SU1–SU4) y de presión laboral de AMJ 2026 salieron
  **plausibles pero fabricadas**. Ya está corregido (ADR-0002), y por eso el validador
  recomputa esas tasas desde sus componentes en vez de confiar en la columna publicada.

## 4. ⚠️ Escala de las tasas: depende de la tabla de origen

- Tabla **maestra** (`ene_trimestre_totales.parquet`) y **esta capa de conocimiento**:
  tasas en **0–100** (ej. `td = 9.44` = 9,44 %).
- Tabla de **deltas** (`totales_con_deltas.parquet`): tasas en **0–1**.

Toda la evidencia de `conocimiento/` está en **0–100**. No vuelvas a multiplicar por 100.

## 5. Cómo se computa cada cosa (provenance)

| Bloque de evidencia | Fuente | Método |
|---|---|---|
| Nacional (serie completa, todos los meses) | tabla maestra | Lectura directa de columnas (autoritativo, calza con INE). |
| Composición por categoría / sector | tabla maestra | Columnas `categoria_*`, serie nacional completa. |
| Cortes por sexo / edad / región | microdatos del mes central del release | `fact_cal` ponderado, `edad>=15`; un archivo apila todos los años de ese trimestre → serie anual comparable. |

Consistencia verificada: el nacional computado de microdatos calza **exactamente** con
la tabla maestra (misma ponderación `fact_cal`).

## 6. Límites de interpretación (qué NO permite esta base)

- **No permite atribuir causalidad.** La evidencia describe *qué* pasó y su tendencia,
  no *por qué*. Un shock (ej. de precios) puede tener efectos rezagados que un trimestre
  no aísla.
- **La identidad `ft = o + do` es aritmética, no causal.** Explica cómo se reparte una
  variación, no por qué la economía generó (o no) los empleos.
- **Muestral:** cortes muy finos (ej. una región × un grupo etario × un año) pueden tener
  alto error muestral. Los cortes de esta capa son de una sola dimensión por eso.
- **Formalidad e informalidad** tienen serie consistente **desde 2017** (definición OIT).

## 7. Escala de escalas rápida (cheat-sheet para el agente)

- Tasas de esta capa: **0–100**.
- Conteos: personas (no miles).
- `delta_<x>`: variación interanual absoluta. `delta_rel_<x>`: en %. `delta_pp_<x>`: en
  puntos porcentuales (solo tasas).
- Comparación válida = mismo mes central, año contra año.
