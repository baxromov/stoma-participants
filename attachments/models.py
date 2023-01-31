from django.db import models

from participant.models.abstracts import BaseModel


class Attachments(BaseModel):
    file = models.FileField(upload_to='passports/')
