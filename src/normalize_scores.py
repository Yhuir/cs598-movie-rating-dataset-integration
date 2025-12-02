import pandas as pd
from pathlib import Path

def to_percent(x):
    """
    Convert strings like '83%' or 8.3 into 0–100 scale.
    
    Args:
        x: Input value (str or float)
    Returns:
        float: Normalized percentage score or None
    
    """
    if pd.isna(x):
        return None
    if isinstance(x, str) and "%" in x:
        return float(x.replace("%", ""))
    try:
        x = float(x)
        return x * 10 if x <= 10 else x
    except:
        return None


def extract_rt_score(row):
    """
    Extract Rotten Tomatoes critic score from OMDb Ratings list.
    
    Args:
        row: DataFrame row with 'Ratings' column.
    Returns:
        float: Rotten Tomatoes score in percent or None
    
    """
    if "Ratings" not in row or pd.isna(row["Ratings"]):
        return None
    try:
        ratings = eval(row["Ratings"]) if isinstance(row["Ratings"], str) else row["Ratings"]
        for r in ratings:
            if r.get("Source") == "Rotten Tomatoes":
                return to_percent(r["Value"])
    except:
        return None
    return None


def main():
    print("Loading files...")

    tmdb = pd.read_csv("data/raw/tmdb_movies_100.csv")
    rt = pd.read_csv("data/raw/rt_omdb_sample.csv")
    links = pd.read_csv("data/intermediate/link_candidates.csv")

    # Detect OMDb title column
    title_cols = [c for c in rt.columns if c.lower() == "title"]
    rt_title_col = title_cols[0] if title_cols else "Title"
    print(f"Detected OMDb title column: {rt_title_col}")

    # Merge
    merged = (
        links.merge(tmdb, left_on="tmdb_title", right_on="title", how="left")
              .merge(rt, left_on="rt_title", right_on=rt_title_col, how="left", suffixes=("_tmdb", "_rt"))
    )

    print(f"After merge: {merged.shape[0]} rows, {merged.shape[1]} columns")

    # Normalize IMDb rating 
    if "imdbRating" in merged.columns:
        merged["imdb_rating_norm"] = merged["imdbRating"].apply(to_percent)
    else:
        merged["imdb_rating_norm"] = None

    # Normalize Rotten Tomatoes critic score
    if "rt_score" in merged.columns:
        merged["rt_score_norm"] = merged["rt_score"].apply(to_percent)
    else:
        merged["rt_score_norm"] = merged.apply(extract_rt_score, axis=1)

    # Rating gap 
    merged["rating_gap"] = merged["rt_score_norm"] - merged["imdb_rating_norm"]

    # Z-scores
    for col in ["imdb_rating_norm", "rt_score_norm"]:
        mean = merged[col].mean()
        std = merged[col].std()
        merged[f"{col}_z"] = (merged[col] - mean) / std

    out_path = Path("data/curated/movies_with_scores.csv")
    merged.to_csv(out_path, index=False)
    print(f"✅ Saved normalized dataset → {out_path}")


if __name__ == "__main__":
    main()
