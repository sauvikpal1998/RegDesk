from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class MaleHall(models.Model):
  name = models.CharField(max_length=25)
  filled = models.IntegerField(default=0)
  capacity = models.IntegerField(default=0)

  def __str__(self):
        return str(self.name)

class FemaleHall(models.Model):
  name = models.CharField(max_length=25)
  filled = models.IntegerField(default=0)
  capacity = models.IntegerField(default=0)

  def __str__(self):
        return str(self.name)
  
class Allotment(models.Model):
  name = models.OneToOneField(User, on_delete=models.CASCADE)
  male_hall = models.ForeignKey(MaleHall, on_delete=models.CASCADE, null=True)
  female_hall = models.ForeignKey(FemaleHall, on_delete=models.CASCADE, null=True)

  def __str__(self):
        return str(self.name) + " " + str(self.hall)

class AltAllotment(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  male_hall = models.ForeignKey(MaleHall, on_delete=models.CASCADE, null=True)
  male_num = models.IntegerField(null=True)
  female_hall = models.ForeignKey(FemaleHall, on_delete=models.CASCADE, null=True)
  female_num = models.IntegerField(null=True)
  category = models.CharField(max_length=20)