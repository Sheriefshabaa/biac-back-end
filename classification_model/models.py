from django.db import models

# Create your models here.

def upload_to(instance, filename):
    return 'input_images/{filename}'.format(filename=filename)


class ClassificationBurn (models.Model):
    img_url_before = models.ImageField(upload_to=upload_to, blank=True, null=True)
    img_url_after= models.ImageField(upload_to=upload_to, blank=True, null=True)
    result = models.CharField(max_length=80, blank=False, null=False)
