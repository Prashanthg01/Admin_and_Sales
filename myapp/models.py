from django.db import models

class ClientData(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phonenumber = models.CharField(max_length=15)
    timestamp = models.DateTimeField(auto_now_add=True)
    investigate_date = models.DateField(null=True, blank=True)
    schedule_date = models.DateField(null=True, blank=True)
    lead = models.CharField(max_length=100)
    response = models.TextField()
    assigned_user = models.CharField(max_length=15)

    def __str__(self):
        return self.name
    
class UserSubmits(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phonenumber = models.CharField(max_length=15)
    timestamp = models.DateTimeField(auto_now_add=True)
    investigate_date = models.DateField(null=True, blank=True)
    schedule_date = models.DateField(null=True, blank=True)
    lead = models.CharField(max_length=100)
    response = models.TextField()
    assigned_user = models.CharField(max_length=15)
    reviewed = models.IntegerField(default=0)

    def __str__(self):
        return self.name