from rest_framework import serializers
from .models import User, Movie, Follow, Review, Activity, Rate, Collection, Genre


class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    follower_list = serializers.SerializerMethodField()
    following_list = serializers.SerializerMethodField()
    rated_movies = serializers.SerializerMethodField()
    reviewed_movies = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password',
                  'follower_list', 'following_list', 'rated_movies', 'reviewed_movies']

    def retrieve(self, instance):
        return instance

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    def get_follower_list(self, obj):
        follower = obj.followers_set.all()
        return FollowSerializer(follower, many=True).data

    # def get_following_list(self, obj):
    #     following = obj.following_set.all()
    #     return FollowSerializer(following, many=True).data

    def get_following_list(self, obj):
        following = obj.following_set.all().values_list('following_id', flat=True)
        return list(following)

    def get_rated_movies(self, obj):
        rates = obj.rate_set.all()
        return RateSerializer(rates, many=True).data

    def get_reviewed_movies(self, obj):
        reviews = obj.review_set.all()
        return ReviewSerializer(reviews, many=True).data


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ['follower', 'following']


class ReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = ['id', 'user', 'user_name', 'movie', 'content']

    def get_user_name(self, obj):
        return obj.user.username


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']


class MovieSerializer(serializers.HyperlinkedModelSerializer):
    review_list = serializers.SerializerMethodField()
    genres_list = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = ['id', 'url', 'name', 'average_rating',
                  'review_list', 'genres_list', 'total_people_rated']

    def get_review_list(self, obj):
        reviews = obj.review_set.all()
        return ReviewSerializer(reviews, many=True).data

    def get_genres_list(self, obj):
        genres = obj.genres.all()
        return GenreSerializer(genres, many=True).data


class CollectionSerializer(serializers.ModelSerializer):
    followers_list = serializers.SerializerMethodField()
    movies_list = serializers.SerializerMethodField()

    class Meta:
        model = Collection
        fields = ['id', 'name', 'user',
                  'is_public', 'movies_list', 'followers_list']

    def get_followers_list(self, obj):
        followers = obj.followers.all()
        follower_names = [follower.username for follower in followers]
        return follower_names

    def get_movies_list(self, obj):
        movies = obj.movies.all()
        movie_names = [movie.name for movie in movies]
        return movie_names


class ActivitySerializer(serializers.ModelSerializer):
    message = serializers.SerializerMethodField()

    class Meta:
        model = Activity
        fields = ['user', 'type', 'activity_id', 'message']

    def get_message(self, obj):
        if obj.type == 'rate':
            movie = Movie.objects.get(id=obj.activity_id)
            return f"{obj.user} rated '{movie.name}'"
        elif obj.type == 'review':
            review = Review.objects.get(id=obj.activity_id)
            movie = review.movie
            return f"{obj.user} gave a review to '{movie.name}': '{review.content}'"
        # elif obj.type == 'collection':
        #     collection = Collection.objects.get(id=obj.activity_id)
        #     return f"{obj.user} created new collection: '{collection.name}'. Do you want to follow ? "


class RateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rate
        fields = '__all__'
