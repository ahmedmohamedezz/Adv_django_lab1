from .models import Movie, Link, Tag, Rate
from django.shortcuts import render
from django.db.models import Q, F
from django.http import JsonResponse, HttpResponse
import cProfile
import io
import pstats
from django.db import connection


# tested by debug_toolbar or inside silk
def test_n_plus_1(request):
    # slow
    # movies = Movie.objects.all()

    # fast
    movies = Movie.objects.prefetch_related("tags").all()

    context = {
        "movies": movies,
    }

    return render(request, "index.html", context)


def test_qf(request):
    # movies are labeled "Movie 1" ==> "Movie 100"
    # query: select movies start with `Movie 2` or `Movie 4` and not `Movie 41`
    # all case-insensitive

    # 1. test query
    movies = Movie.objects.filter(
        Q(title__istartswith="movie 2")
        | (Q(title__istartswith="movie 4") & ~Q(title__icontains="movie 41"))
    )

    # 2. dynamic filter
    filters = []

    startswith = "movie 2"
    does_not_startswith = "movie 100"

    if startswith:
        filters.append(Q(title__istartswith=startswith))

    if does_not_startswith:
        filters.append(~Q(title__istartswith=does_not_startswith))

    if filters:
        movies = Movie.objects.filter(*filters)

    context = {
        "movies": movies,
    }

    # -------------------------------
    # update using F
    Movie.objects.filter(title__startswith="Movie 1").update(title=F("genre"))

    movies = Movie.objects.all()
    context["movies"] = movies

    # note that template make extra queries as it's used by all views
    return render(request, "index.html", context)


def test_only_defer(request):
    # movies = Movie.objects.only("genre")
    # for m in movies:
    #     print(m.genre)

    movies = Movie.objects.defer("genre")
    for m in movies:
        print(m.title)


def test_values_values_list(request):
    # select key-value pairs (dicts)
    # movies = Movie.objects.values("genre")

    # select the values without keys (tuples)
    movies = Movie.objects.values_list("genre")

    context = {"movies": movies}

    # note that template make extra queries as it's used by all views
    return render(request, "index.html", context)


def test_db_index_with_c_profile(request):
    profiler = cProfile.Profile()
    profiler.enable()
    
    # indexed column
    movie_title = Movie.objects.filter(title__istartswith="a")[0]
    
    # not indexed column
    tag_name = Movie.objects.filter(title__istartswith="a")[0]
    
    profiler.disable()
    
    s = io.StringIO()
    ps = pstats.Stats(profiler, stream=s)
    ps.strip_dirs()
    ps.sort_stats("cumtime")
    ps.print_stats()
    
    result = s.getvalue()

    return JsonResponse({"result": result})
    


def test_connection_age(request):
    movies = list(Movie.objects.all())
    id_1 = id(connection.connection)

    movies = Movie.objects.all()
    movies = movies[:10]
    id_2 = id(connection.connection)

    return JsonResponse({"same connection": id_1 == id_2})
