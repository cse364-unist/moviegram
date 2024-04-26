from django.contrib import admin
from .models import Movie, Genre, Review, Activity

class ReviewAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
# Register your models here.
admin.site.register(Movie) 
admin.site.register(Genre)
admin.site.register(Review, ReviewAdmin) 
admin.site.register(Activity) 