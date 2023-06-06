from rest_framework import serializers, status
from .models import Category, Event, TicketPrice, TrendingEvents

class CreateEventPriceSerializer(serializers.ModelSerializer):
    id= serializers.IntegerField(read_only=True) 
    price=serializers.IntegerField(required=False)
    class Meta:
        model=TicketPrice
        fields=[ 
            'id', 'event', 'label', 'price', 'description', 'is_free', 'qty'
        ]

    def validate_event(self, value):
        request=self.context.get('request')
        if value.user != request.user:
            raise serializers.ValidationError("invalid event id ")
        return value

class EventTicketPricesSerializer(serializers.Serializer):
    id=serializers.IntegerField(read_only=True)
    label=serializers.CharField(read_only=True)
    price=serializers.FloatField(read_only=True)
    is_free=serializers.BooleanField(read_only=True)
    desciption=serializers.CharField(read_only=True)
    tickets_available=serializers.IntegerField(read_only=True, source='get_tickets_available')


class EventCreateSerializer(serializers.ModelSerializer):
    user=serializers.CharField(read_only=True)
    id=serializers.UUIDField(read_only=True)
    tickets=EventTicketPricesSerializer(read_only=True, many=True, source='event_fees')
    tags=serializers.ListField(child=serializers.CharField(),required=False, write_only=True)
    # tag=serializers.SerializerMethodField()
    approved=serializers.BooleanField(read_only=True)
    class Meta:
        model=Event
        fields=['id', 'user','name','category','tags','country','state','address', 'city', 'image', 'description', 'start_date', 'end_date', 'approved','tickets',]

    def to_representation(self, instance):
        res= super().to_representation(instance)
        try:
            res['tags']= eval(instance.tags)
        except:
            res['tags'] = instance.tags
        return res
    def validate(self, attrs):
        if attrs['start_date'] > attrs['end_date']:
            raise serializers.ValidationError({'start_date':'invalid dates'})
        return attrs

class EventSerializer(serializers.Serializer):
    user=serializers.StringRelatedField(read_only=True)
    id=serializers.UUIDField(read_only=True)
    name=serializers.CharField(read_only=True)
    country=serializers.CharField(read_only=True)
    city=serializers.CharField(read_only=True)
    state=serializers.CharField(read_only=True)
    address=serializers.CharField(read_only=True)
    image=serializers.ImageField(read_only=True)
    tickets=EventTicketPricesSerializer(read_only=True, many=True, source='event_fees')
    start_date=serializers.DateTimeField(read_only=True)
    end_date=serializers.DateTimeField(read_only=True)
    approved=serializers.BooleanField(read_only=True)






class BuyTicketSerializer(serializers.Serializer):
    qty=serializers.IntegerField(min_value=1)
    emails=serializers.ListField(child=serializers.EmailField(), required=False)

    def validate(self, attrs):
            if not attrs.get('emails'):
                user=self.context.get('request').user
                emails=[user.email for i in range(attrs.get('qty'))]
                attrs.update({'emails':emails})
                return attrs
            elif len(attrs['emails']) != attrs['qty']:
                    raise serializers.ValidationError('incomplete emails provided, qty and emails dont match')
            return attrs


class CategorySerializer(serializers.Serializer):
    name=serializers.CharField()
    slug=serializers.SlugField(read_only=True)

    def validate(self, attrs):
        name=attrs['name']
        category=Category.objects.filter(name__iexact=name)
        if category.exists():
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

