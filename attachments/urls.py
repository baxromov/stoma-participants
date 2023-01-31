from django.urls import path, include
from rest_framework.routers import DefaultRouter

from attachments.views import AttachmentsModelViewSet

router = DefaultRouter()

router.register('attachments', AttachmentsModelViewSet)

urlpatterns = [
    path('', include(router.urls))
]
