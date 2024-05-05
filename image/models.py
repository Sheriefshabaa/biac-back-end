from django.db import models
from users.models import CustomUser
# Create your models here.


def upload_to(instance, filename):
    return 'input_images/{filename}'.format(filename=filename)



class Image (models.Model):
    provided_image = models.ImageField(upload_to=upload_to,blank=False)
    image_width = models.IntegerField()  
    image_height = models.IntegerField() 
    captured_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    # def __sntr__(self):
    #     retur f"provided Image(id: {self.image_id}, captured_by: {self.user_id.first_name})"


