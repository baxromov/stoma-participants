from django.urls import path
from participant.views import ParticipantTemplateView, SuccessTemplateView
from django_countries import countries

urlpatterns = [
    path('', ParticipantTemplateView.as_view(), name='participant'),
    path('success', SuccessTemplateView.as_view(), name='success')
]
