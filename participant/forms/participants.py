from django.forms import ModelForm, TextInput, ChoiceField
from django_countries.widgets import CountrySelectWidget

from participant.models import Participant


class ParticipantModelForm(ModelForm):
    class Meta:
        model = Participant
        fields = [
            'first_name',
            'last_name',
            'phone',
            'address',
            'instagram_username',
            'country'
        ]
        exclude = ['created_at', 'updated_at']
        # widgets = {
        #     'first_name': TextInput(attrs={'class': 'form-control'}),
        #     'last_name': TextInput(attrs={'class': 'form-control'}),
        #     'phone': TextInput(attrs={'class': 'form-control'}),
        #     'address': TextInput(attrs={'class': 'form-control'}),
        #     'instagram_username': TextInput(attrs={'class': 'form-control'}),
        #     'country': CountrySelectWidget(attrs={
        #         'class': 'form-select',
        #     }),
        # }
