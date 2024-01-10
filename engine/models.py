from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser


# Create your models here.
# user only for authorization 
class AuthUser(AbstractUser):
    email = models.EmailField(unique=True)
    class Meta:
        ordering = ['username']

class UserProfile(models.Model):
    user = models.OneToOneField(AuthUser, on_delete=models.CASCADE, primary_key=True)
    score = models.IntegerField()
    social_media_links = models.URLField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    contact_information = models.CharField(max_length=255, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)


class Driver(models.Model):
    first_name = models.CharField(max_length=155)
    last_name = models.CharField(max_length=155)
    number = models.SmallIntegerField()
    team = models.CharField(max_length=155)



class DriverChoice(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    chosen_order = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(3)])  # 1 for first place, 2 for second, etc.


class Race(models.Model):
    grand_prix = models.CharField(max_length=155)
    circuit = models.CharField(max_length=155) 
    date = models.DateField()


class TopThreeTip(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    first_place = models.ForeignKey(DriverChoice, on_delete=models.CASCADE, related_name='first_place')
    second_place = models.ForeignKey(DriverChoice, on_delete=models.CASCADE, related_name='second_place')
    third_place = models.ForeignKey(DriverChoice, on_delete=models.CASCADE, related_name='third_place')
    race = models.ForeignKey(Race, on_delete=models.CASCADE, related_name='race')

class ResultRace(models.Model):
    position = models.SmallIntegerField()
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name='results')  # related_name for reverse queries
    race = models.ForeignKey(Race, on_delete=models.CASCADE, related_name='results')  # related_name for reverse queries