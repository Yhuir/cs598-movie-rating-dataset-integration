# src/ingest_imdb.py

"""
Ingest IMDb public datasets and link them to the TMDb pilot subset.

- Downloads IMDb title.basics.tsv.gz and title.ratings.tsv.gz if not present
- Filters to feature films
- Merges basics + ratings
- Links to data/raw/tmdb_movies_100.csv via fuzzy title matching and ±1 year tolerance
- Outputs:
    - data/raw/imdb_all_movies.csv  (filtered IMDb universe)
    - data/intermediate/imdb_tmdb_links.csv  (match table with similarity scores)
"""

import os
import gzip
import shutil
from pathlib import Path
from difflib import SequenceMatcher

import pandas as pd
import requests

IMDB_BASE_URL = "https://datasets.imdbws.com/"
BASICS_FILE = "title.basics.tsv.gz"
RATINGS_FILE = "title.ratings.tsv.gz"


def download_if_missing(url: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        print(f"✅{dest.name} already exists, skipping download.")
        return

    print(f"Downloading {dest.name} from IMDb...")
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(dest, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    print(f"✅Downloaded to {dest}")


def read_tsv_gz(path: Path) -> pd.DataFrame:
    return pd.read_csv(
        path,
        sep="\t",
        na_values="\\N",
        low_memory=False,
    )


def title_similarity(a: str, b: str) -> float:
    if pd.isna(a) or pd.isna(b):
        return 0.0
    return SequenceMatcher(None, str(a).lower(), str(b).lower()).ratio()


def main():
    base_raw = Path("data/raw/imdb")
    base_raw.mkdir(parents=True, exist_ok=True)

    basics_path = base_raw / BASICS_FILE
    ratings_path = base_raw / RATINGS_FILE

    # 1. Download IMDb datasets if needed
    download_if_missing(IMDB_BASE_URL + BASICS_FILE, basics_path)
    download_if_missing(IMDB_BASE_URL + RATINGS_FILE, ratings_path)

    # 2. Load IMDb basics + ratings
    print("Loading IMDb basics and ratings...")
    basics = read_tsv_gz(basics_path)
    ratings = read_tsv_gz(ratings_path)

    # 3. Filter to feature films (tconst type 'movie')
    movies = basics[basics["titleType"] == "movie"].copy()
    movies = movies[["tconst", "primaryTitle", "originalTitle", "startYear", "isAdult", "runtimeMinutes", "genres"]]

    # Optionally drop adult titles
    movies = movies[movies["isAdult"] != 1]

    # Merge ratings
    movies_ratings = movies.merge(ratings, on="tconst", how="left")
    movies_ratings.rename(
        columns={
            "averageRating": "imdb_avg_rating",
            "numVotes": "imdb_num_votes",
        },
        inplace=True,
    )

    imdb_all_out = Path("data/raw/imdb_all_movies.csv")
    movies_ratings.to_csv(imdb_all_out, index=False)
    print(f"✅Saved filtered IMDb movie universe: {imdb_all_out} ({len(movies_ratings)} rows)")

    # 4. Link IMDb to TMDb pilot subset by title + year
    tmdb_path = Path("data/raw/tmdb_movies_100.csv")
    if not tmdb_path.exists():
        raise FileNotFoundError(
            f"{tmdb_path} not found. Run src/acquire_tmdb.py before ingesting IMDb."
        )

    tmdb = pd.read_csv(tmdb_path)
    # ensure year is numeric
    tmdb["release_year"] = pd.to_numeric(tmdb["release_year"], errors="coerce")
    movies_ratings["startYear"] = pd.to_numeric(movies_ratings["startYear"], errors="coerce")

    link_rows = []
    for _, tm in tmdb.dropna(subset=["title", "release_year"]).iterrows():
        year = int(tm["release_year"])

        # Candidate IMDb movies within ±1 year
        candidates = movies_ratings[
            movies_ratings["startYear"].between(year - 1, year + 1, inclusive="both")
        ]

        best_row = None
        best_sim = 0.0

        for _, imdb_row in candidates.iterrows():
            sim = title_similarity(tm["title"], imdb_row["primaryTitle"])
            if sim > best_sim:
                best_sim = sim
                best_row = imdb_row

        if best_row is not None and best_sim >= 0.80:
            link_rows.append(
                {
                    "tmdb_id": tm["id"],
                    "tmdb_title": tm["title"],
                    "tmdb_release_year": tm["release_year"],
                    "imdb_tconst": best_row["tconst"],
                    "imdb_title": best_row["primaryTitle"],
                    "imdb_startYear": best_row["startYear"],
                    "imdb_avg_rating": best_row["imdb_avg_rating"],
                    "imdb_num_votes": best_row["imdb_num_votes"],
                    "similarity": round(best_sim, 3),
                }
            )

    links_df = pd.DataFrame(link_rows)
    imdb_links_out = Path("data/intermediate/imdb_tmdb_links.csv")
    imdb_links_out.parent.mkdir(parents=True, exist_ok=True)
    links_df.to_csv(imdb_links_out, index=False)

    print(f"✅ Linked {len(links_df)} IMDb titles to TMDb pilot subset.")
    print(f"   Saved to {imdb_links_out}")


if __name__ == "__main__":
    main()
