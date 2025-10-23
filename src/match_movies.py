import pandas as pd
from difflib import SequenceMatcher
from pathlib import Path

def title_similarity(a, b):
    if pd.isna(a) or pd.isna(b):
        return 0
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def main():
    tmdb = pd.read_csv("data/raw/tmdb_movies_100.csv")
    rt = pd.read_csv("data/raw/rt_omdb_sample.csv")

    # optional IMDb later
    tmdb["release_year"] = tmdb["release_year"].astype(str)
    rt["year"] = rt["year"].astype(str)

    candidates = []

    for _, tm in tmdb.iterrows():
        # match by same year ±1 and high title similarity
        matches = rt[rt["year"].astype(str).isin([tm["release_year"], str(int(tm["release_year"]) + 1), str(int(tm["release_year"]) - 1)])]
        for _, row in matches.iterrows():
            sim = title_similarity(tm["title"], row["title"])
            if sim > 0.8:
                candidates.append({
                    "tmdb_id": tm["id"],
                    "tmdb_title": tm["title"],
                    "rt_title": row["title"],
                    "rt_year": row["year"],
                    "similarity": round(sim, 3)
                })

    link_df = pd.DataFrame(candidates)
    link_df.to_csv("data/intermediate/link_candidates.csv", index=False)
    print(f"✅ Found {len(link_df)} candidate matches, saved to data/intermediate/link_candidates.csv")

if __name__ == "__main__":
    main()
