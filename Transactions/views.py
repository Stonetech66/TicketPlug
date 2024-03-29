from Events.models import OrderTicket
from rest_framework import generics, status
from .serializers import PaymentSErializer, CheckoutSerializer
from rest_framework.views import APIView
import requests
from django.conf import settings
from .tasks import create_payment_record, payment_failed
from rest_framework.response import Response

# Create your views here.
from . models import SoldTicket

class Makepayment(APIView):
    '''
    endpoint to make payment, if the user is sending the tickets to only one email it should be put in the email field
    '''
    serializer_class =PaymentSErializer
    def get_serializer(self):
        return PaymentSErializer()

    def get(self , *args, **kwargs):
        user=self.request.user
        id= self.kwargs["pk"]
        try:
          order=OrderTicket.objects.get(id=id, user=user, status='not completed')
          return Response(CheckoutSerializer(order).data)

        except:
             return Response({"error":" invalid id or you dont have any tickets for this event"}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, *args, **kwargs):
        serializer=self.serializer_class(data=self.request.data)
        pk=self.kwargs['pk']
        order=OrderTicket.objects.filter(user=self.request.user, id=pk, status='not completed')
        if order.exists():
            if serializer.is_valid(raise_exception=True):
                order=order.last()
                price=order.get_total_price()
                user_id=str(self.request.user.id)
                email=serializer.validated_data.get('email')
                user_email=str(self.request.user.email)
                if price == 0:
                     create_payment_record.delay(amount=price, email=email, user_id=user_id, bought_ticket_id=pk)
                     return Response({"message" :"checkout successful, check your email to find your tickets"}) 
                else:    
                  url='https://api.paystack.co/transaction/initialize'
                  header={'authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}'}
                  try:
                    resp=requests.post(url, timeout=100, headers=header, json={'amount':price*100, 'email':user_email, 'metadata':{'user_id':str(user), 'bought_ticket_id':str(p), 'price':price,'email':email, },})
                    return Response(resp.json())
                  except Exception as e:
                    return Response({'error': f'{e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({'error':'invalid uuid or you have not selected a ticket yet'}, status=status.HTTP_404_NOT_FOUND)

class PayStack_Webhook(APIView):
    permission_classes=[]
    swagger_schema=None
    def post(self,request, *args, **kwargs):
        data=request.data
        if data['event']== 'charge.success':
            user_id=data['data']['metadata']['user_id']
            bought_ticket=data['data']['metadata']['bought_ticket_id']
            price=data['data']['metadata']['price']
            email=data['data']['metadata']['email']
            create_payment_record(amount=price, email=email, user_id=user_id, bought_ticket_id=bought_ticket)

        elif data['event'] =='charge.failed':
            user_id=data['data']['metadata']['user_id']
            bought_ticket=data['data']['metadata']['bought_ticket_id']
            price=data['data']['metadata']['price']
            email=data['data']['metadata']['email']
            payment_failed(amount=price, email=email, user_id=user_id, bought_ticket_id=bought_ticket)      
        return Response(status=status.HTTP_200_OK)


    
class VerifyQrcode(APIView):
    permission_classes=[] 
    def get(self, *args, **kwargs):
        event=self.kwargs['event']
        key= self.kwargs['key']
        try:        
          ticket= SoldTicket.objects.select_related("ticket").get(ticket__event__id=event, key=key, used=False)
          return Response({'valid':True, 'event':{"id":ticket.ticket.event.id,"name":ticket.ticket.event.name, 'label':ticket.ticket.label,}})
        except:
           return Response({'valid':False}) 

