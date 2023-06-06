from django.db import models
from Users.models import User
import uuid
from Events.models import OrderTicket, TicketPrice








class Payment(models.Model):
    id=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    user=models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='user_payments')
    payment_id=models.CharField(max_length=30)
    amount=models.FloatField()
    ticket=models.OneToOneField(OrderTicket, on_delete=models.CASCADE, related_name='payment')
    date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.payment_id

    def get_event_owner_payment(self):
        return self.amount 

class SoldTicket(models.Model):
    id=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    payment=models.ForeignKey(Payment, on_delete=models.CASCADE )
    ticket=models.ForeignKey(TicketPrice, related_name='ticket', on_delete=models.SET_NULL, null=True)
    event=models.ForeignKey(OrderTicket, on_delete=models.SET_NULL, null=True, related_name='event_tickets')
    key=models.CharField(max_length=16)
    user=models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='user_purchased_tickets')
    used=models.BooleanField(default=False)

    def __str__(self):
        return str(self.user.email)
