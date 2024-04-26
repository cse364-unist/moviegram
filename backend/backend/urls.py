from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from moviegram.views import UserViewSet, MovieViewSet, RecommendViewSet, FollowViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'movies', MovieViewSet, basename='movie')
router.register(r'recommend', RecommendViewSet, basename='recommend')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/<int:user_id>/follow/',
         FollowViewSet.as_view({'post': 'create'}), name='user-follow'),
    path('users/<int:user_id>/unfollow/',
         FollowViewSet.as_view({'delete': 'delete'}), name='user-unfollow'),
    path('movies/<int:movie_id>/rate/',
         MovieViewSet.as_view({'post': 'rate'}), name='movie-rate'),
    path('movies/<int:movie_id>/review/',
         MovieViewSet.as_view({'post': 'give_review'}), name='movie-review'),
    path('', include(router.urls)),
]
