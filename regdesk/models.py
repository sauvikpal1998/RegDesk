from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Hall(models.Model):
  name = models.CharField(max_length=25)
  filled = models.IntegerField(default=0)
  capacity = models.IntegerField(default=0)
  gender = models.CharField(max_length=5, default=None)

  def __str__(self):
        return str(self.name)

  
class Allotment(models.Model):
  name = models.OneToOneField(User, on_delete=models.CASCADE)
  hall = models.ForeignKey(Hall, on_delete=models.CASCADE)
  
  def __str__(self):
        return str(self.name) + " " + str(self.hall)
