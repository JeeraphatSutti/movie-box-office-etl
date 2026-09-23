import pandas as pd
from datetime import datetime, timezone
from config import BRONZE_PATH, STATE_PATH, RAW_DIR


def ingest():
    processed = set()
    if STATE_PATH.exists():
        processed = set(pd.read_parquet(STATE_PATH)["filename"])

    csv_files = sorted(RAW_DIR.glob("*.csv"))
    new_files = [f for f in csv_files if f.name not in processed]

    if not new_files:
        print("No new files. Nothing to do.")
        return

    new_dfs = []
    for f in new_files:
        df = pd.read_csv(f)
        df["_ingested_at"] = datetime.now(timezone.utc)
        df["_source_file"] = f.name
        new_dfs.append(df)
        print(f"Ingested new file: {f.name} ({len(df)} rows)")

    new_df = pd.concat(new_dfs, ignore_index=True)

    if BRONZE_PATH.exists():
        old_df = pd.read_parquet(BRONZE_PATH)
        new_df = new_df[~new_df["MovieID"].isin(old_df["MovieID"])]
        df = pd.concat([old_df, new_df], ignore_index=True)
    else:
        df = new_df

    BRONZE_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(BRONZE_PATH, index=False)

    old_state = (
        pd.read_parquet(STATE_PATH)
        if STATE_PATH.exists()
        else pd.DataFrame(columns=["filename", "processed_at"])
    )
    new_state = pd.DataFrame({
        "filename": [f.name for f in new_files],
        "processed_at": [datetime.now(timezone.utc)] * len(new_files),
    })
    state = pd.concat(
        [old_state[~old_state["filename"].isin(new_state["filename"])], new_state],
        ignore_index=True,
    )

    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    state.to_parquet(STATE_PATH, index=False)

    print(f"Bronze (incremental): +{len(new_df)} new rows, total {len(df)} rows -> {BRONZE_PATH}")


if __name__ == "__main__":
    ingest()
