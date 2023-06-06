from django.urls import path
from . import views
urlpatterns=[ 
    path('approve-event/<uuid:pk>/', views.UpdateEventstatus.as_view()),


]