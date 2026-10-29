# ADR-0003 — Los extremos de una serie se computan, no se heredan

- **Estado:** Aceptada
- **Fecha:** 2026-10-29
- **Ámbito:** `conocimiento/hallazgos/` + `conocimiento/metodologia.md`
- **Decide sobre:** cómo se escriben y se re-verifican las afirmaciones de extremo
  («el máximo», «el mínimo», «el más alto desde») y de universalidad («en todo el
  período», «nunca», «por primera vez») en los hallazgos curados.

---

## Contexto

Al recurar los hallazgos para el release `2026-08-jas` aparecieron **dos afirmaciones
falsas** que venían vigentes del release anterior:

1. `h-tend-brecha-participacion-sexo` afirmaba que la desocupación femenina se mantuvo
   por sobre la masculina **«en todo el período»** 2010-2026. Falso: en 2020 la
   masculina fue mayor.
2. `h-tend-envejecimiento-y-juvenil` situaba el mínimo de la desocupación juvenil en
   **15,4 % (2015)**. Falso: el mínimo es 2013.

La primera hipótesis fue que las dos se habían falseado al cambiar el mes central de la
serie (de los trimestres JJA a los JAS). **Al comprobarlo, no era así:** las dos ya eran
falsas en la serie sobre la que fueron escritas.

| Afirmación | Serie JJA (donde se escribió) | Serie JAS |
|---|---|---|
| TD femenina siempre sobre la masculina | falso (2020: 12,06 % vs 13,49 %) | falso (2020: 11,65 % vs 12,83 %) |
| Mínimo de la TD juvenil | 2013 · 15,00 % (no 2015 · 15,44 %) | 2013 · 14,43 % |

El error, entonces, no fue de empalme de series: fue **afirmar un universal y un extremo
sin computarlos sobre la serie completa**. Son las dos clases de afirmación más fáciles de
escribir de memoria y las únicas que un solo punto nunca puede respaldar.

### El segundo riesgo, que es real pero no causó esto

La ENE publica doce series anuales comparables, una por mes central, y **cada una tiene sus
propios extremos**. Medido entre los dos últimos releases, con el mismo indicador y el mismo
año:

| Indicador | Serie JJA | Serie JAS |
|---|---|---|
| Mínimo de la TD juvenil | 2013 · 15,00 % | 2013 · 14,43 % |
| Sobrecalificación, último dato | 32,25 % | 31,83 % |
| Sobrecalificación, máximo de la serie | 2018 · 33,01 % | 2018 · 32,50 % |
| Brecha TD 25-34 vs nacional, 2026 | 2,54 pp | 2,67 pp |
| Brecha TD 25-34, máximo previo | 2017 · 2,58 pp | 2017 · 2,57 pp |
| Brecha de participación por sexo, 2026 | 17,29 pp | 17,32 pp |
| Ocupados de 65 y más en 2010 | 316.087 | 316.138 |

La fila de la brecha 25-34 muestra por qué importa: con los mismos datos y el mismo año, en
la serie JJA el valor de 2026 **queda bajo** el récord no pandémico de 2017 y en la serie JAS
**es el máximo de toda la serie**. La conclusión cualitativa se invierte. Heredar un extremo
de un release al siguiente no es una imprecisión de decimales: puede cambiar el enunciado.

Esto no es nuevo del todo — ADR-0001 ya anotó como deuda que los cortes cubren solo el mes
central del release — pero ahí era una limitación de *disponibilidad de datos*. Aquí es una
regla de *redacción de hallazgos*, que es lo que faltaba.

## Decisión

### 1. Un extremo o un universal se computa antes de escribirse

Ninguna ficha afirma «el máximo», «el mínimo», «el más alto desde», «por primera vez»,
«nunca» o «en todo el período» sin que esa afirmación se haya calculado sobre la serie
completa de `evidencia/series-*.json` en el mismo acto de curación. No se hereda del release
anterior, no se escribe de memoria y no se deduce del enunciado de otra ficha.

El contraejemplo vale más que la afirmación: cuando el cómputo encuentra excepciones, van
dichas (2020 en la brecha por sexo), y cuando el extremo es de un subconjunto, va acotado
(«el más alto fuera de la pandemia», no «el más alto»).

### 2. Toda afirmación de extremo declara sobre qué serie se midió

Las doce series anuales son objetos distintos. Cada ficha con un extremo dice en sus
`caveats` si se midió sobre la **serie anual del mes central del release** (diecisiete
puntos, uno por año) o sobre los **199 trimestres móviles**. Las dos son legítimas y
responden preguntas distintas; confundirlas no.

### 3. Al cambiar el mes central, los extremos se recalculan

Un release nuevo con otro mes central no es el mismo release con datos frescos: es otra
serie. Las fichas de tendencia (`h-tend-*`), que se actualizan en sitio, recalculan sus
extremos completos, no solo su último punto.

### 4. Lo que falla se deja escrito en la ficha que lo reemplaza

Cuando una afirmación se corrige, el caveat de la ficha nueva dice qué decía la anterior y
por qué era falsa. Sin eso, la corrección es invisible para quien ya citó la versión vieja.

## Consecuencias

**Positivas**
- Las afirmaciones más citables de la capa —los récords— pasan a ser las más verificadas,
  en vez de las más frágiles.
- La curación de cada release incluye un paso mecánico y repetible: recomputar extremos.
- El rastro de correcciones queda en el propio dato, no solo en el historial de git.

**Costos / límites asumidos**
- Curar una ficha de tendencia es más caro: obliga a recorrer la serie, no a copiar el
  enunciado anterior y cambiarle las cifras.
- La regla es una convención de redacción, **no un chequeo automatizado**: el validador
  comprueba que las fichas declaren `vigencia` y `confianza` y que sus caveats estén
  glosados, pero no puede verificar que un «máximo» lo sea. Un extremo mal computado sigue
  pasando la validación.
- Las doce series conviven, así que dos fichas correctas pueden dar cifras distintas del
  mismo indicador. Por eso la regla 2 obliga a declarar la serie.

## Alternativas consideradas

- **Automatizar la verificación de extremos en el validador.** Deseable, rechazada por
  ahora: exigiría que cada afirmación declarara en forma estructurada qué extremo pretende
  (indicador, serie, subconjunto, operador), lo que es casi reescribir el enunciado en
  código. Queda como deuda: el caso más acotado —que el último punto de una serie sea o no
  su máximo— sí es automatizable y vale la pena hacerlo primero.
- **Prohibir las afirmaciones de extremo en los hallazgos.** Rechazada: son parte de lo que
  hace útil un hallazgo. El problema no es afirmarlas, es no computarlas.
- **Fijar un único mes central canónico para todas las tendencias.** Rechazada: el release
  vigente manda, y amarrar las tendencias a un mes central fijo obligaría a regenerar
  evidencia de otro trimestre para cada publicación.

## Referencias

- Incidente y corrección: commits de la recuración `2026-08-jas` (hallazgos v3.4).
- Deuda relacionada: ADR-0001, «Límites / deuda asumida» (los cortes cubren solo el mes
  central del release).
- Regla operativa en la capa: `conocimiento/metodologia.md`, sección 1-bis.
- Principios de diseño aplicados (KB MindTheContext): evidencia ≠ hallazgo (el rigor viaja
  con el dato; ante lo no derivable, decirlo en vez de fabricarlo); decisiones validadas por
  evidencia.
