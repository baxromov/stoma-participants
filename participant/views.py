from django.views.generic import CreateView, ListView, TemplateView

from participant.forms.participants import ParticipantModelForm
from participant.models import Participant
from django_countries import countries


class ParticipantTemplateView(CreateView, ListView):
    model = Participant
    form_class = ParticipantModelForm
    template_name = 'main.html'
    success_url = 'success'


class SuccessTemplateView(TemplateView):
    template_name = 'success.html'
