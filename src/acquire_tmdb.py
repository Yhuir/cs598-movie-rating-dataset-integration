import pandas as pd
import json
from pathlib import Path

def extract_names(json_str, key="name", top_n=3):
    """Extract top N names (e.g., genres, cast) from a JSON-like string."""
    if not isinstance(json_str, str):
        return None
    try:
        items = json.loads(json_str.replace("'", '"'))
        return "|".join([x[key] for x in items[:top_n]])
    except Exception:
        return None

def main():
    # --- Paths ---
    base_path = Path("data/raw/the-movies-dataset")

    movies_path = base_path / "movies_metadata.csv"
    credits_path = base_path / "credits.csv"

    print("Loading data...")
    movies = pd.read_csv(movies_path, low_memory=False)
    credits = pd.read_csv(credits_path)

    # --- Select and clean movie columns ---
    movies_subset = movies[[
        "id", "title", "original_title", "release_date",
        "budget", "revenue", "runtime", "genres", "popularity"
    ]].copy()

    # Extract year and clean genres
    movies_subset["release_year"] = movies_subset["release_date"].astype(str).str[:4]
    movies_subset["genres"] = movies_subset["genres"].apply(lambda x: extract_names(x) if isinstance(x, str) else None)

    # --- Extract director and cast ---
    credits["cast_top3"] = credits["cast"].apply(lambda x: extract_names(x, key="name", top_n=3))
    def get_director(crew_str):
        if not isinstance(crew_str, str):
            return None
        try:
            crew = json.loads(crew_str.replace("'", '"'))
            directors = [m["name"] for m in crew if m.get("job") == "Director"]
            return directors[0] if directors else None
        except Exception:
            return None
    credits["director"] = credits["crew"].apply(get_director)

    credits_small = credits[["id", "cast_top3", "director"]]

    # --- Ensure consistent types for merging ---
    movies_subset["id"] = movies_subset["id"].astype(str)
    credits_small["id"] = credits_small["id"].astype(str)

    # --- Merge and sample ---
    merged = movies_subset.merge(credits_small, on="id", how="left")
    merged_sample = merged.head(100)

    # --- Save output ---
    output_path = Path("data/raw/tmdb_movies_100.csv")
    merged_sample.to_csv(output_path, index=False)
    print(f"✅Saved sample: {output_path} ({len(merged_sample)} rows)")

if __name__ == "__main__":
    main()
