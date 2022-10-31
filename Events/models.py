from django.db import models
from Users.models import User
from ADMIN.models import AdminSetting
from django.template.defaultfilters import slugify
import uuid
# Create your models here.

class Category(models.Model):
    name=models.CharField(max_length=50, unique=True)
    slug=models.SlugField(max_length=50, editable=False, primary_key=True)

    def __str__(self):
        return self.name

    def clean(self, *args, **kwargs):
        c=Category.objects.filter(name__iexact=self.name)
        if c.exists():
            raise ValueError({'name':'category with this name already exists'})
        return c
    
    def save(self, *args, **kwargs):
        self.slug=slugify(self.name)
        super().save(*args, **kwargs)


class Event(models.Model):
    user=models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    id=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    name=models.CharField(max_length=500)
    country=models.CharField(max_length=300)
    category=models.ManyToManyField(Category, related_name= 'event_categories')
    city=models.CharField(max_length=300)
    state=models.CharField(max_length=300)
    address=models.CharField(max_length=400)
    tags=models.CharField(max_length=500, null=True, blank=True)
    description=models.TextField()
    image_1=models.ImageField(null=True, blank=True, upload_to='media/')
    image_2=models.ImageField(null=True, blank=True, upload_to='media/')
    image_3=models.ImageField(null=True, blank=True, upload_to='media/')
    approved=models.BooleanField(default=False)
    date_added=models.DateTimeField(auto_now_add=True)
    start_date=models.DateTimeField()
    end_date=models.DateTimeField()

    class Meta:
        ordering= ['-date_added']

    def __str__(self):
        return self.name
    
 


class TicketPrice(models.Model):
    label=models.CharField(max_length=50)
    price=models.FloatField()
    event=models.ForeignKey(Event, on_delete=models.CASCADE, related_name='event_fees')
    description=models.TextField()

    def __str__(self):
        return f"{self.event} ({self.label})"


class BuyTicket(models.Model):
    id=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_tickets')
    event_ticket=models.ForeignKey(TicketPrice, on_delete=models.SET_NULL, null=True)
    qty=models.PositiveIntegerField(default=1)
    emails=models.CharField(max_length=9000, blank=True, null=True)
    date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.event_ticket.event.name

    def get_total_ticket_price(self):
        return self.event_ticket.price * self.qty



Order_Status=[ 
    ('completed', 'completed'),
    ('not completed', 'not completed')
]

class OrderTicket(models.Model):
    id=models.UUIDField(default=uuid.uuid4,editable=False, primary_key=True )
    event=models.ForeignKey(Event, on_delete=models.SET_NULL, null=True, related_name='event_orders')
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_orders')
    tickets=models.ManyToManyField(BuyTicket)
    status=models.CharField(choices=Order_Status, max_length=20, default='not completed')
    date=models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=['-date']
    
    def __str__(self):
        return self.event.name

    def get_total_price(self):
        total=0
        for i in self.tickets.all():
            total += i.get_total_ticket_price()
        return total




class TrendingEvents(models.Model):
    events=models.ManyToManyField(Event, related_name='events')

