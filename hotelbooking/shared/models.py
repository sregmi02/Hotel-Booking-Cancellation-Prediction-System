from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager
from django.core.validators import RegexValidator
from datetime import datetime, timedelta
from django.dispatch import receiver
from django.db.models.signals import post_save
class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, fullname, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, fullname=fullname, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_customer(self, email, username, fullname, password=None, **extra_fields):
        extra_fields.setdefault('is_customer', True)
        extra_fields.setdefault('is_staff', False)
        return self.create_user(email, username, fullname, password, **extra_fields)

    def create_employee(self, email, username, fullname, password=None, **extra_fields):
        extra_fields.setdefault('is_employee', True)
        extra_fields.setdefault('is_staff', True)
        return self.create_user(email, username, fullname, password, **extra_fields)
    
    def create_superuser(self, email, username, fullname, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, username, fullname, password, **extra_fields)
    
    def customer_authenticate(self, username=None, password=None, **extra_fields):
        if not username:
            return None
        
        user = self.get_by_natural_key(username = username)

        if user.check_password(password) and user.is_customer:
            return user

        return None
    
    def employee_authenticate(self, username=None, password=None, **extra_fields):
        if not username:
            return None
        
        user = self.get_by_natural_key(username = username)

        if user.check_password(password) and user.is_employee:
            return user

        return None
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=255, unique = True)
    fullname = models.CharField(max_length=255)
    is_customer = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)
    repeated_guest = models.BooleanField(null  = True, default = False)
    pending_status = models.BooleanField(default = False, null = True)
    previous_bookings_not_cancelled = models.IntegerField(default=0)
    previous_bookings_cancelled = models.IntegerField(default=0)
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'fullname']

    def __str__(self):
        return f"{self.username}"
    
class Room(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=5, default = 0, decimal_places=2)
    description = models.CharField(max_length=250, blank = True, null = True)
    image = models.ImageField(upload_to = 'uploads/rooms', null=True)
    max_capacity = models.PositiveIntegerField(null = True)
    def __str__(self):
        return self.name

class Prediction(models.Model):
    prediction_status = models.BooleanField(default=None, null=True)

class Booking(models.Model):
    MealPlan = (
        ('Not Selected', 'None'),
        ('Meal Plan 1', 'Breakfast'),
        ('Meal Plan 2', 'Dinner and Breakfast'),
        ('Meal Plan 3', 'Dinner, Breakfast, and Lunch'),
    )
    # Branch = (
    #     ('Branch 1', 'Portugal'),
    #     ('Branch 2', 'Barcelona'),
    #     ('Branch 3', 'Lisbon'),
    #     ('Branch 4', 'Seville'),
    #     ('Branch 5', 'Valencia'),
    # )
    CheckedInStatus = (
        ('True','Checked In'),
        ('False','Not Checked In'),
    )

    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    prediction = models.OneToOneField(Prediction, on_delete=models.CASCADE, null = True)
    no_of_rooms = models.PositiveIntegerField(default=1)
    no_of_adults = models.PositiveIntegerField(default = 1)
    no_of_children = models.IntegerField(default = 0)
    checkin_date = models.DateField(default = datetime.now().date())
    checkin_month = models.IntegerField(null = True)
    checkin_day = models.IntegerField(null = True)
    checkout_date = models.DateField(default = datetime.now().date() + timedelta(days=1))
    booking_date = models.DateField(default = datetime.now().date())
    no_of_days = models.IntegerField(blank = True, null = True)
    weeknights = models.IntegerField(null = True)
    weekend_nights = models.IntegerField(null = True)
    lead_time = models.IntegerField(blank = True, null = True)
    meal_plan = models.CharField(max_length=255, choices = MealPlan, default = 'None')
    car_parking = models.BooleanField(default = False)
    # branch = models.CharField(max_length=255, choices=Branch, default ='Branch 1')
    city_tour_guide = models.BooleanField(default = False, null = True)
    room_amenities = models.BooleanField(default = False, null = True)
    jacuzzi = models.BooleanField(default = False, null = True)
    airport_pickup = models.BooleanField(default = False, null = True)
    wheelchair = models.BooleanField(default = False, null = True)
    no_of_special_requests = models.IntegerField(null = True)
    dynamic_price = models.DecimalField(max_digits = 10, decimal_places = 2, null = True)
    status = models.BooleanField(null = True)
    advance = models.DecimalField(max_digits = 10, decimal_places = 2, null = True)
    processed = models.BooleanField(default = False)
    paid = models.BooleanField(default = False)
    checked_in_status = models.BooleanField(default = None, null = True)
    stripe_checkout_id = models.CharField(max_length = 500, null = True)
    def calculateprice(self):
        price = float(self.room.price)
        arrival_month = self.checkin_date.month

        if arrival_month in [1,2]:
            price_multiplier = 0.90
        elif arrival_month in [3,4,5,6,7]:
            price_multiplier = 1
        elif arrival_month in [8,9,10]:
            price_multiplier = 1.25
        else:
            price_multiplier = 1.20
        date_price = price*price_multiplier

        final_price = date_price*self.no_of_rooms

        return final_price
    
    def calculate_special_requests(self):
        # Calculate and return the number of selected special requests
        selected_requests = [self.city_tour_guide,self.room_amenities,self.jacuzzi,self.airport_pickup,self.wheelchair]
        no_of_special_requests = sum (1 for option in selected_requests if option)
        return no_of_special_requests

    def set_prediction_status(self, status):
        prediction = Prediction.objects.create(prediction_status=status)
        self.prediction = prediction
        self.save()

    def save(self, *args, **kwargs):
        self.no_of_days = (self.checkout_date - self.checkin_date).days
        total_people = self.no_of_adults + (self.no_of_children)
        self.no_of_rooms = -(-total_people // self.room.max_capacity)
        self.lead_time = (self.checkin_date - self.booking_date).days
        self.weeknights = sum(1 for single_date in [self.checkin_date + timedelta(days=n) for n in range(self.no_of_days)]
                         if single_date.weekday() < 5)
        self.weekend_nights = (self.no_of_days - self.weeknights) 
        self.dynamic_price = self.calculateprice()
        self.no_of_special_requests = self.calculate_special_requests()
        self.checkin_month = self.checkin_date.month
        self.checkin_day = self.checkin_date.day 
        if self.status == False:
            self.customer.previous_bookings_cancelled +=1
            self.customer.save()
        if self.status == True:
            self.customer.previous_bookings_not_cancelled +=1
            self.customer.save()
        if self.customer.previous_bookings_not_cancelled >= 1:
            self.customer.repeated_guest = True
            self.customer.save()
        else:
            self.customer.repeated_guest = False
            self.customer.save()
        
        super().save(*args, **kwargs)
        
        
    
    def __str__(self):
        return f'{self.room} by {self.customer.username}'