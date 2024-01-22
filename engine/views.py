from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied

from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action


from .models import Race, TopThreeTip, UserProfile, AuthUser
from .serializers import HomeSerializer, LeaderboardSerializer, RaceSerializer, TopThreeTipCreateSerializer, TopThreeTipSerializer, TopThreeTipUpdateserializer, UserProfileSerializer
from .permissions import IsOwnerOrReadOnly



# Create your views here.

# home page for looking at placed serializers 

class TopThreeViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TopThreeTipCreateSerializer
        if self.request.method == 'GET':
            return TopThreeTipSerializer
        if self.request.method == 'PATCH':
            return TopThreeTipUpdateserializer
        
    def get_queryset(self):
        user_profile = self.request.user.userprofile
        queryset = TopThreeTip.objects.filter(user_profile=user_profile)
        return queryset

    def perform_create(self, serializer):
        user_profile = self.request.user.userprofile
        serializer.save(user_profile=user_profile)

# class for HOME view 

class HomeView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = HomeSerializer

    def get(self, request, *args, **kwargs):
        user = request.user
        user_profile = UserProfile.objects.get(user=user)
       
        evaluated_tips = TopThreeTip.objects.filter(user_profile=user_profile, race__date__lt=timezone.now())
        upcoming_tips = TopThreeTip.objects.filter(user_profile=user_profile, race__date__gte=timezone.now())
        next_race = self.get_next_race()

        serialized_data = self.get_serializer({
            'profile': user_profile,
            'evaluated_tips': evaluated_tips,
            'upcoming_tips': upcoming_tips,
            'next_race': next_race,
            'score': user_profile.score,
        })

        return Response(serialized_data.data)

    def get_next_race(self):
        try:
            next_race = Race.objects.filter(date__gt=timezone.now()).earliest('date')
        except ObjectDoesNotExist:
            next_race = "Not scheduled"
        return next_race

# PROFILES 
    
class UserProfileViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'patch', 'delete']
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    serializer_class = UserProfileSerializer
    
    queryset= UserProfile.objects.all()

    def get_serializer_context(self):
        return {'request': self.request}

    def get_object(self):
        # Get the UserProfile object based on the user making the request
        user_id = self.kwargs['pk']
        return get_object_or_404(self.queryset.prefetch_related('tips'), user__id=user_id)

    

class RaceView(viewsets.ModelViewSet):
    http_method_names = ['get']

    queryset = Race.objects.all()
    
    serializer_class = RaceSerializer
    permission_classes = [IsAuthenticated]


class LeaderboardViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = UserProfile.objects.order_by('-score')  # Order by score in descending order
    serializer_class = LeaderboardSerializer