from django.urls import reverse
from Events.models import Event
from Events.serializers import EventSerializer
from .models import User
from rest_framework import serializers
from dj_rest_auth.serializers import PasswordResetSerializer
from allauth.account import models
from django.contrib.auth import authenticate 
class EventTicketSerializer(serializers.Serializer):
    event=serializers.StringRelatedField(read_only=True)
    label=serializers.CharField(read_only=True)
    price=serializers.FloatField(read_only=True)
    is_free=serializers.BooleanField(read_only=True)
    qty=serializers.IntegerField()
    available_tickets=serializers.IntegerField(read_only=True, source="get_available_tickets")
    sold=serializers.IntegerField(read_only=True)



class UserEventSerializer(EventSerializer):
    total_tickets_sold=serializers.SerializerMethodField()
    tickets=EventTicketSerializer(many=True, read_only=True, source='event_fees')
    def get_total_tickets_sold(self, obj):
        return obj.total_tickets_sold()


class BoughtTicketSerializer(serializers.Serializer):
    ticket=serializers.CharField(read_only=True, source='event_ticket.label')
    qty=serializers.IntegerField(read_only=True)

class UserBoughtTicketsHistory(serializers.Serializer):
    event_id= serializers.UUIDField(read_only=True, source="event.id")
    event=serializers.StringRelatedField()
    tickets=BoughtTicketSerializer(read_only=True, many=True)
  



    


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



class PasswordReset(PasswordResetSerializer):
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
    email=serializers.EmailField(read_only=True)
    first_name=serializers.CharField(read_only=True)
    last_name=serializers.CharField(read_only=True)
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

class RegisterSerializer(serializers.Serializer):
     email=serializers.EmailField()
     first_name=serializers.CharField()
     last_name=serializers.CharField()
     password=serializers.CharField()
    
     def save(self, request):
        email=self.data.get('email')
        first_name=self.data.get('first_name')
        last_name=self.data.get('last_name')
        password=self.data.get('password')
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('user with this email already exists') 
        user=User.objects.create_user(email=email,first_name=first_name,last_name=last_name, password=password)
        return user
class LoginSerializer(serializers.Serializer):
    email=serializers.EmailField()
    password=serializers.CharField()

    def validate(self, attrs):
       user=authenticate(email=attrs['email'], password=attrs['password']) 
       if user ==None:
           raise serializers.ValidationError('invalid email or password') 
       return attrs
       
