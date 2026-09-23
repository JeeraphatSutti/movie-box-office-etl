# Movie Box Office ETL Pipeline

An end-to-end ETL pipeline built with the **medallion architecture** (Bronze → Silver → Gold)
that incrementally ingests raw movie box office data (~1M records), cleans and validates it,
and produces aggregate analytics ready for reporting.

## Architecture
data/raw/.csv Raw source CSV files (landing zone)
│
▼ bronze_ingest.py
data/bronze/movies.parquet Raw + ingestion metadata (_ingested_at, _source_file)
│
▼ silver_transform.py
data/silver/movies_clean.parquet Cleaned, deduplicated, validated records
│
▼ gold_aggregate.py
data/gold/.parquet Aggregates: by year, by genre, top directors

## Key Features

- **Incremental ingestion** — a state file tracks processed filenames, so re-running
  only ingests new files. Safe to re-run at any time.
- **Idempotent** — ingesting the same file twice does not duplicate data
  (deduplicated by `MovieID` business key).
- **Data lineage** — every record carries `_ingested_at` and `_source_file`.
- **Data quality checks** — null handling, deduplication, date parsing
  (DD-MM-YYYY), year sanity filtering, and cross-validation of `ReleaseYear`
  against `ReleaseDate`.

## Data Quality Results

| Check | Result |
|---|---|
| Raw records ingested | 1,000,005 |
| Records after cleaning | 1,000,002 |
| Year mismatch (ReleaseYear vs ReleaseDate) | 0 rows |

## Gold Layer Outputs

| File | Description |
|---|---|
| `movies_by_year.parquet` | Movie count, budget, revenue, avg ratings, ROI per release year (76 years) |
| `movies_by_genre.parquet` | Revenue and ROI performance per genre (8 genres) |
| `top_directors.parquet` | Top 10 directors by total global revenue |

### Sample Insight — Top 5 Genres by Global Revenue

| Genre | Movies | Total Revenue (USD) | Avg IMDb |
|---|---|---|---|
| Drama | 250,019 | 6.79T | 6.49 |
| Comedy | 199,833 | 5.44T | 6.50 |
| Action | 150,132 | 4.03T | 6.50 |
| Horror | 100,010 | 2.75T | 6.50 |
| Thriller | 100,071 | 2.75T | 6.50 |

Revenue concentration is driven by genre **volume** rather than per-title ROI —
average ROI is nearly identical (~2.77x) across all genres.

## How to Run

```bash
pip install -r requirements.txt

# Run the full pipeline (bronze -> silver -> gold)
python src/run_pipeline.py

# Or run each layer individually
python src/bronze_ingest.py
python src/silver_transform.py
python src/gold_aggregate.py

Drop new CSV files into data/raw/ and re-run — only new files will be ingested.