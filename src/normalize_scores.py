import pandas as pd
from pathlib import Path

def to_percent(x):
    """Convert strings like '83%' or 8.3 to numeric 0–100"""
    if pd.isna(x):
        return None
    if isinstance(x, str) and "%" in x:
        return float(x.strip("%"))
    try:
        x = float(x)
        return x * 10 if x <= 10 else x
    except Exception:
        return None

def main():
    tmdb = pd.read_csv("data/raw/tmdb_movies_100.csv")
    rt = pd.read_csv("data/raw/rt_omdb_sample.csv")
    links = pd.read_csv("data/intermediate/link_candidates.csv")

    merged = links.merge(tmdb, left_on="tmdb_title", right_on="title", how="left") \
                  .merge(rt, left_on="rt_title", right_on="title", how="left", suffixes=("_tmdb", "_rt"))

    merged["imdb_rating_norm"] = merged["imdb_rating"].apply(to_percent)
    merged["rt_score_norm"] = merged["rt_score"].apply(to_percent)

    # compute z-scores for comparison
    for col in ["imdb_rating_norm", "rt_score_norm"]:
        mean = merged[col].mean()
        std = merged[col].std()
        merged[f"{col}_z"] = (merged[col] - mean) / std

    out = Path("data/curated/movies_with_scores.csv")
    merged.to_csv(out, index=False)
    print(f"✅ Saved normalized dataset: {out}")

if __name__ == "__main__":
    main()
