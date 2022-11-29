from django.urls import path
from participant.views import ParticipantTemplateView

urlpatterns = [
    path('', ParticipantTemplateView.as_view(), name='home')
]
