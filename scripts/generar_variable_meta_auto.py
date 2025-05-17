# scripts/generar_variable_meta_auto.py
import json, pathlib, inspect, textwrap

from scripts import _column_defs as cols

# 1) Variables actuales: código → label
var_labels = dict(cols.PUBLIC_COLS)

# 2) Cargamos tu VARIABLE_META existente
meta = {**cols.VARIABLE_META}   # copy

# 3) Aseguramos que todas las claves existan
for code, label in var_labels.items():
    if code not in meta:
        meta[code] = {
            "label": label,
            "description": "",
            "notes": "",
            "source": ""
        }

# 4) Guardamos en un .py aparte para que revises el diff
dst = pathlib.Path("scripts/_column_defs_variables_auto.py")
header = "# Auto-generado por generar_variable_meta_auto.py – revisa y copia lo necesario\n\nVARIABLE_META = "
dst.write_text(header + json.dumps(meta, indent=4, ensure_ascii=False))
print("✅ Archivo listo para revisar ➜", dst)
