from __future__ import annotations
from typing import Iterable, Optional
import re
import pandas as pd
from matplotlib import pyplot as plt

SPECIAL_LISTED_IN_PHRASES = [
    "Arts, Entertainment, and Culture",  # Amazon special case
]



def _standardise_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    return df


def _split_multivalue(
    series: pd.Series,
    *,
    sep: str = ",",
    protect_phrases: Optional[Iterable[str]] = None,
) -> pd.Series:
    """
    Split comma-separated strings into lists, with optional phrase protection.
    Returns lists; missing/blank -> [].
    """
    protect_phrases = list(protect_phrases or [])
    placeholder_map = {p: f"__PHRASE_{i}__" for i, p in enumerate(protect_phrases)}

    def split_one(x):
        if not isinstance(x, str) or not x.strip():
            return []

        s = x
        for phrase, ph in placeholder_map.items():
            s = s.replace(phrase, ph)

        parts = [p.strip() for p in s.split(sep) if p.strip()]

        # restore protected phrases
        restored = []
        for p in parts:
            for phrase, ph in placeholder_map.items():
                p = p.replace(ph, phrase)
            restored.append(p)

        return restored

    return series.apply(split_one)


# streaming_func.py functuons for cleaning streaming dataframes
def clean_streaming_df(df_raw: pd.DataFrame) -> pd.DataFrame:
    """
    Clean a streaming-catalog dataframe (Netflix / Disney+ / Prime style).

    Expected columns (if present):
      - cast, country, listed_in : comma-separated strings
      - duration : e.g. "90 min" or "3 Seasons"
      - rating   : string rating (may be missing)

    Output columns added:
      - duration_mins (Int64)
      - duration_seasons (Int64)
    """

    df = _standardise_columns(df_raw)

    # Split multivalue fields into lists
    df["cast"] = _split_multivalue(df["cast"], sep=",")
    df["country"] = _split_multivalue(df["country"], sep=",")
    df["listed_in"] = _split_multivalue(
        df["listed_in"], sep=",", protect_phrases=SPECIAL_LISTED_IN_PHRASES
    )
    
    ###
    # # Extract duration as numeric (for movies) or number of seasons/episodes (for TV shows)    
    # def parse_minutes(x):
    #     if isinstance(x, str):
    #         s = x.strip()
    #         if "min" in s:
    #             try:
    #                 return int(s.split()[0])
    #             except ValueError:
    #                 return None
    #     return None
    
    # def parse_seasons(x):
    #     if isinstance(x, str):
    #         s = x.strip()
    #         # handle both singular "Season" and plural "Seasons"
    #         if "Season" in s or "Seasons" in s:
    #             try:
    #                 return int(s.split()[0])
    #             except ValueError:
    #                 return None
    #     return None
    
    # df["duration_mins"] = df["duration"].apply(parse_minutes)
    # df["duration_seasons"] = df["duration"].apply(parse_seasons)
    ###

    # Parse duration using regex (robust + readable)
    duration = df["duration"].astype("string")

    mins = duration.str.extract(r"^\s*(\d+)\s*min", expand=False)
    seasons = duration.str.extract(r"^\s*(\d+)\s*Season", expand=False)

    df["duration_mins"] = pd.to_numeric(mins, errors="coerce").astype("Int64")
    df["duration_seasons"] = pd.to_numeric(seasons, errors="coerce").astype("Int64")
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

    # Explode genres & subsequently explode casts so each row has 1 actor & 1 genre
    exploded = df.explode("listed_in").explode("cast")

    # Clean up: drop empty/NaN genres & actors
    l = exploded["listed_in"].astype("string").str.strip()
    c = exploded["cast"].astype("string").str.strip()
    mask = l.notna() & c.notna() & (l != "") & (c != "")

    # Group by genre & count unique actors
    genre_actor_counts = (
        exploded.loc[mask]
        .groupby(l[mask])["cast"]
        .nunique()
        .sort_values(ascending=False)
    )

    return genre_actor_counts



def plot_top_unique_actors(series, title, top_n=10, figsize=(10, 4)):
    top = series.sort_values(ascending=False).head(top_n).sort_values()
    ax = top.plot(kind="barh", figsize=figsize)
    ax.set_title(title)
    ax.set_xlabel("Number of unique actors")
    ax.set_ylabel("Genre")
    plt.tight_layout()
    plt.show()



def plot_top_countries(country_col: pd.Series, title: str, top_n: int = 10, figsize=(10, 4)) -> pd.Series:
    """
    Plot top-N countries as a horizontal bar chart.

    Expects country_col to be a Series where each row is either:
      - a list of countries (preferred after cleaning), or
      - a single country string, or
      - missing/empty.

    Returns the top-N counts (Series), useful if you want to print/save them.
    """

    s = country_col.explode()

    s = s.dropna().astype(str).str.strip()
    s = s[s != ""]

    top = s.value_counts().head(top_n).sort_values()  # sort for nicer barh ordering

    ax = top.plot(kind="barh", figsize=figsize)
    ax.set_title(title)
    ax.set_xlabel("Number of titles")
    ax.set_ylabel("Country")
    plt.tight_layout()
    plt.show()