from django.db import models
from django.contrib.auth.models import User
from registration.models import Data
# Create your models here.

class MaleHall(models.Model):
  name = models.CharField(max_length=25)
  left = models.IntegerField(default=0)
  capacity = models.IntegerField(default=0)

  def __str__(self):
    return str(self.name)
  
  def inc(self, count = 1):
    self.left = self.left - count
    self.save()
    
  def dec(self, count = 1):
    self.left = self.left + count
    self.save()


class FemaleHall(models.Model):
  name = models.CharField(max_length=25)
  left = models.IntegerField(default=0)
  capacity = models.IntegerField(default=0)

  def __str__(self):
    return str(self.name)

  def inc(self, count = 1):
    self.left = self.left - count
    self.save()

  def dec(self, count = 1):
    self.left = self.left + count
    self.save()

  
class Allotment(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  userdata = models.ForeignKey(Data, on_delete=models.CASCADE)
  male_hall = models.ForeignKey(MaleHall, on_delete=models.CASCADE, null=True)
  female_hall = models.ForeignKey(FemaleHall, on_delete=models.CASCADE, null=True)
  hall_stat = models.CharField(max_length = 1, default = 0)

  def __str__(self):
    return str(self.user) + " " + str(self.male_hall) + " " + str(self.female_hall)

  def hall_checkin(self):
    self.hall_stat = 1
    self.save()

  def hall_checkout(self):
    self.hall_stat = 0
    self.save()
  
  def save(self, *args, **kwargs):
    self.userdata = Data.objects.get(user = self.user)
    super().save(*args, **kwargs)  # Call the "real" save() method.



class AltAllotment(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  userdata = models.ForeignKey(Data, on_delete=models.CASCADE)
  male_hall = models.ForeignKey(MaleHall, on_delete=models.CASCADE, null=True)
  male_num = models.IntegerField(null=True, default=0)
  female_hall = models.ForeignKey(FemaleHall, on_delete=models.CASCADE, null=True)
  female_num = models.IntegerField(null=True,default=0)
  category = models.CharField(max_length=20)
  hall_stat = models.CharField(max_length = 1, default = 0)
  def __str__(self):
    return str(self.user) + " " + str(self.category) + " " + str(self.male_hall) + " " +str(self.female_hall)
  
  def hall_checkin(self):
    self.hall_stat = 1
    self.save()

  def hall_checkout(self):
    self.hall_stat = 0
    self.save()
  
  
  def save(self, *args, **kwargs):
    self.userdata = Data.objects.get(user = self.user)
    super().save(*args, **kwargs)  # Call the "real" save() method.



class OfflinePayment(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  amount = models.CharField(max_length = 10, null = True)
  method = models.CharField(max_length=126, null = True)
  time = models.DateTimeField(auto_now_add=True)
  def __str__(self):
    return 'GES ID ' +str(self.user.pk)+ ', INR ' +str(self.amount)