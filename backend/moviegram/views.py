# Django imports
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.db import transaction


# DRF imports
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination  # Import pagination class

# Project imports
from .serializers import UserSerializer, FollowSerializer, MovieSerializer, ReviewSerializer, ActivitySerializer, RateSerializer, CollectionSerializer
from .models import Movie, Review, Follow, Activity, Rate, Collection
from .recommendation import recommend_movies_for_user


class UserViewSet(viewsets.ViewSet):

    def list(self, request):
        User = get_user_model()
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        # usernames = [user['username'] for user in serializer.data]
        # return Response(usernames)
        return Response(serializer.data)

    def create(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            validated_data['password'] = make_password(
                validated_data['password'])

            user = serializer.save()
            return Response({'id': user.id, 'username': user.username}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FollowViewSet(viewsets.ViewSet):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request, user_id):
        User = get_user_model()

        try:
            user_to_follow = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'message': "User is not found. Please provide existing user to follow."}, status=status.HTTP_404_NOT_FOUND)

        if user_to_follow.id == request.user.id:
            return Response({'message': "Can't follow yourself. Provide different user."}, status=status.HTTP_400_BAD_REQUEST)

        follow_data = {'follower': request.user.id,
                       'following': user_to_follow.id}
        serializer = FollowSerializer(data=follow_data)

        if serializer.is_valid():
            serializer.save()
            return Response({'message': f'You now follow {user_to_follow.get_username()}.'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': "You already follow this user."}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, user_id):
        User = get_user_model()

        try:
            user_to_unfollow = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'message': "User is not found. Please provide existing user to unfollow."}, status=status.HTTP_404_NOT_FOUND)

        try:
            follow_instance = Follow.objects.get(
                follower=request.user, following=user_to_unfollow)
            follow_instance.delete()
            return Response({'message': f'You have unfollowed {user_to_unfollow.get_username()}.'}, status=status.HTTP_200_OK)
        except Follow.DoesNotExist:
            return Response({'error': 'You are not following this user.'}, status=status.HTTP_404_NOT_FOUND)


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    pagination_class = PageNumberPagination

    def list(self, request):
        queryset = Movie.objects.order_by('id')

        paginator = self.pagination_class()
        paginated_queryset = paginator.paginate_queryset(queryset, request)

        serializer = MovieSerializer(
            paginated_queryset, many=True, context={'request': request})

        return paginator.get_paginated_response(serializer.data)

    def create(self, request, *args, **kwargs):
        if not (request.user.is_authenticated and request.user.is_staff):
            return Response({'error': 'You do not have permission to perform this action.'}, status=status.HTTP_403_FORBIDDEN)
        return super().create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if not (request.user.is_authenticated and request.user.is_staff):
            return Response({'error': 'You do not have permission to perform this action.'}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        if not (request.user.is_authenticated and request.user.is_staff):
            return Response({'error': 'You do not have permission to perform this action.'}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def rate(self, request, movie_id):
        if not request.user.is_authenticated:
            return Response({'error': 'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED)
        movie = get_object_or_404(Movie, pk=movie_id)

        if 'rating' not in request.data:
            return Response({'error': 'Rating is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            rating = int(request.data['rating'])
        except ValueError:
            return Response({'error': 'Invalid rating value'}, status=status.HTTP_400_BAD_REQUEST)

        rating = int(request.data['rating'])
        if rating < 1 or rating > 5:
            return Response({'error': 'Rating must in range 1 - 5'}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            # Create Rate instance
            rate_data = {'user': request.user.id,
                         'movie': movie.id, 'rate': rating}
            rate_serializer = RateSerializer(data=rate_data)

            if rate_serializer.is_valid():
                rate_instance = rate_serializer.save()
            else:
                # return Response(rate_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                return Response({"message": f'User already rated movie {movie_id}'}, status=status.HTTP_400_BAD_REQUEST)

            # Create Activity instance
            activity_data = {'user': request.user.id,
                             'type': 'rate', 'activity_id': rate_instance.id}
            activity_serializer = ActivitySerializer(data=activity_data)

            if activity_serializer.is_valid():
                activity_serializer.save()
            else:
                return Response(activity_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            movie.refresh_from_db()

            # Update movie rating
            movie.total_people_rated += 1
            movie.rating_sum += rating
            movie.average_rating = movie.rating_sum / movie.total_people_rated
            movie.save()

            serializer = MovieSerializer(movie)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def give_review(self, request, movie_id):
        if not request.user.is_authenticated:
            return Response({'error': 'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED)

        movie = get_object_or_404(Movie, pk=movie_id)

        if 'content' not in request.data:
            return Response({'error': 'Content is required'}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            review_data = {
                'movie': movie_id,
                'user': request.user.id,
                'content': request.data['content']
            }
            serializer = ReviewSerializer(data=review_data)

            if serializer.is_valid():
                review_instance = serializer.save()
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            # Create Activity instance
            activity_data = {'user': request.user.id,
                             'type': 'review', 'activity_id': review_instance.id}
            activity_serializer = ActivitySerializer(data=activity_data)

            if activity_serializer.is_valid():
                activity_serializer.save()
            else:
                return Response(activity_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            return Response(serializer.data, status=status.HTTP_201_CREATED)


class CollectionViewSet(viewsets.ModelViewSet):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    pagination_class = PageNumberPagination

    def list(self, request):
        queryset = Collection.objects.filter(is_public=True).order_by('id')

        paginator = self.pagination_class()
        paginated_queryset = paginator.paginate_queryset(queryset, request)

        serializer = CollectionSerializer(paginated_queryset, many=True)

        return paginator.get_paginated_response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        if not instance.is_public:
            if not (request.user.is_authenticated and request.user.id == instance.user.id):
                return Response({'error': 'You do not have permission to perform this action.'}, status=status.HTTP_403_FORBIDDEN)
        serializer = CollectionSerializer(instance)
        return Response(serializer.data)

    def follow(self, request, collection_id):
        user = request.user

        if not user.is_authenticated:
            return Response({'error': 'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            collection = Collection.objects.get(
                id=collection_id, is_public=True)
        except Collection.DoesNotExist:
            return Response({'error': "Collection is not found or not public. Please provide an existing public collection to follow."}, status=status.HTTP_404_NOT_FOUND)

        if user in collection.followers.all():
            return Response({"error": "You already follow this collection ! "})

        collection.followers.add(user)
        return Response({"message": f'{user.username} now follows {collection.name} collection'})

    def unfollow(self, request, collection_id):
        user = request.user

        if not user.is_authenticated:
            return Response({'error': 'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            collection = Collection.objects.get(
                id=collection_id, is_public=True)
        except Collection.DoesNotExist:
            return Response({'error': "Collection is not found or not public. Please provide an existing public collection to unfollow."}, status=status.HTTP_404_NOT_FOUND)

        if user not in collection.followers.all():
            return Response({"error": "You don't follow this collection! "})

        collection.followers.remove(user)
        return Response({"message": f'{user.get_username()} unfollowed the {collection.name} collection! '})

    def create(self, request):
        user = request.user
        if not user.is_authenticated:
            return Response({'error': 'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED)

        if "name" not in request.data:
            return Response({'error': 'Name is required'}, status=status.HTTP_400_BAD_REQUEST)

        if "is_public" not in request.data:
            return Response({'error': 'Public is required'}, status=status.HTTP_400_BAD_REQUEST)

        collection_data = {'name': request.data['name'],
                           'is_public': request.data['is_public'], 'user': user.id}

        serializer = CollectionSerializer(data=collection_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class RecommendViewSet(viewsets.GenericViewSet):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request):
        user_id = request.user.id
        movies = recommend_movies_for_user(user_id)
        return Response({"message": movies}, status=status.HTTP_200_OK)


class FeedViewSet(viewsets.GenericViewSet):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        follow_users_id = [
            follow.following.id for follow in user.following_set.all()]

        activities = Activity.objects.filter(
            user_id__in=follow_users_id).order_by('-created_at')
        serializer = ActivitySerializer(activities, many=True)

        return Response({'activities': serializer.data})
