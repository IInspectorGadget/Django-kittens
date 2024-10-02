from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, permissions
from rest_framework.exceptions import ValidationError

from .models import Breed, Kitten, KittenRating
from .permissions import IsOwnerOrReadOnly, CanRateOthersKittens
from .serializers import BreedSerializer, KittenSerializer, KittenRatingSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication

class BreedViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Breed.objects.all()
    serializer_class = BreedSerializer


class KittenViewSet(viewsets.ModelViewSet):
    queryset = Kitten.objects.all()
    serializer_class = KittenSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    authentication_classes = [JWTAuthentication]

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['breed_id']

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @swagger_auto_schema(
        operation_description="Получить список котят с фильтрами",
        manual_parameters=[
            openapi.Parameter(
                'breed_id',
                openapi.IN_QUERY,
                description="Фильтр по ID породы",
                type=openapi.TYPE_INTEGER
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class KittenRatingViewSet(viewsets.ModelViewSet):
    queryset = KittenRating.objects.all()
    serializer_class = KittenRatingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, CanRateOthersKittens]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        kitten = Kitten.objects.get(pk=request.data['kitten'])

        if kitten.owner == request.user:
            raise ValidationError("Вы не можете оценивать своих котят")

        return super().create(request, *args, **kwargs)