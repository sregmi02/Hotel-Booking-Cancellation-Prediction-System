from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name = 'home_user'),
    path('aboutus', views.about, name = 'about_us'),
    path('rooms/', views.rooms, name = 'rooms'),
    path('login_user/', views.login_user, name = 'login_user'),
    path('logout_user/', views.logout_user, name = 'logout_user'),
    path('register_user/', views.register_user, name = 'register_user'),
    path('room/<int:pk>', views.room, name = 'room'),
    path('my_bookings/', views.requested_bookings, name = 'requested_bookings'),
    path('booking_details/<int:pk>', views.booking_details, name = 'booking_details'),
    path('my_cancellations/', views.my_cancellations, name = 'my_cancellations'),
    path('cancel_booking/<int:pk>', views.cancel_booking, name = 'cancel_booking'),
    path('update_booking/<int:pk>', views.update_booking, name = 'update_booking'),
    path('booking_form/<int:pk>',views.booking_form, name = "booking_form"),
    path('pending_payments/',views.pending_payments, name = "pending_payments"),
    
]