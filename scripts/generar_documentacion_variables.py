# scripts/generar_documentacion_variables.py
import pathlib, json, pandas as pd
from scripts._column_defs import VARIABLE_META, START_DATES, END_DATES

DOCS_DIR = pathlib.Path("docs")
DOCS_DIR.mkdir(exist_ok=True)

# 1) JSON
json_path = DOCS_DIR / "variables.json"
json_path.write_text(json.dumps(VARIABLE_META, indent=2, ensure_ascii=False), encoding="utf-8")
print("✅  Guardado:", json_path.resolve())

# 2) Tabla Markdown
df = (
    pd.DataFrame(VARIABLE_META)
      .T.reset_index(names="codigo")
      .assign(
          desde=lambda d: d["codigo"].map(START_DATES),
          hasta=lambda d: d["codigo"].map(END_DATES)
      )
      .fillna("")                            # celdas vacías → cadena vacía
      .dropna(axis=1, how="all")             # elimina columnas 'desde'/'hasta' si están 100 % vacías
)

cols = ["codigo", "label", "description"] + [c for c in ("desde", "hasta") if c in df.columns]
md_table = df[cols].to_markdown(index=False)

md_path = DOCS_DIR / "variables.md"
md_path.write_text(md_table, encoding="utf-8")
print("✅  Guardado:", md_path.resolve())
