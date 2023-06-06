from rest_framework import serializers
from Events.models import Event



class ApproveEventSerializer(serializers.ModelSerializer):
    class Meta:
        model=Event
        fields=['approved']