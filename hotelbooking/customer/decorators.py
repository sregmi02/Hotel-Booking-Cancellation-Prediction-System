from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect

def customer_required(view_func):
    actual_decorator = user_passes_test(
        lambda user: user.is_authenticated and user.is_customer,
        login_url=reverse_lazy('login_user'), # Redirect to login page if not logged in as employee
    )
    return actual_decorator(view_func)
