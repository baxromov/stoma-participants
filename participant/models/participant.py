from django.db import models
from django_countries.fields import CountryField

from participant.models.abstracts import BaseModel


class Participant(BaseModel):
    first_name = models.CharField(max_length=63, verbose_name='Имя')
    last_name = models.CharField(max_length=63, verbose_name='Фамилия')
    phone = models.CharField(max_length=20, verbose_name='Телефон', unique=True)
    country = CountryField(verbose_name='Страна')
    address = models.CharField(max_length=255, verbose_name='Адрес')
    instagram_username = models.CharField(max_length=100, null=True, unique=True,
                                          verbose_name='Имя пользователя в инстаграме')

    class Meta:
        verbose_name_plural = 'Участник'

    def __str__(self):
        return self.instagram_username
