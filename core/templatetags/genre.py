import requests, os
from django import template
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
TMDB_API_KEY = os.environ.get('TMDB_API_KEY')
register = template.Library()
# @register.filter
# def movie_genre_extractor(movie_id):
#     tv = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}").json()
    
#     genres = tv['genres']
#     genres_list = [g['name'] for g in genres]

#     return genres_list

# @register.filter
# def tv_genre_extractor(tv_id):
#     tv = requests.get(f"https://api.themoviedb.org/3/tv/{tv_id}?api_key={TMDB_API_KEY}").json()
    
#     genres = tv['genres']
#     genres_list = [g['name'] for g in genres]

#     return genres_list

@register.filter
def movie_genre_gen(genre_id):
    genres = requests.get(f"https://api.themoviedb.org/3/genre/movie/list?api_key={TMDB_API_KEY}").json()
    for g in genres['genres']:
        if int(g['id']) == int(genre_id):
            return g['name']

@register.filter
def tv_genre_gen(genre_id):
    genres = requests.get(f"https://api.themoviedb.org/3/genre/tv/list?api_key={TMDB_API_KEY}").json()
    for g in genres['genres']:
        if int(g['id']) == int(genre_id):
            return g['name']