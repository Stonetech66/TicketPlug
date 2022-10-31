from rest_framework import serializers, status
from .models import Category, Event, TicketPrice, TrendingEvents

class CreateEventPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model=TicketPrice
        fields=[ 
            'id','event', 'label', 'price', 'description'
        ]

    def validate_event(self, value):
        request=self.context.get('request')
        if value.user != request.user:
            raise serializers.ValidationError("invalid event id this event dosent belong to you")
        return value

class EventTicketPricesSerializer(serializers.Serializer):
    id=serializers.FloatField(read_only=True)
    label=serializers.CharField(read_only=True)
    price=serializers.FloatField(read_only=True)
    desciption=serializers.CharField(read_only=True)


class EventCreateSerializer(serializers.ModelSerializer):
    user=serializers.CharField(read_only=True)
    id=serializers.UUIDField(read_only=True)
    tickets=EventTicketPricesSerializer(read_only=True, many=True, source='event_fees')
    tags=serializers.ListField(child=serializers.CharField(),required=False, write_only=True)
    tag=serializers.SerializerMethodField()
    Category=serializers.StringRelatedField(many=True, read_only=True, source='category')
    approved=serializers.BooleanField(read_only=True)
    class Meta:
        model=Event
        fields=['id', 'user','name', 'Category','category','tag','tags','country','state','address', 'city', 'image_1', 'image_2', 'image_3', 'description', 'start_date', 'end_date', 'approved','tickets',]

    def get_tag(self, obj):
        if type(obj.tags) == list:
            return obj.tags       
        else:
            return eval(obj.tags)
    def validate(self, attrs):
        if attrs['start_date'] > attrs['end_date']:
            raise serializers.ValidationError({'start_date':'invalid dates'})
        return attrs

class EventSerializer(serializers.Serializer):
    user=serializers.CharField(read_only=True)
    id=serializers.UUIDField(read_only=True)
    name=serializers.CharField(read_only=True)
    country=serializers.CharField(read_only=True)
    city=serializers.CharField(read_only=True)
    state=serializers.CharField(read_only=True)
    address=serializers.CharField(read_only=True)
    image_1=serializers.ImageField(read_only=True)
    image_2=serializers.ImageField(read_only=True)
    image_3=serializers.ImageField(read_only=True)
    tickets=EventTicketPricesSerializer(read_only=True, many=True, source='event_fees')
    start_date=serializers.DateTimeField(read_only=True)
    end_date=serializers.DateTimeField(read_only=True)
    approved=serializers.BooleanField(read_only=True)






class BuyTicketSerializer(serializers.Serializer):
    ticket_id=serializers.IntegerField(source='event_ticket')
    qty=serializers.IntegerField()
    emails=serializers.ListField(child=serializers.EmailField(), required=False)

class CategorySerializer(serializers.Serializer):
    name=serializers.CharField()
    slug=serializers.SlugField(read_only=True)

    def validate(self, attrs):
        c=attrs['name']
        p=Category.objects.filter(name__iexact=c)
        if p.exists():
            raise serializers.ValidationError({'name':'category with this name already exists'})
        return attrs

    def create(self, validated_data):
        name=validated_data['name']
        return Category.objects.create(name=name)


class TrendingEventSerializer(serializers.ModelSerializer):
    event=EventSerializer(read_only=True, many=True, source='events')
    class Meta:
        model=TrendingEvents
        fields=['events', 'event']
        extra_kwargs={'events':{'write_only':True}}

