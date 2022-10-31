from django.shortcuts import render
from Events.permissions import IsAdmin
from rest_framework import generics, permissions

from ADMIN.models import AdminSetting

from .serializers import AdminSettingSerializer
# Create your views here.

class AdminSettings(generics.RetrieveUpdateAPIView):
    serializer_class=AdminSettingSerializer
    permission_classes=[permissions.IsAuthenticated, IsAdmin]

    def get_object(self):
        return AdminSetting.objects.last()

