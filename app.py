import streamlit as st
from utils import recommend, final_data

# Set wide layout
st.set_page_config(layout="wide")

# Custom CSS: padding and centering header (not widgets)
st.markdown(
    """
    <style>
        .block-container { padding-left: 18rem; padding-right: 18rem; }
        h1 { text-align: center; }
    </style>
    """,
    unsafe_allow_html=True
)

# Title
st.markdown("<h1>🎬 Movie Recommender System</h1>", unsafe_allow_html=True)

# Center selectbox and button in 3 column layout (middle column wider)
col1, col2, col3 = st.columns([1, 2, 1])  # center col is wider

with col2:
    # Centered label above selectbox
    st.markdown(
        "<div style='text-align: center; font-weight: bold; font-size: 20px; margin-bottom: 0px;'>Select a movie you have watched:</div>",
        unsafe_allow_html=True
    )
    # Add a placeholder "Select movie" option
    movie_options = ['Select movie'] + list(final_data['title'].values)

    option = st.selectbox(
        '',  # hide default label
        movie_options,
        index=0,  # default selection is placeholder
        key="movie_select"
    )

    # Center the Recommend button inside col2 using nested columns
    inner_col1, inner_col2, inner_col3 = st.columns([2, 2, 2])
    with inner_col2:
        recommend_btn = st.button('Recommend')
    
    st.markdown("<hr>", unsafe_allow_html=True)

# Recommendations display as cards (3 per row)
if recommend_btn:
    if option == 'Select movie':
        st.warning("Please select a movie to get recommendations.")
    else:
        recommendations, posters = recommend(option)
        movies_per_row = 3
        for row_start in range(0, len(recommendations), movies_per_row):
            titles_row = recommendations[row_start:row_start+movies_per_row]
            posters_row = posters[row_start:row_start+movies_per_row]
            cols = st.columns(len(titles_row))
            print(posters_row)
            for idx, col in enumerate(cols):
                with col:
                    # Encode the movie title for URL
                    import urllib.parse
                    movie_title_encoded = urllib.parse.quote(titles_row[idx])

                    st.markdown(
                        f"""
                        <a href="https://www.google.com/search?q={movie_title_encoded}" target="_blank" style="text-decoration: none; color: inherit;">
                            <div style="
                                border: 1px solid #ddd;
                                border-radius: 12px;
                                padding: 10px;
                                text-align: center;
                                box-shadow: 2px 2px 8px rgba(0,0,0,0.15);
                                background-color: #0a0606;
                                margin: 10px;
                                cursor: pointer;
                            ">
                                <div style="font-weight: 600; margin-bottom: 8px; font-size: 20px;">
                                    {titles_row[idx]}
                                </div>
                                <img src="{posters_row[idx]}" style="width: 180px; height: 270px; border-radius: 8px; object-fit: cover;">
                            </div>
                        </a>
                        """,
                        unsafe_allow_html=True
                    )

