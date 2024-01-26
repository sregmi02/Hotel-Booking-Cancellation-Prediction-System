from django.shortcuts import render, redirect, get_object_or_404
from shared.models import Room, Booking, CustomUser
from django.contrib import messages
import stripe
from django.conf import settings
from .models import PendingAlert
from django.contrib.auth import login, authenticate, logout
from .forms import CustomerLoginForm, CustomerRegistrationForm, BookingForm
from django.contrib.auth.decorators import login_required
# Create your views here.
def home(request):
    return render(request, 'customer/home.html', {})

def about(request):
    return render(request, 'customer/about.html', {})

@login_required(login_url="login_user")
def rooms(request):
        rooms = Room.objects.all()
        return render(request, 'customer/rooms.html', {'rooms': rooms })

def login_user(request):
    if request.method == 'POST':
        form = CustomerLoginForm(request, data = request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Logged In")
            customer = request.user
            bookings = Booking.objects.filter(customer = customer, status = None, processed = True, paid = False)
            if (bookings):
                messages.success(request, "You Have Pending Payments")
            return redirect('home_user')
        else:
            messages.success(request, "username or password incorrect")
            return redirect('login_user')
    else:
        form = CustomerLoginForm()
    return render(request, 'customer/login.html', {'form':form})
    

def logout_user(request):
    logout(request)
    messages.success(request, "Logged Out")
    return redirect ('home_user')

def register_user(request):
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            user = CustomUser.objects.create_customer(
                email=form.cleaned_data['email'],
                username=form.cleaned_data['username'],
                fullname=form.cleaned_data['fullname'],
                password=form.cleaned_data['password1'],
                phone_number=form.cleaned_data.get('phone_number'),
            )
            login(request, user)  # Automatically log in the user after registration
            messages.success(request, 'Successfully Registered')
            return redirect('home_user')  # Redirect to customer dashboard or another page
    else:
        form = CustomerRegistrationForm()
    return render(request, 'customer/register.html', {'form': form})

@login_required(login_url="login_user")
def room(request, pk):
    room = Room.objects.get(id=pk)
    return render(request, 'customer/room.html', {'room':room})
  
@login_required(login_url="login_user")
def booking_form(request, pk):
    room = Room.objects.get(id = pk)
    customer = request.user  
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            no_of_adults = form.cleaned_data['no_of_adults']
            no_of_children = form.cleaned_data['no_of_children']
            checkin_date =form.cleaned_data['checkin_date']
            checkout_date = form.cleaned_data['checkout_date']
            meal_plan = form.cleaned_data['meal_plan']
            car_parking = form.cleaned_data['car_parking']
            branch = form.cleaned_data['branch']
            children_meal= form.cleaned_data['children_meal']
            city_map = form.cleaned_data['city_map']
            tour_guide =  form.cleaned_data['tour_guide']
            airport_pickup =  form.cleaned_data['airport_pickup']
            wheelchair =  form.cleaned_data['wheelchair']
            Booking.objects.create(
                room = room, 
                customer = customer, 
                no_of_adults = no_of_adults,  
                no_of_children = no_of_children, 
                checkin_date = checkin_date, 
                checkout_date = checkout_date,
                meal_plan = meal_plan,
                car_parking = car_parking,
                branch = branch, 
                children_meal = children_meal,
                city_map = city_map,
                tour_guide = tour_guide,
                airport_pickup = airport_pickup,
                wheelchair = wheelchair,
                )
            messages.success(request, "Booking Request Sent")
            return redirect('home_user')
    else:
        form = BookingForm()
    return render(request, 'customer/booking_form.html', {'room':room, 'form':form})
@login_required(login_url="login_user")
def requested_bookings(request):
    customer = request.user
    bookings = Booking.objects.filter(customer = customer, status = None, processed = False)
    return render(request, 'customer/request_bookings.html', {'bookings':bookings})

@login_required(login_url="login_user")
def pending_payments(request):
    customer = request.user
    bookings = Booking.objects.filter(customer = customer, status = None, processed = True, paid = False)
    return render(request, 'customer/pending_payments.html', {'bookings':bookings})

@login_required(login_url="login_user")
def booking_details(request, pk):
    booking = Booking.objects.get(id = pk)
    return render(request, 'customer/booking_details.html', {'booking':booking})

@login_required(login_url="login_user")
def my_cancellations(request):
    customer = request.user
    cancellations = Booking.objects.filter(customer = customer, status = False)
    return render(request, 'customer/my_cancellations.html', {'cancellations':cancellations})

@login_required(login_url="login_user")
def cancel_booking(request, pk):
    booking = Booking.objects.get(id = pk)
    if booking.customer == request.user:
        booking.status = False
        customer = request.user
        customer.previous_bookings_cancelled += 1
        customer.save()
        booking.save()
    return redirect('my_bookings')

@login_required(login_url="login_user")
def update_booking(request, pk):
    booking = get_object_or_404(Booking, id = pk)
    if booking.customer == request.user:
        form = BookingForm(request.POST, instance = booking)
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                messages.success(request, ("Successfully Updated"))
                return redirect('requested_bookings')
        else:
            form = BookingForm(instance = booking)
        return render(request, 'customer/update_booking.html', {'form': form, 'booking': booking})


stripe.api_key = settings.API_KEY
DOMAIN_URL = 'http://127.0.0.1:8000'
@login_required(login_url="login_user")
def payment(request, pk):
    booking = Booking.objects.get(id = pk)
    print(booking.advance)
    if request.method == 'POST':
            product = stripe.Product.create(name = booking.room.name)
            product_price = stripe.Price.create(
                product = product, unit_amount = int(booking.advance * 100), currency = 'eur'
            )
            customer = stripe.Customer.create(name = request.user.fullname, email = request.user.email)

            stripe_checkout_session  = stripe.checkout.Session.create(
                #ui_mode = "embedded",
                line_items=[
                    {"price": product_price,
                     "quantity": 1}],
                success_url= DOMAIN_URL + "/payment_success?session_id={CHECKOUT_SESSION_ID}&pk="+str(pk),
                cancel_url= DOMAIN_URL + "/payment_failed",
                mode = 'payment',
                customer = customer.stripe_id,
            )

            return redirect(to=stripe_checkout_session.url)
    return render(request, 'customer/payment.html', {'booking':booking})

def payment_success(request):
    stripe_session = stripe.checkout.Session.retrieve(request.GET.get("session_id"))
    booking = Booking.objects.get(id = int(request.GET.get("pk")))
    customer = stripe.Customer.retrieve(stripe_session.customer)
    booking.stripe_checkout_id = request.GET.get('session_id')
    booking.paid = True
    booking.save()
    return render(request, 'customer/payment_success.html', {'customer':customer})


def payment_failed(request):
    return render(request, 'customer/payment_failed.html', {})
