import pandas as pd
from pathlib import Path

RAW_DIR = Path("data/raw")
TMDB_SAMPLE = RAW_DIR / "tmdb_movies_100.csv"


def ensure_dirs():
    """Ensure required directory structure exists."""
    (RAW_DIR / "imdb").mkdir(parents=True, exist_ok=True)
    (RAW_DIR / "the-movies-dataset").mkdir(parents=True, exist_ok=True)
    Path("data/intermediate").mkdir(parents=True, exist_ok=True)
    Path("data/curated").mkdir(parents=True, exist_ok=True)


def main():
    print("📂 Loading TMDb sample data...")
    ensure_dirs()

    if not TMDB_SAMPLE.exists():
        raise FileNotFoundError(
            f"\ntmdb_movies_100.csv missing.\n"
            f"Expected at: {TMDB_SAMPLE}\n\n"
            f"➡ FIX: Place your TMDb sample file in data/raw/tmdb_movies_100.csv\n"
        )

    df = pd.read_csv(TMDB_SAMPLE)
    print(f"Loaded {len(df)} TMDb rows.")

    # Ensure correct dtypes
    if "id" in df.columns:
        df["id"] = df["id"].astype(str)

    df.to_csv(TMDB_SAMPLE, index=False)
    print(f"✅ Verified TMDb sample → {TMDB_SAMPLE}")


if __name__ == "__main__":
    main()
