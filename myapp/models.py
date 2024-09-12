from django.db import models
from django.contrib.auth.models import User

class ClientData(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phonenumber = models.CharField(max_length=15)
    timestamp = models.DateTimeField(auto_now_add=True)  # Automatically adds today's date and time
    investigate_date = models.DateField(null=True, blank=True)  # Allow null and blank values
    schedule_date = models.DateField(null=True, blank=True)     # Allow null and blank values
    lead = models.CharField(max_length=100)
    response = models.TextField()
    assigned_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name