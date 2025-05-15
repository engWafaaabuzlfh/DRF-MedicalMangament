from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.timezone import now
from .managers import UserManager


# Create your models here.
class User(AbstractUser):
    mark_as_read = models.BooleanField(default=False)
    image = models.ImageField(upload_to='profiles/', default='profiles/prof.png')
    berthday = models.DateField(null=True)
    gender = models.CharField(max_length=20, null=True)
    phone_number = PhoneNumberField(unique=True, blank=True, null=True)
    objects = UserManager()
    def __str__(self):
        return f"{self.username} {self.email}  {self.gender} {self.phone_number}"


class ActiveAccessToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.TextField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"AccessToken for {self.user}"
