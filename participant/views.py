from django.views.generic import CreateView

from participant.forms.participants import ParticipantModelForm
from participant.models import Participant


class ParticipantTemplateView(CreateView):
    model = Participant
    form_class = ParticipantModelForm
    template_name = 'index.html'
    success_url = '/'
