# ADR-0001 — Capa de conocimiento sobre los datos ENE

- **Estado:** Aceptada
- **Fecha:** 2026-08-05
- **Ámbito:** `conocimiento/` + `scripts/generar_conocimiento.py`
- **Decide sobre:** cómo exponer los datos de empleo (ENE) para que agentes de IA construyan
  reportes y respuestas de forma rigurosa y reproducible.

---

## Contexto

El repo `datos-empleo-chile` transforma microdatos crudos de la ENE (INE) en tablas
procesadas (microdatos por mes, agregados trimestrales, resúmenes). Para *usar* esos datos
—responder preguntas, escribir reportes— un agente (Claude u otro) hasta ahora debía:

1. Conocer la mecánica de los datos (escalas, `fact_cal`, palabras reservadas SQL, la
   recalibración Censo 2017, qué tabla usar para qué).
2. Re-procesar los parquet en cada sesión.
3. Distinguir por su cuenta un hecho verificable de una interpretación.

Esto es frágil: repite trabajo, invita a errores de dominio (ej. leer una tasa en la escala
equivocada, o contrastar una cifra recalibrada con un boletín antiguo) y no deja rastro de
qué es evidencia y qué es juicio. Necesitábamos una **capa de contexto** estable entre los
datos crudos y los productos (reportes/respuestas).

## Decisión

Crear una **capa de conocimiento** (`conocimiento/`) organizada en **tres estratos**, con una
regla de oro: **evidencia ≠ hallazgo**.

| Estrato | Archivos | Naturaleza | Se actualiza |
|---|---|---|---|
| **Contexto / contrato** | `ontologia.md`, `indicadores.json`, `metodologia.md`, `README.md` | Estable, autorado | Solo si cambia una definición |
| **Evidencia** | `evidencia/*.json` | Objetiva, computada, con provenance | En cada publicación del INE (regenerable) |
| **Hallazgos** | `hallazgos/hallazgos.json` | Interpretación curada, con refs a evidencia | Cuando se valida un insight |

- El **contrato** define *qué* significa cada indicador (fórmula, unidad, escala, fuente) y
  las reglas de rigor (recalibración, `fact_cal`, límites de interpretación).
- La **evidencia** son hechos reproducibles: snapshot del último release, series completas,
  cortes y descriptores de tendencia. La produce un solo script.
- Los **hallazgos** son interpretaciones. Cada uno **enlaza la evidencia que lo respalda** y
  declara `confianza`, `caveats`, `ventana_temporal`, `no_implica` y `vigencia`.

### Decisiones de diseño específicas (y su porqué)

1. **Separación evidencia/hallazgo como invariante.** Un agente debe poder saber si cita un
   hecho o una opinión. Los hallazgos apuntan a evidencia; nunca al revés.
   *(Principio: contrato vs. juicio.)*

2. **Fuentes según el consumo, no según la UI.**
   - Nacional + composición (categoría/sector) + formalidad → **tabla maestra** (autoritativa,
     calza con INE, serie completa, todos los meses).
   - Cortes por sexo / edad / región / nacionalidad → **microdatos del mes central del
     release** ponderados por `fact_cal`; un archivo apila todos los años de ese trimestre, lo
     que da una serie anual comparable procesando un solo archivo.
   *(Principio: la granularidad sigue al consumo.)*

3. **Reproducibilidad por script, no artefactos a mano.** `scripts/generar_conocimiento.py`
   regenera **todo** el estrato de evidencia desde los parquet. El contrato y los hallazgos se
   curan a mano (el script no los toca). *(Principio: dev espeja prod; evidencia validada.)*

4. **Cortes de una sola dimensión (por ahora).** Los cruces finos (ej. región × sexo × edad)
   tienen error muestral alto. Cada corte lleva `n` (tamaño muestral sin ponderar) como señal
   de fragilidad. Los cruces se dejan explícitamente fuera y la capa deriva al agente a los
   microdatos cuando se necesitan. *(Principio: decisiones validadas por evidencia; claridad
   robusta.)*

5. **Orden de lectura estable → variable.** El `README` fija el orden ontología → indicadores
   → metodología → evidencia → hallazgos, para que lo estable quede al inicio del contexto del
   agente. *(Principio: orden cache-óptimo en prompts.)*

6. **El rigor viaja con el dato.** Escala 0–100 documentada, la recalibración Censo 2017
   explicada con el ejemplo `fact` vs `fact_cal`, y los límites (no causalidad, error muestral,
   formalidad desde 2017) en `metodologia.md`. Cada hallazgo declara su `no_implica`.

7. **Ciclo de vida de los hallazgos.** Campo `vigencia` (`vigente | revisar | superado`) con
   la regla: al regenerar evidencia de un nuevo release, revisar los hallazgos previos.

## Consecuencias

**Positivas**
- Un agente responde preguntas complejas de forma cuantificada y **trazable sin tocar un
  parquet** (probado: pregunta nacional + cortes + tendencia + caveats resuelta solo con la
  capa).
- La capa **falla de forma segura**: ante un cruce no disponible, obliga a decir "no
  derivable, ir a microdatos" en vez de inventar.
- Reproducible: un comando regenera la evidencia tras cada release del INE.
- Consistencia verificada: nacional de microdatos = tabla maestra; suma de cortes = nacional.

**Límites / deuda asumida**
- Sin cruces multidimensionales ni corte por rama de actividad (se pueden agregar).
- Los cortes cubren solo el **mes central del release** (consecuencia del diseño
  un-archivo-por-corte); tendencias por otro mes central exigen regenerar con ese release.
- Los hallazgos duplican cifras de la evidencia (comodidad de cita vs. fuente única);
  mitigado con el sello de `release` y la regla de `vigencia`.
- El contrato es autorado: cambios de definición requieren edición manual y criterio.

## Alternativas consideradas

- **Sin capa, el agente procesa parquet cada vez.** Rechazada: repite trabajo, propensa a
  errores de dominio, no separa evidencia de juicio.
- **Solo artefactos estáticos generados una vez.** Rechazada: no sobrevive a nuevas
  publicaciones del INE; viola dev-espeja-prod.
- **Todo en Markdown narrativo.** Rechazada para la evidencia: un agente necesita estructura
  consultable (JSON); el Markdown se reserva para contrato y ontología.
- **Cortes con todos los cruces.** Rechazada por ahora: error muestral; se prefiere servir lo
  robusto y marcar lo frágil con `n`.

## Regeneración y mantenimiento

```bash
python -m scripts.generar_conocimiento   # regenera conocimiento/evidencia/*
```

Tras cada release: (1) correr el generador; (2) revisar `vigencia` de los hallazgos previos;
(3) curar hallazgos nuevos si la evidencia los respalda.

## Referencias

- Entrada a la capa: `conocimiento/README.md`.
- Fuentes crudas y advertencias: `DATOS.md` (proyecto de análisis) / este repo.
- Principios de diseño aplicados (KB MindTheContext): contrato vs. juicio; granularidad sigue
  al consumo; dev espeja prod; orden cache-óptimo; decisiones validadas por evidencia; captura
  en el momento del insight.
