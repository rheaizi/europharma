from django.db import models


# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=50)
    password = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Medicine(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.IntegerField()
    quantity = models.IntegerField()
    image = models.ImageField(upload_to='img/')

    def __str__(self):
        return self.name


class Admins(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=50)
    password = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Image(models.Model):
    image = models.ImageField(upload_to='img/')
