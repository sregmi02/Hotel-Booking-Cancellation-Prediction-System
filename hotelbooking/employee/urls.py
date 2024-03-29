from django.urls import path
from . import views
urlpatterns = [
    path('', views.pending_bookings, name = 'pending_bookings'),
    path('login_emp/', views.login_emp, name = 'login_emp'),
    path('logout_emp/' , views.logout_emp, name = 'logout_emp'),
    path('register_emp/', views.register_emp, name = 'register_emp'),
    path('processed_bookings/', views.processed_bookings, name = 'processed_bookings'),
    path('confirmed_bookings/', views.confirmed_bookings, name = 'confirmed_bookings'),
    path('cancelled_bookings/', views.cancelled_bookings, name = 'cancelled_bookings'),
    path('booking_details_emp/<int:pk>', views.booking_details_emp, name = 'booking_details_emp'),
    path('result/<int:pk>', views.result, name = 'result'),
    path('checkin/<int:pk>', views.checkin_booking, name = 'checkin_booking'),
    path('notcheckin/<int:pk>', views.not_checkin_booking, name = 'not_checkin_booking'),
]