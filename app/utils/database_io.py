import sqlite3
import pandas as pd

DB_PATH = "data/steam_catalog.db"

def get_all_game_names():
    conn = sqlite3.connect(DB_PATH)
    # Get names for the search dropdown
    df = pd.read_sql_query("SELECT appid, name FROM game_details", conn)
    conn.close()
    return df

def get_game_by_id(appid):
    conn = sqlite3.connect(DB_PATH)
    query = "SELECT * FROM game_details WHERE appid = ?"
    df = pd.read_sql_query(query, conn, params=(int(appid),))
    conn.close()
    return df.iloc[0] if not df.empty else None
