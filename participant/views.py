from django.views.generic import CreateView, ListView

from participant.forms.participants import ParticipantModelForm
from participant.models import Participant
from django_countries import countries


class ParticipantTemplateView(CreateView, ListView):
    model = Participant
    form_class = ParticipantModelForm
    template_name = 'main.html'
    success_url = '/'

    def get_context_data(self, **kwargs):
        ctx = super(ParticipantTemplateView, self).get_context_data(**kwargs)
        ctx['countries'] = dict(countries)
        return ctx
