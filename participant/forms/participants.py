from django import forms
from django.contrib import messages
from django.forms import ModelForm, TextInput, ChoiceField
from django_countries.widgets import CountrySelectWidget
from instagrapi.exceptions import UserNotFound

from core.settings import INSTAGRAM_USER
from participant.models import Participant
from utils.instagramapi import ParseOneUserInstagram


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
        widgets = {
            'first_name': TextInput(attrs={'class': 'form-control'}),
            'last_name': TextInput(attrs={'class': 'form-control'}),
            'phone': TextInput(attrs={'class': 'form-control'}),
            'address': TextInput(attrs={'class': 'form-control'}),
            'instagram_username': TextInput(attrs={'class': 'form-control', 'label': 'Вы должны подписаться на страницу Instagram, тогда вы сможете продолжить!'}),
            'country': CountrySelectWidget(attrs={
                'class': 'form-select',
            }),
        }

    def clean(self):
        if "instagram_username" not in self.cleaned_data:
            raise forms.ValidationError('No user!')
        try:
            parser = ParseOneUserInstagram(self.cleaned_data["instagram_username"], INSTAGRAM_USER)
        except UserNotFound:
            raise forms.ValidationError('User doesn\'t exist')

        if not parser.is_following():
            raise forms.ValidationError('User not following!')
        return self.cleaned_data
