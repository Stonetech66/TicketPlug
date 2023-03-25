from Events.serializers import EventSerializer
from rest_framework import generics, permissions
from Events.models import OrderTicket,  Event
from Transactions.models import Payment
from .serializers import ApproveEventSerializer, UserDashboardSerializer, UserPaymentHistory, UserBoughtTicketsHistory, UserEventSerializer
from dj_rest_auth.views import PasswordResetView
from .serializers import PasswordReset
from Events.permissions import IsAdmin
class PaymentHistoryView(generics.ListAPIView):
    serializer_class=UserPaymentHistory

    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user)


class MyboughtTickets(generics.ListAPIView):
    serializer_class=UserBoughtTicketsHistory

    def get_queryset(self):
        return OrderTicket.objects.filter(user=self.request.user, status='completed').prefetch_related('tickets', 'tickets__event_ticket', 'tickets__event_ticket__event')



class ListUnApprovedEvents(generics.ListAPIView):
    serializer_class=EventSerializer
    permission_classes=[permissions.IsAuthenticated, IsAdmin]

    def get_queryset(self):
        return Event.objects.filter(approved=False).select_related('user').prefetch_related('event_fees')

class UpdateEventstatus(generics.UpdateAPIView):
    serializer_class=ApproveEventSerializer
    permission_classes=[permissions.IsAuthenticated, IsAdmin]
    queryset=Event.objects.all()




class UserDashBoard(generics.RetrieveAPIView):
    serializer_class=UserDashboardSerializer

    def get_object(self):
        return self.request.user


class UserCreatedEvents(generics.ListAPIView):
    serializer_class=UserEventSerializer
    def get_queryset(self):
        return Event.objects.filter(user=self.request.user).select_related('user').prefetch_related('event_fees')

# class UserWalletBalanceView(generics.RetrieveAPIView):
#     serializer_class=WalletSerializer

#     def get_object(self):
#         return self.request.user

class PasswordResetview(PasswordResetView):
    serializer_class=PasswordReset
    permission_classes=[]

