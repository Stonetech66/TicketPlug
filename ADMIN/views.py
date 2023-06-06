from django.shortcuts import render
from Events.permissions import IsAdmin
from rest_framework import generics, permissions
from .serializers import ApproveEventSerializer
from Events.models import Event




class UpdateEventstatus(generics.UpdateAPIView):
    serializer_class=ApproveEventSerializer
    permission_classes=[permissions.IsAuthenticated, IsAdmin]
    queryset=Event.objects.all()
