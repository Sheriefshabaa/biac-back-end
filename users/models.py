from django.db import models

from django.db import models
from django.contrib.auth.models import AbstractUser


GENDER_SELECTION = [
    ('M', 'Male'),
    ('F', 'Female'),
]



def upload_to(instance, filename):
    return 'user_image/{filename}'.format(filename=filename)

class CustomUser(AbstractUser):
    first_name=models.CharField(max_length=20)
    last_name=models.CharField(max_length=20)
    gender = models.CharField(blank=True,max_length=20, choices=GENDER_SELECTION,null=True)
    phone_number = models.CharField(blank=True,max_length=30,null=True)
    date_of_birth = models.DateField(blank=True,null=True)
    is_premium = models.BooleanField(default=False)
    age = models.IntegerField(blank=True, null=True)
    user_image = models.ImageField(upload_to=upload_to, blank=True, null=True)
    is_active = models.BooleanField(default=True)


