from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from shared.models import CustomUser, Booking
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import datetime

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['checked_in_status']
        widgets = {
            'checked_in_status' : forms.Select(attrs = {'class': 'form-control'}),
        }
    def clean(self):
        cleaned_data = super().clean()
        checked_in_status = cleaned_data.get('checked_in_status')
        checkin_date = self.instance.checkin_date
        if checkin_date != datetime.now().date():
            self.add_error("checked_in_status", "Today is not the check-in date.")
        return cleaned_data
class EmployeeRegistrationForm(UserCreationForm):
    username = forms.CharField(max_length=100, label = "", widget = forms.TextInput(attrs = {'class':'form-control', 'placeholder':'Username'}))
    fullname = forms.CharField(max_length=100, label = "", widget = forms.TextInput(attrs = {'class':'form-control', 'placeholder':'Full Name'}))
    phone_number = forms.CharField(max_length=15, label = "",  required=False,  widget = forms.TextInput(attrs = {'class':'form-control', 'placeholder':'Phone Number'}))
    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'fullname', 'phone_number', 'password1', 'password2']
    def __init__(self, *args, **kwargs):
        super(EmployeeRegistrationForm, self).__init__(*args, **kwargs)  
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


        

class EmployeeLoginForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password']
        widgets = {
        'username' : forms.TextInput(attrs={'class': 'form-control'}),
        'password' : forms.PasswordInput(attrs={'class': 'form-control'})
        }