import pandas as pd
from config import BRONZE_PATH, SILVER_PATH


def transform():
    df = pd.read_parquet(BRONZE_PATH)
    print(f"Loaded bronze: {len(df)} rows")

    df = df.dropna(subset=["Title", "ReleaseDate", "MovieID"])
    df = df.drop_duplicates(subset=["MovieID"])

    df["ReleaseDate"] = pd.to_datetime(df["ReleaseDate"], dayfirst=True, errors="coerce")
    df = df.dropna(subset=["ReleaseDate"])

    year_min, year_max = 1900, pd.Timestamp.now().year + 5
    df = df[df["ReleaseDate"].dt.year.between(year_min, year_max)]

    mismatch = (df["ReleaseDate"].dt.year != df["ReleaseYear"]).sum()
    print(f"Year mismatch (ReleaseYear vs ReleaseDate): {mismatch} rows")

    SILVER_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(SILVER_PATH, index=False)
    print(f"Silver: {len(df)} rows -> {SILVER_PATH}")


if __name__ == "__main__":
    transform()
