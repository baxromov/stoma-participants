from django.db.models import Q

from pyclick.models import ClickTransaction


def cancel_previous_transactions(data):
    ClickTransaction.objects.filter(
        Q(participant_data__phone=data["phone"]) | Q(participant_data__instagram_username=data["instagram_username"])
    ).update(status=ClickTransaction.CANCELED)
