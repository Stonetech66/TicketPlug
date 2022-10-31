from .permissions import IsAdmin, IsAdminorReadOnly, IsOwner
from .serializers import BuyTicketSerializer,  CategorySerializer, EventCreateSerializer, EventSerializer, CreateEventPriceSerializer, TrendingEventSerializer
from rest_framework import generics, permissions, status, filters
from .models import Category, Event, BuyTicket, OrderTicket, TicketPrice, TrendingEvents
from rest_framework.views import APIView
from rest_framework.response import Response
from django.urls import reverse
from django.core.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend




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
        return Event.objects.filter(approved=True).select_related('user').prefetch_related('event_fees')


class EventCreateView(generics.CreateAPIView):
    '''
    endpoint to Create a event 
    
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


class BuyTicketView(APIView):
    '''
    (*important A GET request must be made first when the user wants to buy a ticket for a event, it should be made only once and with a query parameter event= id of the event the user wants to buy e.g ( `buy-ticket/?event=(id of the evnt the user wants to buy` )))
    (POST: endpoint to buy a ticket  Note:  if a user decides to send the ticket to more than one email, the emails should be put in a list  and added to the emails field else if the user picks one email the email should be put in this endpoint endpoint(make-payment/)
    ( *fields:  ticket_id: ( ` id of the event ticket that the user wants to buy` ), qty: ( `quantity of the ticket the user wants to buy should be an integer` ), emails: (` a list of the emails the user wants to send the tickets to can be left blank` ) )
    '''
    serializer_class= BuyTicketSerializer

    def get_serializer(self):
        return BuyTicketSerializer()

    def get(self, request, *args, **kwargs):
        event=str(request.GET.get('event'))
        if event == None:
            return Response({'error':'You must include the event query in your get request which must contain the id of the event'})
        try:
            p=OrderTicket.objects.filter(user=request.user, event__id=event ,status='not completed')
        except ValidationError:
            return Response({"message":'invalid event uid'}, status=status.HTTP_400_BAD_REQUEST)
        if p.exists():
            p=p.last()
            p.tickets.clear()
            return Response({'message':'user has incomplete order'})
        return Response({"message":'no incomplete order'})

    def post(self, request, *args, **kwargs):

        serializer=self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
                user=self.request.user
                event_ticket=serializer.validated_data.get('event_ticket')
                print(event_ticket)
                qty=serializer.validated_data.get('qty')
                emails=serializer.validated_data.get('emails')
                if emails != None and len(emails) != qty:
                    return Response({'emails':'incomplete emails provided, qty and emails dont match'}, status=status.HTTP_400_BAD_REQUEST)
                p=TicketPrice.objects.filter(id=event_ticket)
                if p.exists():
                    c=BuyTicket.objects.create(user=user, event_ticket=p.last(), qty=qty, emails=str(emails))
                    try:
                        p=OrderTicket.objects.get(user=request.user,event=c.event_ticket.event, status='not completed' )
                    except:
                        p=OrderTicket.objects.create(user=request.user, event=c.event_ticket.event)
                    p.tickets.add(c)
                    p.save()
                    return Response({"payme-link":reverse('payment', kwargs={'uuid':p.id}), 'amount_to_pay':p.get_total_price()})
                return Response({'error':'invalid ticket id entered'}, status=status.HTTP_400_BAD_REQUEST)



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
        return TrendingEvents.objects.prefetch_related('events').last().events.all().select_related('user').prefetch_related('event_fees')


class TrendingEventView(generics.UpdateAPIView):
    '''
    endpoint to update the trending events, just input the id of the events you want to be trending
    '''
    serializer_class=TrendingEventSerializer
    permission_classes=[permissions.IsAuthenticated, IsAdmin]
    


    def get_object(self):
        return TrendingEvents.objects.prefetch_related('events').last()







