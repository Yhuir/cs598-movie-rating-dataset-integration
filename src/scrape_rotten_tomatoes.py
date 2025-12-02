import os, time, requests, pandas as pd
from dotenv import load_dotenv
from tqdm import tqdm

load_dotenv()
API_KEY = os.getenv("OMDB_API_KEY")
BASE = "http://www.omdbapi.com/"

def fetch_rating(title, retries=5, delay=2):
    """Fetch OMDb rating with retry logic."""
    BASE = "http://www.omdbapi.com/"

    params = {
        "apikey": API_KEY,
        "t": title
    }

    for attempt in range(1, retries + 1):
        try:
            r = requests.get(BASE, params=params, timeout=10)
            r.raise_for_status()
            return r.json()
        
        except Exception as e:
            print(f"OMDb request failed (attempt {attempt}/{retries}): {e}")
            if attempt < retries:
                time.sleep(delay)
            else:
                print("Max retries reached. Skipping this title.")
                return None

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
    print("Saved Rotten Tomatoes + IMDb ratings sample.")

if __name__ == "__main__":
    main()
