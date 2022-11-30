from django.urls import path
from participant.views import ParticipantTemplateView
from django_countries import countries
print(dict(countries))
urlpatterns = [
    path('', ParticipantTemplateView.as_view(), name='participant')
]
