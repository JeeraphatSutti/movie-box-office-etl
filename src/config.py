from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

RAW_DIR = DATA_DIR / "raw"
BRONZE_PATH = DATA_DIR / "bronze" / "movies.parquet"
SILVER_PATH = DATA_DIR / "silver" / "movies_clean.parquet"
GOLD_DIR = DATA_DIR / "gold"
STATE_PATH = DATA_DIR / "_state" / "processed_files.parquet"
