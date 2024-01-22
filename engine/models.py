from datetime import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError



# Create your models here.

# user only for authorization 
class AuthUser(AbstractUser):
    email = models.EmailField(unique=True)
    class Meta:
        ordering = ['username']

# each user has user profile 
class UserProfile(models.Model):
    user = models.OneToOneField(AuthUser, on_delete=models.CASCADE, primary_key=True)
    score = models.IntegerField(default=0)
    social_media_links = models.URLField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username


class Driver(models.Model):
    first_name = models.CharField(max_length=155)
    last_name = models.CharField(max_length=155)
    number = models.SmallIntegerField()
    team = models.CharField(max_length=155)

    def __str__(self) -> str:
        return self.first_name +" "+  self.last_name


class Race(models.Model):
    round = models.SmallIntegerField()
    grand_prix = models.CharField(max_length=155)
    circuit = models.CharField(max_length=155) 
    date = models.DateField()

    def __str__(self) -> str:
        return f"{self.grand_prix} - {self.circuit}"


class TopThreeTip(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='tips')
    first_place = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name='first_place')
    second_place = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name='second_place')
    third_place = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name='third_place')
    race = models.ForeignKey(Race, on_delete=models.CASCADE, related_name='race')
    date = models.DateTimeField(auto_now_add=True)
    evaluated = models.BooleanField(default=False)
    precision = models.FloatField(null=True, blank=True)
    points = models.IntegerField(null=True, blank=True)


    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user_profile', 'race'], name='unique_user_race_top_three_tip')
        ]

    def clean(self):
        # Ensure that the selected drivers are unique within the context of the race
        selected_drivers = [self.first_place, self.second_place, self.third_place]
        # Remove None values (if any)
        selected_drivers = [driver for driver in selected_drivers if driver is not None]

        if len(set(selected_drivers)) != len(selected_drivers):
            raise ValidationError("Selected drivers must be unique within the context of the race.")
        
        current_datetime = timezone.now()
        if self.race.date <= current_datetime:
            raise ValidationError("Cannot update a tip after the race has started.")



class ResultRace(models.Model):
    position = models.SmallIntegerField()
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name='results')  # related_name for reverse queries
    race = models.ForeignKey(Race, on_delete=models.CASCADE, related_name='results')  # related_name for reverse queries

    class Meta:
        unique_together = ['race', 'driver']


class Leaderboard(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='leaderboard')
   

    class Meta:
        ordering = ['user']