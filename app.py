import altair as alt
import pandas as pd
import streamlit as st

st.set_page_config(page_title="MovieLens Dashboard", layout="wide")


@st.cache_data
def load_ratings():
    """Read the ratings file once and reuse it when widgets change."""
    df = pd.read_csv("data/movie_ratings.csv")
    # Release year is stored like 1996.0; drop rows with no year for year charts/filters.
    df["year"] = pd.to_numeric(df["year"], errors="coerce")
    df["genres"] = df["genres"].fillna("Unknown")
    return df


def sorted_bar_chart(df, category_col, value_col):
    """Horizontal bars sorted by the value, largest at the top."""
    chart = (
        alt.Chart(df)
        .mark_bar()
        .encode(
            y=alt.Y(category_col, sort="-x", title=""),
            x=alt.X(value_col, title=value_col.replace("_", " ")),
            tooltip=[category_col, value_col],
        )
    )
    st.altair_chart(chart, use_container_width=True)


def split_genres(df):
    """Turn pipe-separated genres into one row per genre.

    Example: a movie tagged Comedy|Romance becomes two rows, one Comedy and one Romance.
    That movie is counted in both genres. We do this before any genre counting or averaging.
    """
    out = df.copy()
    out["genre"] = out["genres"].str.split("|")
    out = out.explode("genre")
    out["genre"] = out["genre"].str.strip()
    out = out[out["genre"] != ""]
    return out


ratings = load_ratings()

st.title("MovieLens Ratings Dashboard")
st.write(
    "One row in the data is one user rating a movie. "
    "Use the sidebar to filter by release year and genre, then scroll through the four questions."
)

# --- Interactive controls (at least two) ---
years = ratings["year"].dropna()
min_year = int(years.min())
max_year = int(years.max())

st.sidebar.header("Filters")
year_range = st.sidebar.slider(
    "Movie release years",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year),
)

genre_table = split_genres(ratings)
all_genres = sorted(genre_table["genre"].unique())
selected_genres = st.sidebar.multiselect(
    "Genres (leave empty to include all)",
    options=all_genres,
    default=[],
)

# Filter ratings by release year, then by genre if the user picked any.
filtered = ratings[
    ratings["year"].between(year_range[0], year_range[1]) | ratings["year"].isna()
]
if selected_genres:
    movie_ids = genre_table.loc[
        genre_table["genre"].isin(selected_genres), "movie_id"
    ].unique()
    filtered = filtered[filtered["movie_id"].isin(movie_ids)]

st.sidebar.write(f"Showing **{len(filtered):,}** ratings after filters.")

# --- Question 1 ---
st.header("1. What is the distribution of movie genres?")
st.write(
    "Movies can belong to several genres at once. Before counting, the dashboard splits "
    "the `genres` column on `|` (the pipe character) and makes one row per genre. "
    "Then it keeps **one row per movie**, so a popular movie is not counted extra times "
    "just because it has more ratings. A Comedy|Romance movie adds 1 to Comedy and 1 to Romance."
)

movies = filtered.drop_duplicates(subset=["movie_id"])
movies_by_genre = split_genres(movies)
genre_counts = (
    movies_by_genre.groupby("genre")
    .size()
    .reset_index(name="number_of_movies")
    .sort_values("number_of_movies", ascending=True)
)

sorted_bar_chart(genre_counts, "genre", "number_of_movies")
st.caption("Bars are sorted by count, not alphabetically. Drama is the most common genre.")

# --- Question 2 ---
st.header("2. Which genres have the highest and lowest average ratings?")
st.write(
    "Each rating is copied to every genre tagged on that movie. "
    "Then we take the mean rating per genre. This is a rating-level average, "
    "so genres with lots of ratings have more influence from those individual scores."
)

ratings_by_genre = split_genres(filtered)
genre_avg = (
    ratings_by_genre.groupby("genre")["rating"]
    .mean()
    .reset_index(name="average_rating")
    .sort_values("average_rating", ascending=True)
)

if not genre_avg.empty:
    lowest = genre_avg.iloc[0]
    highest = genre_avg.iloc[-1]
    st.write(
        f"**Highest:** {highest['genre']} ({highest['average_rating']:.2f}). "
        f"**Lowest:** {lowest['genre']} ({lowest['average_rating']:.2f})."
    )

sorted_bar_chart(genre_avg, "genre", "average_rating")

# --- Question 3 ---
st.header("3. How have average ratings changed across movie release years?")
st.write(
    "This uses the movie **release** year (`year`), not the year the user submitted the rating "
    "(`rating_year`). Each point is the mean of all ratings for movies released that year."
)

by_year = (
    filtered.dropna(subset=["year"])
    .groupby("year")["rating"]
    .mean()
    .reset_index()
)
by_year["year"] = by_year["year"].astype(int)
st.line_chart(by_year.set_index("year")["rating"])
st.caption("X-axis is release year. Y-axis is mean rating (about 1 to 5).")

# --- Question 4 ---
st.header("4. Top 5 highest-rated movies, with a ratings floor")
st.write(
    "A movie with two 5-star ratings should not beat a well-known film with hundreds of ratings. "
    "So we only keep movies with enough ratings, then take the top 5 by average rating. "
    "Both floors from the assignment are shown so you can compare them."
)


def top_movies(df, min_ratings):
    stats = (
        df.groupby(["movie_id", "title"], as_index=False)
        .agg(average_rating=("rating", "mean"), number_of_ratings=("rating", "size"))
    )
    enough = stats[stats["number_of_ratings"] >= min_ratings]
    top = (
        enough.sort_values(
            ["average_rating", "number_of_ratings"],
            ascending=[False, False],
        )
        .head(5)
        .reset_index(drop=True)
    )
    top["average_rating"] = top["average_rating"].round(3)
    return top[["title", "average_rating", "number_of_ratings"]]


col50, col150 = st.columns(2)

with col50:
    st.subheader("At least 50 ratings")
    top50 = top_movies(filtered, 50)
    st.dataframe(top50, width="stretch", hide_index=True)
    if not top50.empty:
        sorted_bar_chart(top50, "title", "average_rating")

with col150:
    st.subheader("At least 150 ratings")
    top150 = top_movies(filtered, 150)
    st.dataframe(top150, width="stretch", hide_index=True)
    if not top150.empty:
        sorted_bar_chart(top150, "title", "average_rating")

st.caption(
    "If a title drops off the 150 list, it had a high average but fewer than 150 ratings."
)
