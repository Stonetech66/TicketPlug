import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
import Events
import Transactions
# Create your models here.


class User(AbstractUser):
    email=models.EmailField(unique=True)
    id=models.UUIDField(default=uuid.uuid4,  editable=False, unique=True, primary_key=True)
    

    def get_total_amount_earned(self):
        c=Transactions.models.Payment.objects.filter(ticket__event__user=self)
        total=0
        for i in c:
            total += i.get_event_owner_payment()
        return total 

    def get_total_tickets_sold(self):
        p=Transactions.models.SoldTicket.objects.filter(ticket_class__event__user=self).count()
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



    
