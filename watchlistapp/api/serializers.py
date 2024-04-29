from rest_framework import serializers
from watchlistapp.models import Movie, TVShow, Person, Genre, Review, Award, Cast, Platform, Season, Episode


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'

class PlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = Platform
        fields = '__all__'


class PersonSerializer(serializers.ModelSerializer):
    movies = serializers.SerializerMethodField()
    # image = serializers.ImageField(source='image.url') 
    class Meta:
        model = Person
        fields = ['name','movies','role']

    def get_movies(self, obj):
        # Assuming you have a many-to-many relationship between Person and Movie
        return [movie.title for movie in obj.movies.all()]

class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Review
        # fields = '__all__'
        exclude = ('movie', )


class AwardSerializer(serializers.ModelSerializer):
    name = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Award
        exclude = ['movie']


class EpisodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Episode
        fields = '__all__'


class SeasonSerializer(serializers.ModelSerializer):
    episodes = EpisodeSerializer(many=True, read_only=True)

    class Meta:
        model = Season
        fields = '__all__'


class CastSerializer(serializers.ModelSerializer):
    person = serializers.CharField(source='name')   
    image = serializers.CharField()
    role = serializers.CharField()
    class Meta:
        model = Cast
        fields = ['person','image','role']


class TVShowSerializer(serializers.ModelSerializer):
    cast = PersonSerializer(many=True, read_only=True)
    creator = PersonSerializer()

    class Meta:
        model = TVShow
        fields = '__all__'


class MovieSerializer(serializers.ModelSerializer):
    director = PersonSerializer()
    cast = CastSerializer(many=True)
    reviews = ReviewSerializer(many=True, source='movie_reviews')
    awards = AwardSerializer(many=True, source = 'movie_awards')

    class Meta:
        model = Movie
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Retrieve platform names instead of IDs
        platform_name = instance.platform.name
        representation['platform'] = platform_name
        
        # Retrieve platform names instead of IDs
        reviews_data = []
        for review in instance.movie_reviews.all():
            author_name = review.author.username
            review_data = ReviewSerializer(review).data
            review_data['author'] = author_name
            reviews_data.append(review_data)
        
        representation['reviews'] = reviews_data
        
        # Retrieve genre names instead of IDs
        genre_names = instance.genre.values_list('name', flat=True)
        representation['genre'] = genre_names
        return representation