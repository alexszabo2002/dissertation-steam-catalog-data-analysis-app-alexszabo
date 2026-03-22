import streamlit as st

def render_steam_card(game):
    # Apply background to the ENTIRE page, not just the container
    st.markdown(f"""
        <style>
        [data-testid="stAppViewContainer"] {{
            background-image: linear-gradient(rgba(23, 26, 33, 0.4), rgba(23, 26, 33, 0.4)), 
                              url("{game['background_image']}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        
        /* Ensure text stays readable against a clearer background */
        [data-testid="stAppViewContainer"] p, [data-testid="stAppViewContainer"] h1, [data-testid="stAppViewContainer"] h2, [data-testid="stAppViewContainer"] h3 {{
            color: white !important;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.8);
        }}

        .steam-card-box {{
            background: rgba(23, 26, 33, 0.7); /* Darker box for content contrast */
            border-radius: 10px;
            padding: 25px;
            border: 1px solid rgba(102, 192, 244, 0.3);
        }}
        
        /* Thumbnails Styling */
        .thumb-nav img {{
            border: 2px solid #1b2838;
            border-radius: 4px;
            cursor: pointer;
            transition: 0.2s;
        }}
        .thumb-nav img:hover {{
            border: 2px solid #66c0f4;
        }}
        .tag-container {{
            padding: 10px 0;
            line-height: 2.2; /* Space between rows */
        }}
        .category-tag {{
            display: inline-block;
            background: #4c6b22; /* Greenish for categories */
            color: white;
            padding: 2px 12px;
            border-radius: 15px;
            margin-right: 8px;
            margin-bottom: 8px;
            font-size: 0.85rem;
            border: 1px solid rgba(255,255,255,0.2);
        }}
        .genre-tag {{
            display: inline-block;
            background: #2a475e; /* Classic Steam Blue for genres */
            color: #66c0f4;
            padding: 2px 12px;
            border-radius: 15px;
            margin-right: 8px;
            margin-bottom: 8px;
            font-size: 0.85rem;
            border: 1px solid #66c0f4;
        }}
        .section-label {{
            color: #8f98a0;
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 5px;
        }}
        </style>
    """, unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="steam-container">', unsafe_allow_html=True)
        
        # TOP CONTAINER
        top_left, top_right = st.columns([1, 2])

        with top_left:
            st.image(game['header_image'], use_container_width=True)
            st.write(game['short_description'])
            st.caption(f"**Released:** {game['release_date']}")
            st.caption(f"**Developer:** {game['developers']}")
            st.caption(f"**Publisher:** {game['publishers']}")
            
            # Price logic

            initial = game['initial_price']
            final = game['final_price']

            # State 1: Data is NULL/None -> Display nothing
            if initial is None or final is None:
                st.write("")

            # State 2: Game is FREE
            elif "FREE" in final.upper():
                c1, c2 = st.columns(2)
                c1.markdown(f":green[**FREE**]")
                c2.markdown("")

            # State 3: Standard Paid Game
            else:
                c1, c2 = st.columns(2)
                c1.markdown(f":red[~~{initial}~~]")
                c2.markdown(f":green[**{final}**]")

        with top_right:
            # 1. Big Main Image
            st.image(st.session_state.selected_ss, use_container_width=True)
            
            # 2. Thumbnail Navigation Row
            ss_list = [game['screenshot1'], game['screenshot2'], game['screenshot3']]
            ss_list = [s for s in ss_list if s] # Filter out missing images
            
            # Create a row of columns for thumbnails
            cols = st.columns(len(ss_list))
            
            for idx, url in enumerate(ss_list):
                with cols[idx]:
                    # Display the small version of the image
                    st.image(url, use_container_width=True)
                    
                    # Invisible or small button to "Select" this image
                    if st.button("Select", key=f"sel_{idx}", use_container_width=True):
                        st.session_state.selected_ss = url
                        st.rerun()

        st.divider()

        # BOTTOM CONTAINER
        # Row 1: Categories
        st.markdown('<p class="section-label">Categories</p>', unsafe_allow_html=True)
        if game['categories']:
            cats = game['categories'].split(',')
            cat_html = "".join([f'<span class="category-tag">{c.strip()}</span>' for c in cats])
            st.markdown(f'<div class="tag-container">{cat_html}</div>', unsafe_allow_html=True)
        else:
            st.caption("No categories listed.")

        # Row 2: Genres
        st.markdown('<p class="section-label">Genres</p>', unsafe_allow_html=True)
        if game['genres']:
            gens = game['genres'].split(',')
            gen_html = "".join([f'<span class="genre-tag">{g.strip()}</span>' for g in gens])
            st.markdown(f'<div class="tag-container">{gen_html}</div>', unsafe_allow_html=True)
        else:
            st.caption("No genres listed.")

        # Recommendations Footer
        st.markdown(f"""
            <div style="margin-top: 20px; padding: 10px; background: rgba(0,0,0,0.3); border-radius: 5px;">
                <span style="color: #66c0f4; font-size: 1.2rem;">👍</span> 
                <span style="font-weight: bold;">{game['recommendations']:,}</span> 
                <span style="color: #8f98a0;"> user recommendations</span>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
