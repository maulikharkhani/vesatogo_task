from django.contrib import admin

# Register your models here.
from webapi.models import *

admin.site.register(Movies)
admin.site.register(Geners)
admin.site.register(ProductionCompany)
admin.site.register(ProductionCountries)
admin.site.register(SpokenLanguages)
admin.site.register(WatchedMovies)