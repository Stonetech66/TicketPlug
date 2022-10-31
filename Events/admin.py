from django.contrib import admin
from  .models import Event, OrderTicket, BuyTicket,  TicketPrice, Category, TrendingEvents
# Register your models here.


def approve_event(modeladmin, request, queryset):
    queryset.update(approved=True)

approve_event.short_description='approve selected events'

class Event_priceinline(admin.TabularInline):
    model=TicketPrice

class EventAdmin(admin.ModelAdmin):
    inlines=[Event_priceinline]
    list_display=['name', 'city', 'state', 'country' ,'start_date', 'end_date']
    list_filter=['start_date', 'end_date', 'city', 'category__name']
    search_fields=['name', 'city', 'state']

class Event_FeeAdmin(admin.ModelAdmin):
    list_display=['event', 'label', 'price']
    list_display_links=['event', 'label']



admin.site.register(Event, EventAdmin)
admin.site.register(TicketPrice, Event_FeeAdmin)
admin.site.register(Category)
admin.site.register(TrendingEvents)
admin.site.register(BuyTicket)
admin.site.register(OrderTicket)

