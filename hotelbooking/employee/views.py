from django.shortcuts import render, redirect
from shared.models import CustomUser
from .forms import EmployeeLoginForm, EmployeeRegistrationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from customer.models import PendingAlert
from shared.models import Booking
from django.contrib.auth.decorators import login_required
from employee.forms import BookingForm
from .decorators import employee_required
import pickle 
import pandas as pd
import sys
from datetime import datetime
sys.path.append(r'C:\Users\sssre\Documents\CSIT VII\Final Year Project\model')

# Create your views here.
def home_emp(request):
    return render(request, 'employee/home_emp.html', {})

def login_emp(request):
    if request.method == 'POST':
        form = EmployeeLoginForm(request, data = request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Logged In')
            return redirect('pending_bookings')
        else:
            messages.success(request, "username or password incorrect")
            return redirect('login_emp')
    else:
        return render(request, 'employee/login_emp.html', {})

def register_emp(request):
    if request.method == 'POST':
        form = EmployeeRegistrationForm(request.POST)
        if form.is_valid():
            user = CustomUser.objects.create_employee(
                email=form.cleaned_data['email'],
                username=form.cleaned_data['username'],
                fullname=form.cleaned_data['fullname'],
                password=form.cleaned_data['password1'],
                phone_number=form.cleaned_data.get('phone_number'),
            )
            login(request, user)  # Automatically log in the user after registration
            messages.success(request, "Logged In")
            return redirect('pending_bookings')  # Redirect to employee dashboard or another page
    else:
        form = EmployeeRegistrationForm()
    return render(request, 'employee/register_emp.html', {'form': form})

def logout_emp(request):
    logout(request)
    messages.success(request, "Logged Out")
    return redirect ('login_emp')

@employee_required
def pending_bookings(request):
    bookings = Booking.objects.filter(processed = False, status = None)
    return render(request, 'employee/pending_bookings.html', {'bookings':bookings})

@employee_required
def processed_bookings(request):
    bookings = Booking.objects.filter(processed = True, status = None)
    return render(request, 'employee/processed_bookings.html', {'bookings':bookings})

@employee_required
def confirmed_bookings(request):
    bookings = Booking.objects.filter(status = True)
    return render(request, 'employee/confirmed_bookings.html', {'bookings':bookings})

@employee_required
def cancelled_bookings(request):
    bookings = Booking.objects.filter(status = False)
    return render(request, 'employee/cancelled_bookings.html', {'bookings':bookings})

@employee_required
def booking_details_emp(request, pk):
    booking = Booking.objects.get(id = pk)
    # form = BookingForm(request.POST, instance = booking)
    # if request.method == 'POST':
    #     if form.is_valid():
    #         form.save()
    #         print(booking.no_of_adults)  
    #         return redirect('home_emp')
    # else:
    #     form = BookingForm(instance = booking)  
    return render(request, 'employee/booking_details_emp.html', {'booking': booking})

@employee_required
def customer_list(request):
    customer = CustomUser.objects.filter(is_customer = True)
    return render (request, 'employee/customer_list.html', {'customer':customer})

def getPredictions(no_of_adults, no_of_children, no_of_weekend_nights, no_of_week_nights, type_of_meal_plan,
                   required_car_parking_space, room_type_reserved, arrival_month, arrival_date,
                   repeated_guest, no_of_previous_cancellations , no_of_previous_bookings_not_canceled,
                   no_of_special_requests, lead_time, avg_price_per_room):
    model = pickle.load(open("ml_model","rb"))
    data = {
        'no_of_adults':no_of_adults,
        'no_of_children':no_of_children,
        'no_of_weekend_nights':no_of_weekend_nights, 
        'no_of_week_nights':no_of_week_nights, 
        'type_of_meal_plan':type_of_meal_plan,
        'required_car_parking_space':required_car_parking_space, 
        'room_type_reserved':room_type_reserved, 
        'arrival_month':arrival_month,
        'arrival_date':arrival_date,
        'repeated_guest':repeated_guest,
        'no_of_previous_cancellations':no_of_previous_cancellations,
        'no_of_previous_bookings_not_canceled':no_of_previous_bookings_not_canceled,
        'no_of_special_requests':no_of_special_requests,
        'lead_time':lead_time,
        'avg_price_per_room':avg_price_per_room
    }
    X_test = pd.DataFrame(data,index=[0])
    X_pass = X_test.to_numpy()
    prediction = model.predict(X_pass,n_features = X_test.columns)
    if prediction == 0:
        return 'unlikely to cancel'
    elif prediction == 1:
        return 'likely to cancel'


def result(request,pk):
    booking = Booking.objects.get(id = pk)
    no_of_adults = int(booking.no_of_adults)
    no_of_children = int(booking.no_of_children)
    no_of_weekend_nights = int(booking.weekend_nights)
    no_of_week_nights = int(booking.weeknights)
    if booking.meal_plan == "Meal Plan 1":
        type_of_meal_plan = 0
    elif booking.meal_plan == "Meal Plan 2":
        type_of_meal_plan = 2
    elif booking.meal_plan == "Meal Plan 3":
        type_of_meal_plan = 3
    else:
        type_of_meal_plan = 1
    if booking.car_parking == True:
        required_car_parking_space = 1
    else:
        required_car_parking_space = 0
    if booking.room.name == "Standard Room":
        room_type_reserved = 0
    if booking.room.name == "Deluxe Room":
        room_type_reserved = 1
    if booking.room.name == "Suite":
        room_type_reserved = 2
    if booking.room.name == "Economy":
        room_type_reserved = 3
    if booking.room.name == "Heritage Room":
        room_type_reserved = 4
    if booking.room.name == "Villa":
        room_type_reserved = 5
    if booking.room.name == "Executive Room":
        room_type_reserved = 6
        

    arrival_month = int(booking.checkin_month)
    arrival_date = int(booking.checkin_day)
    if booking.customer.repeated_guest == True:
        repeated_guest = 1
    else:
        repeated_guest = 0
    no_of_previous_cancellations = int(booking.customer.previous_bookings_cancelled)
    no_of_previous_bookings_not_canceled = int(booking.customer.previous_bookings_not_cancelled)
    no_of_special_requests = int(booking.no_of_special_requests)
    lt = int(booking.lead_time)
    lead_time = (((lt-84.25)/82.32)) #standardizing
    ap = int(booking.dynamic_price/booking.no_of_rooms)
    avg_price_per_room = ((ap-105.78)/32.39) #standardizing
    
    result = getPredictions(no_of_adults, no_of_children, no_of_weekend_nights, no_of_week_nights, type_of_meal_plan,
                   required_car_parking_space, room_type_reserved, arrival_month, arrival_date,
                   repeated_guest, no_of_previous_cancellations , no_of_previous_bookings_not_canceled,
                   no_of_special_requests, lead_time, avg_price_per_room)
    if result == 'unlikely to cancel':
        booking.set_prediction_status(False)
        booking.advance = 0.25*float(booking.dynamic_price)
    elif result == 'likely to cancel':
        booking.set_prediction_status(True)
        booking.advance = 0.5*float(booking.dynamic_price)
    booking.processed = True
    PendingAlert.objects.create(customer = booking.customer, message = f"Your Booking (ID: {booking.id}) has been processed. Please proceed to payment.")
    booking.save()
    
    print(result)
    return render(request, 'employee/booking_details_emp.html', {'booking':booking})

def checkin_booking(request, pk):
    booking = Booking.objects.get(id = pk)
    if (booking.paid):
        if (booking.checkin_date <= datetime.now().date()):
            print(booking.checkin_date)
            print(datetime.now().date())
            print("True")
            booking.status = True
            booking.processed = True
            booking.save()
            messages.success(request, f'Booking (ID: {booking.id}) by {booking.customer.fullname} added to Confirmed Bookings')
            return redirect('confirmed_bookings')
        else:
            print("False")
            print(booking.id)
            print(booking.checkin_date)
            print(datetime.now().date())
            messages.success(request, f'Checkin date for Booking (ID: {booking.id}) has not arrived yet')
            return redirect('processed_bookings')
    else:
        messages.success(request, f'The Booking (ID: {booking.id}) has not been paid for')
        return redirect('processed_bookings')

def not_checkin_booking(request, pk):
    booking = Booking.objects.get(id = pk)
    print(booking.id)
    if (booking.checkin_date <= datetime.now().date()):
        booking.status = False
        booking.processed = True
        booking.save()
        messages.success(request, f'Booking (ID: {booking.id}) by {booking.customer.fullname} added to Cancelled Bookings')
        return redirect('cancelled_bookings')
    else:
        messages.success(request, 'Checkin date has not arrived yet')
        return redirect('processed_bookings')

