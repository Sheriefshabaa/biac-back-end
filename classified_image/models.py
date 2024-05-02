from django.db import models
from image.models import Image

class Classified_image (models.Model) :
    image_id = models.ForeignKey(Image, on_delete=models.CASCADE)
    volunteers_evaluation_score = models.IntegerField(null=True)
    number_of_evalutors_per_image = models.IntegerField(null=True)
    image_with_model_classification = models.ImageField(null=False)
    confidence_score = models.FloatField(null=True)
    burn_degree = models.CharField(max_length=50,null=True)
    image_width = models.IntegerField(null=True)  
    image_height = models.IntegerField(null=True) 
    image_cordinate_x = models.IntegerField(null=True)  
    image_cordinate_y = models.IntegerField(null=True) 



