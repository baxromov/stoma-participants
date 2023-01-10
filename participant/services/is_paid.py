from django.db.models import Q
from participant.models import Participant


def is_paid_created_participant(data):
    """User is created only after successful payment"""
    return Participant.objects.filter(
        Q(instagram_username=data["instagram_username"]) | Q(phone=data["phone"])).exists()
