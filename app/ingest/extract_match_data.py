from pathlib import Path
from zipfile import ZipFile

from app.config import config


def extract_all_zips():
    for p in sorted(Path.glob(config.data_path / "zips", "*.zip")):
        print(f"extracting {p}...")
        count = 0
        with ZipFile(p) as zip:
            zip.extractall(config.data_path / "all")
            count += 1
        print(f"...{count=}")
