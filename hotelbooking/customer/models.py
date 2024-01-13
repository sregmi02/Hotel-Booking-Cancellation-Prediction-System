from django.db import models
from shared.models import CustomUser
# Create your models here.
class PendingAlert(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete = models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
