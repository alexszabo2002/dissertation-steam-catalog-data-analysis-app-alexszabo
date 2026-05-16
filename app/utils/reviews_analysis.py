import pandas as pd
import sqlite3

DB_PATH = "data/steam_catalog.db"

def get_sentiment_data():
    conn = sqlite3.connect(DB_PATH)
    query = """
    SELECT 
        d.name, d.final_price, d.genres,
        r.steamspy_positive_reviews, r.steamspy_negative_reviews, r.steamspy_total_reviews, r.review_score_description
    FROM game_details d
    INNER JOIN game_reviews r ON d.appid = r.appid
    """
    df = pd.read_sql_query(query, conn)
    conn.close()

    # Clean NULLs from critical columns
    # We drop rows that lack the basic data needed for a ratio
    df = df.dropna(subset=['steamspy_positive_reviews', 'steamspy_negative_reviews', 'final_price'])

    # Advanced Price Parser
    def parse_price(val):
        if not val or "FREE" in str(val).upper(): 
            return 0.0
        try:
            # Splits "19.99 EUR" and takes "19.99"
            return float(str(val).split(' ')[0])
        except (ValueError, IndexError):
            return None # Handle rows that are totally malformed
            
    df['price_numeric'] = df['final_price'].apply(parse_price)
    
    # Filter out games with 0 reviews to avoid division errors
    df = df[df['steamspy_total_reviews'] > 0].copy()
    df['positive_ratio'] = (df['steamspy_positive_reviews'] / df['steamspy_total_reviews']) * 100
    
    # Drop any rows where price parsing resulted in None
    df = df.dropna(subset=['price_numeric'])
    
    return df
