from django.urls import path
from . import views
urlpatterns=[ 
    path('payment-history/', views.PaymentHistoryView.as_view()),
    path('my-bought-tickets/', views.MyboughtTickets.as_view()),
    path('update-event-status/<uuid:id>/', views.UpdateEventstatus.as_view()),
    path('unapproved-events/', views.ListUnApprovedEvents.as_view()),
    path('dashboard/', views.UserDashBoard.as_view()),
    path('my-events/', views.UserCreatedEvents.as_view()),
    path('password-reset/', views.PasswordResetView.as_view())
]