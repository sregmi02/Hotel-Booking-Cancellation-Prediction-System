from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Room, Booking, Prediction
from django.contrib import admin

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['email', 'username', 'fullname', 'is_customer', 'is_employee','previous_bookings_cancelled','repeated_guest']
    readonly_fields = [f.name for f in CustomUser._meta.get_fields()]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

class BookingAdmin(admin.ModelAdmin):
    readonly_fields = [f.name for f in Booking._meta.get_fields()]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

class PredictionAdmin(admin.ModelAdmin):
    readonly_fields = [f.name for f in Prediction._meta.get_fields()]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Room)
admin.site.register(Booking, BookingAdmin)
admin.site.register(Prediction, PredictionAdmin)