from django.shortcuts import render, redirect, get_object_or_404
from shared.models import Room, Booking, CustomUser
from django.contrib import messages
import stripe
from .decorators import customer_required
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

@customer_required
def rooms(request):
        rooms = Room.objects.all().order_by('price')
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
            )
            login(request, user)  # Automatically log in the user after registration
            messages.success(request, 'Successfully Registered')
            return redirect('home_user')  # Redirect to customer dashboard or another page
    else:
        form = CustomerRegistrationForm()
    return render(request, 'customer/register.html', {'form': form})

@customer_required
def room(request, pk):
    room = Room.objects.get(id=pk)
    return render(request, 'customer/room.html', {'room':room})
  
@customer_required
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
            # branch = form.cleaned_data['branch']
            city_tour_guide= form.cleaned_data['city_tour_guide']
            room_amenities = form.cleaned_data['room_amenities']
            jacuzzi =  form.cleaned_data['jacuzzi']
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
                city_tour_guide = city_tour_guide,
                room_amenities= room_amenities,
                jacuzzi = jacuzzi,
                airport_pickup = airport_pickup,
                wheelchair = wheelchair,
                )
            customer.pending_status = True
            customer.save()
            messages.success(request, "Booking Request Sent")
            return redirect('home_user')
    else:
        form = BookingForm()
    return render(request, 'customer/booking_form.html', {'room':room, 'form':form, 'customer': customer})

@customer_required
def requested_bookings(request):
    customer = request.user
    bookings = Booking.objects.filter(customer = customer, status = None, processed = False)
    print(customer.pending_status)
    return render(request, 'customer/request_bookings.html', {'bookings':bookings, 'customer': customer})

@customer_required
def pending_payments(request):
    customer = request.user
    bookings = Booking.objects.filter(customer = customer, status = None, processed = True, paid = False)
    return render(request, 'customer/pending_payments.html', {'bookings':bookings})

@customer_required
def completed_payments(request):
    customer = request.user
    bookings = Booking.objects.filter(customer = customer, paid = True, status = None)
    return render(request, 'customer/completed_payments.html', {'bookings':bookings})

@customer_required
def booking_details(request, pk):
    booking = Booking.objects.get(id = pk)
    return render(request, 'customer/booking_details.html', {'booking':booking})

@customer_required
def my_cancellations(request):
    customer = request.user
    cancellations = Booking.objects.filter(customer = customer, status = False)
    return render(request, 'customer/my_cancellations.html', {'cancellations':cancellations})

@customer_required
def cancel_booking(request, pk):
    booking = Booking.objects.get(id = pk)
    if booking.customer == request.user:
        print(booking.id)
        booking.status = False
        customer = request.user
        customer.previous_bookings_cancelled += 1
        customer.save()
        booking.save()
        if booking.paid == False:
            customer.pending_status = False
            customer.save()
        print(customer.pending_status)
        messages.success(request, f"Booking {booking.id} Cancelled")
    if request.META.get('HTTP_REFERER').endswith('/my_bookings/'):
        return redirect('requested_bookings')  # Redirect to the paid bookings page
    elif request.META.get('HTTP_REFERER').endswith('/pending_payments/'):
        return redirect('pending_payments')
    elif request.META.get('HTTP_REFERER').endswith('/completed_payments/'):
        return redirect('completed_payments')

@customer_required
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
@customer_required
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

@customer_required
def payment_success(request):
    stripe_session = stripe.checkout.Session.retrieve(request.GET.get("session_id"))
    booking = Booking.objects.get(id = int(request.GET.get("pk")))
    customer = stripe.Customer.retrieve(stripe_session.customer)
    booking.stripe_checkout_id = request.GET.get('session_id')
    booking.paid = True
    booking.save()
    customer1 = request.user
    customer1.pending_status = False
    customer1.save()
    return render(request, 'customer/payment_success.html', {'customer':customer})


def payment_failed(request):
    return render(request, 'customer/payment_failed.html', {})
