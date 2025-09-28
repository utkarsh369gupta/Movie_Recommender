import pickle
import requests
import random
import os
from dotenv import load_dotenv


# Load environment variables for TMDB API key
# load_dotenv()
api_key = "a5be7b745ddc7b07cae03e52d1a5e1ce"


# Load Data
final_data = pickle.load(open('final_df.pkl', 'rb'))
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
similarities = pickle.load(open('similarities.pkl', 'rb'))


# Fallback images for poster not found or errors
imgnotfound = [
    'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRYm8ZC1SBgsIwqxTTIRc5Z7xIWJuTT5qfTew&s',
    "https://m.media-amazon.com/images/I/61s8vyZLSzL._UF894,1000_QL80_.jpg",
    "https://mir-s3-cdn-cf.behance.net/project_modules/disp_webp/fb3ef66312333.5691dd2253378.jpg",
    "https://mir-s3-cdn-cf.behance.net/project_modules/disp_webp/fac16491945367.5e3ebd0d19991.jpg",
    "https://ih1.redbubble.net/image.25042430.9585/flat,750x,075,f-pad,750x1000,f8f8f8.jpg",
    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQvNWtK8GwpqfOI41hhtcG66dbTrwmKXAa4Q7s3syW5HGkC1TEMUgrwzaKQGAFt5h6oY3c&usqp=CAU",
    "https://img.freepik.com/free-vector/error-404-concept-landing-page_52683-10996.jpg?semt=ais_hybrid&w=740&q=80"
]


########## Helper Functions ##########

def fetch_movie_id(movie_name):
    try:
        url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={movie_name}"
        response = requests.get(url).json()
        results = response.get('results')
        if results and len(results) > 0:
            return results[0]['id']
        else:
            return None
    except Exception as e:
        print(movie_name)
        print("Error fetching movie ID:", e)
        return None


def fetch_poster(movie_id):
    try:
        if not movie_id:
            return imgnotfound[random.randint(0, len(imgnotfound) - 1)]
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
        response = requests.get(url).json()
        poster_path = response.get('poster_path')
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500{poster_path}"
        else:
            return imgnotfound[random.randint(0, len(imgnotfound) - 1)]
    except Exception as e:
        print("Error fetching poster:", e)
        return imgnotfound[random.randint(0, len(imgnotfound) - 1)]


def fetch_poster_by_name(movie_name):
    tmdb_movie_id = fetch_movie_id(movie_name)
    return fetch_poster(tmdb_movie_id)


########## Recommendation Logic ##########

def recommend(movie):
    if movie not in final_data['title'].values:
        return [], []

    mov_index = final_data[final_data['title'] == movie].index[0]
    distances = similarities[mov_index]
    mov_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:7]

    recommended_movies = []
    recommended_posters = []

    for i in mov_list:
        title = final_data.iloc[i[0]].title
        recommended_movies.append(title)
        poster = fetch_poster_by_name(title)
        recommended_posters.append(poster)
    return recommended_movies, recommended_posters
