# Create your models here.
from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator
from django.contrib.auth.models import User

class Genre(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self) -> str:
        return str(self.id) + ' - ' + str(self.name)

class Platform(models.Model):
    name = models.CharField(max_length=100)
    about = models.CharField(max_length=255)
    website_url = models.URLField()
    
    def __str__(self) -> str:
        # return str(self.id) + ' - ' + str(self.name)
        return str(self.name)

class Person(models.Model):
    name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    bio = models.TextField()
    role = models.CharField(max_length=100,null=True)
    image = models.ImageField(upload_to='person_images/')  # Example path, adjust as needed
    movies = models.ManyToManyField('Movie', related_name='person_movies')
    tv_shows = models.ManyToManyField('TVShow', related_name='person_tvshows', blank=True)
    
    def __str__(self) -> str:
        return self.name

class Content(models.Model):
    title = models.CharField(max_length=100)
    release_date = models.DateField()
    genre = models.ManyToManyField('Genre')
    plot_summary = models.TextField()
    image = models.ImageField(upload_to='content_images/')  # Adjust upload_to as needed
    trailer_link = models.URLField()
    avg_rating = models.FloatField(default=0)
    num_rating = models.IntegerField(default=0)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

class Movie(Content):
    director = models.ForeignKey('Person', on_delete=models.CASCADE, related_name='movies_director', null=True, blank=True)
    cast = models.ManyToManyField('Person', through='Cast', related_name='movies_cast')
    platform = models.ForeignKey('Platform', on_delete=models.CASCADE)
    reviews = models.ManyToManyField('Review', related_name='movie_reviews', null=True, blank=True)
    awards = models.ManyToManyField('Award', related_name='movies', null=True, blank=True)
    
    def __str__(self) -> str:
        return self.title

class TVShow(Content):
    creator = models.ForeignKey('Person', on_delete=models.CASCADE, related_name='created_tvshows')
    cast = models.ManyToManyField('Person', through='Cast', related_name='tvshows')
    platform = models.ForeignKey('Platform', on_delete=models.CASCADE)
    reviews = models.ForeignKey('Review', on_delete=models.CASCADE, related_name='tvshow_reviews')
    awards = models.ManyToManyField('Award', related_name='tvshows')
    seasons = models.ManyToManyField('Season')


class Cast(models.Model):
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE, related_name='movies_cast',null=True, blank=True)
    tvshow = models.ForeignKey('TVShow', on_delete=models.CASCADE, related_name='tvshow_cast',null=True, blank=True)
    person = models.ForeignKey('Person', on_delete=models.CASCADE)
    # role = models.CharField(max_length=100)
    
    def __str__(self) -> str:
        return f"{self.person}"

class Review(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1),MaxValueValidator(10)])
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE, related_name='movie_reviews', null=True, blank=True)
    tvshow = models.ForeignKey('TVShow', on_delete=models.CASCADE, related_name='tvshow_reviews', null=True, blank=True)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return f"{self.author} - {self.movie} - {self.rating}"

class Award(models.Model):
    # name = models.CharField(max_length=100)
    name = models.ForeignKey('Person', on_delete=models.CASCADE, related_name='name_awards')
    category = models.CharField(max_length=100)
    awardfor = models.CharField(max_length=100,default='NA')
    year = models.DateField()
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE, related_name='movie_awards', null=True, blank=True)
    tvshow = models.ForeignKey('TVShow', on_delete=models.CASCADE, related_name='tvshow_awards', null=True, blank=True)
    
    def __str__(self) -> str:
        return f"{self.name} - {self.category} - {self.movie}"

class Season(models.Model):
    number = models.IntegerField()
    release_date = models.DateField()
    tv_show = models.ForeignKey(TVShow, on_delete=models.CASCADE)

class Episode(models.Model):
    title = models.CharField(max_length=100)
    release_date = models.DateField()
    plot_summary = models.TextField()
    rating = models.FloatField()
    image = models.ImageField(upload_to='episode_images/')  # Example path, adjust as needed
    tv_show = models.ForeignKey(TVShow, on_delete=models.CASCADE)

