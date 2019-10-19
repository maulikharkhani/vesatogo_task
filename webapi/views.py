from webapi.models import *
from django.db.models import Q
from django.db.models import Min, Count
from django.db.models import F

# rest framework
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT
from django.http import Http404
from rest_framework.views import APIView


# permission classes
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,

    )

# serializers
from webapi.serializers import ( 
        MoviesListSerializer,
        MoviesDetailsSerializer,

        WatchedListCreateSerializer,

        WatchedMoviesCreateSerializer,
    )

#timezone
from django.utils import timezone
import datetime


#-------------------------------- Fetch movies list start --------------------------------------------#

class MoviesListAPIView(APIView):
    """
    List all Movies.
    """
    permission_classes = [AllowAny]


    def get(self, request, format=None):
        instance_movies = Movies.objects.all()
        serializer = MoviesListSerializer(instance_movies, many=True)
        return Response(serializer.data)

#-------------------------------- Fetch movies list end  --------------------------------------------#


#-------------------------------- Fetch selected movies detail start --------------------------------------------#
class MoviesDetaisAPIView(APIView):
    """
    Details of selected movies .
    """
    permission_classes = [AllowAny]

    def get_object(self, pk):
        try:
            return Movies.objects.get(pk=pk)
        except Movies.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        instance_movies = self.get_object(pk)
        serializer = MoviesDetailsSerializer(instance_movies)
        return Response(serializer.data)

#-------------------------------- Fetch selected movies detail start --------------------------------------------#


#-------------------------------- Create watched movies start --------------------------------------------#
class WatchedListCreateAPIView(APIView):
    """
    Create a watch list.
    """
    permission_classes = [AllowAny]
    serializer_class = WatchedListCreateSerializer


    def post(self, request, format=None):
        serializer = WatchedListCreateSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

#-------------------------------- Create watched movies start --------------------------------------------#


#-------------------------------- Add movies in watched list start --------------------------------------------#
class WatchedMoviesCreateAPIView(APIView):
    """
    Add movies in watched list.
    """
    permission_classes = [AllowAny]
    serializer_class = WatchedMoviesCreateSerializer


    def post(self, request, format=None):
        serializer = WatchedMoviesCreateSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

#-------------------------------- Add movies in watched list start --------------------------------------------#




#-------------------------------- Fetch recommended movies detail start --------------------------------------------#
class RecommendedMoviesDetaisAPIView(APIView):
    """
    Details of selected movies .
    """
    permission_classes = [AllowAny]

    def get_object(self, pk):
        try:
            return WatchedList.objects.get(pk=pk)
        except WatchedList.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        instance_watched_list = self.get_object(pk)


        check_adult_watch = True if WatchedMovies.objects.filter(code=instance_watched_list, movies__adult=True).count() > 0  else False 
        instance_watched_movies_id = WatchedMovies.objects.filter(code=instance_watched_list).values_list('movies__id', flat=True).distinct()
        instance_watched_movies_gener_list = WatchedMovies.objects.filter(code=instance_watched_list, created__gte=(timezone.now().date() - datetime.timedelta(days=30))).values('movies__geners__name').annotate(count=Count('movies__geners__name')).values_list('movies__geners__name', flat=True).distinct().order_by('-count')
        if instance_watched_movies_gener_list.count() == 0:
            instance_watched_movies_gener_list = WatchedMovies.objects.filter(code=instance_watched_list, created__gte=(timezone.now().date() - datetime.timedelta(days=90))).values('movies__geners__name').annotate(count=Count('movies__geners__name')).values_list('movies__geners__name', flat=True).distinct().order_by('-count')

        if instance_watched_movies_gener_list.count() == 0:
            instance_watched_movies_gener_list = WatchedMovies.objects.filter(code=instance_watched_list, created__gte=(timezone.now().date() - datetime.timedelta(days=180))).values('movies__geners__name').annotate(count=Count('movies__geners__name')).values_list('movies__geners__name', flat=True).distinct().order_by('-count')

        instance_watched_movies_spoken_languages_list = WatchedMovies.objects.filter(code=instance_watched_list).values_list('movies__spoken_languages__name', flat=True).distinct()
        
        instance_recommendedMovies = Movies.objects.filter(adult=check_adult_watch)

        if instance_watched_movies_gener_list.count() != 0:
            instance_recommendedMovies = instance_recommendedMovies.filter(geners__name__in=instance_watched_movies_gener_list[:3])
        
        if instance_watched_movies_spoken_languages_list.count():
            nstance_recommendedMovies = instance_recommendedMovies.filter(spoken_languages__name__in=instance_watched_movies_spoken_languages_list[:2])

        print('instance_watched_movies_id', instance_watched_movies_id)
        instance_recommendedMovies = Movies.objects.filter(id__in=instance_recommendedMovies.values_list('id', flat=True).distinct()).exclude(id__in=instance_watched_movies_id).order_by('-popularity', '-vote_average', '-release_date')
        serializer = MoviesDetailsSerializer(instance_recommendedMovies, many=True)
        return Response(serializer.data)

#-------------------------------- Fetch recommended movies detail start --------------------------------------------#