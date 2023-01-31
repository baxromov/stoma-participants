from rest_framework.viewsets import ModelViewSet
from attachments.models import Attachments
from attachments.serializers import AttachmentsModelSerializer


class AttachmentsModelViewSet(ModelViewSet):
    queryset = Attachments.objects.all()
    serializer_class = AttachmentsModelSerializer
