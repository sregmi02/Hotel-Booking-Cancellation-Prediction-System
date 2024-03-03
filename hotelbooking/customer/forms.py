from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from shared.models import CustomUser, Booking
from datetime import datetime, timedelta
from django.core.exceptions import ValidationError
class CustomerRegistrationForm(UserCreationForm):
    username = forms.CharField(max_length=100, label = "", widget = forms.TextInput(attrs = {'class':'form-control', 'placeholder':'Username'}))
    fullname = forms.CharField(max_length=100, label = "", widget = forms.TextInput(attrs = {'class':'form-control', 'placeholder':'Full Name'}))
    # phone_number = forms.CharField(max_length=10, label = "",  required=False,  widget = forms.TextInput(attrs = {'class':'form-control', 'placeholder':'Phone Number'}))

    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'fullname','password1', 'password2']
    def __init__(self, *args, **kwargs):
        super(CustomerRegistrationForm, self).__init__(*args, **kwargs)  
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['email'].label = ''
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].help_text = ''
        self.fields['password1'].label = ''
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].help_text = ''
        self.fields['password2'].label = ''

class CustomerLoginForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password']
        widgets = {
        'username' : forms.TextInput(attrs={'class': 'form-control'}),
        'password' : forms.PasswordInput(attrs={'class': 'form-control'})
        }
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            model = CustomUser
            user = model.objects.customer_authenticate(username = username, password = password)

            if user is None:
                raise forms.ValidationError("Invalid Login Credentials for Customer")
        return cleaned_data

class BookingForm(forms.ModelForm):
    
    class Meta:
        model = Booking
        fields = ['no_of_adults','no_of_children','checkin_date','checkout_date','meal_plan','car_parking','city_tour_guide','room_amenities','jacuzzi','airport_pickup','wheelchair']
        widgets = {
            'no_of_adults' : forms.NumberInput(attrs = {'class': 'form-control'}),
            'no_of_children' : forms.NumberInput(attrs = {'class': 'form-control'}),
            'meal_plan' : forms.Select(attrs = {'class': 'form-control'}),
            'car_parking' : forms.CheckboxInput(attrs = {'class': 'form-check-input'}),
            # 'branch' : forms.Select(attrs = {'class': 'form-control'}),
            'checkin_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'checkout_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'city_tour_guide': forms.CheckboxInput(attrs = {'class': 'form-check-input'}),
            'room_amenities': forms.CheckboxInput(attrs = {'class': 'form-check-input'}),
            'jacuzzi' : forms.CheckboxInput(attrs = {'class': 'form-check-input'}),
            'airport_pickup' : forms.CheckboxInput(attrs = {'class': 'form-check-input'}),
            'wheelchair' : forms.CheckboxInput(attrs = {'class': 'form-check-input'}),
        }   
    
    def clean(self):
        cleaned_data = super().clean()
        checkin_date = cleaned_data.get('checkin_date')
        checkout_date = cleaned_data.get('checkout_date')
        no_of_children = cleaned_data.get('no_of_children')
        no_of_adults = cleaned_data.get('no_of_adults')
        no_of_days = (checkout_date- checkin_date).days
        booking_date = datetime.now().date()
        lead_time = (checkin_date - booking_date).days
        print(f'Lead Time: {lead_time}')
        if (lead_time > 365):
            self.add_error("checkin_date", "Bookings cannot be made more than a year ahead of arrival.")
        # if(no_of_days > 25):
        #     self.add_error("checkout_date", "Bookings can be made for 25 days only")
        if checkin_date and checkin_date < datetime.now().date():
            self.add_error("checkin_date","Checkin date cannot be in the past")
        if checkout_date and checkout_date < checkin_date:
            self.add_error("checkout_date","Checkout date must be at least 1 day after arrival date.")
        if no_of_children  < 0:
            self.add_error("no_of_children", "Number of Children cannot be negative")
        if no_of_adults > 10:
            self.add_error("no_of_adults", "This Value cannot be greater than 10")
        if no_of_adults < 1:
            self.add_error("no_of_adults", "This Value cannot be less than 1")
        if no_of_children > 10:
            self.add_error("no_of_children", "This Value cannot be greater than 10")
        return cleaned_data