# Curating a Multi-Source Dataset for Film Industry Analysis

This repository contains an end-to-end data curation workflow for integrating
movie metadata and ratings from **TMDb**, **IMDb**, and **Rotten Tomatoes / OMDb**
into a unified, analysis-ready dataset.

The curated dataset is designed to support questions such as:

- How do critic and audience ratings differ across platforms and genres?
- Is there a measurable relationship between financial success and critical reception?
- Which movie categories show the strongest divergence between critic and audience sentiment?

The project implements the full data lifecycle introduced in CS598:
**acquisition, quality assessment, cleaning, integration, modeling, metadata, and documentation**.
All steps are implemented as modular Python scripts and Jupyter notebooks.

---

## Repository Structure
- `data/`: Contains raw and processed datasets.
- `notebooks/`: Jupyter notebooks for data exploration and analysis.
- `src/`: Python scripts for data acquisition, cleaning, and integration.
- `docs/`: Documentation and metadata files.
- `README.md`: This file.
- `requirements.txt`: List of Python dependencies.
- `LICENSE`: License information for the project.

## Preparing the Dataset

The repository does not include raw third-party datasets due to licensing restrictions.
However, the entire dataset can be reproduced automatically using the provided pipeline scripts.

You do not need to manually download any of the datasets unless running offline.

This section explains how to prepare the required folder structure and how each script populates it.

1. Data Directory Structure
Your project expects the following folder layout:

```plaintext
data/
  raw/
    imdb/
      title.basics.tsv.gz
      title.ratings.tsv.gz
    the-movies-dataset/
      credits.csv
      keywords.csv
      ratings_small.csv
      more...
    tmdb_movies_100.csv
    imdb_all_movies.csv
    rt_omdb_sample.csv
  intermediate/
  curated/
```

If running the project for the first time, create the base folders:
```bash
mkdir -p data/raw/imdb data/raw/the-movies-dataset data/intermediate data/curated
```

**These folders will be filled automatically by the pipeline scripts.**


## Installation and Setup

1. Clone the repository:
```bash
git clone https://github.com/Yhuir/cs598-movie-rating-dataset-integration.git
cd cs598-movie-rating-dataset-integration
```

2. Create and activate a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

4. 4. Add your OMDb API key to a `.env` file in the root directory:
```makefile
OMDB_API_KEY=your_api_key_here
```
This key enables fetching Rotten Tomatoes + IMDb ratings through the OMDb API.

## Running the Full Pipeline

You can run each step individually or run the entire pipeline at once.

If you choose to run the entire pipeline at once, then you **don't** need to run the individual steps below.

### Run the entire pipeline at once
```bash
python src/run_all.py
```

### Individual Steps
Step 1 — Acquire TMDb metadata:
```bash
python src/acquire_tmdb.py
```

Outputs (inside data/raw/):
```plaintext
tmdb_movies_100.csv
the-movies-dataset/credits.csv
the-movies-dataset/keywords.csv
the-movies-dataset/ratings_small.csv
```

Step 2 — Step 2 — Fetch Rotten Tomatoes + IMDb ratings (via OMDb)
```bash
python src/scrape_rotten_tomatoes.py
```

Outputs:
```plaintext
data/raw/rt_omdb_sample.csv
```

Step 3 — Ingest IMDb datasets (TSV) and link with TMDb
```bash
python src/ingest_imdb.py
```

Downloads official IMDb archive files into:

```plaintext
data/raw/imdb/title.basics.tsv.gz
data/raw/imdb/title.ratings.tsv.gz
```

Then produces:

```plaintext
data/raw/imdb_all_movies.csv
data/intermediate/imdb_tmdb_links.csv
```

Step 4 — Match TMDb ↔ Rotten Tomatoes titles
```bash
python src/match_movies.py
```

Creates candidate cross-source matches:

```plaintext
data/intermediate/link_candidates.csv
```

Step 5 — Normalize and create curated dataset
```bash
python src/normalize_scores.py
```

Produces the final curated dataset:

```plaintext
data/curated/movies_with_scores.csv
```
This CSV is the unified table combining TMDb metadata, IMDb ratings, and Rotten Tomatoes critic scores — normalized and ready for analysis.

## Usage

### Option A — Jupyter Notebook

1. Launch Jupyter Notebook
First activate your virtual environment (important!):

```bash
source venv/bin/activate
```

Then start Jupyter:

```bash
jupyter notebook
```

2. Navigate to the Notebook

In the Jupyter file browser, open:

```plaintext
notebooks/02_explore_curated_dataset.ipynb
```

This notebook is fully self-contained and loads the curated dataset from:

```plaintext
data/curated/movies_with_scores.csv
```

3. Run the Notebook Cells

At the top menu, click: Run → Run All Cells
The notebook walks you through the analysis step-by-step.

4. What the Notebook Produces
The notebook generates:

IMDb vs Rotten Tomatoes (Normalized Ratings) Scatter Plot
- Shows whether critics and audiences agree across platforms
- Points near the diagonal → agreement
- Outlier points highlight strong disagreement


Genre-Level Critic–Audience Gap Visualization
- Computes average: RT score – IMDb score
- Positive = critics prefer the genre
- Negative = audiences prefer the genre
- Helps identify “critic favorites” or “audience favorites”
This supports your project’s goal of demonstrating how the cleaned dataset can answer analytical questions.

Budget vs Critic Score Analysis
- Scatter plot with log-scaled budget
- Tests whether higher budgets correlate with higher critic ratings
- Results show weak or no correlation for this pilot dataset



### Option B — Streamlit Dashboard

Run the Streamlit app:
```bash
streamlit run streamlit_app.py
```

Dashboard features:

- Dataset preview
- IMDb vs Rotten Tomatoes normalized scatter plot
- Genre gap visualization
- Budget vs critic score (log scale)
- Clear descriptions under each graph

## Data Sources 

See ethics_legal.md for full details.

Summary:

- TMDb dataset (Kaggle) — CC0 license
- IMDb datasets — permitted for non-commercial academic use
- Rotten Tomatoes + IMDb ratings accessed through OMDb API under its ToS
- No scraping of protected sites
- No personal or sensitive data used
- All usage aligns with the non-commercial educational purpose of CS598

## License

This project is licensed under the MIT License. See the LICENSE file for details.
