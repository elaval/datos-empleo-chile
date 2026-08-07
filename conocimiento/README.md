# Capa de conocimiento — empleo en Chile (ENE)

Capa intermedia entre los **datos crudos** (`../data/`) y los **reportes/respuestas**.
Está diseñada para que un agente (Claude u otro) construya conocimiento de orden superior
—reportes, respuestas, análisis— **sin re-procesar los datos crudos**.

> El **porqué** de este diseño (arquitectura de tres estratos, evidencia ≠ hallazgo, fuentes,
> reproducibilidad y límites) está en [`docs/decisions/0001-capa-de-conocimiento.md`](../docs/decisions/0001-capa-de-conocimiento.md).

## Cómo leer esta capa (orden recomendado)

Lee de lo **estable** a lo **variable** (así lo estable queda al inicio del contexto y es
cacheable):

1. **`ontologia.md`** — qué es cada concepto y cómo se relacionan (el árbol PET→FT→O/DO,
   las tres tasas, las identidades). Léelo primero para razonar sin errores de dominio.
2. **`indicadores.json`** — el **contrato**: definición formal, unidad, escala y fórmula de
   cada indicador y dimensión.
3. **`metodologia.md`** — la **capa de rigor**: provenance, ponderación `fact_cal`, escala
   0–100, la **recalibración Censo 2017**, y qué NO permite concluir la base.
4. **`evidencia/`** — los **hechos computados** (regenerables). Ver abajo.
5. **`hallazgos/hallazgos.json`** — **insights curados** sobre la evidencia, con sus refs,
   confianza y caveats.
   - Los **caveats** son o bien un **slug** del glosario canónico en
     `esquema.caveats.glosario`, o bien una **frase completa** cuando la advertencia es
     específica de ese hallazgo. Regla para expandirlos: si el texto tiene espacios ya es
     prosa; si es kebab-case, hay que buscarlo en el glosario. **Un consumidor no debe mostrar
     el slug crudo.**

## Los tres estratos

| Estrato | Archivos | Naturaleza | Se actualiza |
|---|---|---|---|
| **Contexto / contrato** | `ontologia.md`, `indicadores.json`, `metodologia.md` | Estable, autorado | Solo si cambia una definición |
| **Evidencia** | `evidencia/*.json` | Objetiva, computada, con provenance | En cada publicación del INE (regenerar) |
| **Hallazgos** | `hallazgos/hallazgos.json` | Interpretación curada | Cuando se valida un nuevo insight |

**Regla de oro:** evidencia ≠ hallazgo. La evidencia es un hecho reproducible; el hallazgo
es una interpretación que **apunta** a la evidencia que lo sostiene. No los confundas al citar.

## Contenido de `evidencia/`

- **`snapshot.json`** — foto del último release: nacional (con variación interanual),
  composición de ocupados **con Δ interanual** (incl. agregados asalariados vs. independientes
  y el desglose asalariado público vs privado), un bloque **`formalidad`** (formal/informal y
  tasa de informalidad `toi`, con Δ), y cortes por **sexo / edad / región / nacionalidad** con
  su Δ interanual. Cada corte trae `n` (tamaño muestral sin ponderar): `n` bajo ⇒ mayor error
  muestral, leer con cautela.
- **`series-nacional.json`** — serie completa (todos los períodos y meses centrales) de los
  indicadores nacionales + composición + informalidad + ocupados por sexo.
- **`series-cortes.json`** — series anuales comparables (mismo mes central, año contra año)
  por sexo, edad y región.
- **`tendencias.json`** — descriptores calculados de la serie **nacional**: primero/último
  valor, hace 1 y 5 años, máximo, mínimo, dirección del último año y **cambio de largo plazo**
  (primer → último año), para el mes central del release.
- **`tendencias-cortes.json`** — los mismos descriptores, pero **por grupo de cada corte**
  (sexo / edad / región / nacionalidad). Evita que un agente tenga que recomputar tendencias
  desde `series-cortes.json`. `cambio_largo_plazo` viene en pp para tasas y en absoluto + %
  para stocks.
- **`_meta.json`** — release, fuentes, cobertura y fecha de generación.

## Regenerar la evidencia

Tras cada nueva publicación del INE (nuevos `.csv` en `data/raw/ine/` procesados a los
parquet de `data/processed/`):

```bash
python -m scripts.generar_conocimiento
```

Regenera todo `evidencia/` desde la tabla maestra y los microdatos del mes central del
último release. Los estratos de contrato y de hallazgos **no** se tocan automáticamente:
el contrato es estable y los hallazgos se curan a mano (revisar si un hallazgo previo sigue
vigente con la nueva evidencia).

## Validar el pack (doble chequeo)

```bash
python -m scripts.validar_conocimiento
```

Verifica en **tres vías independientes** y sale con código ≠ 0 si algo falla:

| Bloque | Qué comprueba | Qué detecta |
|---|---|---|
| **A. Coherencia interna** | identidades (`FT = O + DO`, `TD = 100·DO/FT`); que cada partición sume el total **en niveles y en variaciones**; que los slugs de caveats estén glosados | inconsistencias dentro de la base |
| **B. vs microdatos** | recómputo independiente desde los microdatos ponderando por `fact_cal` (nacional, composición, formalidad y los cuatro cortes con su `n`) | errores del generador |
| **C. vs boletines INE** | contraste contra las cifras publicadas por el INE, transcritas a mano en `referencia-ine.json` | que la base entera se haya desviado de la fuente oficial |

(B) y (C) son complementarios: (B) puede pasar y (C) fallar. Al incorporar un release
nuevo, transcribir las cifras de su boletín a `referencia-ine.json` para que (C) lo cubra.

**Niveles y variaciones se verifican por separado**, a propósito: un error puede aparecer en
los deltas —o en un gráfico que los muestre— sin romper ninguna suma de stock. Para las
particiones con residuo (educación tiene ocupados sin dato de nivel; jornada, ocupados que no
declaran horas) el residuo y su variación se publican en el `_cobertura` del bloque, de modo
que la suma cuadre **exactamente** y no por tolerancia.

> ⚠ (C) solo aplica a **releases recientes**. Los boletines anteriores a la recalibración
> post-Censo 2017 **no** coinciden con esta base, y eso es esperado, no un error (ver el
> caveat `recalibracion-censo-2017`).

## Referencias externas transcritas

- **`referencia-ine.json`** — cifras de los boletines trimestrales del INE (las usa el
  bloque C de la validación).
- **`referencia-ine-ciso18.json`** — serie **anual** CISO-18 2020–2025 (anexos G/H del
  documento metodológico de adopción de la CISO-18, INE 2026). Solo contexto histórico de
  la nueva clasificación: base ANUAL (no comparable con trimestres móviles), **no derivable
  de los microdatos públicos** (las variables CISO se publican desde AMJ 2026) y no
  comparable con `categoria_ocupacion` (CISE-93). Ver
  [`ADR-0002`](../docs/decisions/0002-cambio-esquema-ine-ciso18.md).

## Escala rápida (para no equivocarse)

- Tasas: **0–100** (ej. `td = 9.44` = 9,44 %).
- Conteos: personas (no miles).
- Comparación válida: **mismo mes central, año contra año**.
- Ponderación de microdatos: **siempre** `fact_cal`.
- Al citar cifras históricas: recordar la **recalibración** (no calzan con boletines antiguos).
