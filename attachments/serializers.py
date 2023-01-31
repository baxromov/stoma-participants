from rest_framework import serializers
from attachments import models


class AttachmentsModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Attachments
        fields = '__all__'

    def create(self, validated_data):
        attachments = super(AttachmentsModelSerializer, self).create(validated_data)
        return attachments
