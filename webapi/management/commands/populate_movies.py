from django.core.management.base import BaseCommand
from django.utils import timezone

from webapi.models import *

import requests

import datetime

class Command(BaseCommand):
    help = 'Populate movies data from other source'

    def handle(self, *args, **kwargs):
        #latest Movies
        discover_url = 'https://api.themoviedb.org/3/discover/movie'
        for i in range(1,100):
            try:
            

                discover_params = dict(
                    api_key='946f38ce21511b7502877838e75206c8',
                    page=i,
                )

                discover = requests.get(url=discover_url, params=discover_params)
                discover_data = discover.json()

                for data in discover_data['results']:

                    movies_params = dict(
                        api_key='946f38ce21511b7502877838e75206c8',
                    )

                    movies_url = 'https://api.themoviedb.org/3/movie/%s' %(str(data['id']))
                    movies = requests.get(url=movies_url, params=movies_params)
                    movies_data = movies.json()
                    
                    
                    instance_movies = Movies(
                        adult = movies_data['adult'],
                        backdrop_path = movies_data['backdrop_path'],
                        budget = movies_data['budget'], 
                        belongs_to_collection = movies_data['belongs_to_collection'],
                        home_page = movies_data['homepage'],
                        reference_id = movies_data['id'],
                        imdb_id = movies_data['imdb_id'],
                        original_language = movies_data['original_language'],
                        original_title = movies_data['original_title'],
                        overview = movies_data['overview'],
                        popularity = movies_data['popularity'],
                        poster_path = movies_data['poster_path'],
                        release_date = datetime.datetime.strptime(movies_data['release_date'], '%Y-%m-%d') ,
                        revenue = movies_data['revenue'],
                        runtime = movies_data['runtime'],
                        status = movies_data['status'],
                        tagline = movies_data['tagline'],
                        title = movies_data['title'],
                        video = movies_data['video'],
                        vote_average = movies_data['vote_average'],
                        vote_count = movies_data['vote_count'],
                    )
                    instance_movies.save()

                    for geners in movies_data['genres']:
                        instance_geners, created = Geners.objects.get_or_create(reference_id = geners['id'], name = geners['name'])
                        print('instance_geners', instance_geners)
                        instance_movies.geners.add(instance_geners.id)
                        


                    for production_company in movies_data['production_companies']:
                        instance_production_company, created = ProductionCompany.objects.get_or_create(
                            reference_id = production_company['id'],
                            name = production_company['name'],
                            logo_path = production_company['logo_path'],
                            origin_country = production_company['origin_country'],
                        )
                        instance_movies.production_company.add(instance_production_company.id)


                    for production_countries in movies_data['production_countries']:
                        instance_production_countries, created = ProductionCountries.objects.get_or_create(
                            iso_3166_1 = production_countries['iso_3166_1'],
                            name = production_countries['name'],
                        )
                        instance_movies.production_countries.add(instance_production_countries.id)


                    for spoken_languages in movies_data['spoken_languages']:
                        instance_spoken_languages, created = SpokenLanguages.objects.get_or_create(
                            iso_639_1 = spoken_languages['iso_639_1'],
                            name = spoken_languages['name'],
                        )
                        instance_movies.spoken_languages.add(instance_spoken_languages.id)


                    instance_movies.save()


            except Exception as e:
                pass

                