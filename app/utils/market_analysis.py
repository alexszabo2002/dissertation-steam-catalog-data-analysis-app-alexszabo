import pandas as pd
from wordcloud import WordCloud, STOPWORDS
import plotly.express as px
import matplotlib.pyplot as plt
import sqlite3
from collections import Counter
import re

DB_PATH = "data/steam_catalog.db"

def get_market_overview_data():
    conn = sqlite3.connect(DB_PATH)
    # We only need name and genres for these two charts
    df = pd.read_sql_query("SELECT name, genres, developers FROM game_details", conn)
    conn.close()
    return df

def get_top_developers(df, limit=10):
    # Defining the developers we want to exclude from the count (common words that aren't really developers)
    exclude_list = ["Inc.", "Ltd.", "LTD.", "LLC"]

    # Steam developers are often comma-separated: "Dev A, Dev B"
    # We split them and 'explode' to count each individually
    devs_expanded = df['developers'].str.split(', ').explode()
    
    # Clean the strings (remove extra whitespace)
    devs_expanded = devs_expanded.str.strip()
    
    # Remove the excluded names
    # We use ~ (not) and .isin() to filter them out
    filtered_devs = devs_expanded[~devs_expanded.isin(exclude_list)]
    
    # Count and return the top results
    dev_counts = filtered_devs.value_counts().reset_index()
    dev_counts.columns = ['Developer', 'Games_Count']
    
    return dev_counts.head(limit)

def generate_wordcloud(titles_series):
    # Combine all titles into one long string
    text = " ".join(titles_series.dropna().astype(str))
    
    # Set stopwords
    custom_stopwords = set(STOPWORDS)
    custom_stopwords.update({"the", "and", "or", "i", "ii", "iii", "iv", "v", "x", "s", "one", "new", "edition", "game", "final", "zero", "hd", "fantasy"})
    
    # First, process the text to get the frequencies so we can use them for scaling colors
    # We instantiate a temporary wordcloud object just to access process_text correctly
    temp_wc = WordCloud(stopwords=custom_stopwords, collocations=False)
    word_counts_dict = temp_wc.process_text(text)
    
    # Sort them by frequency and take top 50
    sorted_counts = sorted(word_counts_dict.items(), key=lambda x: x[1], reverse=True)[:50]
    
    # Convert back to a dictionary for the wordcloud generator
    top_50_dict = dict(sorted_counts)
    
    # Create a custom color function based on frequency
    # We fetch the chosen colormap from matplotlib
    cmap = plt.get_cmap('Blues') 
    
    def frequency_color_func(word, font_size, position, orientation, random_state=None, **kwargs):
        # Normalize the frequency of the word between 0.0 and 1.0 based on the top dict
        max_freq = max(top_50_dict.values()) if top_50_dict else 1
        current_freq = top_50_dict.get(word, 1)
        
        # Scale it so the least frequent words aren't completely invisible (min alpha/intensity of 0.2)
        normalized_freq = 0.2 + (current_freq / max_freq) * 0.8
        
        # Get the RGBA color from the matplotlib colormap
        rgba = cmap(normalized_freq)
        
        # Convert to a format WordCloud understands: "rgb(r, g, b)"
        return f"rgb({int(rgba[0]*255)}, {int(rgba[1]*255)}, {int(rgba[2]*255)})"

    # 3. Create the final wordcloud using generate_from_frequencies
    wc = WordCloud(
        width=800, 
        height=400, 
        background_color='rgba(255,255,255,0)', # Transparent background
        max_words=50,
        stopwords=custom_stopwords,
        collocations=False
    ).generate_from_frequencies(top_50_dict) # Generates strictly from the top 50
    
    # Apply the custom color function
    wc.recolor(color_func=frequency_color_func)
    
    return wc, sorted_counts

def get_genre_counts(df):
    # Split the comma-separated genres and explode them into individual rows
    genres_expanded = df['genres'].str.split(', ').explode()
    counts = genres_expanded.value_counts().reset_index()
    counts.columns = ['Genre', 'Count']
    return counts
