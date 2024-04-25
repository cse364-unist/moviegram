from rest_framework import serializers
from .models import User, Movie, Follow

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


# class FollowingSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Follow
#         fields = ("id", "following", "created")

# class FollowersSerializer(serializers.ModelSerializer):
    
#     class Meta:
#         model = Follow
#         fields = ("id", "follower", "created")


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id', 'name', 'average_rating']
    
    def list(self, instance): 
        return instance
