# ADR-0004 — Qué variable es un indicador se verifica contra la fuente externa, no contra su coherencia

- **Estado:** Aceptada
- **Fecha:** 2026-10-31
- **Ámbito:** `scripts/generar_totales_trimestrales.py` + `scripts/validar_conocimiento.py`
  + `conocimiento/referencia-ine.json`
- **Decide sobre:** cómo se elige, se documenta y se blinda la variable de microdato con
  la que se construye un indicador de la capa, cuando la ENE ofrece más de una candidata
  con nombre parecido.

---

## Contexto

Al publicar el bloque de rama de actividad (JAS 2026) resultó que las 21 columnas
`rama_1` … `rama_21` se computaban desde `r_p_rev4cl_caenes`, y la variable que usa el INE
para su tabla publicada es `b14_rev4cl_caenes`. La ENE 2026 trae tres candidatas con nombre
casi idéntico: `b13_rev4cl_caenes`, `b14_rev4cl_caenes` y `r_p_rev4cl_caenes`.

**Ninguna verificación interna podía detectarlo.** Las dos variables coinciden en el
**90,4 %** de las filas y suman casi el mismo total de ocupados:

| | Suma ponderada, JAS 2026 | Ocupados |
|---|---|---|
| `b14_rev4cl_caenes` | 9.246.378 | 9.274.742 |
| `r_p_rev4cl_caenes` | 9.247.050 | 9.274.742 |

Las 21 secciones cuadraban contra el total, el residuo sin rama declarada era del orden
esperado (~28 mil personas), las variaciones interanuales tenían signos y magnitudes
creíbles, y las series de los diez años disponibles eran suaves. Un bloque construido con
la variable equivocada **pasa todos los controles de coherencia que la capa sabía hacer**.

Lo que no cuadraba era el boletín. Contraste contra el n°336, variación a doce meses:

| Rama | INE | `b14` | `r_p` |
|---|---|---|---|
| Industrias manufactureras | −8,1 % | −8,1 % | −6,7 % |
| Información y comunicaciones | −20,8 % | −20,8 % | −19,2 % |
| Actividades financieras y de seguros | −14,1 % | −14,1 % | −17,1 % |
| Actividades inmobiliarias | +19,1 % | +19,1 % | +7,2 % |
| Enseñanza | +2,4 % | +2,4 % | +8,5 % |
| Hombres, manufactura | −10,2 % | −10,2 % | −8,8 % |
| Mujeres, información y comunicaciones | −33,1 % | −33,1 % | −32,7 % |

Siete de siete con `b14`. Ninguna con `r_p`.

### Por qué importaba

El error no era decimal. Con `r_p`, tres ramas cambiaban de signo y el titular era falso:

| Rama | Con `r_p` | Con `b14` |
|---|---|---|
| Administración pública y defensa | −54.494 (−7,45 %) | **+3.688 (+0,69 %)** |
| Explotación de minas y canteras | −4.134 | **+7.498** |
| Servicios administrativos y de apoyo | +6.760 | **−13.290** |
| Enseñanza | +53.569 (+8,54 %) | +19.246 (+2,39 %) |
| Industrias manufactureras | −59.248 | −74.000 (−8,13 %) |

La administración pública aparecía como **la segunda mayor destrucción de empleo del
trimestre** cuando en realidad sube. Esa cifra estaba a un paso de publicarse.

### La familia a la que pertenece este error

Es el tercero del mismo tipo en esta capa, y los tres se parecen más de lo que parece:

- **ADR-0002** — el INE renombró `id` a `idisp`; el pipeline rellenaba con NA en vez de
  fallar y las tasas SU1–SU4 salieron *plausibles pero fabricadas*.
- **ADR-0003** — un extremo heredado de otra serie anual seguía siendo una cifra con la
  forma correcta, solo que de otra serie.
- **Este** — una variable parecida produce un bloque con la forma correcta y el contenido
  equivocado.

El patrón común no es el descuido: es que **la plausibilidad no es evidencia**. Un
resultado puede ser coherente consigo mismo, con sus sumas y con su historia, y no ser el
que describe la realidad que se quiere describir.

---

## Decisión

### 1. La variable de un indicador se elige contrastando contra la fuente, no razonando sobre su nombre

Cuando la ENE ofrece varias variables candidatas, la que se usa es **la que reproduce la
cifra publicada por el INE**, verificada una por una sobre varias celdas independientes
(aquí: siete, incluidas dos desagregadas por sexo). El nombre de la variable, su prefijo y
lo que parezca significar no deciden nada. Si ninguna candidata reproduce el boletín, el
indicador **no se publica** hasta entender por qué.

### 2. La elección se documenta donde está el código, con las cifras que la sostienen

El comentario junto a las reglas de `generar_totales_trimestrales.py` lleva la tabla de
contraste completa: qué publica el INE, qué da la variable elegida y qué da la descartada.
No basta con decir «usar b14»: hay que dejar la evidencia de por qué, porque quien lea el
código en dos años va a ver dos variables equivalentes y ninguna razón para preferir una.

### 3. El validador recomputa el indicador desde la variable correcta

Un chequeo en el bloque B del validador reconstruye las 21 ramas desde
`b14_rev4cl_caenes` y las compara con lo publicado. Su propósito **no** es comprobar la
aritmética —eso ya lo hacen las sumas— sino **clavar la variable**: si alguien vuelve a
`r_p`, el bloque seguirá sumando bien y las cifras seguirán siendo plausibles, y solo este
chequeo lo dirá.

### 4. Las cifras del boletín que verifican la elección entran a `referencia-ine.json`

Las seis variaciones a doce meses que reconcilian quedaron transcritas en
`rama_variaciones_12m_pct`, y el bloque C las verifica en cada corrida. Esto convierte el
hallazgo de un día en una comprobación permanente.

### 5. Lo que no reconcilia se registra, no se acomoda

«Otras actividades de servicios» da −5,24 % contra el −5,1 % del boletín, y ninguna
agrupación con las secciones vecinas (R, T, U) se acerca más. La brecha quedó en
`rama_variaciones_12m_pct_no_reconcilia`, con su magnitud y la constancia explícita de que
su causa no está establecida. **No se amplió la tolerancia para que pasara**: una
tolerancia estirada hasta que el caso pase deja de verificar lo que decía verificar.

### 6. Un indicador con fuente externa disponible no se publica sin contrastarla

La capa ya tenía tres vías de validación; lo que faltaba era usarlas **antes** de publicar
y no después. Para todo bloque nuevo, el contraste contra el boletín es parte del trabajo
de publicarlo, no una verificación posterior.

---

## Consecuencias

- Las cifras de rama servidas por esta capa **cambiaron** el 31-10-2026. Cualquier cifra
  sectorial tomada de esta fuente antes de esa fecha no es la del INE. Queda avisado en el
  registro de cambios del saber (v0.2.8), porque el aviso le sirve a quien consultó, no a
  quien mantiene.
- El validador pasó de 62 a 76 comprobaciones.
- Las pruebas de funcionamiento del saber incluyen un caso con una cifra histórica conocida
  (JAS 2017, manufactura: 906.672) que falla si la variable vuelve a cambiar.
- **Queda deuda:** `b13`, `b14` y `r_p` siguen sin documentar en `docs/variables.json`,
  igual que las ~175 variables de la ENE que el panel procesado no conserva. La diferencia
  conceptual exacta entre `b14` y `r_p` no está establecida: sabemos cuál reproduce al INE,
  no qué mide la otra.
- **Este ADR no instala un chequeo genérico.** No hay forma automática de saber que una
  variable es la equivocada; lo que hay es la obligación de contrastar contra la fuente al
  publicar, y un centinela por indicador una vez elegida.

## Referencias

- Incidente y corrección: commit `35da305` de `datos-empleo-chile`.
- Errores hermanos: ADR-0002 (renombre silencioso), ADR-0003 (extremo heredado).
- Regla operativa en la capa: `conocimiento/metodologia.md`, sección 3-bis.
- Contraste externo: `conocimiento/referencia-ine.json`, release `2026-08-jas`.
- Principios de diseño aplicados (KB MindTheContext): decisiones validadas por evidencia
  (correr el contraste y aceptar que refute la hipótesis); evidencia ≠ hallazgo (el rigor
  viaja con el dato; ante lo no derivable, decirlo en vez de fabricarlo).
