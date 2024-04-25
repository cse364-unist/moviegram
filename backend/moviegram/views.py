from django.shortcuts import render
from django.http import JsonResponse
from .recommendation import recommend_movies_for_user

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer


from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth.hashers import make_password


class UserViewSet(viewsets.ViewSet):
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


class Recommend(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_id = request.user.id
        movies = recommend_movies_for_user(user_id)
        return Response({"message":movies}, status=status.HTTP_200_OK)