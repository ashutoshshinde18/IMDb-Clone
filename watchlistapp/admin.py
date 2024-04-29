from django.contrib import admin
from watchlistapp.models import (Genre, Platform, Person, Content,
                                 Movie, TVShow, Cast, Review, Award,
                                 Season, Episode)
# Register your models here.


admin.site.register(Genre)
admin.site.register(Platform)
admin.site.register(Person)
admin.site.register(Movie)
admin.site.register(TVShow)
admin.site.register(Cast)
admin.site.register(Review)
admin.site.register(Award)
admin.site.register(Season)
admin.site.register(Episode)