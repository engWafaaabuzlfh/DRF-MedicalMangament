from django.db import models
from authentication.models import User
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.

class Diagnosis(models.Model):
    disease = models.CharField(max_length=200, null=True)
    note_1 = models.TextField(null=True)
    note_2 = models.TextField(null=True)

    def __str__(self):
        return self.disease


class Invoice(models.Model):
    total = models.IntegerField(null=True)
    Paid = models.IntegerField(null=True)
    number_of_visits = models.IntegerField(null=True)
    def __str__(self):
        return self.total
class Patiant(models.Model):
    CHOICES = (
        ('male', 'male'),
        ('female', 'female'),
    )
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doctors')
    name = models.CharField(max_length=200, null=True)
    age = models.IntegerField(null=True)
    gender = models.CharField(max_length=10, choices=CHOICES, default='male', null=True)
    phone = PhoneNumberField(null=True)
    address = models.CharField(max_length=200, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    diagnosis = models.ForeignKey(Diagnosis, on_delete=models.CASCADE, null=True)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, null=True)
    def __str__(self):
        return self.name
    


