from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect

def employee_required(view_func):
    actual_decorator = user_passes_test(
        lambda user: user.is_authenticated and user.is_employee,
        login_url=reverse_lazy('login_emp'), # Redirect to login page if not logged in as employee
    )
    return actual_decorator(view_func)
