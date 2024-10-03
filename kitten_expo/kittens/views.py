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

    @swagger_auto_schema(
        operation_description="Получить список всех пород"
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Получить информацию о конкретной породе"
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


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
        operation_description="Получить список котят с фильтрами по породе",
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

    @swagger_auto_schema(
        operation_description="Создать нового котенка"
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Получить информацию о конкретном котенке"
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Обновить информацию о котенке"
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Частично обновить информацию о котенке"
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Удалить котенка"
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class KittenRatingViewSet(viewsets.ModelViewSet):
    queryset = KittenRating.objects.all()
    serializer_class = KittenRatingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, CanRateOthersKittens]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @swagger_auto_schema(
        operation_description="Оценить котенка"
    )
    def create(self, request, *args, **kwargs):
        kitten = Kitten.objects.get(pk=request.data['kitten'])

        if kitten.owner == request.user:
            raise ValidationError("Вы не можете оценивать своих котят")

        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Получить список всех оценок котят"
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Получить информацию о конкретной оценке"
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Обновить информацию о конкретной оценке"
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Частично обновить информацию о конкретной оценке"
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Удалить оценку"
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)