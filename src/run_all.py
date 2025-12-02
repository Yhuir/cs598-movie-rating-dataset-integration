import subprocess
import sys
import os
from pathlib import Path

# Ensure script is run from project root
PROJECT_ROOT = Path(__file__).resolve().parents[1]
os.chdir(PROJECT_ROOT)

STEPS = [
    ("Acquire TMDb metadata",            "python src/acquire_tmdb.py"),
    ("Fetch Rotten Tomatoes + IMDb (OMDb)", "python src/scrape_rotten_tomatoes.py"),
    ("Ingest IMDb TSV archives",         "python src/ingest_imdb.py"),
    ("Match TMDb ↔ Rotten Tomatoes",     "python src/match_movies.py"),
    ("Normalize & integrate dataset",    "python src/normalize_scores.py"),
]

def run_step(label, command):
    print(f"\n▶ {label}")
    print(f"   Running: {command}")

    result = subprocess.run(command, shell=True)

    if result.returncode != 0:
        print(f"\nERROR: Step failed — {label}")
        sys.exit(result.returncode)
    else:
        print(f"✅ Completed: {label}")

def main():
    print("Starting full data pipeline...\n")

    for label, cmd in STEPS:
        run_step(label, cmd)

    final_path = PROJECT_ROOT / "data" / "curated" / "movies_with_scores.csv"
    print("\nPipeline complete!")
    print(f"Final curated dataset created at:\n   {final_path}\n")


if __name__ == "__main__":
    main()
