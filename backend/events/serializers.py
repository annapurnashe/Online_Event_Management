from rest_framework import serializers
from .models import Event, Booking

class EventSerializer(serializers.ModelSerializer):
    available_seats = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()  

    class Meta:
        model = Event
        fields = '__all__'
        read_only_fields = ['created_by', 'created_at']

    def get_available_seats(self, obj):
        return obj.available_seats()

    def get_image_url(self, obj): 
        if obj.image:
            return f"http://127.0.0.1:8000{obj.image.url}"
        return None

class BookingSerializer(serializers.ModelSerializer):
    event = EventSerializer(read_only=True)
    event_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = Booking
        fields = ['id', 'user', 'event', 'event_id', 'ticket_quantity', 'total_amount', 'booking_date']
        read_only_fields = ['user', 'total_amount', 'booking_date']