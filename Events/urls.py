from django.urls import path
from . import views
urlpatterns= [ 
    path('', views.EventView.as_view(), name='all-events'),
    path('create/event/', views.EventCreateView.as_view()),
    path('<uuid:pk>/', views.EventDetailView.as_view(), name='event-detail'),
    path('buy-ticket/', views.BuyTicketView.as_view(), name='buy-ticket'),
    path('create/event-ticket/', views.CreateEventTicketPrice.as_view()),
    path('categories/', views.CategoryView.as_view()), 
    path('update-trending-events/', views.TrendingEventView.as_view()),
    path('trending-events/', views.TrendingEventss.as_view())
]