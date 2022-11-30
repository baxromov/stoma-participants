from django.db import models

# Create your models here.
from payments.models import BasePayment


class Payment(BasePayment):
    pass
