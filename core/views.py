from django.contrib import messages
from django.shortcuts import render, redirect
from dotenv import load_dotenv, find_dotenv
import os, requests, http, socket
from django.http import JsonResponse, HttpResponse
from datetime import date
from .models import Comment, Watchlist
from django.urls import resolve
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

load_dotenv(find_dotenv())

TMDB_API_KEY = os.environ.get('TMDB_API_KEY')
# Create your views here.
def pagination(page, api_call):
    data = f"{api_call}&page={page}"
    return data.json()

def home(request):
    # latest_movie = requests.get(f"https://api.themoviedb.org/3/movie/latest?api_key={TMDB_API_KEY}&language=en-US").json()
    latest_movies = requests.get(f"https://api.themoviedb.org/3/discover/movie?api_key={TMDB_API_KEY}&include_video=false&primary_release_date.lte={date.today()}").json()
    # latest_tv_show = requests.get(f"https://api.themoviedb.org/3/tv/latest?api_key={TMDB_API_KEY}&language=en-US").json()
    latest_tv_shows = requests.get(f"https://api.themoviedb.org/3/discover/tv?api_key={TMDB_API_KEY}&include_video=false&primary_release_date.lte={date.today()}").json()
    popular_movies = requests.get(f"https://api.themoviedb.org/3/movie/popular?api_key={TMDB_API_KEY}&language=en-US&page=1").json()
    popular_tv_shows = requests.get(f"https://api.themoviedb.org/3/tv/popular?api_key={TMDB_API_KEY}&language=en-US&page=1").json()
    animation_movies = requests.get(f"https://api.themoviedb.org/3/discover/movie?api_key={TMDB_API_KEY}&language=en-US&sort_by=popularity.desc&page=1&with_genres=16").json()
    upcoming_movies = requests.get(f"https://api.themoviedb.org/3/movie/upcoming?api_key={TMDB_API_KEY}&language=en-US&page=1").json()
    upcoming_tv_shows = requests.get(f"https://api.themoviedb.org/3/tv/upcoming?api_key={TMDB_API_KEY}&language=en-US&page=1").json()
    trending_movies = requests.get(f"https://api.themoviedb.org/3/trending/movie/week?api_key={TMDB_API_KEY}").json()
    trending_tv_shows = requests.get(f"https://api.themoviedb.org/3/trending/tv/week?api_key={TMDB_API_KEY}").json()
    return render(request, 'core/index.html', {
        'latest_movies': latest_movies,
        'latest_tv_shows': latest_tv_shows,
        'popular_movies': popular_movies,
        'popular_tv_shows': popular_tv_shows,
        'animation_movies': animation_movies,
        'upcoming_movies': upcoming_movies,
        'upcoming_tv_shows': upcoming_tv_shows,
        'trending_movies': trending_movies,
        'trending_tv_shows': trending_tv_shows,
        })

def movies_search(request, q=None):
    query = request.GET.get('q')
    page = request.POST.get('page')

    if query:
        movies_data = requests.get(f"https://api.themoviedb.org/3/search/{request.GET.get('type')}?api_key={TMDB_API_KEY}&language=en-US&include_adult=false&query={query}").json()
        if page:
            movies_data = requests.get(f"https://api.themoviedb.org/3/search/{request.GET.get('type')}?api_key={TMDB_API_KEY}&language=en-US&page={page}&include_adult=false&query={query}").json()
    else:
        return redirect('404')

    return render(request, 'core/search_result.html', {'data': movies_data, 'total_pages': movies_data['total_pages'], 'query': query, 'type': request.GET.get('type'), 'page': request.POST.get('page')})

def movie_details(request, movie_id):
    try:
        watchlist_instance = Watchlist.objects.get(movie_id=movie_id, user=request.user)
    except:
        watchlist_instance = None
    data = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&language=en-US")
    try:
        movie_key = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key={TMDB_API_KEY}").json()['results'][0]['key']
    except:
        movie_key = None
    similar_movies = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}/similar?api_key={TMDB_API_KEY}&language=en-US&page=1").json()
    comments = Comment.objects.filter(movie_id=movie_id)
    return render(request, 'core/movie_details.html', {'data': data.json(), 'movie_key': movie_key, 'similar_movies': similar_movies, 'comments': comments, 'watchlist_instance': watchlist_instance})


def tv_details(request, tv_id):
    context = {}
    seasons = {}
    try:
        watchlist_instance = Watchlist.objects.get(movie_id=tv_id, user=request.user)
    except:
        watchlist_instance = None
    data = requests.get(f"https://api.themoviedb.org/3/tv/{tv_id}?api_key={TMDB_API_KEY}&language=en-US").json()
    similar_tv_shows = requests.get(f"https://api.themoviedb.org/3/tv/{tv_id}/similar?api_key={TMDB_API_KEY}&language=en-US&page=1").json()
    for season in data['seasons']:
        season = requests.get(f"https://api.themoviedb.org/3/tv/{tv_id}/season/{season['season_number']}?api_key={TMDB_API_KEY}&language=en-US").json()
        seasons[f"{season['season_number']}"] = season
    try:
        context['tv_movie'] = requests.get(f"https://api.themoviedb.org/3/tv/{tv_id}/videos?api_key={TMDB_API_KEY}").json()['results'][0]
    except:
        context['tv_movie'] = None
    context['comments'] = Comment.objects.filter(movie_id=tv_id)
    context['similar_tv_shows'] = similar_tv_shows
    context['seasons'] = seasons
    context['data'] = data
    context['watchlist_instance'] = watchlist_instance
    return render(request, 'core/tv_details.html', context)

# def get_latest_movies(request):
#     latest_movies = requests.get(f"https://api.themoviedb.org/3/movie/latest?api_key={TMDB_API_KEY}&language=en-US")
#     return render(request, 'core/index.html', {'latest_movies': latest_movies})

# def get_latest_tv_shows(request):
#     latest_tv_shows = requests.get(f"https://api.themoviedb.org/3/tv/latest?api_key={TMDB_API_KEY}&language=en-US")
#     return render(request, 'core/index.html', {'latest_tv_shows': latest_tv_shows})

def get_popular_movies(request):
    page = request.POST.get('page')
    if page:
        popular_movies = requests.get(f"https://api.themoviedb.org/3/movie/popular?api_key={TMDB_API_KEY}&language=en-US&page={page}").json()
    else:
        popular_movies = requests.get(f"https://api.themoviedb.org/3/movie/popular?api_key={TMDB_API_KEY}&language=en-US").json()
    return render(request, 'core/popular_movies.html', {'popular_movies': popular_movies, 'page': page, 'total_pages': popular_movies['total_pages']})

def get_popular_tv_shows(request):
    page = request.POST.get('page')
    if page:
        popular_tv_shows = requests.get(f"https://api.themoviedb.org/3/tv/popular?api_key={TMDB_API_KEY}&language=en-US&page={page}").json()
    else:
        popular_tv_shows = requests.get(f"https://api.themoviedb.org/3/tv/popular?api_key={TMDB_API_KEY}&language=en-US").json()
    return render(request, 'core/popular_tv_shows.html', {'popular_tv_shows': popular_tv_shows, 'page': page, 'total_pages': popular_tv_shows['total_pages']})

def get_animation_movies(request):
    page = request.POST.get('page')
    if page:
        animation_movies = requests.get(f"https://api.themoviedb.org/3/discover/movie?api_key={TMDB_API_KEY}&language=en-US&sort_by=popularity.desc&&page={page}&with_genres=16").json()
    else:
        animation_movies = requests.get(f"https://api.themoviedb.org/3/discover/movie?api_key={TMDB_API_KEY}&language=en-US&sort_by=popularity.desc&with_genres=16").json()
    return render(request, 'core/animations.html', {'animation_movies': animation_movies, 'page': page, 'total_pages': animation_movies['total_pages']})

def get_upcoming_movies(request):
    upcoming_movies = requests.get(f"https://api.themoviedb.org/3/movie/upcoming?api_key={TMDB_API_KEY}&language=en-US&page=1")
    return render(request, 'core/index.html', {'upcoming_movies': upcoming_movies})

def get_upcoming_tv_shows(request):
    upcoming_tv_shows = requests.get(f"https://api.themoviedb.org/3/tv/upcoming?api_key={TMDB_API_KEY}&language=en-US&page=1")
    return render(request, 'core/index.html', {'upcoming_tv_shows': upcoming_tv_shows})

def movies_catalog(request):
    genre = request.GET.get('genre') or 28
    page = request.POST.get('page') or 1
    
    if genre:
        movies_catalog = requests.get(f"https://api.themoviedb.org/3/discover/movie?api_key={TMDB_API_KEY}&language=en-US&sort_by=popularity.desc&page={page}&with_genres={genre}").json()
    else:
        movies_catalog = requests.get(f"https://api.themoviedb.org/3/movie/top_rated?api_key={TMDB_API_KEY}&include_video=false&language=en-US&page={page}").json()
    
    return render(request, 'core/movies_catalog.html', {'movies_catalog': movies_catalog, 'page': page, 'total_pages': movies_catalog['total_pages'], 'genre': genre})

def tv_shows_catalog(request):
    genre = request.GET.get('genre') or 10759
    page = request.POST.get('page') or 1
    
    tv_shows_catalog = requests.get(f"https://api.themoviedb.org/3/discover/tv?api_key={TMDB_API_KEY}&language=en-US&sort_by=popularity.desc&page={page}&with_genres={genre}").json()
    
    return render(request, 'core/tv_shows_catalog.html', {'tv_shows_catalog': tv_shows_catalog, 'page': page, 'total_pages': tv_shows_catalog['total_pages'], 'genre': genre})
    
def movie_make_comment(request, movie_id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            user = request.user
            comment = request.POST.get('comment')
            comment = Comment.objects.create(user=user, movie_id=movie_id, comment=comment)
            return redirect('movie_details', movie_id=movie_id)
    else:
        return HttpResponse('You must be authenticated to add comments.')
    comments = Comment.objects.filter(movie_id=movie_id)
    return render(request, 'core/movie_details.html', {'comments': comments})

def tv_show_make_comment(request, tv_id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            user = request.user
            comment = request.POST.get('comment')
            comment = Comment.objects.create(user=user, movie_id=tv_id, comment=comment)
            return redirect('tv_details', tv_id=tv_id)
    else:
        return HttpResponse('You must be authenticated to add comments.')
    comments = Comment.objects.filter(movie_id=tv_id)
    return render(request, 'core/tv_details.html', {'comments': comments})

def add_to_watchlist_movie(request, movie_id):
    context = {}
    user = request.user
    if user.is_authenticated:
        if not Watchlist.objects.filter(user=user, movie_id=movie_id, movie_type='movie').exists():
            instance = Watchlist.objects.create(user=user, movie_id=movie_id, movie_type='movie')
            context['instance'] = instance
            # bool = True
            return redirect('watchlist')
        else:
            return HttpResponse('This movie is already in your Watchlist')
    else:
        return redirect('accounts:sign_in')
        # return HttpResponse('You must be authenticated before you can add movies to your watchlist')
    return render(request, 'movie_details.html', context)
    # return JsonResponse(bool, safe=False)

def add_to_watchlist_tv(request, tv_id):
    context = {}
    user = request.user
    if not user.is_authenticated:
        return redirect('accounts:sign_in')

    if not Watchlist.objects.filter(user=user, movie_id=tv_id).exists():
        instance = Watchlist.objects.create(user=user, movie_id=tv_id, movie_type='tv')
        context['instance'] = instance
        return redirect('watchlist')
    else:
        return HttpResponse('This Tv Show is already in your Watchlist')
    return render(request, 'tv_details.html', context)

def remove_from_watchlist(request, movie_id):
    user = request.user
    Watchlist.objects.get(user=user, movie_id=movie_id).delete()
    return redirect('watchlist')

def watchlist(request):
    watch_type = request.GET.get('watch_type')
    watchlist_movies = {}
    watchlist = Watchlist.objects.filter(user=request.user)
    for movie in watchlist:
        if movie.movie_type == watch_type:
            movie_call = requests.get(f"https://api.themoviedb.org/3/{watch_type}/{movie.movie_id}?api_key={TMDB_API_KEY}&language=en-US").json()
            watchlist_movies[f'{movie.movie_id}'] = movie_call
    return render(request, 'core/watchlist.html', {'watchlist_movies': watchlist_movies, 'watch_type': watch_type})

def movie_gen(movie_id):
    data = requests.get(f"")
def grid_catalog(request):
    return render(request, 'catalog1.html')

def list_catalog(request):
    return render(request, 'catalog2.html')

def pricing_plan(request):
    return render(request, 'pricing.html')

def faq(request):
    return render(request, 'faq.html')

def about(request):
    return render(request, 'about.html')

def error_404(request):
    return render(request, '404.html')
