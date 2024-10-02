# kittens/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BreedViewSet, KittenViewSet, KittenRatingViewSet

router = DefaultRouter()
router.register(r'breeds', BreedViewSet)  # Маршруты для работы с породами
router.register(r'kittens', KittenViewSet)  # Маршруты для работы с котятами
router.register(r'ratings', KittenRatingViewSet)  # Маршруты для работы с оценками котят

urlpatterns = [
    path('', include(router.urls)),  # Включение маршрутов, зарегистрированных в роутере
]
