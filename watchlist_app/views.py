from django.shortcuts import render
from watchlist_app.models import Movie
from django.http import JsonResponse

# Create your views here.
def movie_list(request):
    movie = Movie.objects.all()
    data = {'Movie': list(movie.values())}
    return JsonResponse(data)

def movie_details(request, pk):
    movie = Movie.objects.get(pk=pk)
    data = {
        'name': movie.name,
        'description': movie.description,
        'active': movie.active
    }
    return JsonResponse(data)
    