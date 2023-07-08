from django.db import models

# Create your models here.

class ParkingSpot(models.Model):
    name = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

class Reservation(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    parking_spot = models.ForeignKey('ParkingSpot', on_delete=models.CASCADE)
    hours = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=8, decimal_places=2)

class User(models.Model):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20)