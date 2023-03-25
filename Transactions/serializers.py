from rest_framework import serializers



class PaymentSErializer(serializers.Serializer):
    email=serializers.EmailField(required=False)
    
class TicketSerializer(serializers.Serializer):
    ticket=serializers.CharField(read_only=True, source='event_ticket.label')
    qty=serializers.IntegerField(read_only=True)
    total=serializers.FloatField(read_only=True, source="get_total_ticket_price")
class CheckoutSerializer(serializers.Serializer):
    event= serializers.CharField(source="event.name", read_only=True)
    tickets= TicketSerializer(read_only=True, many=True,)
    total= serializers.FloatField(source="get_total_price", read_only=True)
# class WithdrawSerializer(serializers.Serializer):
#     amount=serializers.FloatField()
