#!/usr/bin/env python3
"""
generar_totales_con_deltas.py

This script processes all local parquet files from data/processed/microdatos/
and generates employment totals with year-over-year deltas in data/processed/resumenes/
"""

import duckdb
from pathlib import Path

# Configuration
MICRODATOS_DIR = Path("data/processed/microdatos")
RESUMENES_DIR = Path("data/processed/resumenes")
RESUMENES_DIR.mkdir(exist_ok=True)

def main():
    con = duckdb.connect()
    
    # Create a view of all parquet files
    parquet_files = sorted(MICRODATOS_DIR.glob("ene-*.parquet"))
    if not parquet_files:
        print("No parquet files found in data/processed/microdatos/")
        return
    
    print(f"Processing {len(parquet_files)} files...")
    
    # Create union of all files
    union_query = " UNION ALL ".join([
        f"SELECT * FROM read_parquet('{file}')" for file in parquet_files
    ])
    
    con.execute(f"CREATE OR REPLACE VIEW empRaw AS ({union_query})")
    
    # Main query
    query = """
    WITH tabla AS (
      SELECT 
        ano_trimestre, 
        mes_central, 

        -- Total
        SUM(CASE WHEN activ = 1 THEN fact_cal ELSE 0 END)::INT AS O,
        SUM(CASE WHEN activ = 2 THEN fact_cal ELSE 0 END)::INT AS DO,
        SUM(CASE WHEN activ = 2 THEN fact_cal ELSE 0 END)::FLOAT / 
          NULLIF(SUM(CASE WHEN activ BETWEEN 1 AND 2 THEN fact_cal ELSE 0 END)::FLOAT, 0) AS TD,
        SUM(CASE WHEN cae_especifico BETWEEN 1 AND 9 THEN fact_cal ELSE 0 END)::INT AS FT,

        -- Hombre
        SUM(CASE WHEN activ = 1 AND sexo = 1 THEN fact_cal ELSE 0 END)::INT AS O_hombre,
        SUM(CASE WHEN activ = 2 AND sexo = 1 THEN fact_cal ELSE 0 END)::INT AS DO_hombre,
        SUM(CASE WHEN activ = 2 AND sexo = 1 THEN fact_cal ELSE 0 END)::FLOAT / 
          NULLIF(SUM(CASE WHEN activ BETWEEN 1 AND 2 AND sexo = 1 THEN fact_cal ELSE 0 END)::FLOAT, 0) AS TD_hombre,

        -- Mujer
        SUM(CASE WHEN activ = 1 AND sexo = 2 THEN fact_cal ELSE 0 END)::INT AS O_mujer,
        SUM(CASE WHEN activ = 2 AND sexo = 2 THEN fact_cal ELSE 0 END)::INT AS DO_mujer,
        SUM(CASE WHEN activ = 2 AND sexo = 2 THEN fact_cal ELSE 0 END)::FLOAT / 
          NULLIF(SUM(CASE WHEN activ BETWEEN 1 AND 2 AND sexo = 2 THEN fact_cal ELSE 0 END)::FLOAT, 0) AS TD_mujer,

        -- Porcentaje Mujer
        SUM(CASE WHEN activ = 1 AND sexo = 2 THEN fact_cal ELSE 0 END)::FLOAT / 
          NULLIF(SUM(CASE WHEN activ = 1 THEN fact_cal ELSE 0 END)::FLOAT, 0) AS Porcentaje_mujer,

        -- Chileno
        SUM(CASE WHEN activ = 1 AND nacionalidad = 152 THEN fact_cal ELSE 0 END)::INT AS O_chileno,
        SUM(CASE WHEN activ = 2 AND nacionalidad = 152 THEN fact_cal ELSE 0 END)::INT AS DO_chileno,
        SUM(CASE WHEN activ = 2 AND nacionalidad = 152 THEN fact_cal ELSE 0 END)::FLOAT / 
          NULLIF(SUM(CASE WHEN activ BETWEEN 1 AND 2 AND nacionalidad = 152 THEN fact_cal ELSE 0 END)::FLOAT, 0) AS TD_chileno,

        -- Extranjero
        SUM(CASE WHEN activ = 1 AND nacionalidad <> 152 THEN fact_cal ELSE 0 END)::INT AS O_extranjero,
        SUM(CASE WHEN activ = 2 AND nacionalidad <> 152 THEN fact_cal ELSE 0 END)::INT AS DO_extranjero,
        SUM(CASE WHEN activ = 2 AND nacionalidad <> 152 THEN fact_cal ELSE 0 END)::FLOAT / 
          NULLIF(SUM(CASE WHEN activ BETWEEN 1 AND 2 AND nacionalidad <> 152 THEN fact_cal ELSE 0 END)::FLOAT, 0) AS TD_extranjero,

        -- Porcentaje Extranjero
        SUM(CASE WHEN activ = 1 AND nacionalidad <> 152 THEN fact_cal ELSE 0 END)::FLOAT / 
          NULLIF(SUM(CASE WHEN activ = 1 THEN fact_cal ELSE 0 END)::FLOAT, 0) AS Porcentaje_extranjero,

        -- Formalidad
        SUM(CASE WHEN ocup_form = 1 THEN fact_cal ELSE 0 END)::INT AS O_formal,
        SUM(CASE WHEN ocup_form = 2 THEN fact_cal ELSE 0 END)::INT AS O_informal,
        SUM(CASE WHEN ocup_form = 2 THEN fact_cal ELSE 0 END)::FLOAT / 
          NULLIF(SUM(CASE WHEN activ = 1 THEN fact_cal ELSE 0 END)::FLOAT, 0) AS Porcentaje_informal,

        -- Sector
        SUM(CASE WHEN categoria_ocupacion = 1 THEN fact_cal ELSE 0 END)::INT AS O_empleador,
        SUM(CASE WHEN categoria_ocupacion = 2 THEN fact_cal ELSE 0 END)::INT AS O_cuenta_propia,
        SUM(CASE WHEN categoria_ocupacion = 3 THEN fact_cal ELSE 0 END)::INT AS O_sector_privado,
        SUM(CASE WHEN categoria_ocupacion = 4 THEN fact_cal ELSE 0 END)::INT AS O_sector_publico,
        SUM(CASE WHEN categoria_ocupacion = 5 THEN fact_cal ELSE 0 END)::INT AS O_domestico_afuera,
        SUM(CASE WHEN categoria_ocupacion = 6 THEN fact_cal ELSE 0 END)::INT AS O_domestico_adentro,
        SUM(CASE WHEN categoria_ocupacion = 7 THEN fact_cal ELSE 0 END)::INT AS O_familiar_no_remunerado,

        -- Porcentaje Sector Público
        SUM(CASE WHEN categoria_ocupacion = 4 THEN fact_cal ELSE 0 END)::FLOAT / 
          NULLIF(SUM(CASE WHEN activ = 1 THEN fact_cal ELSE 0 END)::FLOAT, 0) AS Porcentaje_sector_publico

      FROM empRaw
      WHERE edad >= 15
      GROUP BY ano_trimestre, mes_central
    )

    SELECT 
      t1.ano_trimestre,
      t1.mes_central,

      -- Niveles actuales
      t1.O, t1.DO, t1.TD, t1.FT,
      t1.O_hombre, t1.DO_hombre, t1.TD_hombre,
      t1.O_mujer, t1.DO_mujer, t1.TD_mujer, t1.Porcentaje_mujer,
      t1.O_chileno, t1.DO_chileno, t1.TD_chileno,
      t1.O_extranjero, t1.DO_extranjero, t1.TD_extranjero, t1.Porcentaje_extranjero,
      t1.O_formal, t1.O_informal, t1.Porcentaje_informal,
      t1.O_empleador, t1.O_cuenta_propia, t1.O_sector_privado, t1.O_sector_publico,
      t1.O_domestico_afuera, t1.O_domestico_adentro, t1.O_familiar_no_remunerado,
      t1.Porcentaje_sector_publico,

      -- Deltas interanuales
      (t1.O - t2.O) AS delta_O,
      (t1.O - t2.O)::Float / NULLIF(t2.O, 0) AS delta_relativo_O,
      (t1.DO - t2.DO) AS delta_DO,
      (t1.DO - t2.DO)::Float / NULLIF(t2.DO, 0) AS delta_relativo_DO,

      (t1.TD - t2.TD) AS delta_TD,
      (t1.FT - t2.FT) AS delta_FT,

      (t1.O_hombre - t2.O_hombre) AS delta_O_hombre,
      (t1.O_hombre - t2.O_hombre)::Float / NULLIF(t2.O_hombre, 0) AS delta_relativo_O_hombre,
      (t1.DO_hombre - t2.DO_hombre) AS delta_DO_hombre,
      (t1.TD_hombre - t2.TD_hombre) AS delta_TD_hombre,

      (t1.O_mujer - t2.O_mujer) AS delta_O_mujer,
      (t1.O_mujer - t2.O_mujer)::Float / NULLIF(t2.O_mujer, 0) AS delta_relativo_O_mujer,
      (t1.DO_mujer - t2.DO_mujer) AS delta_DO_mujer,
      (t1.TD_mujer - t2.TD_mujer) AS delta_TD_mujer,
      (t1.Porcentaje_mujer - t2.Porcentaje_mujer) AS delta_pp_Porcentaje_mujer,

      (t1.O_chileno - t2.O_chileno) AS delta_O_chileno,
      (t1.DO_chileno - t2.DO_chileno) AS delta_DO_chileno,
      (t1.TD_chileno - t2.TD_chileno) AS delta_TD_chileno,

      (t1.O_extranjero - t2.O_extranjero) AS delta_O_extranjero,
      (t1.O_extranjero - t2.O_extranjero)::Float / NULLIF(t2.O_extranjero, 0) AS delta_relativo_O_extranjero,

      (t1.DO_extranjero - t2.DO_extranjero) AS delta_DO_extranjero,
      (t1.TD_extranjero - t2.TD_extranjero) AS delta_TD_extranjero,
      (t1.Porcentaje_extranjero - t2.Porcentaje_extranjero) AS delta_pp_Porcentaje_extranjero,

      (t1.O_formal - t2.O_formal) AS delta_O_formal,
      (t1.O_formal - t2.O_formal)::Float / NULLIF(t2.O_formal, 0) AS delta_relativo_O_formal,

      (t1.O_informal - t2.O_informal) AS delta_O_informal,
      (t1.Porcentaje_informal - t2.Porcentaje_informal) AS delta_pp_Porcentaje_informal,

      (t1.O_empleador - t2.O_empleador) AS delta_O_empleador,
      (t1.O_cuenta_propia - t2.O_cuenta_propia) AS delta_O_cuenta_propia,
      (t1.O_sector_privado - t2.O_sector_privado) AS delta_O_sector_privado,
      (t1.O_sector_privado - t2.O_sector_privado)::Float / NULLIF(t2.O_sector_privado, 0) AS delta_relativo_O_sector_privado,

      (t1.O_sector_publico - t2.O_sector_publico) AS delta_O_sector_publico,
      (t1.O_sector_publico - t2.O_sector_publico)::Float / NULLIF(t2.O_sector_publico, 0) AS delta_relativo_O_sector_publico,

      (t1.O_domestico_afuera - t2.O_domestico_afuera) AS delta_O_domestico_afuera,
      (t1.O_domestico_adentro - t2.O_domestico_adentro) AS delta_O_domestico_adentro,
      (t1.O_familiar_no_remunerado - t2.O_familiar_no_remunerado) AS delta_O_familiar_no_remunerado,
      (t1.Porcentaje_sector_publico - t2.Porcentaje_sector_publico) AS delta_pp_Porcentaje_sector_publico

    FROM tabla t1
    LEFT JOIN tabla t2 
      ON t2.mes_central = t1.mes_central
      AND t2.ano_trimestre = t1.ano_trimestre - 1
    ORDER BY t1.ano_trimestre, t1.mes_central
    """
    
    con.execute("CREATE OR REPLACE TABLE totales AS " + query)
    
    # Save as CSV and Parquet
    csv_file = RESUMENES_DIR / "totales_con_deltas.csv"
    parquet_file = RESUMENES_DIR / "totales_con_deltas.parquet"
    
    con.execute(f"COPY totales TO '{csv_file}' (FORMAT 'csv', HEADER);")
    con.execute(f"COPY totales TO '{parquet_file}' (FORMAT 'parquet');")
    
    con.close()
    
    print(f"✅ Employment totals with deltas saved:")
    print(f"   CSV: {csv_file}")
    print(f"   Parquet: {parquet_file}")

if __name__ == "__main__":
    main()