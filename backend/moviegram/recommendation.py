# Aizat write down the recommendation logic here
from django.contrib.auth import get_user_model
from moviegram.models import Movie

User = get_user_model()


def recommend_movies_for_user(user_id):
    user = User.objects.get(id=user_id)  # current authenticated user
    # ids of users that current user follows
    followings_ids = [
        following.following.id for following in user.following_set.all()]
    username = user.get_username()

    if len(followings_ids) == 0: # case when the user does not follow others, just return the popular movies by rating
        pass
    else: # else return movie recommendations based on friends activity(friends' movie rates )
        return f'Below are the recommended movies for {username} (id = {user.id}) Based on his friends activity: {followings_ids}'
