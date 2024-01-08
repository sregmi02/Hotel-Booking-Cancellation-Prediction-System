from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Room, Booking

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['email', 'username', 'fullname', 'is_customer', 'is_employee','previous_bookings_cancelled']

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Room)
admin.site.register(Booking)