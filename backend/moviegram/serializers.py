from rest_framework import serializers
from .models import User, Movie, Follow, Review

class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    def list(self, instance):
        return instance


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