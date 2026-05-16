import pandas as pd
import sqlite3
from modules.database import Session, GameDetails

def sync_reviews_to_db(csv_path='data/reviews.csv'):
    # 1. Connect to DB and get the list of AppIDs we actually care about
    conn = sqlite3.connect('data/steam_catalog.db')
    existing_appids_df = pd.read_sql_query("SELECT appid FROM game_details", conn)
    
    print(f"Reading {csv_path}...")
    # 2. Load the CSV (Using low_memory=False to handle mixed types in large files)
    reviews_df = pd.read_csv(csv_path, low_memory=False)

    # 3. Perform a LEFT JOIN
    # This keeps all AppIDs from game_details and adds review columns where they match
    final_df = pd.merge(existing_appids_df, reviews_df, on='appid', how='left')

    print(f"Merging complete. Total rows to sync: {len(final_df)}")

    # 4. Save to a new table called 'game_reviews'
    # if_exists='replace' creates the table or overwrites it if you run it again
    final_df.to_sql('game_reviews', conn, if_exists='replace', index=False)
    
    conn.close()
    print("Successfully created 'game_reviews' table with matched data.")

if __name__ == "__main__":
    sync_reviews_to_db()
