import pandas as pd
import sqlite3
import itertools
from collections import Counter

DB_PATH = "data/steam_catalog.db"

def get_matching_data(column_name):
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(f"SELECT appid, {column_name} FROM game_details", conn)
    conn.close()
    
    # Split strings into lists
    df[column_name] = df[column_name].str.split(',').apply(lambda x: [i.strip() for i in x] if x else [])
    
    # Generate all pairs of categories/genres found in the same game
    pair_counts = Counter()
    individual_counts = Counter()
    
    for row in df[column_name]:
        for item in row:
            individual_counts[item] += 1
        for pair in itertools.combinations(sorted(row), 2):
            pair_counts[pair] += 1
            
    # Transform to DataFrame for plotting
    data = []
    for (item_a, item_b), both_count in pair_counts.items():
        # X-axis: Popularity (Sum of games having either A or B)
        # Y-axis: Synergy (Games having BOTH)
        either_count = individual_counts[item_a] + individual_counts[item_b] - both_count
        data.append({
            'Pair': f"{item_a} + {item_b}",
            'Item A': item_a,
            'Item B': item_b,
            'Total_Games_Either': either_count,
            'Games_With_Both': both_count,
            'Synergy_Score': (both_count / either_count) * 100
        })
        
    return pd.DataFrame(data)
