import pandas as pd
from config import SILVER_PATH, GOLD_DIR


def aggregate():
    df = pd.read_parquet(SILVER_PATH)
    print(f"Loaded silver: {len(df)} rows")

    by_year = df.groupby("ReleaseYear").agg(
        movie_count=("MovieID", "count"),
        total_budget=("BudgetUSD", "sum"),
        total_global_revenue=("Global_BoxOfficeUSD", "sum"),
        avg_imdb=("IMDbRating", "mean"),
        avg_rt=("RottenTomatoesScore", "mean"),
    ).reset_index()
    by_year["roi"] = by_year["total_global_revenue"] / by_year["total_budget"]

    by_genre = df.groupby("Genre").agg(
        movie_count=("MovieID", "count"),
        total_global_revenue=("Global_BoxOfficeUSD", "sum"),
        avg_imdb=("IMDbRating", "mean"),
        avg_roi=("Global_BoxOfficeUSD", lambda x: x.sum() / df.loc[x.index, "BudgetUSD"].sum()),
    ).reset_index().sort_values("total_global_revenue", ascending=False)

    top_directors = df.groupby("Director").agg(
        movie_count=("MovieID", "count"),
        total_global_revenue=("Global_BoxOfficeUSD", "sum"),
        avg_imdb=("IMDbRating", "mean"),
    ).reset_index().sort_values("total_global_revenue", ascending=False).head(10)

    GOLD_DIR.mkdir(parents=True, exist_ok=True)
    by_year.to_parquet(GOLD_DIR / "movies_by_year.parquet", index=False)
    by_genre.to_parquet(GOLD_DIR / "movies_by_genre.parquet", index=False)
    top_directors.to_parquet(GOLD_DIR / "top_directors.parquet", index=False)

    print(f"Gold: {len(by_year)} years, {len(by_genre)} genres, top {len(top_directors)} directors -> {GOLD_DIR}")
    print("\nTop 5 genres by revenue:")
    print(by_genre.head(5).to_string(index=False))


if __name__ == "__main__":
    aggregate()
