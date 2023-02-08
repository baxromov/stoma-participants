from typing import Optional

from rest_framework import status

from participant.services import is_paid_created_participant, cancel_previous_transactions
from pyclick.views import PyClickMerchantAPIView

from core.settings import DEFAULT_AMOUNT, RETURN_URL
from pyclick.models import ClickTransaction
from rest_framework.response import Response
from rest_framework.views import APIView

from instagrapi.exceptions import UserNotFound

from core.settings import INSTAGRAM_USER
from utils.instagramapi import ParseOneUserInstagram
import logging

logging.basicConfig(
    filename="test.log",
    level=logging.INFO,
    format="%(asctime)s:%(levelname)s:%(message)s"
)


class ParticipantCreateAPIView(APIView):
    def post(self, request):
        logging.info("hello world")
        request.data["instagram_username"] = request.data["instagram_username"].lstrip("@")

        if is_paid_created_participant(request.data):
            return Response({"error": "Пользователь уже прошёл регистрацию"}, status=status.HTTP_400_BAD_REQUEST)
        if error := check_instagram(request.data["instagram_username"]):
            return error

        photos_info = request.data.pop("dragger")
        request.data["photos"] = [str(photo["response"]["id"]) for photo in photos_info]
        cancel_previous_transactions(request.data)
        transaction = ClickTransaction.objects.create(participant_data=request.data, amount=DEFAULT_AMOUNT)
        url = PyClickMerchantAPIView.generate_url(order_id=transaction.id, amount=transaction.amount,
                                                  return_url=RETURN_URL)
        return Response({"redirect_url": url}, status=status.HTTP_200_OK)


def check_instagram(instagram_username) -> Optional[Response]:
    try:
        parser = ParseOneUserInstagram(instagram_username, INSTAGRAM_USER)
    except UserNotFound:
        return Response({"error": "Пользователь не существует"}, status=status.HTTP_400_BAD_REQUEST)
    if not parser.is_following():
        return Response({"error": "Пользователь не подписан"}, status=status.HTTP_400_BAD_REQUEST)
