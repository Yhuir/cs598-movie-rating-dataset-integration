import os, time, requests, pandas as pd
from dotenv import load_dotenv
from tqdm import tqdm

load_dotenv()
API_KEY = os.getenv("OMDB_API_KEY")
BASE = "http://www.omdbapi.com/"

def fetch_rating(title):
    params = {"t": title, "apikey": API_KEY}
    r = requests.get(BASE, params=params)
    if r.status_code != 200:
        return None
    data = r.json()
    if data.get("Response") == "False":
        return None
    ratings = {r["Source"]: r["Value"] for r in data.get("Ratings", [])}
    return {
        "title": data.get("Title"),
        "year": data.get("Year"),
        "imdb_rating": data.get("imdbRating"),
        "rt_score": ratings.get("Rotten Tomatoes"),
        "metascore": data.get("Metascore")
    }

def main():
    df = pd.read_csv("data/raw/tmdb_movies_100.csv")
    titles = df["title"].dropna().unique()[:50]  # limit for pilot run
    results = []
    for t in tqdm(titles, desc="Fetching OMDb ratings"):
        record = fetch_rating(t)
        if record:
            results.append(record)
        time.sleep(0.3)
    out = pd.DataFrame(results)
    out.to_csv("data/raw/rt_omdb_sample.csv", index=False)
    print("✅ Saved Rotten Tomatoes + IMDb ratings sample.")

if __name__ == "__main__":
    main()
