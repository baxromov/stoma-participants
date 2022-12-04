from django.urls import path
from participant.views import ParticipantTemplateView, SuccessTemplateView

urlpatterns = [
    path('', ParticipantTemplateView.as_view(), name='participant'),
    path('success', SuccessTemplateView.as_view(), name='success')
]
