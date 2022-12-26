from django.urls import path
# from participant.views import ParticipantTemplateView, SuccessTemplateView
from participant.views import ParticipantCreateAPIView

urlpatterns = [
    path('', ParticipantCreateAPIView.as_view(), name='participant'),
]
