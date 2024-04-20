from django.db import models

class Genre(models.Model): 
    name = models.CharField(max_length=100)

    def __str__(self): 
        return self.name 
    

class Movie(models.Model):
    name = models.CharField(max_length=100) 
    genres = models.ManyToManyField(Genre) 


    def __str__(self): 
        return self.name 