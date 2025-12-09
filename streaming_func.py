

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