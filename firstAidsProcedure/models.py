from django.db import models

# Create your models here.

class FirstAidsProcedure(models.Model):
    procedure = models.CharField(max_length=100)
    procedure_for_degree = models.CharField(max_length=50)
    procedure_order = models.IntegerField()
