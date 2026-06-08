from pathlib import Path

ROOT_DIR = Path(__file__).parent.resolve()
DATA_DIR = ROOT_DIR / "data"

PATHS = {
    "institutos": DATA_DIR / "institutos.json",
}
