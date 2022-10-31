from django.urls import path 
from . import views
urlpatterns=[ 
    # path('withdraw/', views.WithdrawView.as_view()),
    path('make-payment/<uuid>/', views.Makepayment.as_view(), name='payment'),
    path('paystack-webhook/', views.PayStack_Webhook.as_view(), name='paystack-webhook'),
    # path('complete-withdrawal/<uuid>/', views.CompleteWithdrawal)
]