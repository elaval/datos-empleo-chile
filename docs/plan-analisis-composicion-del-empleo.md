# Plan de análisis — la dinámica de la composición del empleo y del desempleo

Estado: propuesta · 31-10-2026 · release de referencia: `2026-08-jas`

## 1. La pregunta

La desocupación nacional llegó a 9,80 % en julio-septiembre de 2026, la segunda cifra más alta
de la serie después de 2020, y los ocupados cayeron por segunda vez en diecisiete años. La
pregunta que este plan quiere responder no es cuánto subió la desocupación, sino **qué cambió en
la forma en que se contrata y no se contrata a la gente** — y en qué medida lo que estamos viendo
es un ciclo o un desplazamiento de régimen.

La intuición de partida tiene apoyo empírico inmediato. En el trimestre JAS, entre 2025 y 2026:

| Categoría ocupacional | Variación |
|---|---|
| Asalariados del sector privado | −115.699 |
| Asalariados del sector público | −31.692 |
| Empleadores | −8.103 |
| **Cuenta propia** | **+39.121** |
| Servicio doméstico | +6.695 |
| Familiares no remunerados | +6.803 |
| **Total ocupados** | **−102.875** |

La caída no es «del empleo»: es del **empleo asalariado**, y coexiste con un aumento del trabajo
por cuenta propia. Eso ya no es una cifra de coyuntura, es una afirmación sobre composición — y
es exactamente el tipo de afirmación que este plan debe sostener o refutar con serie larga.

## 2. Lo que ya está medido y no estamos usando

El hallazgo más barato del inventario: `data/processed/agregados/integrado/ene_trimestre_totales.csv`
tiene **133 columnas × 199 trimestres móviles**, y la capa de conocimiento (`conocimiento/evidencia/`)
publica solo un subconjunto. Están computadas y sin superficie:

| Bloque | Columnas | Cobertura real |
|---|---|---|
| Cesantes vs. buscan trabajo por primera vez | `cesantes`, `busca_trabajo_por_primera_vez` | **199 trimestres (2010-02 → 2026-08)** |
| Rama de actividad económica (CAENES rev4) | `rama_1` … `rama_21` | 109 trimestres (desde 2017-08) — **venían mal computadas; corregido, ver Línea E** |
| Cotizantes de pensiones | `cotizantes`, `dependientes_cotizantes`, y versiones por sector | 109 trimestres (desde 2017-08) |
| Desajuste educativo | `o_ed_sup_ciuo_alta`, `_media_baja`, `_no_alta` | 199 trimestres |
| Grupos de ocupación CIUO | `grupo_ciuo88_*` (2010→2019), `grupo_ciuo08_*` (2017→2026) | con solape 2017-2019 |
| Jornada y parcialidad | `tpi`, `tpv`, `tp_sin_declarar_voluntariedad`, tramos de horas | 199 trimestres |
| Servicio doméstico puertas afuera / adentro | `categoria_serv_domestico_*` | 199 trimestres |
| Inactividad desagregada | `fft_iniciadores`, `fft_inactivos_habituales`, `deseo_trabajar` | 199 / 199 / 79 (desde 2020-02) |

**JAS 2017 es una bisagra**: informalidad, cotizantes, rama CAENES y CIUO-08 empiezan todas ahí.
Hay entonces dos ventanas distintas y conviene decirlo en cada gráfico: diecisiete años para lo
básico, **diez años (2017-2026) para casi todo lo estructural**.

## 3. Lo que exige trabajo de pipeline

Los microdatos crudos están completos localmente: 199 archivos en `data/raw/ine/`, 222 columnas en
el más reciente. El panel procesado (`data/processed/microdatos/ene-NN-*.parquet`, uno por mes
central) conserva **47 de esas 222 columnas**. Fuera del panel, y por tanto fuera de alcance hasta
que se extienda, quedan las variables que responden directamente «cómo se contrata»:

| Variable | Qué mide | Disponible desde |
|---|---|---|
| `b15_1`, `b15_2` | Acuerdo escrito o de palabra; indefinido, plazo fijo o por obra | **2010** |
| `b17_mes`, `b17_ano` | Mes y año de inicio del empleo actual → antigüedad | **2010** |
| `b12` | Tamaño del establecimiento | **2010** |
| `e15_meses` / `e15_anos` → `e21_tramo` | Duración de la búsqueda de empleo | 2010, con cambio de nombre y de formato ~2020 |
| `e16_ciuo88`, `e18_ciiu_rev3` → equivalentes | Ocupación y rama del **empleo anterior** del desocupado | 2010, con cambio de clasificación |
| `ocup_honorarios` | Ocupados a honorarios | ~2020 |
| `plataformas_digitales`, `pd_ley`, `sda_pd` | Trabajo en plataformas y su encuadre legal | ~2020 |
| `meses_ocup_actual`, `cdi`, `cdd`, `cd`, `dep_economica`, `no_prevision` | Batería de contratista dependiente (CISO-18) | **solo 2026** |
| `estrato`, `conglomerado` | Diseño muestral → errores estándar | 2010 |
| `parentesco`, `hogar`, `nro_linea` | Estructura del hogar → jefatura, hogares sin ocupados | 2010 |
| `estudia_actual`, `curso` | Jóvenes que no estudian ni trabajan | 2010 |

`b15_1` y `b15_2` desde 2010 son el activo más valioso de esta lista: diecisiete años de **tipo de
contrato**, que es la variable que la narrativa necesita y que ningún informe del INE pone en serie
larga.

## 4. El hallazgo del inventario: los microdatos permiten seguir a la misma persona

Comprobado en esta sesión, no supuesto. La variable `idrph` **identifica a la misma persona entre
trimestres**:

- JAS 2025 → JAS 2026: **25.150 personas enlazadas** (25,9 % de la muestra del trimestre).
- Coherencia del enlace: 99,75 % mismo sexo, 99,98 % misma región, 98,69 % con edad +0 a +2 años.
- En el panel completo del mes central agosto, **419.045 personas (33 %) aparecen en dos o más años**.

Con eso se construye una matriz de transición real. La de JAS 2025 → JAS 2026, sin ponderar:

| Estado en 2025 | → Ocupado | → Desocupado | → Fuera de la fuerza de trabajo |
|---|---|---|---|
| Ocupado | 82,9 % | 4,5 % | 12,7 % |
| Desocupado | 48,3 % | 23,7 % | 28,0 % |
| Fuera de la FT | 10,3 % | 3,8 % | 85,9 % |

Esto es otra clase de dato que todo lo anterior: no compara dos fotos agregadas, mide **flujos de
personas**. Es lo único del plan que responde literalmente a «cómo se ha movido el perfil».

Y es también lo más fácil de publicar mal. Tres límites que deben ir pegados a cualquier cifra
que salga de aquí:

1. **`fact_cal` es un ponderador transversal, no longitudinal.** No está diseñado para representar
   a la población en la submuestra que permanece. Las transiciones se reportan como proporciones
   dentro de la muestra enlazada, no como niveles poblacionales, hasta que se construya y valide
   un ponderador propio.
2. **La permanencia del 25,9 % no es aleatoria.** Quien se muda, quien emigra y quien deja de
   responder salen del enlace, y es verosímil que esas salidas correlacionen con pérdida de empleo.
   El sesgo tiene signo probable, no magnitud conocida: hay que acotarlo antes de afirmar.
3. **Trimestres móviles vecinos comparten dos meses de levantamiento.** El 90,7 % de solape entre
   JJA y JAS 2026 no son observaciones nuevas, es la misma entrevista reutilizada. El flujo solo
   es genuino entre entrevistas distintas: el eje debe ser `ano_encuesta` + `mes_encuesta`, no el
   trimestre móvil.

## 5. Las líneas de análisis

Ordenadas por razón entre valor narrativo y costo. Cada una declara con qué se hace y qué la refutaría.

### Línea A — ¿Quién absorbe el ajuste? (serie larga de categoría ocupacional)
**Pregunta:** ¿la caída del empleo asalariado con alza del cuenta propia es un patrón de cada
desaceleración, o 2026 es distinto?
**Insumo:** agregados ya computados, 199 trimestres. Costo bajo.
**Método:** serie JAS por categoría, variación interanual, y participación de cada categoría en el
total. Contrastar 2009-2010, 2020-2021 y 2024-2026.
**Refutación:** si en cada episodio anterior el cuenta propia también subió mientras caía el
asalariado, lo de 2026 es el patrón cíclico conocido y no hay nada estructural que contar.

### Línea B — El contrato, no la categoría
**Pregunta:** entre quienes sí tienen empleo dependiente, ¿cambió la forma del vínculo? ¿Más plazo
fijo y por obra, menos indefinido? ¿Menos cotización?
**Insumo:** `cotizantes` / `dependientes_cotizantes` desde 2017 (ya computado: 83,96 % → 83,57 %
entre JAS 2025 y 2026) **más** `b15_1` / `b15_2` desde 2010, que exigen extender el panel.
Costo medio.
**Método:** serie de composición del vínculo dentro de los dependientes; tasa de cotización como
proxy independiente de la misma cosa. Las dos series deben moverse juntas; si no, una de las dos
está mal construida.
**Refutación:** si la mezcla indefinido / plazo fijo es plana en diecisiete años, la tesis de la
precarización del vínculo no se sostiene y hay que contar la historia por el lado del volumen.
**Esta es la línea central del plan.**

### Línea C — El perfil del desempleo
**Pregunta:** ¿quiénes son el millón de desocupados? ¿Perdieron un empleo o nunca lo tuvieron?
¿Cuánto llevan buscando? ¿De qué sector salieron?
**Insumo:** `cesantes` y `busca_trabajo_por_primera_vez` están computados para los 199 trimestres y
no se publican. Ya se ve que entre JAS 2025 y 2026 los cesantes suben +115.131 y los que buscan por
primera vez +18.457. La duración de la búsqueda y la rama del empleo anterior exigen armonizar
`e15_*` con `e21_tramo` y `e18_ciiu_rev3` con su equivalente CAENES. Costo bajo la primera parte,
medio el resto.
**Método:** descomponer la desocupación en cesantía y primera búsqueda; serie de duración; tabla de
rama de origen.
**Refutación:** si la duración de la búsqueda no se alargó, el alza es rotación y no estancamiento,
que es una historia distinta y más benigna.

### Línea D — Flujos de personas
**Pregunta:** de los que estaban ocupados hace un año, ¿cuántos siguen ocupados y en qué? ¿La
salida es a desocupación o a inactividad?
**Insumo:** enlace por `idrph` (sección 4). Costo medio-alto, incluido el trabajo de validación.
**Método:** matriz de transición a 12 meses por año desde 2011, para tener base de comparación;
dentro de los que siguen ocupados, cambio de categoría, de formalidad y de rama. Antes de publicar:
reproducir con el enlace un agregado conocido y medir cuánto se desvía.
**Refutación:** si la matriz de 2025-2026 es indistinguible de la de años normales, no hay cambio
de dinámica que reportar, y eso también es un resultado.
**Es la línea diferenciadora: nadie publica esto en Chile de forma regular.**

### Línea E — ¿Dónde se destruyó el empleo? (rama de actividad)
**Insumo:** `rama_1` … `rama_21` desde 2017-08. Diez puntos JAS. Costo bajo. Lo anterior a 2017
es recuperable desde CIIU rev3 a un dígito con pérdida de detalle: decidir si vale el esfuerzo
después de ver los diez años.
**Hecho — con una corrección de por medio.** Las 21 columnas estaban computadas desde
`r_p_rev4cl_caenes`, que no es la variable que usa el INE. Coincidía con la correcta en el 90,4 %
de las filas, así que las sumas cuadraban y las cifras parecían razonables: la administración
pública aparecía como la segunda mayor destrucción de empleo (−54.494) cuando en realidad sube
(+3.688), y la enseñanza crecía 8,5 % en vez de 2,4 %. Corregido a `b14_rev4cl_caenes`, que
reproduce el boletín. Ver metodologia.md §3-bis.

### Línea F — Composición vs. tasa (descomposición shift-share)
**Pregunta:** ¿cuánto del alza de la desocupación nacional es que cambió la población —más adultos
mayores, más población extranjera, más escolaridad— y cuánto es que empeoró dentro de cada grupo?
**Insumo:** `conocimiento/evidencia/series-cortes.json` ya trae **17 puntos anuales por grupo** para
sexo (2), edad (6), región (16) y nacionalidad (2), con `pet`, `ft`, `o`, `do` y las tres tasas.
Costo bajo: es aritmética sobre datos ya publicados.
**Método:** descomposición estándar en efecto composición y efecto intra-grupo.
**Por qué importa:** es lo que separa «el mercado laboral empeoró» de «cambió quién lo compone», y
sin esto cualquier afirmación estructural queda expuesta a la objeción obvia.

### Línea G — Precisión: errores estándar
**Pregunta:** ¿cuáles de las diferencias que reportamos son distinguibles del ruido muestral?
**Insumo:** `estrato` y `conglomerado` están en los microdatos crudos desde 2010 y permiten estimar
varianzas con el diseño real. Costo medio.
**Por qué importa, concretamente:** en el ranking regional de alzas de JAS 2026, las tres primeras
—Los Lagos +2,20 pp, Maule +2,14, O'Higgins +2,07— caben dentro de 0,13 pp. Hoy no tenemos con qué
decir si ese orden significa algo. Un intervalo por región convierte un ranking frágil en una
afirmación defendible, o lo desarma a tiempo.

## 6. Trampas que este plan hereda

- **Doce series anuales, no una** (ADR-0003): los extremos y los récords se computan dentro de la
  serie del mes central que se está citando.
- **CISO-18 solo desde AMJ 2026**: la serie de contratistas dependientes tiene cuatro trimestres y
  no es extensible hacia atrás ni comparable con CISE-93.
- **Dos quiebres de clasificación**: CIUO-88 → CIUO-08 y CIIU rev3 → CAENES rev4, ambos alrededor de
  2017. El solape 2017-2019 de CIUO permite medir el tamaño del quiebre; úsalo antes de empalmar.
- **Jornada legal**: la rebaja a 42 horas rige desde el 26-04-2026 y contamina cualquier serie de
  horas que cruce esa fecha. La nota ya se computa en `generar_conocimiento.py`.
- **Denominadores de subutilización**: SU1 y SU2 sobre FT+ID; SU3 y SU4 sobre FTA. No son
  intercambiables.
- **Recalibración post-Censo 2017**: los niveles difieren de boletines antiguos; no citar cifras de
  boletines viejos junto a las de esta serie.
- **Evidencia ≠ hallazgo**: todo lo que salga de estas líneas entra como evidencia regenerable por
  script; la interpretación se cura a mano en `conocimiento/hallazgos/`, con confianza, caveats y
  `no_implica`.

## 7. Orden propuesto

1. **Publicar lo que ya está computado** (Líneas A, C-primera-parte, E): nuevos bloques en la capa
   de evidencia a partir de los agregados. Es el mejor retorno por hora de trabajo del plan.
2. **Shift-share** (Línea F): aritmética sobre los cortes ya publicados. Da el marco que permite
   interpretar todo lo demás sin caer en el error de composición.
3. **Extender el panel a las variables de contrato** (Línea B): `b15_1`, `b15_2`, `b17_*`, `b12`.
   Diecisiete años de tipo de contrato es el corazón de la narrativa.
4. **Flujos** (Línea D), con la validación como parte del entregable, no como un paso posterior.
5. **Errores estándar** (Línea G) y el resto de la Línea C.

Las tres primeras etapas son suficientes para contar la narrativa. Las dos últimas son las que la
vuelven difícil de refutar.
