from django.urls import path 
from . import views
urlpatterns=[ 

    path('make-payment/<uuid:pk>/', views.Makepayment.as_view(), name='payment'),
    path('paystack-webhook/', views.PayStack_Webhook.as_view(), name='paystack-webhook'),
    path('verify-qrcode/<uuid:event>/<int:key>/',views.VerifyQrcode.as_view(), name='verify-qrcode')

]
