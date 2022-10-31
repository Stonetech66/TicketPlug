from rest_framework import serializers
from .models import AdminSetting

class AdminSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model=AdminSetting
        fields=[ 
            'header_image',
            'payment_charge'
        ]



class  ContactForm(serializers.Serializer):
    Firstname=serializers.CharField()
    lastname=serializers.CharField()
    email=serializers.EmailField()
    message=serializers.CharField(min_length=10)