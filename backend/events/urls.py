from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'events', views.EventViewSet)
router.register(r'bookings', views.BookingViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('user/', views.get_user, name='get_user'),
    path('book/<int:event_id>/', views.book_event, name='book_event'),
    path('admin-stats/', views.admin_stats, name='admin_stats'),
    path('chatbot/', views.chatbot_response, name='chatbot'), 
]