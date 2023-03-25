import uuid
from django.db import models
import Events
import Transactions
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import uuid


class UserManager(BaseUserManager):
    def create_user(self, email, password, first_name:str=None, last_name:str=None,):

        if not email:
            raise TypeError("Users must have an email")
    
        
        user= self.model(email=self.normalize_email(email), first_name= first_name, last_name=last_name)
        user.set_password(password)
        user.save(using=self.db)
        return user


    def create_superuser(self, email, password,first_name:str=None, last_name:str=None, ):

        user=self.create_user(email=email, password=password, first_name=first_name, last_name=last_name)
        user.is_superuser=True
        user.is_staff= True
        user.save(using=self.db)
        
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email=models.EmailField(unique=True, max_length=255)
    first_name= models.CharField(max_length=100, null=True)
    last_name=models.CharField(max_length=100, null=True)
    id= models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    is_active= models.BooleanField(default=True)
    is_staff= models.BooleanField(default=False)
    is_superuser=models.BooleanField(default=False)
    objects= UserManager()
    USERNAME_FIELD="email"

    @property
    def fullname(self):
        return f"{self.first_name} {self.last_name}"
    
    def __str__(self):
        return self.email

    def get_total_amount_earned(self):
        c=Transactions.models.Payment.objects.filter(ticket__event__user=self)
        total=0
        for i in c:
            total += i.get_event_owner_payment()
        return total 

    def get_total_tickets_sold(self):
        p=Transactions.models.SoldTicket.objects.filter(ticket__event__user=self).count()
        return p

    def get_total_event_created(self):
        event=Events.models.Event.objects.filter(user=self)
        return event.count()


    # def get_total_withdrawn_amount(self):
    #     c=Transactions.models.Withdrawal.objects.filter(user=self, status='completed')
    #     total=0
    #     for i in c:
    #         total += i.amount
    #     return total

    # def get_wallet_balance(self):
    #     return self.get_total_amount_earned() - self.get_total_withdrawn_amount()



    
