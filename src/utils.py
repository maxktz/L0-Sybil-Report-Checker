from logging import RootLogger
from pathlib import Path
import zipfile
from src.core.config import ROOT_DIR
from src.sybil_checker import SybilAddresses


def write_sybil_addresses_to_file(addresses: SybilAddresses) -> Path:
    file = ROOT_DIR / "sybil-report.csv"
    text = """Source, t.me/xcrypto_dev
Address, Github Issue Numbers
"""
    for addr, issue_numbers in addresses.items():
        text += f"\n{addr}, {' '.join(map(str, issue_numbers))}"
    file.write_text(text, encoding="utf8")
    zipped_file = file.with_suffix(".csv.zip")
    with zipfile.ZipFile(zipped_file.as_posix(), "w") as zipf:
        zipf.write(file, compress_type=zipfile.ZIP_DEFLATED)
    file.unlink()
    return zipped_file
