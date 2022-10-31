from django.contrib import admin
from .models import Payment, SoldTicket
# Register your models here.

def deactivate_tickets(modeladmin, request, queryset):
    queryset.update(inactive=True)
deactivate_tickets.short_description='deactivate selected tickets'
class SoldTicketAdmin(admin.ModelAdmin):
    list_display=['user','event','used']
    list_filter=['used']
    actions=[deactivate_tickets]

class PaymentAdmin(admin.ModelAdmin):
    list_display=['user', 'amount', 'date', 'ticket']
    list_display_links=['user','ticket']
    list_filter=['date']



admin.site.register(SoldTicket, SoldTicketAdmin)
admin.site.register(Payment, PaymentAdmin)

