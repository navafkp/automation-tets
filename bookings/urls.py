from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('room/', views.room_list, name='room'),
    path('rooms/<int:id>', views.room_detail, name='room_detail'),
    path('bookings/', views.BookingCreateView.as_view(), name='booking-create'),
    
]