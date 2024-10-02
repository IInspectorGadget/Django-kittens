import pytest
from django.core.management import call_command
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from .models import Breed, Kitten, KittenRating



@pytest.fixture(scope='function', autouse=True)
def clear_test_db():
    """Очищает тестовую базу данных перед каждым тестом."""
    print("Clearing test database")
    call_command('flush', '--no-input')

@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticated_client(user):
    """Создает аутентифицированный клиент."""
    client = APIClient()
    client.login(username='testuser', password='testpass')
    return client

@pytest.fixture
def user():
    return User.objects.create_user(username="testuser", password="password")


@pytest.fixture
def another_user():
    return User.objects.create_user(username="anotheruser", password="password")


@pytest.fixture
def breed():
    return Breed.objects.create(name="Siberian")


@pytest.fixture
def kitten(user, breed):
    return Kitten.objects.create(breed=breed, color="White", age_in_months=4, description="Fluffy kitten", owner=user)

@pytest.fixture
def kitten_rating(kitten, user):
    """Создает тестовую оценку котенка."""
    return KittenRating.objects.create(kitten=kitten, user=user, rating=5)

@pytest.mark.django_db
def test_list_breeds(api_client):
    Breed.objects.create(name="Siberian")
    Breed.objects.create(name="Bengal")

    response = api_client.get('/api/breeds/')
    assert response.status_code == 200
    assert len(response.data) == 2

@pytest.mark.django_db
def test_create_kitten(api_client, user, breed):
    api_client.force_authenticate(user=user)

    data = {
        "breed": breed.id,
        "color": "White",
        "age_in_months": 4,
        "description": "A cute kitten"
    }

    response = api_client.post('/api/kittens/', data)
    assert response.status_code == 201
    assert Kitten.objects.count() == 1

@pytest.mark.django_db
def test_create_kitten_rating(api_client, user, another_user, kitten):
    api_client.force_authenticate(user=another_user)

    data = {
        "kitten": kitten.id,
        "rating": 5
    }

    response = api_client.post('/api/ratings/', data)
    assert response.status_code == 201
    assert KittenRating.objects.count() == 1
    assert KittenRating.objects.first().rating == 5

@pytest.mark.django_db
def test_create_kitten_rating_for_own_kitten(api_client, user, kitten):
    api_client.force_authenticate(user=user)

    data = {
        "kitten": kitten.id,
        "rating": 5
    }

    response = api_client.post('/api/ratings/', data)
    assert response.status_code == 400
    assert "Вы не можете оценивать своих котят" in str(response.data)

@pytest.mark.django_db
def test_delete_rating(api_client, another_user, kitten_rating):
    """Тест для удаления оценки котенка."""
    api_client.force_authenticate(user=another_user)
    response = api_client.delete(f'/api/ratings/{kitten_rating.id}/')
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert KittenRating.objects.count() == 0

@pytest.mark.django_db
def test_update_rating(api_client, another_user, kitten_rating):
    """Тест для обновления оценки котенка."""
    api_client.force_authenticate(user=another_user)
    data = {
        'rating': 4
    }
    response = api_client.patch(f'/api/ratings/{kitten_rating.id}/', data=data)
    assert response.status_code == status.HTTP_200_OK
    kitten_rating.refresh_from_db()
    assert kitten_rating.rating == 4

@pytest.mark.django_db
def test_get_rating_by_id(api_client, another_user, kitten_rating):
    """Тест для получения оценки котенка по ID."""
    api_client.force_authenticate(user=another_user)
    response = api_client.get(f'/api/ratings/{kitten_rating.id}/')
    assert response.status_code == status.HTTP_200_OK
    assert response.data['rating'] == 5

@pytest.mark.django_db
def test_list_ratings(api_client, another_user, kitten, kitten_rating):
    """Тест для получения списка оценок котят."""
    api_client.force_authenticate(user=another_user)
    response = api_client.get('/api/ratings/')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1