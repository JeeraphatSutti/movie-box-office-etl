import time
from bronze_ingest import ingest
from silver_transform import transform
from gold_aggregate import aggregate


def run():
    start = time.time()
    print("=== BRONZE ===")
    ingest()
    print("=== SILVER ===")
    transform()
    print("=== GOLD ===")
    aggregate()
    print(f"\nPipeline completed in {time.time() - start:.2f}s")


if __name__ == "__main__":
    run()
