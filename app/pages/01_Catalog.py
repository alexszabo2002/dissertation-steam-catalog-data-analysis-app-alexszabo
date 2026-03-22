import streamlit as st
from utils.database_io import get_all_game_names, get_game_by_id
from utils.ui_components import render_steam_card

st.title("🔍 Search the Catalog")

# Load names for the searchbar
names_df = get_all_game_names()

selected_game_name = st.selectbox(
    "Search for a game name:",
    options=names_df['name'].tolist(),
    index=None,
    placeholder="Type game name here..."
)

if selected_game_name:
    # Find the appid for the selected name
    appid = names_df[names_df['name'] == selected_game_name]['appid'].values[0]
    # Fetch full data
    game_data = get_game_by_id(appid)
    
    if game_data is not None:
        # Check if the AppID has changed. 
        # If it has, immediately set the state to the first screenshot of the NEW game.
        if "current_appid" not in st.session_state or st.session_state.current_appid != appid:
            st.session_state.selected_ss = game_data['screenshot1']
            st.session_state.current_appid = appid
        
        # Now render the card
        render_steam_card(game_data)
