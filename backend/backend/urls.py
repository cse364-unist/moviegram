from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from moviegram.views import UserViewSet, Recommend

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('recommend/', Recommend.as_view(), name='recommend'),
]
