from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password


from .recommendation import recommend_movies_for_user

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination  # Import pagination class


from .serializers import UserSerializer, FollowSerializer, MovieSerializer
from .models import Movie, Follow 


class UserViewSet(viewsets.ViewSet):

    def list(self, request): 
        User = get_user_model()
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        usernames = [user['username'] for user in serializer.data]
        return Response(usernames)
    
    def create(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            # Hash the password before saving the user
            validated_data = serializer.validated_data
            validated_data['password'] = make_password(validated_data['password'])
            
            user = serializer.save()
            return Response({'id': user.id, 'username': user.username}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class FollowViewSet(viewsets.ViewSet): 
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        pk = kwargs.get('pk')

        if pk: 
            user_to_follow_id = get_object_or_404(User, pk=pk)
            User = get_user_model()
            
            follow_data = {'follower': request.user.id, 'following': user_to_follow_id}
            serializer = FollowSerializer(data=follow_data)
            
            # Validate and save the Follow object
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'User followed successfully.'}, status=status.HTTP_201_CREATED)
            else: 
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
        return Response({'message':'Provide user id to follow.'}, status=status.HTTP_400_BAD_REQUEST) 


class MovieViewSet(viewsets.ViewSet): 
    
    pagination_class = PageNumberPagination  # Apply pagination class

    def list(self, request):
        queryset = Movie.objects.all()

        # Paginate the queryset
        paginator = self.pagination_class()
        paginated_queryset = paginator.paginate_queryset(queryset, request)

        # Serialize paginated queryset
        serializer = MovieSerializer(paginated_queryset, many=True)

        # Return paginated response
        return paginator.get_paginated_response(serializer.data)
    
    def rate(self, request, movie_id):
        movie = get_object_or_404(Movie, pk=movie_id)

        if 'rating' not in request.data:
            return Response({'error': 'Rating is required'}, status=status.HTTP_400_BAD_REQUEST)

        rating = int(request.data['rating'])
        if rating < 1 or rating > 5:
            return Response({'error':'Rating must in range 1 - 5'}, status=status.HTTP_400_BAD_REQUEST)

        # Update movie rating
        movie.total_people_rated += 1
        movie.rating_sum += rating
        movie.average_rating = movie.rating_sum / movie.total_people_rated
        movie.save()

        serializer = MovieSerializer(movie)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RecommendViewSet(viewsets.GenericViewSet):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request):
        user_id = request.user.id
        movies = recommend_movies_for_user(user_id)
        return Response({"message": movies}, status=status.HTTP_200_OK)