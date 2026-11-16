# MovieLens Dashboard

A beginner-friendly Streamlit dashboard for the MovieLens ratings data. It answers four questions:

1. How are movie genres distributed? (movies can have more than one genre)
2. Which genres have the highest and lowest average ratings?
3. How have average ratings changed across movie **release** years?
4. What are the top 5 movies with at least 50 ratings, and how does that list change at 150 ratings?

## Run locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Data

`data/movie_ratings.csv` has one row per rating (`user_id`, `movie_id`, `rating`, `title`, `year`, `genres`, and more). Genres are pipe-separated, for example `Comedy|Romance`.
