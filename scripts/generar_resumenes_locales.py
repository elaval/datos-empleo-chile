#!/usr/bin/env python3
"""
generar_resumenes_locales.py

This script processes all local parquet files from data/processed/microdatos/
and generates summarized versions in data/processed/resumenes/
"""

import duckdb
from pathlib import Path

# Configuration
MICRODATOS_DIR = Path("data/processed/microdatos")
RESUMENES_DIR = Path("data/processed/resumenes")
RESUMENES_DIR.mkdir(exist_ok=True)

def process_file(parquet_file):
    """Process a single parquet file and generate its summary"""
    # Extract period code from filename (e.g., "ene-08-jas.parquet" -> "08-jas")
    period_code = parquet_file.stem.replace("ene-", "")
    summary_file = RESUMENES_DIR / f"resumen-{period_code}.parquet"
    
    print(f"Processing {parquet_file.name} -> {summary_file.name}")
    
    con = duckdb.connect()
    
    query = f"""
    CREATE OR REPLACE TABLE tmp_summary AS
    WITH tabla AS (
      SELECT 
        ano_trimestre, 
        mes_central, 
        CASE WHEN nacionalidad = 152 THEN 'chilena' ELSE 'extranjera' END AS nacionalidad,
        CASE 
          WHEN activ = 1 THEN 'ocupado' 
          WHEN activ = 2 THEN 'desocupado' 
          WHEN activ = 3 THEN 'fuera de la fuerza de trabajo' 
          ELSE 'NA' END AS actividad,
        CASE 
          WHEN categoria_ocupacion = 0 THEN 'No Corresponde' 
          WHEN categoria_ocupacion = 1 THEN 'Empleador' 
          WHEN categoria_ocupacion = 2 THEN 'Cuenta propia' 
          WHEN categoria_ocupacion = 3 THEN 'Asalariado sector privado' 
          WHEN categoria_ocupacion = 4 THEN 'Asalariado sector público' 
          WHEN categoria_ocupacion = 5 THEN 'Personal de servicio doméstico puertas afuera' 
          WHEN categoria_ocupacion = 6 THEN 'Personal de servicio doméstico puertas adentro' 
          WHEN categoria_ocupacion = 7 THEN 'Familiar o personal no remunerado' 
          ELSE 'NA' END AS categoria,  
        CASE 
          WHEN region = 1 THEN 'Tarapacá' 
          WHEN region = 2 THEN 'Antofagasta' 
          WHEN region = 3 THEN 'Atacama' 
          WHEN region = 4 THEN 'Coquimbo' 
          WHEN region = 5 THEN 'Valparaíso' 
          WHEN region = 6 THEN 'O''Higgins' 
          WHEN region = 7 THEN 'Maule' 
          WHEN region = 8 THEN 'Biobío' 
          WHEN region = 9 THEN 'La Araucanía' 
          WHEN region = 10 THEN 'Los Lagos' 
          WHEN region = 11 THEN 'Aysén' 
          WHEN region = 12 THEN 'Magallanes' 
          WHEN region = 13 THEN 'Metropolitana' 
          WHEN region = 14 THEN 'Los Ríos' 
          WHEN region = 15 THEN 'Arica y Parinacota' 
          WHEN region = 16 THEN 'Ñuble' 
          ELSE 'NA' END AS region,  
        CASE 
          WHEN ocup_form = 1 THEN 'Ocupado formal' 
          WHEN ocup_form = 2 THEN 'Ocupado informal' 
          ELSE 'NA' END AS formalidad,
        CASE 
          WHEN sexo = 1 THEN 'Hombre' 
          WHEN sexo = 2 THEN 'Mujer' 
          ELSE 'NA' END AS sexo,
        fact_cal
      FROM read_parquet('{parquet_file}')
      WHERE edad >= 15
    )
    SELECT 
      '{period_code}' AS periodo,
      ano_trimestre, 
      mes_central, 
      sexo, 
      nacionalidad, 
      actividad, 
      categoria,
      formalidad,
      SUM(fact_cal) AS personas
    FROM tabla
    GROUP BY 
      ano_trimestre, mes_central, sexo, nacionalidad, actividad, categoria, formalidad;
    """
    
    con.execute(query)
    con.execute(f"COPY tmp_summary TO '{summary_file}' (FORMAT 'parquet');")
    con.close()

def main():
    # Process all parquet files
    parquet_files = sorted(MICRODATOS_DIR.glob("ene-*.parquet"))
    
    if not parquet_files:
        print("No parquet files found in data/processed/microdatos/")
        return
    
    for parquet_file in parquet_files:
        process_file(parquet_file)
    
    # Create combined summary
    print("Creating combined summary...")
    con = duckdb.connect()
    
    combined_file = RESUMENES_DIR / "todos-los-resumenes.parquet"
    con.execute(f"""
    CREATE OR REPLACE TABLE combined AS
    SELECT * FROM read_parquet('{RESUMENES_DIR}/resumen-*.parquet');
    """)
    
    con.execute(f"COPY combined TO '{combined_file}' (FORMAT 'parquet');")
    con.close()
    
    print(f"✅ Combined summary created: {combined_file}")
    print(f"✅ Processed {len(parquet_files)} files")

if __name__ == "__main__":
    main()