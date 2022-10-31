from django.urls import reverse
from Events.models import Event
from .models import User
from rest_framework import serializers
from dj_rest_auth.serializers import PasswordResetSerializer
from allauth.account import models

class EventTicketSerializer(serializers.Serializer):
    event=serializers.StringRelatedField(read_only=True)
    label=serializers.CharField(read_only=True)
    price=serializers.FloatField(read_only=True)


class BoughtTicketSerializer(serializers.Serializer):
    ticket=serializers.CharField(read_only=True, source='event_ticket.label')
    qty=serializers.IntegerField(read_only=True)

class UserBoughtTicketsHistory(serializers.Serializer):
    event_link=serializers.SerializerMethodField()
    event=serializers.StringRelatedField()
    tickets=BoughtTicketSerializer(read_only=True, many=True)
  


    def get_event_link(self, obj):
        return reverse('event-detail', kwargs={'pk':obj.event.id})
    


class UserPaymentHistory(serializers.Serializer):
    payment_id=serializers.CharField(read_only=True)
    amount=serializers.FloatField(read_only=True)
    date=serializers.DateTimeField(read_only=True)

class ApproveEventSerializer(serializers.ModelSerializer):
    class Meta:
        model=Event
        fields=['approved']


class UserDashboardSerializer(serializers.Serializer):
    total_amount_earned=serializers.SerializerMethodField()
    total_tickets_sold=serializers.SerializerMethodField()
    total_event_created=serializers.SerializerMethodField()

    def get_total_amount_earned(self, obj):
        return obj.get_total_amount_earned()

    def get_total_tickets_sold(self, obj):
        return obj.get_total_tickets_sold()
    
    def get_total_event_created(self, obj):
        return obj.get_total_event_created()



class UserCreatedEvents(serializers.Serializer):
    name=serializers.CharField(read_only=True)



class PasswordResetSerializer(PasswordResetSerializer):
    class Meta:
        ref_name='password reset'

    def validate_email(self, value):
        # Create PasswordResetForm with the serializer
        self.reset_form = self.password_reset_form_class(data=self.initial_data)
        if not self.reset_form.is_valid():
            raise serializers.ValidationError(self.reset_form.errors)
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError('user with this email does not exists')
        return value

class UserDetailSerializer(serializers.Serializer):
    id=serializers.UUIDField(read_only=True)
    username=serializers.CharField()
    email=serializers.EmailField(read_only=True)
    is_superuser=serializers.BooleanField(read_only=True)
    is_staff=serializers.BooleanField(read_only=True)
    email_confirmed=serializers.SerializerMethodField()


    def get_email_confirmed(self, obj,):
        p=models.EmailAddress.objects.filter(email=obj.email)
        if p.exists():
            if p.last().verified == True:
                return True
            return False
        return False

