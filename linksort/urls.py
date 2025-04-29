from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CollectionViewSet

router = DefaultRouter()
router.register(r'', CollectionViewSet, basename='collection')

urlpatterns = [
    path('', include(router.urls)),
]