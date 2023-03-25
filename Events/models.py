from django.db import models
from cloudinary.models import CloudinaryField
from Users.models import User
import uuid
from django.core.exceptions import ValidationError

class Category(models.Model):
    name=models.CharField(max_length=50, unique=True, primary_key=True)


    class Meta:
        verbose_name_plural= "categories"
        ordering=["name"]
    def __str__(self): 
        return self.name
    


    def clean(self, *args, **kwargs):
        c=Category.objects.filter(name__iexact=self.name)
        if c.exists():
            raise ValidationError({'name':'category with this name already exists'})
        return c
    



class Event(models.Model):
    user=models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    id=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    name=models.CharField(max_length=500)
    country=models.CharField(max_length=300)
    category=models.ManyToManyField(Category, related_name= 'event_categories')
    city=models.CharField(max_length=300)
    state=models.CharField(max_length=300)
    address=models.CharField(max_length=400)
    tags=models.CharField(max_length=500,default=[] ,blank=True)
    description=models.TextField()
    image=CloudinaryField('images', null=True, blank=True)
    approved=models.BooleanField(default=False)
    date_added=models.DateTimeField(auto_now_add=True)
    start_date=models.DateTimeField()
    end_date=models.DateTimeField()

    class Meta:
        ordering= ['-date_added']
        indexes=[models.Index(fields=['date_added', 'approved'])]

    def __str__(self):
        return self.name

    def total_tickets_sold(self)-> int:
        total=0
        for i in self.event_fees.all():
            total += i.sold
        return total
    
 


class TicketPrice(models.Model):
    label=models.CharField(max_length=50)
    price=models.FloatField(default=0)
    event=models.ForeignKey(Event, on_delete=models.CASCADE, related_name='event_fees')
    description=models.TextField()
    is_free=models.BooleanField(default=False)
    sold=models.PositiveIntegerField(default=0)
    qty=models.PositiveIntegerField(default=0)


    def save(self, *args, **kwargs):
        if self.is_free:
            self.price= 0
        return super().save(*args, **kwargs)

    
    def get_tickets_available(self):
        return self.qty - self.sold

    def __str__(self)->str:
        return f"{self.event} ({self.label})"


class BuyTicket(models.Model):
    id=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_tickets', null=True)
    event_ticket=models.ForeignKey(TicketPrice, on_delete=models.SET_NULL, null=True)
    qty=models.PositiveIntegerField(default=1)
    emails=models.CharField(max_length=9000, blank=True, null=True)
    order=models.ForeignKey('OrderTicket', on_delete=models.CASCADE, related_name='tickets')
    date=models.DateTimeField(auto_now_add=True)
    completed=models.BooleanField(default=False)



    def get_total_ticket_price(self):
        return self.event_ticket.price * self.qty



Order_Status=[ 
    ('completed', 'completed'),
    ('not completed', 'not completed')
]

class OrderTicket(models.Model):
    id=models.UUIDField(default=uuid.uuid4,editable=False, primary_key=True )
    event=models.ForeignKey(Event, on_delete=models.SET_NULL, null=True, related_name='event_orders')
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_orders', null=True)
    status=models.CharField(choices=Order_Status, max_length=20, default='not completed')
    date=models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=['-date']
    
    def __str__(self):
        return str(self.user)

    def get_total_price(self):
        total=0
        for i in self.tickets.all():
            total += i.get_total_ticket_price()
        return total




class TrendingEvents(models.Model):
    events=models.ManyToManyField(Event, related_name='events')

