from django.db import models

from django.contrib.auth.models import AbstractUser 

# Create your models here.

class MyUser(AbstractUser):
    email = models.EmailField()
    class Meta:
        ordering = ['username']

class Driver(models.Model):
    first_name = models.CharField(max_length=155)
    last_name = models.CharField(max_length=155)
    number = models.SmallIntegerField()
    team = models.CharField(max_length=155)

class DriverChoice(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    chosen_order = models.PositiveIntegerField()  # 1 for first place, 2 for second, etc.

class TopThreeTip(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    first_place = models.ForeignKey(DriverChoice, on_delete=models.CASCADE, related_name='first_place')
    second_place = models.ForeignKey(DriverChoice, on_delete=models.CASCADE, related_name='second_place')
    third_place = models.ForeignKey(DriverChoice, on_delete=models.CASCADE, related_name='third_place')



