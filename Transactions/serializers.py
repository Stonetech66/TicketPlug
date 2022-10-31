from rest_framework import serializers



class PaymentSErializer(serializers.Serializer):
    email=serializers.EmailField(required=False)
    
# class WithdrawSerializer(serializers.Serializer):
#     amount=serializers.FloatField()
