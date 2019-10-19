from django.db import models
import os
from django.utils.translation import ugettext_lazy as _

# for array field
from jsonfield import JSONField

class Geners(models.Model):
    reference_id = models.CharField(_("reference_id"), max_length=50)
    name = models.CharField(_("name"), max_length=250)

    class Meta:
        unique_together = ('reference_id', 'name')

    def __str__(self):
        return self.name

class ProductionCompany(models.Model):
    name = models.CharField(_("name"), max_length=250)
    reference_id = models.CharField(_("reference_id"), max_length=50)
    logo_path = models.CharField(_("logo_path"), max_length=250, null=True, blank=True)
    origin_country = models.CharField(_("origin_country"), max_length=250)

    class Meta:
        unique_together = ('name', 'reference_id', 'logo_path', 'origin_country')

    def __str__(self):
        return self.name


class ProductionCountries(models.Model):
    iso_3166_1 = models.CharField(_("iso_3166_1"), max_length=250)
    name = models.CharField(_("name"), max_length=250)

    class Meta:
        unique_together = ('iso_3166_1', 'name')

    def __str__(self):
        return self.iso_3166_1

class SpokenLanguages(models.Model):
    iso_639_1 = models.CharField(_("iso_639_1"), max_length=250)
    name = models.CharField(_("name"), max_length=250)

    class Meta:
        unique_together = ('iso_639_1', 'name')

    def __str__(self):
        return self.iso_639_1

class Movies(models.Model):
    adult = models.BooleanField(_("adult"), default=False)
    backdrop_path = models.CharField(_("backdrop path"), max_length=250, null=True, blank=True)
    budget = models.BigIntegerField(_("budget"))
    belongs_to_collection = JSONField(null=True, blank=True)
    home_page = models.CharField(_("home page"), max_length=250, null=True, blank=True)
    reference_id = models.CharField(_("reference id"), max_length=250, unique=True)
    imdb_id = models.CharField(_("imdb id"), max_length=250, null=True, blank=True)
    original_language = models.CharField(_("original language"), max_length=250)
    original_title = models.CharField(_("original title"), max_length=250)
    overview = models.TextField(_("overview"), null=True, blank=True)
    popularity = models.BigIntegerField(_("popularity"))
    poster_path = models.CharField(_("poster path"), max_length=250, null=True, blank=True)
    release_date = models.DateField(_("release date"), auto_now=False, auto_now_add=False)
    revenue = models.BigIntegerField(_("revenue"), null=True, blank=True)
    runtime = models.IntegerField(_("run time"), null=True, blank=True)
    status = models.CharField(_("status"), max_length=250)
    tagline = models.CharField(_("tag line"), max_length=250, null=True, blank=True)
    title = models.CharField(_("title"), max_length=250)
    video = models.BooleanField(_("vedio"), default=False)
    vote_average = models.BigIntegerField(_("vote average"))
    vote_count = models.BigIntegerField(_("vote count"))
    geners = models.ManyToManyField("Geners")
    production_company = models.ManyToManyField("ProductionCompany")
    production_countries = models.ManyToManyField("ProductionCountries")
    spoken_languages = models.ManyToManyField("SpokenLanguages")

    def __str__(self):
        return self.original_title


class WatchedList(models.Model):
    code = models.CharField(_("code nmae"), max_length=50, primary_key=True)

    def __str__(self):
        return str(self.code)


class WatchedMovies(models.Model):
    code = models.ForeignKey("WatchedList", related_name='watch_list', on_delete=models.CASCADE)
    movies = models.ForeignKey("Movies", related_name='watched_user', on_delete=models.CASCADE)
    created = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('code', 'movies')

    def __str__(self):
        return self.movies.original_title