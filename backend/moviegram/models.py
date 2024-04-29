from django.db import models
from django.contrib.auth.models import User


class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Movie(models.Model):
    name = models.CharField(max_length=100)
    genres = models.ManyToManyField(Genre)
    total_people_rated = models.IntegerField(default=0)
    rating_sum = models.IntegerField(default=0)
    average_rating = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Rate(models.Model):
    ONE_STAR = 1
    TWO_STARS = 2
    THREE_STARS = 3
    FOUR_STARS = 4
    FIVE_STARS = 5

    RATING_CHOICES = [
        (ONE_STAR, '1 Star'),
        (TWO_STARS, '2 Stars'),
        (THREE_STARS, '3 Stars'),
        (FOUR_STARS, '4 Stars'),
        (FIVE_STARS, '5 Stars'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rate = models.IntegerField(choices=RATING_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'movie')

    def __str__(self):
        return f'{self.user.username} rated {self.movie.title}'


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username} >> {self.movie.name}'


class Follow(models.Model):
    follower = models.ForeignKey(
        User, related_name='following_set', on_delete=models.CASCADE)
    following = models.ForeignKey(
        User, related_name='followers_set', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['follower', 'following']


class Activity(models.Model):
    ACTIVITY_CHOICES = {
        ('rate', 'Rate'),
        ('review', 'Review'),
        ('collection', 'Collection'),
    }

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=ACTIVITY_CHOICES)
    activity_id = models.BigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}'s activity"


class Collection(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_public = models.BooleanField(default=False)
    movies = models.ManyToManyField('Movie', related_name='collections')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    followers = models.ManyToManyField(
        User, related_name='followed_collections', null=True, blank=True)

    def __str__(self):
        return self.name
