from django.db import models
from django.contrib.auth.models import User


class Breed(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Kitten(models.Model):
    breed = models.ForeignKey(Breed, on_delete=models.CASCADE, related_name='kittens')
    color = models.CharField(max_length=50)
    age_in_months = models.PositiveIntegerField()
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.color} kitten, {self.age_in_months} months old'


class KittenRating(models.Model):
    kitten = models.ForeignKey(Kitten, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=[(i, str(i)) for i in range(1, 6)])

    def __str__(self):
        return f'Rating {self.rating} for {self.kitten}'
