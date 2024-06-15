from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from moviegram.views import UserViewSet, MovieViewSet, RecommendViewSet, FollowViewSet, FeedViewSet, CollectionViewSet, CustomLoginView, CustomLogoutView, CustomSignupView

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'movies', MovieViewSet, basename='movie')
router.register(r'recommend', RecommendViewSet, basename='recommend')
router.register(r'collections', CollectionViewSet, basename='collection')

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

    path('collections/<int:collection_id>/follow/',
         CollectionViewSet.as_view({'post': 'follow'}), name='collection-follow'),
    path('collections/<int:collection_id>/unfollow/',
         CollectionViewSet.as_view({'post': 'unfollow'}), name='collection-unfollow'),

    path('collections/<int:collection_id>/add/',
         CollectionViewSet.as_view({'post': 'add_movie'}), name='collection-add'),

    path('', FeedViewSet.as_view({'get': 'list'}), name='feed'),

    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('signup/', CustomSignupView.as_view(), name='signup')

]

urlpatterns += router.urls
