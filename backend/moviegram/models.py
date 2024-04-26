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
