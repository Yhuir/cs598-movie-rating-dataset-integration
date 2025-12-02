import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="Movie Ratings Explorer", layout="wide")

st.title("🎬 Movie Ratings Explorer")
st.write("Interactive viewer for the curated TMDb + IMDb + Rotten Tomatoes dataset.")

@st.cache_data
def load_data():
    return pd.read_csv("data/curated/movies_with_scores.csv")

df = load_data()


# DATA PREVIEW
st.subheader("Dataset Preview")
st.write("Use the slider below to inspect the first few rows of the curated dataset. "
         "This helps you understand the structure of the integrated ratings and metadata.")

num_rows = st.slider("Number of rows to preview:", 5, len(df), 10)
st.dataframe(df.head(num_rows))


# GENRE HANDLING FIX
genre_col = None
for col in df.columns:
    if col.lower() in ["genres", "genre", "tmdb_genres", "genres_tmdb"]:
        genre_col = col
        break

if genre_col is None:
    st.error("No genre column found in dataset. Available columns: " + ", ".join(df.columns))
else:
    df["primary_genre"] = (
        df[genre_col]
        .fillna("")
        .astype(str)
        .str.split("|")
        .str[0]
        .replace("", "Unknown")
    )


# IMDb vs RT
st.subheader("IMDb vs Rotten Tomatoes (Normalized Ratings)")

chart = (
    alt.Chart(df)
    .mark_circle(size=70)
    .encode(
        x=alt.X(
            "imdb_rating_norm",
            title="IMDb Audience Rating (0–100 normalized)"
        ),
        y=alt.Y(
            "rt_score_norm",
            title="Rotten Tomatoes Critic Score (0–100 normalized)"
        ),
        tooltip=[
            "tmdb_title",
            alt.Tooltip("imdb_rating_norm", title="IMDb (0–100)"),
            alt.Tooltip("rt_score_norm", title="RT Critic (0–100)")
        ]
    )
    .interactive()
)

st.altair_chart(chart, use_container_width=True)

st.markdown("""
**What this chart shows:**  
This scatter plot compares *audience ratings* from IMDb with *critic ratings* from Rotten Tomatoes.  
- Points along the **diagonal line** indicate agreement between critics and audiences.  
- Points **above** the diagonal reflect *higher critic scores than audience scores*.  
- Points **below** the diagonal reflect *higher audience scores*.  
""")



# GENRE GAP

st.subheader("Critic–Audience Rating Gap by Genre (RT − IMDb)")

# Compute rating gap per movie
df["rating_gap"] = df["rt_score_norm"] - df["imdb_rating_norm"]

# Aggregate: average gap per primary genre 
gap_df = (
    df.groupby("primary_genre", as_index=False)["rating_gap"]
      .mean()
      .sort_values("rating_gap")
)

gap_chart = (
    alt.Chart(gap_df)
    .mark_bar()
    .encode(
        x=alt.X(
            "rating_gap:Q",
            title="Average Rating Difference (Rotten Tomatoes − IMDb, normalized points)"
        ),
        y=alt.Y(
            "primary_genre:N",
            sort=gap_df["primary_genre"].tolist(),
            title="Primary Genre"
        ),
        tooltip=[
            alt.Tooltip("primary_genre:N", title="Genre"),
            alt.Tooltip("rating_gap:Q", title="Avg RT − IMDb (points)")
        ]
    )
)

st.altair_chart(gap_chart, use_container_width=True)

st.markdown("""
**What this chart shows:**  
This bar chart summarizes the **average critic–audience disagreement per genre**.  
- Positive values (**RT > IMDb**) mean *critics liked that genre more on average*.  
- Negative values (**IMDb > RT**) mean *audiences liked that genre more*.  
- Bars near zero indicate general agreement between critics and audiences within that genre.
""")



# BUDGET vs RT SCORE

st.subheader("Budget vs Rotten Tomatoes Critic Score")

# Ensure budget is numeric
df["budget"] = pd.to_numeric(df["budget"], errors="coerce")

# Drop zero or missing budgets
df_budget = df[df["budget"] > 0].copy()

budget_chart = (
    alt.Chart(df_budget)
    .mark_circle(size=60)
    .encode(
        x=alt.X(
            "budget:Q",
            scale=alt.Scale(type="log"),
            title="Production Budget (log scale, USD)"
        ),
        y=alt.Y(
            "rt_score_norm",
            title="Rotten Tomatoes Critic Score (0–100 normalized)"
        ),
        tooltip=[
            "tmdb_title",
            alt.Tooltip("budget:Q", title="Budget (USD)"),
            alt.Tooltip("rt_score_norm:Q", title="RT Score (0–100)")
        ]
    )
    .interactive()
)

st.altair_chart(budget_chart, use_container_width=True)

st.markdown("""
**What this chart shows:**  
This scatter plot examines whether **big-budget movies receive higher critic scores**.

Movies with a reported budget of **0** (common missing value in TMDb)  
were removed to avoid distortion in the log scale.

- The log scale spreads values across \$3M–\$98M realistically.  
- Missing-budget movies are excluded for clarity.  
- In this curated dataset, there is **no strong relationship** between budget and critic score.
""")

