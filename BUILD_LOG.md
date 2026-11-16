# Build log (Week 4 vibe coding)

Raw notes for next week's audit. Not a polished write-up.

## Moment 1 — first planning prompt

**Prompt I gave:** Help me create a plan to implement a MovieLens dashboard for class using Python and Streamlit, `movie_ratings.csv`, four required questions, at least two interactive controls, pandas and simple charts. Plan files first, keep it beginner-friendly, don't write code yet.

**What the AI produced first:** A project plan (not code): new folder `~/Developer/movielens-dashboard`, file list (`app.py`, `requirements.txt`, `data/movie_ratings.csv`, `README.md`, `BUILD_LOG.md`), explode-on-`|` for multi-genre movies, unique-movie counts for Q1, rating-level means for Q2, release `year` (not `rating_year`) for Q3, top-5 with a rating floor for Q4, year-range + extra widgets.

**What I changed and why:** I approved the plan and asked to build it. For Q4 I asked to **show both 50 and 150 results side by side** instead of only a slider. I also said not to deploy yet.

## Moment 2 — first implementation prompt

**Prompt I gave:** Follow the plan. Keep Python simple and beginner-friendly. Use pandas and Streamlit. Answer all four questions. Show both 50-rating and 150-rating results for Q4. Track prompts in `BUILD_LOG.md`. Create files and build the dashboard; don't deploy.

**What the AI produced first:** This first version of `app.py`: cached CSV load, sidebar year-range slider + genre multiselect, four chart sections, Q4 as two columns (min 50 vs min 150).

**What I changed and why:** First run showed Q1 bars in A–Z order (Action on top), so we switched those bars to Altair with `sort="-x"` so Drama (most movies) sits at the top. Also rounded Q4 averages to 3 decimals and dropped `movie_id` from the tables. Did not deploy.

## Moment 3 — after first run (placeholder)

Add a screenshot note or a “this number looked wrong” note here after you click through the local app.
