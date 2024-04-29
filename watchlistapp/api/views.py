# from rest_framework import generics
# from rest_framework.response import Response
# from watchlistapp.models import Movie, Review
# from .serializers import MovieSerializer, ReviewSerializer
# from django.shortcuts import render
# from rest_framework.validators import ValidationError
# from django.contrib.auth.models import User
# from rest_framework.permissions import IsAuthenticated
# from watchlistapp.api.permissions import ReviewUserOrReadOnly

# def index_view(request):
#     return render(request, 'home/base.html')

# class MovieListView(generics.ListAPIView):
#     queryset = Movie.objects.all()
#     serializer_class = MovieSerializer

#     def list(self, request, *args, **kwargs):
#         queryset = self.get_queryset()
#         serializer = self.get_serializer(queryset, many=True)
#         # return Response(serializer.data)
#         # context = {'movies': serializer.data}  # Add movies to context

#         # return Response(context)
#         print(serializer.data,'=======>serializer data')
#         return render(request, 'movies/movies_list.html', {'movies': serializer.data})
#         # movies = serializer.data
#         # movies_html = render(request, 'movies/movies_list.html', {'movies': movies}).content.decode('utf-8')
#         # return render(request, 'profile.html', {'user': request.user, 'movies_html': movies_html})

# class ReviewCreateView(generics.CreateAPIView):
#     serializer_class = ReviewSerializer
#     permission_classes = [ReviewUserOrReadOnly]
    
#     def perform_create(self, serializer):
#         pk = self.kwargs.get('pk')
#         movie = Movie.objects.get(pk=pk)
#         print(movie,'==>movie')
#         # return 
#         review_user = self.request.user#User.objects.get(username='user')
#         print(review_user,'==>review_user')
#         review_queryset = Review.objects.filter(movie=movie, author=review_user)
        
#         if review_queryset.exists():
#             raise ValidationError('You have already reviewed this movie!')
        
#         if movie.num_rating == 0:
#             movie.avg_rating = serializer.validated_data['rating']
#         else:
#             movie.avg_rating = (movie.avg_rating + serializer.validated_data['rating']) / 2
#         print(movie.avg_rating,'===,movie.avg_rating')
#         movie.num_rating += 1
#         print(movie.num_rating,'===,movie.num_rating')
#         movie.save()
        
        
#         serializer.save(movie=movie, author=review_user)
        
# class ReviewListView(generics.ListAPIView):
#     serializer_class = ReviewSerializer
    
#     def get_queryset(self):
#         pk = self.kwargs['pk']
#         return Review.objects.filter(movie=pk)

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from watchlistapp.models import Movie, Review, Cast
from .serializers import MovieSerializer, ReviewSerializer, AwardSerializer, PersonSerializer
from django.shortcuts import render
from rest_framework.validators import ValidationError
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated,AllowAny
from watchlistapp.api.permissions import ReviewUserOrReadOnly
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from django.db.models import Max
from django.http import JsonResponse
from django.db.models import Q
from django.conf import settings
from django.contrib import messages


@api_view(['GET'])
@permission_classes([AllowAny])
def index_view(request):
    username = request.session.get('username')
    print(request.user,'-------->username indexview')
    # Condition 1: Filter movies created in the past one week
    one_week_ago = datetime.now() - timedelta(days=7)
    recent_movies = Movie.objects.filter(created__gte=one_week_ago)
    recent_movies_serializer = MovieSerializer(recent_movies, many=True)
    
    # Condition 2: Filter movies created yesterday
    yesterday  = datetime.now() - timedelta(days=1)
    movies_added_yesterday = Movie.objects.filter(created__date=yesterday)
    movies_added_yesterday_serializer = MovieSerializer(movies_added_yesterday, many=True)

    # Condition 3: Get all movies list
    all_movies = Movie.objects.all()
    all_movies_serializer = MovieSerializer(all_movies, many=True)

    # Condition 4: Filter movies with avg_rating more than 9
    highly_rated_movies = Movie.objects.filter(avg_rating__gt=9)[:5]
    highly_rated_movies_serializer = MovieSerializer(highly_rated_movies, many=True)
    
    #
    prime_movies = Movie.objects.filter(platform__name="Prime")[:5]
    prime_movies_serializer = MovieSerializer(prime_movies, many=True)
    
    netflix_movies = Movie.objects.filter(platform__name="Netflix")[:5]  
    netflix_movies_serializer = MovieSerializer(netflix_movies, many=True)
    
    # Get the latest added trailer link
    latest_trailer = Movie.objects.aggregate(latest_trailer=Max('trailer_link'))['latest_trailer']
    # return Response(all_movies_serializer.data)
    return render(request, 'movies/movies_list.html', {
        'recent_movies': recent_movies_serializer.data,
        'movies_added_yesterday': movies_added_yesterday_serializer.data,
        'all_movies': all_movies_serializer.data,
        'highly_rated_movies': highly_rated_movies_serializer.data,
        'latest_trailer': latest_trailer,
        'prime_movies': prime_movies_serializer.data,
        'netflix_movies': netflix_movies_serializer.data,
        'username': username
    })

@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def review_create_view(request, pk):
    print('yes its inside review create view',pk)
    if request.method == 'POST':
        try:
            movie = Movie.objects.get(pk=pk)
        except Movie.DoesNotExist:
            # return Response({'error': 'Movie does not exist'}, status=404)
            return JsonResponse({'error': 'Movie does not exist'}, status=404)

        review_user = request.user
        review_queryset = Review.objects.filter(movie=movie, author=review_user)
        
        if review_queryset.exists():
            # raise ValidationError('You have already reviewed this movie!')
            return JsonResponse({'error': 'You have already reviewed this movie!'}, status=400)
        
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            if movie.num_rating == 0:
                movie.avg_rating = serializer.validated_data['rating']
            else:
                movie.avg_rating = (movie.avg_rating + serializer.validated_data['rating']) / 2
            movie.num_rating += 1
            movie.save()
            
            serializer.save(movie=movie, author=review_user)
            # return Response(serializer.data, status=201)
            # Return success response with movie name
            return JsonResponse({'movie_name': movie.title}, status=201)
        # return Response(serializer.errors, status=400)
        # Return validation error if serializer is not valid
        return JsonResponse(serializer.errors, status=400)

# @api_view(['GET'])
# def review_list_view(request, pk):
#     try:
#         movie = Movie.objects.get(pk=pk)
#     except Movie.DoesNotExist:
#         return Response({'error': 'Movie does not exist'}, status=404)

#     reviews = Review.objects.filter(movie=movie)
#     serializer = ReviewSerializer(reviews, many=True)
#     return render(request, 'movies/single_movie.html', {'user_reviews': serializer.data})


def single_movie(request, movie_id):
    # Retrieve the movie object with the provided movie_id
    movie = Movie.objects.get(pk=movie_id)
    
    
    user_review = Review.objects.filter(movie=movie, author=request.user).first()  
    # If the user has reviewed the movie, extract the rating
    user_rating = user_review.rating if user_review else None
    
    movie_all = MovieSerializer(movie)
    # print(movie_all.data)
    # Retrieve awards data for the movie
    awards_data = []
    for award in movie.movie_awards.all():
        # print(award,'--->award')
        award_data = AwardSerializer(award).data
        # print(award_data,'--->award_data')
        persons_with_award = []
        # Assuming the award is associated with a movie and each award has a list of persons associated with it
        for cast in award.movie.cast.all():
            person_data = PersonSerializer(cast).data
            if person_data['name'] in award_data['name']:  # Assuming 'name' is the field name for the person's name
                person_data['image'] = f"https://{settings.AWS_S3_CUSTOM_DOMAIN}/media/{cast.image}"  # Assuming 'image' is the field name for the image
                persons_with_award.append(person_data)
        if persons_with_award:  # Check if there are persons with the same name as the award
            award_data['persons'] = persons_with_award
            awards_data.append(award_data)
            
    cast_info = Cast.objects.filter(movie=movie).exclude(person__role="Director")
    cast_info = [
    {
        'person': {
            'name': cast.person.name,
            'date_of_birth': cast.person.date_of_birth,
            'bio': cast.person.bio,
            'role': cast.person.role,
            'image': f"https://{settings.AWS_S3_CUSTOM_DOMAIN}/media/{cast.person.image}"
        }
    }
    for cast in cast_info
    ]
    
    # user reviews for particular movie
    try:
        movie = Movie.objects.get(pk=movie_id)
    except Movie.DoesNotExist:
        messages.error(request, 'Movie does not exist')

    reviews = Review.objects.filter(movie=movie)
    user_reviews_serializer = ReviewSerializer(reviews, many=True)
    
    return render(request, 'movies/single_movie.html', {'movie': movie_all.data, 'user_rating':user_rating, 'awards_data':awards_data, 'cast_info':cast_info, 'user_reviews':user_reviews_serializer.data})

def search_movies(request):
    query = request.GET.get('q')
    # print(query,'===query')
    if query:
        movies = Movie.objects.filter(title__icontains=query)
        # print(movies,'==-->searched movies')
        search_results = [{'id':movie.id,'title': movie.title, 'image': movie.image.url, 'release_date': movie.release_date.strftime('%Y-%m-%d'), 'cast': [cast.name for cast in movie.cast.all() if cast.role != "Director"]} for movie in movies]
        
    else:
        search_results = []
    return JsonResponse(search_results, safe=False)