import pandas as pd
from rapidfuzz import fuzz, process

def detect_title_column(df):
    """
    Detect the best possible title column from OMDb data.
    """
    possible_cols = ["title", "movie_title", "rt_title", "tmdb_title", "name"]
    for c in df.columns:
        if c.lower() in possible_cols:
            return c
    raise ValueError(f"No recognizable title column found. Columns: {list(df.columns)}")

def main():
    # Load TMDb data
    tmdb = pd.read_csv("data/raw/tmdb_movies_100.csv")
    tmdb["tmdb_title"] = tmdb["title"].astype(str)
    tmdb["tmdb_year"] = tmdb["release_date"].str[:4]

    # Load OMDb / RT data
    rt = pd.read_csv("data/raw/rt_omdb_sample.csv")

    # Automatically detect title column
    rt_title_col = detect_title_column(rt)
    rt["rt_title"] = rt[rt_title_col].astype(str)

    print(f"Using OMDb title column: {rt_title_col}")

    candidates = []

    for idx, row in tmdb.iterrows():
        title_tmdb = row["tmdb_title"]

        match, score, _ = process.extractOne(
            title_tmdb,
            rt["rt_title"],
            scorer=fuzz.token_sort_ratio
        )

        candidates.append({
            "tmdb_id": row["id"],
            "tmdb_title": title_tmdb,
            "tmdb_year": row["tmdb_year"],
            "rt_title": match,
            "similarity": score
        })

    df_out = pd.DataFrame(candidates)
    df_out.to_csv("data/intermediate/link_candidates.csv", index=False)

    print("✅ Saved matches to data/intermediate/link_candidates.csv")

if __name__ == "__main__":
    main()
