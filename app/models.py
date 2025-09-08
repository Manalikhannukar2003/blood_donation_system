from django.db import models

# Create your models here.


# Donor Model
class Donor(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    blood_group = models.CharField(max_length=5)
    contact = models.CharField(max_length=15)
    email = models.EmailField()
    # city = models.CharField(max_length=50)
    last_donation = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} "

# Request Model
class Request(models.Model):
    patient_name = models.CharField(max_length=100)
    blood_group = models.CharField(max_length=5)
    hospital_name = models.CharField(max_length=100)
    # city = models.CharField(max_length=50)
    contact = models.CharField(max_length=15)
    email = models.EmailField()
    # date_needed = models.DateField()
    status=models.CharField(max_length=20,default="Pending")

    def __str__(self):
        return f"Request: {self.patient_name} "
