# Ontología del dominio — empleo en Chile (ENE)

Mapa de conceptos para razonar sobre el mercado laboral chileno. Define los términos y,
sobre todo, **cómo se relacionan**. Los valores concretos están en `evidencia/`; las
definiciones formales y fórmulas en `indicadores.json`.

## Población: el árbol de clasificación

Toda persona de 15 años o más (**PET**, población en edad de trabajar) cae en una y solo
una hoja de este árbol en el trimestre de referencia:

```
PET (15+)
├── Fuerza de trabajo (FT) ── "activos"
│   ├── Ocupados (O)
│   │   ├── por categoría ocupacional:
│   │   │   ├── Empleador
│   │   │   ├── Cuenta propia
│   │   │   ├── Asalariado sector privado
│   │   │   ├── Asalariado sector público
│   │   │   ├── Servicio doméstico
│   │   │   └── Familiar no remunerado
│   │   └── por formalidad: Formal | Informal
│   └── Desocupados (DO)
│       ├── Cesantes (tuvieron empleo antes)
│       └── Buscan trabajo por primera vez
└── Fuera de la fuerza de trabajo ── "inactivos"
    ├── Potencialmente activos
    └── Inactivos habituales
```

**Identidades que se deben respetar siempre:**
- `FT = O + DO`
- `PET = FT + Fuera de la fuerza de trabajo`
- `ΔFT = ΔO + ΔDO` (toda variación de la fuerza de trabajo se reparte entre quienes
  encuentran empleo y quienes no)

## Las tres tasas y qué las mueve

| Tasa | Fórmula | Sube cuando… |
|---|---|---|
| **Desocupación (TD)** | DO / FT | los desocupados crecen más rápido que la fuerza de trabajo. **Puede subir aunque crezca el empleo**, si la fuerza de trabajo crece más. |
| **Participación (TP)** | FT / PET | más gente en edad de trabajar entra a buscar o tener empleo. |
| **Ocupación (TO)** | O / PET | crece el empleo respecto a la población en edad de trabajar. |

> El error de lectura más común: creer que "más ocupados ⇒ baja la desocupación". Falso.
> Lo que decide la TD es la *carrera* entre empleo y fuerza de trabajo, no el nivel de empleo.

## Dimensiones de corte disponibles

- **Sexo** (Hombre / Mujer) — brecha de participación y de TD.
- **Edad** (15-24, 25-34, 35-44, 45-54, 55-64, 65+) — la TD juvenil suele duplicar o
  triplicar la nacional; el empleo mayor (55+) tiene dinámica propia.
- **Región** (16 regiones) — dispersión territorial fuerte.
- **Categoría ocupacional / sector** (público vs privado, asalariado vs independiente) —
  distingue la *calidad* y *dependencia* del empleo. El avance del trabajo por cuenta
  propia cuando cae el asalariado suele leerse como señal de holgura, no de fortaleza.
- **Nacionalidad** (chileno/a / extranjero/a) — los extranjeros suelen tener mayor
  participación y dinámica propia; robusto a nivel nacional.
- **Formalidad** (formal / informal, definición OIT) — partición de los ocupados. La *tasa
  de ocupación informal* (`toi`) resume la informalidad; serie consistente desde 2017. Que el
  empleo crezca por el lado informal es una señal de calidad del empleo, no solo de cantidad.

## Estacionalidad

El empleo tiene un ciclo intra-anual marcado (agricultura, comercio, año escolar). Por eso
la comparación relevante es **año contra año en el mismo mes central**, no mes contra mes.

## Relación con eventos externos

La ENE describe el estado del mercado laboral, no sus causas. Vincular un movimiento con un
evento (cambio de gobierno, shock de precios, reforma) exige análisis adicional y varios
trimestres; un dato aislado no lo permite (ver `metodologia.md` §6).
