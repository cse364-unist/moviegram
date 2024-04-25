# Aizat write down the recommendation logic here 
from django.contrib.auth import get_user_model
from moviegram.models import Movie

User = get_user_model()

def recommend_movies_for_user(user_id):
    user = User.objects.get(id=user_id)
    username = user.get_username()
    return f'Below are the movies for {username}'

