from django.db import models
from django_countries.fields import CountryField

from participant.models.abstracts import BaseModel


class Participant(BaseModel):
    first_name = models.CharField(max_length=63, verbose_name='Имя', null=True)
    last_name = models.CharField(max_length=63, verbose_name='Фамилия', null=True)
    phone = models.CharField(max_length=20, verbose_name='Телефон', unique=True, null=True)
    country = CountryField(verbose_name='Страна', null=True)
    address = models.CharField(max_length=255, verbose_name='Адрес', null=True)
    instagram_username = models.CharField(max_length=100, null=True, unique=True,
                                          verbose_name='Имя пользователя в инстаграме')

    class Meta:
        verbose_name_plural = 'Участник'
