import pandas as pd
import sqlite3

DB_PATH = "data/steam_catalog.db"

def get_trend_data():
    conn = sqlite3.connect(DB_PATH)
    # We need release_date, categories, genres, and is_free for trend analysis
    query = "SELECT release_date, categories, genres, is_free FROM game_details"
    df = pd.read_sql_query(query, conn)
    conn.close()

    # Robust Year Extraction
    # We convert to datetime, errors='coerce' turns bad dates into NaT (Not a Time)
    df['release_year'] = pd.to_datetime(df['release_date'], errors='coerce').dt.year
    
    # Drop rows where year is missing or looks like an outlier (e.g., before 2005 or after 2026)
    df = df.dropna(subset=['release_year'])
    df = df[(df['release_year'] >= 2005) & (df['release_year'] <= 2026)]
    df['release_year'] = df['release_year'].astype(int)

    # Tagging: Multi-player vs Single-player
    df['is_multiplayer'] = df['categories'].str.contains('Multi-player', na=False, case=False)
    df['is_singleplayer'] = df['categories'].str.contains('Single-player', na=False, case=False)

    return df
