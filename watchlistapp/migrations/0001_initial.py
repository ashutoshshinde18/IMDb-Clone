# Generated by Django 5.0.4 on 2024-04-15 11:36

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Award',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('category', models.CharField(max_length=100)),
                ('year', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Platform',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('about', models.CharField(max_length=255)),
                ('website_url', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
                ('release_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('release_date', models.DateField()),
                ('plot_summary', models.TextField()),
                ('rating', models.FloatField()),
                ('image', models.ImageField(upload_to='content_images/')),
                ('trailer_link', models.URLField()),
                ('avg_rating', models.FloatField(default=0)),
                ('num_rating', models.IntegerField(default=0)),
                ('active', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('awards', models.ManyToManyField(blank=True, null=True, related_name='movies', to='watchlistapp.award')),
                ('genre', models.ManyToManyField(to='watchlistapp.genre')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Cast',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('movie', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='movies_cast', to='watchlistapp.movie')),
            ],
        ),
        migrations.AddField(
            model_name='award',
            name='movie',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='movie_awards', to='watchlistapp.movie'),
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('date_of_birth', models.DateField()),
                ('bio', models.TextField()),
                ('role', models.CharField(max_length=100, null=True)),
                ('image', models.ImageField(upload_to='person_images/')),
                ('movies', models.ManyToManyField(related_name='person_movies', to='watchlistapp.movie')),
            ],
        ),
        migrations.AddField(
            model_name='movie',
            name='cast',
            field=models.ManyToManyField(related_name='movies_cast', through='watchlistapp.Cast', to='watchlistapp.person'),
        ),
        migrations.AddField(
            model_name='movie',
            name='director',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='movies_director', to='watchlistapp.person'),
        ),
        migrations.AddField(
            model_name='cast',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='watchlistapp.person'),
        ),
        migrations.AddField(
            model_name='movie',
            name='platform',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='watchlistapp.platform'),
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('rating', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)])),
                ('active', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('movie', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='movie_reviews', to='watchlistapp.movie')),
            ],
        ),
        migrations.AddField(
            model_name='movie',
            name='reviews',
            field=models.ManyToManyField(blank=True, null=True, related_name='movie_reviews', to='watchlistapp.review'),
        ),
        migrations.CreateModel(
            name='TVShow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('release_date', models.DateField()),
                ('plot_summary', models.TextField()),
                ('rating', models.FloatField()),
                ('image', models.ImageField(upload_to='content_images/')),
                ('trailer_link', models.URLField()),
                ('avg_rating', models.FloatField(default=0)),
                ('num_rating', models.IntegerField(default=0)),
                ('active', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('awards', models.ManyToManyField(related_name='tvshows', to='watchlistapp.award')),
                ('cast', models.ManyToManyField(related_name='tvshows', through='watchlistapp.Cast', to='watchlistapp.person')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_tvshows', to='watchlistapp.person')),
                ('genre', models.ManyToManyField(to='watchlistapp.genre')),
                ('platform', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='watchlistapp.platform')),
                ('reviews', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tvshow_reviews', to='watchlistapp.review')),
                ('seasons', models.ManyToManyField(to='watchlistapp.season')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='season',
            name='tv_show',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='watchlistapp.tvshow'),
        ),
        migrations.AddField(
            model_name='review',
            name='tvshow',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tvshow_reviews', to='watchlistapp.tvshow'),
        ),
        migrations.AddField(
            model_name='person',
            name='tv_shows',
            field=models.ManyToManyField(blank=True, related_name='person_tvshows', to='watchlistapp.tvshow'),
        ),
        migrations.CreateModel(
            name='Episode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('release_date', models.DateField()),
                ('plot_summary', models.TextField()),
                ('rating', models.FloatField()),
                ('image', models.ImageField(upload_to='episode_images/')),
                ('tv_show', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='watchlistapp.tvshow')),
            ],
        ),
        migrations.AddField(
            model_name='cast',
            name='tvshow',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tvshow_cast', to='watchlistapp.tvshow'),
        ),
        migrations.AddField(
            model_name='award',
            name='tvshow',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tvshow_awards', to='watchlistapp.tvshow'),
        ),
    ]
