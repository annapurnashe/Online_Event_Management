from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Event, Booking
from .serializers import EventSerializer, BookingSerializer

class EventViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Event CRUD operations.
    """
    queryset = Event.objects.all().order_by('-created_at')
    serializer_class = EventSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

class BookingViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Booking operations.
    """
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


