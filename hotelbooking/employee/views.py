from django.shortcuts import render, redirect
from shared.models import CustomUser
from .forms import EmployeeLoginForm, EmployeeRegistrationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from shared.models import Booking
from django.contrib.auth.decorators import login_required
from employee.forms import BookingForm
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
            return redirect('home_emp')
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
            return redirect('home_emp')  # Redirect to employee dashboard or another page
    else:
        form = EmployeeRegistrationForm()
    return render(request, 'employee/register_emp.html', {'form': form})

def logout_emp(request):
    logout(request)
    messages.success(request, "Logged Out")
    return redirect ('home_emp')

@login_required(login_url="login_emp")
def pending_bookings(request):
    bookings = Booking.objects.filter(processed = False, status = None)
    return render(request, 'employee/pending_bookings.html', {'bookings':bookings})

@login_required(login_url="login_emp")
def processed_bookings(request):
    bookings = Booking.objects.filter(processed = True)
    return render(request, 'employee/processed_bookings.html', {'bookings':bookings})

@login_required(login_url="login_emp")
def confirmed_bookings(request):
    bookings = Booking.objects.filter(status = True)
    return render(request, 'employee/confirmed_bookings.html', {'bookings':bookings})

@login_required(login_url="login_emp")
def cancelled_bookings(request):
    bookings = Booking.objects.filter(status = False)
    return render(request, 'employee/cancelled_bookings.html', {'bookings':bookings})

@login_required(login_url="login_emp")
def booking_details_emp(request, pk):
    booking = Booking.objects.get(id = pk)
    form = BookingForm(request.POST, instance = booking)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            print(booking.no_of_adults)  
            return redirect('home_emp')
    else:
        form = BookingForm(instance = booking)  
    return render(request, 'employee/booking_details_emp.html', {'form':form, 'booking': booking})

@login_required(login_url="login_emp")
def customer_list(request):
    customer = CustomUser.objects.filter(is_customer = True)
    return render (request, 'employee/customer_list.html', {'customer':customer})

def result(request, pk):
    booking = Booking.objects.get(id = pk)
    return render (request, 'employee/result.html', {})