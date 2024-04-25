from django.shortcuts import render
from django.http import JsonResponse
from .recommendation import recommend_movies_for_user

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer

def recommend_movies(request):
    # Check if user is logged in
    if request.user.is_authenticated:
        user = request.user
        recommended_movies = recommend_movies_for_user(user)
        # Serialize recommended movies as JSON
        # data = [{'name': movie.name, 'genres': [genre.name for genre in movie.genres.all()]} for movie in recommended_movies]
        return recommend_movies #JsonResponse(data, safe=False)
    else:
        return JsonResponse({'error': 'User not authenticated. Login to get recommendations.'}, status=401) 
    
class UserViewSet(viewsets.ViewSet):
    def create(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'id': user.id, 'username': user.username}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
