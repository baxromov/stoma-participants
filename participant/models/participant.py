from django.db import models
from django_countries.fields import CountryField

from attachments.models import Attachments
from participant.models.abstracts import BaseModel
from pyclick.models import ClickTransaction


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

    @property
    def file(self):
        ct = ClickTransaction.objects.filter(participant_data__instagram_username=self.instagram_username).last()
        photos = ct.participant_data.get('photos')
        imgs = []
        if photos:
            for photo in photos:
                attachment = Attachments.objects.get(id=int(photo))
                imgs.append(attachment.file.url)
            return imgs
        return None
