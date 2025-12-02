import pandas as pd
from pathlib import Path


# ----------------------------
# HELPERS
# ----------------------------
def to_percent(x):
    """Convert strings like '83%' or numbers like 8.3 into 0–100 scale."""
    if pd.isna(x):
        return None

    # Case 1: string percentage "87%"
    if isinstance(x, str) and "%" in x:
        try:
            return float(x.strip("%"))
        except Exception:
            return None

    # Case 2: numeric 1–10 IMDb score → convert to 0–100
    try:
        x = float(x)
        return x * 10 if x <= 10 else x
    except Exception:
        return None


def detect_title_column(df):
    """Find the correct title column among common OMDb fields."""
    candidates = ["title", "Title", "movie_title", "rt_title", "tmdb_title", "name"]
    for c in df.columns:
        if c in candidates:
            return c
    raise ValueError(f"No usable title column found in OMDb data. Columns: {list(df.columns)}")



# ----------------------------
# MAIN PIPELINE
# ----------------------------
def main():
    print("Loading files...")

    tmdb = pd.read_csv("data/raw/tmdb_movies_100.csv")
    rt = pd.read_csv("data/raw/rt_omdb_sample.csv")
    links = pd.read_csv("data/intermediate/link_candidates.csv")

    # ----------------------------
    # Detect OMDb title column
    # ----------------------------
    rt_title_col = detect_title_column(rt)
    print(f"Detected OMDb title column: {rt_title_col}")

    rt["rt_title"] = rt[rt_title_col].astype(str)
    links["rt_title"] = links["rt_title"].astype(str)
    links["tmdb_title"] = links["tmdb_title"].astype(str)

    # ----------------------------
    # Merge tables
    # ----------------------------
    merged = (
        links
        .merge(tmdb, left_on="tmdb_title", right_on="title", how="left")
        .merge(rt, left_on="rt_title", right_on="rt_title", how="left", suffixes=("_tmdb", "_rt"))
    )

    print(f"After merge: {merged.shape[0]} rows, {merged.shape[1]} columns")

    # ----------------------------
    # Normalize rating fields
    # ----------------------------
    print("Normalizing rating fields...")

    # Detect IMDB rating column in your files
    imdb_col_candidates = ["imdb_rating", "imdbRating", "imdb_score"]
    imdb_col = next((c for c in imdb_col_candidates if c in merged.columns), None)

    rt_col_candidates = ["rt_score", "rtScore", "RottenTomatoes", "Ratings"]
    rt_col = next((c for c in rt_col_candidates if c in merged.columns), None)

    if imdb_col is None or rt_col is None:
        raise ValueError(f"Missing IMDb or RT score columns. IMDb={imdb_col}, RT={rt_col}")

    merged["imdb_rating_norm"] = merged[imdb_col].apply(to_percent)
    merged["rt_score_norm"] = merged[rt_col].apply(to_percent)

    # ----------------------------
    # Compute z-scores
    # ----------------------------
    for col in ["imdb_rating_norm", "rt_score_norm"]:
        mean = merged[col].mean()
        std = merged[col].std()
        merged[f"{col}_z"] = (merged[col] - mean) / std

    # ----------------------------
    # Save output
    # ----------------------------
    out = Path("data/curated/movies_with_scores.csv")
    merged.to_csv(out, index=False)

    print(f"✅ Saved normalized dataset → {out}")


if __name__ == "__main__":
    main()
