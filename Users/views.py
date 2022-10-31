from Events.serializers import EventSerializer
from rest_framework import generics, permissions
from Events.models import OrderTicket,  Event
from Transactions.models import Payment
from .serializers import ApproveEventSerializer, UserDashboardSerializer, UserPaymentHistory, UserBoughtTicketsHistory
from dj_rest_auth.views import PasswordResetView
from .serializers import PasswordResetSerializer
from Events.permissions import IsAdmin
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from dj_rest_auth.registration.views import  SocialLoginView
from allauth.socialaccount.providers.oauth2.client import OAuth2Client

class PaymentHistoryView(generics.ListAPIView):
    '''
    endpoint to see a user payment history
    '''
    serializer_class=UserPaymentHistory

    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user)


class MyboughtTickets(generics.ListAPIView):
    '''
    endpoint to see tickets bought by a user
    '''
    serializer_class=UserBoughtTicketsHistory

    def get_queryset(self):
        return OrderTicket.objects.filter(user=self.request.user, status='completed').prefetch_related('tickets', 'tickets__event_ticket', 'tickets__event_ticket__event')



class ListUnApprovedEvents(generics.ListAPIView):
    '''
    endpoin to list all unapproved events
    '''
    serializer_class=EventSerializer
    permission_classes=[permissions.IsAuthenticated, IsAdmin]

    def get_queryset(self):
        return Event.objects.filter(approved=False).select_related('user').prefetch_related('event_fees')

class UpdateEventstatus(generics.UpdateAPIView):
    '''
    endpoint to approve event
    '''
    serializer_class=ApproveEventSerializer
    permission_classes=[permissions.IsAuthenticated, IsAdmin]
    queryset=Event.objects.all()




class UserDashBoard(generics.RetrieveAPIView):
    serializer_class=UserDashboardSerializer

    def get_object(self):
        return self.request.user


class UserCreatedEvents(generics.ListAPIView):
    '''
    endpoint to see a user created events
    '''
    serializer_class=EventSerializer
    def get_queryset(self):
        return Event.objects.filter(user=self.request.user).select_related('user').prefetch_related('event_fees')

# class UserWalletBalanceView(generics.RetrieveAPIView):
#     serializer_class=WalletSerializer

#     def get_object(self):
#         return self.request.user

class PasswordResetView(PasswordResetView):
    serializer_class=PasswordResetSerializer
    permission_classes=[]




class GoogleLogin(SocialLoginView):
    adapter_class= GoogleOAuth2Adapter
    client_class=OAuth2Client
    callback_url="http://127.0.0.1:8000/"