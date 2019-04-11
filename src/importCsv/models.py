from django.db import models
from django.contrib.auth.models import AbstractUser


class City(models.Model):
    """city model for imported cities"""
    abbrev = models.CharField(max_length=10)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Hotel(models.Model):
    """hotel model for imported hotels which has the corresponding city in the database """
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    data = models.CharField(max_length=50)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Url(models.Model):
    """url model to save entered urls for future updates"""
    title = models.CharField(max_length=50)
    url = models.URLField()
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.title + " " + self.url