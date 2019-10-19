from webapi.models import *

from rest_framework.serializers import (
    CharField,
    ModelSerializer,
    ValidationError,
    )

import datetime

#------------------------- Geners details serializer start ----------------------------#
class GenersSerializer(ModelSerializer):
    class Meta:
        model = Geners
        fields = '__all__' 

#------------------------- Geners details serializer end ----------------------------#


#------------------------- ProductionCompany details serializer start ----------------------------#
class ProductionCompanySerializer(ModelSerializer):
    class Meta:
        model = ProductionCompany
        fields = fields = '__all__' 

#------------------------- ProductionCompany details serializer end ----------------------------#


#------------------------- ProductionCountries details serializer start ----------------------------#
class ProductionCountriesSerializer(ModelSerializer):
    class Meta:
        model = ProductionCountries
        fields = '__all__' 

#------------------------- ProductionCountries details serializer end ----------------------------#


#------------------------- SpokenLanguages details serializer start ----------------------------#
class SpokenLanguagesSerializer(ModelSerializer):
    class Meta:
        model = SpokenLanguages
        fields = '__all__' 

#------------------------- SpokenLanguages details serializer end ----------------------------#


#------------------------- Movies details serializer start ----------------------------#
class MoviesListSerializer(ModelSerializer):
    class Meta:
        model = Movies
        fields = ['id', 'original_title', 'original_language', 'popularity', 'overview', 'release_date', 'title', 'vote_average', 'vote_count']


class MoviesDetailsSerializer(ModelSerializer):
    geners = GenersSerializer(many=True)
    production_company = ProductionCompanySerializer(many=True)
    production_countries = ProductionCountriesSerializer(many=True)
    spoken_languages = SpokenLanguagesSerializer(many=True)
    class Meta:
        model = Movies
        fields = '__all__'


#------------------------- Movies details serializer end ----------------------------#


#------------------------- WatchedMovies details & create serializer start ----------------------------#
class WatchedMoviesCreateSerializer(ModelSerializer):
    class Meta:
        model = WatchedMovies
        fields = '__all__' 


    def validate(self, data):
        """
        Check that the start is before the stop.
        """
        if data['movies'].release_date > datetime.datetime.now().date():
            raise ValidationError("Movie not released you can't add in watched list..!")
        return data


#------------------------- WatchedMovies details & create serializer end ----------------------------#


#------------------------- WatchedList details & create serializer start ----------------------------#
class WatchedListCreateSerializer(ModelSerializer):
    watch_list = WatchedMoviesCreateSerializer(many=True, read_only=True)
    class Meta:
        model = WatchedList
        fields = '__all__' 

#------------------------- WatchedList details & create serializer end ----------------------------#


