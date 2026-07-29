from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import models
from django.views.decorators.csrf import csrf_exempt
from .models import Event, Booking
from .serializers import EventSerializer, BookingSerializer

# ==================== EVENT VIEWSET ====================
class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all().order_by('-created_at')
    serializer_class = EventSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [AllowAny()]

# ==================== BOOKING VIEWSET ====================
class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [AllowAny] 
    def get_queryset(self):
        return self.queryset.all()  

# ==================== AUTH VIEWS ====================
@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def register_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email', '')

    if not username or not password:
        return Response({'error': 'Username and password required'}, status=status.HTTP_400_BAD_REQUEST)
    
    if User.objects.filter(username=username).exists():
        return Response({'error': 'User already exists'}, status=status.HTTP_400_BAD_REQUEST)
    
    user = User.objects.create_user(username=username, password=password, email=email)
    
    return Response({
        'message': 'User created successfully',
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
        }
    }, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({'error': 'Username and password required'}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=username, password=password)
    if user:
        login(request, user)
        request.session.save()
        return Response({
            'message': 'Login successful',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'is_staff': user.is_staff,
            }
        }, status=status.HTTP_200_OK)
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    logout(request)
    return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user(request):
    return Response({
        'id': request.user.id,
        'username': request.user.username,
        'email': request.user.email,
        'is_staff': request.user.is_staff,
    })

# ==================== BOOK EVENT ====================
@api_view(['POST'])
@permission_classes([AllowAny])  # ← तात्पुरतं AllowAny
@csrf_exempt
def book_event(request, event_id):
    try:
        event = Event.objects.get(id=event_id)
        ticket_quantity = int(request.data.get('ticket_quantity', 1))

        # ✅ User logic
        if request.user.is_authenticated:
            user = request.user
        else:
            from django.contrib.auth.models import User
            import uuid
            guest_username = f"guest_{uuid.uuid4().hex[:8]}"
            user, created = User.objects.get_or_create(
                username=guest_username,
                defaults={'email': f"{guest_username}@guest.com"}
            )
            if created:
                user.set_password('guest123')
                user.save()

        if ticket_quantity <= 0:
            return Response({'error': 'Ticket quantity must be greater than 0'}, status=status.HTTP_400_BAD_REQUEST)

        if event.booked_seats + ticket_quantity > event.max_seats:
            return Response({
                'error': f'Only {event.available_seats()} seats available'
            }, status=status.HTTP_400_BAD_REQUEST)

        booking = Booking.objects.create(
            user=user,
            event=event,
            ticket_quantity=ticket_quantity,
            total_amount=event.price * ticket_quantity
        )

        event.booked_seats += ticket_quantity
        event.save()

        return Response({
            'message': 'Booking confirmed successfully',
            'booking': {
                'id': booking.id,
                'event': event.name,
                'ticket_quantity': ticket_quantity,
                'total_amount': booking.total_amount,
                'booking_date': booking.booking_date
            }
        }, status=status.HTTP_201_CREATED)
        
    except Event.DoesNotExist:
        return Response({'error': 'Event not found'}, status=status.HTTP_404_NOT_FOUND)
    except ValueError:
        return Response({'error': 'Invalid ticket quantity'}, status=status.HTTP_400_BAD_REQUEST)

# ==================== ADMIN STATS ====================
@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_stats(request):
    total_events = Event.objects.count()
    total_bookings = Booking.objects.count()
    total_users = User.objects.count()
    total_revenue = Booking.objects.aggregate(total=models.Sum('total_amount'))['total'] or 0

    return Response({
        'total_events': total_events,
        'total_bookings': total_bookings,
        'total_users': total_users,
        'total_revenue': float(total_revenue),
    }, status=status.HTTP_200_OK)





from django.views.decorators.csrf import csrf_exempt
from .chatbot import EventChatbot
import json

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def chatbot_response(request):
    try:
        data = json.loads(request.body)
        user_message = data.get('message', '')
        
        if not user_message:
            return Response({'error': 'Message is required'}, status=400)
        
        chatbot = EventChatbot()
        response = chatbot.get_response(user_message)
        
        return Response({
            'message': response,
            'success': True
        })
    except json.JSONDecodeError:
        return Response({
            'message': 'Invalid JSON format',
            'success': False
        }, status=400)
    except Exception as e:
        print(f"Chatbot Error: {e}")
        return Response({
            'message': "😅 I'm having trouble. Please try again!",
            'success': False
        }, status=500)