# from django.contrib import admin
# from django.urls import path
# from watchlistapp.api.views import MovieListView, ReviewCreateView, ReviewListView, index_view
# from django.conf import settings
# from django.conf.urls.static import static


# urlpatterns = [
#     # path('admin/', admin.site.urls),
#     path('home/', index_view, name='home'),
#     path('movies/list/', MovieListView.as_view(), name='movies-list'),  
#     path('<int:pk>/review-create/', ReviewCreateView.as_view(), name='review-create'),
#     path('<int:pk>/reviews/', ReviewListView.as_view(), name='reviews'),
# ]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.contrib import admin
from django.urls import path
from watchlistapp.api.views import review_create_view, index_view, single_movie, search_movies, review_helpful, review_unhelpful
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('home/', index_view, name='home'),
    path('<int:pk>/review-create/', review_create_view, name='review-create'),
    # path('<int:pk>/reviews/', review_list_view, name='reviews'),
    path('single_movie/<int:movie_id>/', single_movie, name='single_movie'),
    path('search/', search_movies, name='search_movies'),
    path('review_helpful/<int:review_id>/', review_helpful, name='review_helpful'),
    path('review_unhelpful/<int:review_id>/', review_unhelpful, name='review_unhelpful'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
