from rest_framework import serializers
from .models import User, Movie, Follow, Review, Activity #, Collection 


class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    follower_list = serializers.SerializerMethodField()
    following_list = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password',
                  'follower_list', 'following_list']

    def retrieve(self, instance):
        return instance

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    def get_follower_list(self, obj):
        follower = obj.followers_set.all()
        return FollowSerializer(follower, many=True).data

    def get_following_list(self, obj):
        following = obj.following_set.all()
        return FollowSerializer(following, many=True).data


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ['follower', 'following']


class ReviewSerializer(serializers.ModelSerializer):
    # user_name = serializers.SerializerMethodField()
    class Meta:
        model = Review
        fields = ['id', 'user', 'movie', 'content']

    # def get_user_name(self, obj):
    #     return obj.user.username


class MovieSerializer(serializers.ModelSerializer):
    review_list = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = ['name', 'review_list']

    def list(self, instance):
        return instance

    def get_review_list(self, obj):
        reviews = obj.review_set.all()
        return ReviewSerializer(reviews, many=True).data

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
