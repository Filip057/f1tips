from rest_framework_nested import routers
from . import views


router = routers.DefaultRouter()
router.register('tips', views.TopThreeViewSet, basename='top3')
router.register('profile', views.UserProfileViewSet, basename='profile')
router.register('races', views.RaceView, basename='race')
router.register('leaderboard', viewset=views.LeaderboardViewSet, basename='leaderboard')

urlpatterns = router.urls