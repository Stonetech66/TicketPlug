from .permissions import IsAdmin, IsAdminorReadOnly, IsOwner
from .serializers import BuyTicketSerializer,  CategorySerializer, EventCreateSerializer, EventSerializer, CreateEventPriceSerializer, TrendingEventSerializer
from rest_framework import generics, permissions, status, filters
from .models import Category, Event, BuyTicket, OrderTicket, TicketPrice, TrendingEvents
from rest_framework.views import APIView
from rest_framework.response import Response
from django.urls import reverse
from django_filters.rest_framework import DjangoFilterBackend
import pytz
from datetime import datetime, timedelta



class EventView(generics.ListAPIView):
    '''
    List all events that has been be approved by the admin
    
    '''
    serializer_class=EventSerializer
    permission_classes=[]
    filter_backends=[DjangoFilterBackend]
    filterset_fields=['category', 'country']
    search_fields=['name', 'city', 'category__name', 'country']


    def get_queryset(self):
        return Event.objects.filter(approved=True, end_date__gt=datetime.now(tz=pytz.timezone('UTC'))-timedelta(hours=1)).select_related('user').prefetch_related('event_fees')


class EventCreateView(generics.CreateAPIView):
    '''
    endpoint to create an event 
    
    '''
    serializer_class=EventCreateSerializer
    queryset=Event.objects.all()

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

class CreateEventTicketPrice(generics.CreateAPIView):
    '''
   endpoint  to create  tickets for a particular event
   Note: only the owner of a event can create the prices
    '''
    serializer_class=CreateEventPriceSerializer
    queryset=TicketPrice.objects.all()

    
class EventDetailView(generics.RetrieveUpdateDestroyAPIView):
    '''
    endpoint to get all details of a particular Event
    '''
    serializer_class=EventCreateSerializer
    permission_classes=[IsOwner]


    
    def get_queryset(self):
        return Event.objects.all().select_related('user').prefetch_related('event_fees', 'category')

class RemoveTicketView(APIView):
    def post(self, *args, **kwargs):
        pk=self.kwargs["pk"]
        try:
            ticket=TicketPrice.objects.get(id=pk)
            order=OrderTicket.objects.get(user=self.request.user, status= "not completed", event=ticket.event)
            BuyTicket.objects.delete(id=pk, completed=False, order=order)
            return Response({"message": "success"}, status=status.HTTP_204_NO_CONTENT)
        except:
            return Response({"message":"ticket dosent exists or ticket not added"}, status=status.HTTP_400_BAD_REQUEST)
        
class BuyTicketView(APIView):

    serializer_class= BuyTicketSerializer

    def get_serializer(self):
        return BuyTicketSerializer()

    def post(self, request, *args, **kwargs):

        serializer=self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
                    user=self.request.user
                    event_ticket=self.kwargs["event"]
                    qty=serializer.validated_data.get('qty')
                    emails=serializer.validated_data.get('emails')
                    try:
                        ticket=TicketPrice.objects.get(id=event_ticket)
                        if ticket.get_tickets_available() == 0:
                            return Response({'error':'tickets sold out'}, status=status.HTTP_400_BAD_REQUEST)
                        elif ticket.get_tickets_available() < qty:
                            return Response({'error':'tickets available not up to this qty'}, status=status.HTTP_400_BAD_REQUEST)

                    except:
                        return Response({'error':'This ticket cant be found'}, status=status.HTTP_404_NOT_FOUND)
                    order, created=OrderTicket.objects.get_or_create(user=request.user, status='not completed' , event=ticket.event)
                    try:
                        c=BuyTicket.objects.get(user=user, event_ticket=ticket, completed=False, order=order)
                        c.qty=qty
                        c.emails=emails
                        c.save()
                    except:
                        c=BuyTicket.objects.create(user=user, event_ticket=ticket, qty=qty, emails=emails, order=order)
                    return Response({"payment-link":reverse('payment', kwargs={'pk':order.id}), 'amount_to_pay':order.get_total_price()})






class CategoryView(generics.ListCreateAPIView):
    '''
    (GET: endpoint to list all the categories of events)
    (POST: endpoint to create a category)
    '''

    queryset=Category.objects.all()
    serializer_class=CategorySerializer
    permission_classes=[IsAdminorReadOnly]

class TrendingEventss(generics.ListAPIView):
    '''
    endpoint to list all trending events
    '''
    serializer_class=EventSerializer
    permission_classes=[]

    def get_queryset(self):
        try:
  
           return TrendingEvents.objects.prefetch_related('events').last().events.all().select_related('user').prefetch_related('event_fees')
        except:
            return [] 

class TrendingEventView(generics.UpdateAPIView):
    '''
    endpoint to update the trending events, just input the id of the events you want to be trending
    '''
    serializer_class=TrendingEventSerializer
    permission_classes=[permissions.IsAuthenticated, IsAdmin]
    


    def get_object(self):
        return TrendingEvents.objects.prefetch_related('events').last()







