from django.db import models
from users.models import CustomUser
# Create your models here.


GENDER_SELECTION = [
    ('M', 'Male'),
    ('F', 'Female'),
]

IMAGE_TYPE_SELECTION = [
    ('H', 'Hand'),
    ('B', 'Burn'),
]


def upload_to(instance, filename):
    if instance.image_type == 'H':
        return f'tbsa/hand_images/{filename}'.format(filename)
    else:
        return f'tbsa/burn_images/{filename}'.format(filename)



class Tbsa (models.Model):
    patient_name = models.CharField(max_length=25)
    user_id = models.ForeignKey(CustomUser,related_name='useroftbsa' ,on_delete=models.CASCADE)
    age_type = models.CharField(max_length=10, choices=GENDER_SELECTION)
    survival_probability = models.FloatField(null=True, blank=True)
    age = models.IntegerField()
    total_burned_area = models.FloatField(null=True, blank=True)
    is_inhalation = models.BooleanField()
    weight = models.IntegerField()
    first_dose_amount = models.FloatField(null=True, blank=True)
    second_dose_amount = models.FloatField(null=True, blank=True)   
    third_dose_amount = models.FloatField(null=True, blank=True)
    tbsa = models.FloatField(null=True,blank=True)



class Tbsa_image (models.Model):
    tbsa_id = models.ForeignKey(Tbsa,related_name='tbsa_image' ,on_delete=models.CASCADE)
    image = models.ImageField(null=False, upload_to=upload_to)
    image_type = models.CharField(max_length=10,choices=IMAGE_TYPE_SELECTION)