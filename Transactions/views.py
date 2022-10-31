from Events.models import OrderTicket, BuyTicket
from rest_framework import generics, status
from .serializers import PaymentSErializer
from rest_framework.views import APIView
from ADMIN.models import AdminSetting
import requests
from django.conf import settings
from .tasks import Create_PaymentRecord
from rest_framework.response import Response
from rest_framework.response import Response
# Create your views here.


class Makepayment(APIView):
    '''
    endpoint to make payment, if the user is sending the tickets to only one email it should be put in the email field
    '''
    serializer_class =PaymentSErializer
    def get_serializer(self):
        return PaymentSErializer()

    def post(self, *args, **kwargs):
        serializer=self.serializer_class(data=self.request.data)
        p=self.kwargs['uuid']
        j=OrderTicket.objects.filter(user=self.request.user, id=p, status='not completed')
        if j.exists():
            if serializer.is_valid(raise_exception=True):
                j=j.last()
                price=j.get_total_price()
                user=str(self.request.user.id)
                email=serializer.validated_data.get('email')
                u_e=str(self.request.user.email)
                url='https://api.paystack.co/transaction/initialize'
                header={'authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}'}
                try:
                    resp=requests.post(url, timeout=100, headers=header, json={'amount':price*100, 'email':u_e, 'metadata':{'user_id':user, 'bought_ticket_id':p, 'price':price,'email':email, },})
                    return Response(resp.json())
                except Exception as e:
                    return Response({'error': f'{e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({'error':'invalid uuid or you have not selected a ticket yet'}, status=status.HTTP_404_NOT_FOUND)

class PayStack_Webhook(APIView):
    '''
    This does not concern you
    '''
    permission_classes=[]
    swagger_schema=None
    def post(self,request, *args, **kwargs):
        c=request.data
        if c['event']== 'charge.success':
            user_id=c['data']['metadata']['user_id']
            bought_ticket=c['data']['metadata']['bought_ticket_id']
            price=c['data']['metadata']['price']
            email=c['data']['metadata']['email']
            print(bought_ticket)
            Create_PaymentRecord(amount=price, email=email, user_id=user_id, bought_ticket_id=bought_ticket)
            return Response({'message':'ok'},status=status.HTTP_200_OK)
        return Response(status=status.HTTP_200_OK)

# class WithdrawView(APIView):
#     serializer_class=WithdrawSerializer

#     def post(self, request,*args, **kwrargs):
#         serializer=WithdrawSerializer(data=request.data)
#         minimum_withdrawal=AdminSetting.objects.last().minimum_withdrawal
#         wallet=request.user.get_wallet_balance() 
#         if wallet< minimum_withdrawal:
#             return Response({'error':'Insufficient balance'})
#         if serializer.is_valid(raise_exception=True):
#             amount=serializer.validated_data.get('amount')
#             if amount > wallet:
#                 return Response({'error':'insufficient balance your requested amount is greater than your wallet balance'})
#             else:
#                 p=Withdrawal.objects.create(user=request.user, amount=amount)
#                 return Response({'withdrawal-link'})


# class CompleteWithdrawal(APIView):
#     def post(self, request,*args, **kwargs):
#         uid=self.kwargs['uuid']
#         user=request.user.id
#         w=Withdrawal.objects.filter(uid=uid, user=request.user, status='requested')
#         if w.exists():
#             # url= 
#             # headers=
#             # resp=requests.post(url, headers=headers, json={})
#             #return Response(resp.json())
        

    
