from rest_framework import serializers
from .models import Breed, Kitten, KittenRating


class BreedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Breed
        fields = '__all__'


class KittenSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Kitten
        fields = '__all__'


class KittenRatingSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = KittenRating
        fields = '__all__'
