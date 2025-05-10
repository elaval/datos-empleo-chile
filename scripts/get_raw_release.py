# scripts/get_raw_release.py
import pathlib, requests, tarfile, io, sys, os, json

OWNER = "elaval"
REPO  = "datos-empleo-chile"
RAW_DIR = pathlib.Path("data/raw/ine")

def latest_asset_url():
    api = f"https://api.github.com/repos/{OWNER}/{REPO}/releases/latest"
    r = requests.get(api, timeout=30)
    r.raise_for_status()
    assets = r.json()["assets"]
    for a in assets:
        if a["name"].startswith("ene_raw") and a["name"].endswith(".tar.gz"):
            return a["browser_download_url"]
    raise SystemExit("No raw data asset found.")

def main():
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    if any(RAW_DIR.iterdir()):
        print("Raw CSVs already present – skip download.")
        return
    url = latest_asset_url()
    print("Downloading", url)
    buf = io.BytesIO(requests.get(url, timeout=120).content)
    with tarfile.open(fileobj=buf, mode="r:gz") as tar:
        tar.extractall(RAW_DIR)  # extracts into data/raw/ine
    print("Extracted", len(list(RAW_DIR.iterdir())), "files")

if __name__ == "__main__":
    sys.exit(main())
