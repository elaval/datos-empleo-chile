#!/usr/bin/env python3
"""
scripts/update_raw_release.py
=============================
Descarga el CSV bruto de ENE para el mes indicado, recrea el tar.gz con todos
los CSVs en data/raw/ine y publica un nuevo release en GitHub con ese tarball.

Uso:
    python scripts/update_raw_release.py 2025-03

Requisitos:
  - Tener instalado `requests`.
  - Definir la variable de entorno GITHUB_TOKEN con permisos de 
    escritura en el repositorio.
"""
import os
import sys
import glob
import tarfile
import pathlib
import requests

OWNER   = "elaval"
REPO    = "datos-empleo-chile"
RAW_DIR = pathlib.Path("data/raw/ine")
# la carpeta superior, donde se guardará el tar.gz
OUT_DIR = RAW_DIR.parent  

# mapeo mes → sufijo de archivo en INE
SUFIJOS = {
    1: "def",  2: "efm",  3: "fma", 4: "mam",
    5: "amj",  6: "mjj",  7: "jja", 8: "jas",
    9: "aso", 10: "son", 11: "ond", 12: "nde",
}


def download_csv(year: str, month: int) -> pathlib.Path:
    """Descarga el CSV de INE para año/mes, si no existe ya."""
    suf = SUFIJOS.get(month)
    if suf is None:
        sys.exit(f"Mes inválido: {month}")
    mm = f"{month:02d}"
    fname = f"ene-{year}-{mm}-{suf}.csv"
    url = f"https://www.ine.gob.cl/docs/default-source/ocupacion-y-desocupacion/bbdd/{year}/csv/{fname}"
    dest = RAW_DIR / fname

    if dest.exists():
        print(f"⚠ {fname} ya existe en {RAW_DIR}, salto descarga.")
        return dest

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    print(f"⬇️  Descargando {url} …")
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    dest.write_bytes(r.content)
    print(f"✔ Guardado {dest}")
    return dest


def build_tarball() -> pathlib.Path:
    """Recrea el tar.gz con todos los CSV de data/raw/ine."""
    csvs = sorted(RAW_DIR.glob("ene-*.csv"))
    if not csvs:
        sys.exit("❌ No encuentro ningún CSV para empaquetar.")
    years = [int(p.name.split("-")[1]) for p in csvs]
    tar_name = f"ene_raw_{min(years)}-{max(years)}.tar.gz"
    tar_path = OUT_DIR / tar_name

    print(f"📦 Empaquetando {len(csvs)} CSVs en {tar_path.name} …")
    with tarfile.open(tar_path, "w:gz") as tar:
        for p in csvs:
            tar.add(p, arcname=p.name)
    print(f"✔ Creado {tar_path}")
    return tar_path


def create_github_release(tag: str, title: str, body: str, asset_path: pathlib.Path):
    """Crea un release y sube el tar.gz como asset."""
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        sys.exit("❌ Debes definir GITHUB_TOKEN con permisos de repo.")

    headers = {"Authorization": f"token {token}"}
    api_url = f"https://api.github.com/repos/{OWNER}/{REPO}/releases"

    # 1) Crear el release
    payload = {
        "tag_name": tag,
        "name": title,
        "body": body,
        "draft": False,
        "prerelease": False,
    }
    print(f"🚀 Creando release {tag} …")
    resp = requests.post(api_url, json=payload, headers=headers)
    resp.raise_for_status()
    release = resp.json()

    # 2) Subir el asset
    upload_url = release["upload_url"].split("{")[0]
    params = {"name": asset_path.name}
    headers["Content-Type"] = "application/gzip"
    with open(asset_path, "rb") as f:
        print(f"⬆️  Subiendo asset {asset_path.name} …")
        r2 = requests.post(upload_url, params=params, data=f, headers=headers)
        r2.raise_for_status()

    print(f"✔ Release creado: {release['html_url']}")


def main():
    if len(sys.argv) != 2:
        print("Uso: python scripts/update_raw_release.py YYYY-MM")
        sys.exit(1)

    year, mm = sys.argv[1].split("-")
    month = int(mm)

    # 1) Descargo el CSV nuevo
    download_csv(year, month)

    # 2) Reconstruyo el tar.gz
    tarball = build_tarball()

    # 3) Creo el release y subo el asset
    tag   = f"raw-data-{year}-{mm}"
    title = f"Raw data {year}-{mm}"
    body  = f"CSV brutos de ENE actualizados hasta {year}-{mm}."
    create_github_release(tag, title, body, tarball)


if __name__ == "__main__":
    main()
