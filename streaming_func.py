# importing necessary libraries
import pandas as pd

# streaming_func.py functuons for cleaning streaming dataframes
def clean_streaming_df(df_raw):
    
    df = df_raw.copy()
    
    # Standardize column names for easier access & manipulation
    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]
    
    # Split multi-value string columns into lists
    for col in ["cast", "country", "listed_in"]:
        df[col] = df[col].fillna("").apply(
            lambda s: [x.strip() for x in s.split(",")] if s else []
        )
    
    # Extract duration as numeric (for movies) or number of seasons/episodes (for TV shows)    
    def parse_minutes(x):
        if isinstance(x, str):
            s = x.strip()
            if "min" in s:
                try:
                    return int(s.split()[0])
                except ValueError:
                    return None
        return None
    
    def parse_seasons(x):
        if isinstance(x, str):
            s = x.strip()
            # handle both singular "Season" and plural "Seasons"
            if "Season" in s or "Seasons" in s:
                try:
                    return int(s.split()[0])
                except ValueError:
                    return None
        return None
    
    df["duration_mins"] = df["duration"].apply(parse_minutes)
    df["duration_seasons"] = df["duration"].apply(parse_seasons)
    # df["release_year"] = pd.to_numeric(df["release_year"], errors="coerce")
    df["rating"] = df["rating"].fillna("NaN")

    return df


# The unique_actors_per_genre function helps extract  
def unique_actors_per_genre(df: pd.DataFrame) -> pd.Series:
    """
    The dataframe is expected to be a cleaned 'streaming dataframe' where:
      - df['cast'] is a list of actor names (or [])
      - df['listed_in'] is a list of genres (or [])
    
    Returns a Series indexed by genre, with the number of UNIQUE actors
    that have ever appeared in at least one title in that genre.
    """

    # Explode genres so each row has 1 genre
    exploded = df.explode("listed_in")

    # Explode cast so each row has 1 actor & 1 genre
    exploded = exploded.explode("cast")

    # Clean up: drop empty/NaN genres & actors
    exploded["listed_in"] = exploded["listed_in"].astype(str).str.strip()
    exploded["cast"] = exploded["cast"].astype(str).str.strip()

    mask = (
        exploded["listed_in"].notna() &
        (exploded["listed_in"] != "") &
        exploded["cast"].notna() &
        (exploded["cast"] != "")
    )
    exploded = exploded[mask]

    # Group by genre & count unique actors
    genre_actor_counts = (
        exploded
        .groupby("listed_in")["cast"]
        .nunique()          # <– unique actors per genre
        .sort_values(ascending=False)
    )

    return genre_actor_counts