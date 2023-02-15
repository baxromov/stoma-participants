from django.urls import path, include
from participant.views import ParticipantCreateAPIView, ParticipantsModelViewSet
from rest_framework import routers
router = routers.DefaultRouter()

router.register('participants', ParticipantsModelViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('', ParticipantCreateAPIView.as_view(), name='participant'),
]
