from django.contrib.auth.models import User

from rest_framework import serializers
from djoser.serializers import UserSerializer as BaseUserSerializer, UserCreateSerializer as BaseUserCreateSerializer

from .models import AuthUser, Driver, Race, TopThreeTip, UserProfile

# serializer for creating user 
class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        model = AuthUser
        fields = ['id', 'username', 'password',
                 'email']

# serializer for USER 
class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

# serializer for USER PROFILE
class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    class Meta:
        model = UserProfile
        fields = [ 'username', 'social_media_links', 'profile_picture', 'bio', 'score']
        read_only_fields = ['score', 'username']


class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = ['id', 'first_name', 'last_name', 'number', 'team']

class RaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Race
        fields = ['id', 'grand_prix', 'circuit', 'date']

# top three serializers 
        
class TopThreeTipCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopThreeTip
        fields = ['race', 'first_place', 'second_place', 'third_place']


class TopThreeTipUpdateserializer(serializers.ModelSerializer):
    class Meta:
        model = TopThreeTip
        fields = ['first_place', 'second_place', 'third_place']
    
    def validate(self, data):
        first_place = data.get('first_place')
        second_place = data.get('second_place')
        third_place = data.get('third_place')

        # Check if any two places have the same driver
        if (first_place == second_place) or (first_place == third_place) or (second_place == third_place):
            raise serializers.ValidationError("Cannot select the same driver for more than one place.")

        return data

class TopThreeTipSerializer(serializers.ModelSerializer):
    user_profile = UserProfileSerializer()
    first_place = DriverSerializer()
    second_place = DriverSerializer()
    third_place = DriverSerializer()
    race = RaceSerializer()

    class Meta:
        model = TopThreeTip
        fields = ['id', 'user_profile', 'first_place', 'second_place', 'third_place', 'race', 'date']
        read_only_fields = ['user_profile']
    
    

# serializers for HOME
class EvaluatedTipsSerializer(serializers.ModelSerializer):
    first_place = serializers.StringRelatedField()
    second_place = serializers.StringRelatedField()
    third_place = serializers.StringRelatedField()
    race = serializers.StringRelatedField()
    
    class Meta:
        model = TopThreeTip
        fields = ['id', 'first_place', 'second_place', 'third_place', 'race', 'date']
        read_only_fields = ['user_profile']
    
    def to_representation(self, instance):
        if instance.evaluated:
            return super().to_representation(instance)
        return {}

class UpcomingTipsSerializer(serializers.ModelSerializer):
    first_place = serializers.StringRelatedField()
    second_place = serializers.StringRelatedField()
    third_place = serializers.StringRelatedField()
    race = serializers.StringRelatedField()
    class Meta:
        model = TopThreeTip
        fields = ['id', 'first_place', 'second_place', 'third_place', 'race', 'date']
        read_only_fields = ['user_profile']
    
    def to_representation(self, instance):
        if not instance.evaluated:
            return super().to_representation(instance)
        return {}

class HomeSerializer(serializers.Serializer):
    profile = UserProfileSerializer()
    evaluated_tips = EvaluatedTipsSerializer(many=True)
    upcoming_tips = UpcomingTipsSerializer(many=True)
    next_race = RaceSerializer()
    username = serializers.CharField(source='profile.user.username', read_only=True)

    class Meta:
        fields = ['profile', 'evaluated_tips', 'upcoming_tips', 'next_race', 'score', 'username']

# races Serializer 

class RaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Race
        fields = ['grand_prix', 'circuit', 'date']
    

class LeaderboardSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    score = serializers.IntegerField()
    position = serializers.SerializerMethodField()
    
    class Meta:
        model = UserProfile
        fields = ['user', 'score', 'position']

    def get_position(self, obj):
        # Retrieve all users ordered by score
        users_ordered_by_score = UserProfile.objects.order_by('-score', 'user__username')

        # Find the position of the current user
        position = list(users_ordered_by_score).index(obj) + 1

        return position


        
        

