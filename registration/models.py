from django.db import models
from django.contrib.auth.models import User
from regdesk.models import Allotment

class DataAllotmentManager(models.Manager):
    def checkedIn(self):
        # obj = super(DataAllotmentManager, self)
        names = []
        for data in Allotment.objects.all():
            names.append(data.name)
        if self.user not in names:
            return obj
        else:
            return None


class College(models.Model):
    name = models.CharField(max_length=255, null=True)
    designation = models.CharField(max_length=100, default='Faculty')
    city = models.CharField(max_length=255)
    college = models.CharField(max_length=255)
    mobile = models.IntegerField(null=True)
    email = models.EmailField(max_length=255, null=True)

    def __str__(self):
        return self.college + " - " + self.city


class Contingent(models.Model):
    captcha = models.CharField(max_length=100)
    admin = models.OneToOneField(User, on_delete=models.CASCADE)
    college = models.ForeignKey(College, models.SET_NULL, null=True)    # Foreign Key creates a many to one relationship should be same as admin's college
    size = models.IntegerField(default=5)
    stage = models.IntegerField(default=1)
    link = models.CharField(max_length=100, null=False, default='01')

    def __str__(self):
        return str(self.pk) + ". - " + self.college.college


# Default User Info Modal Email ID & Password are stored in default django user modal
class Data(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    category = models.CharField(max_length=50)
    stage = models.SmallIntegerField(default=0)
    gender = models.CharField(max_length=10)
    mobile = models.BigIntegerField()
    tshirt = models.CharField(max_length=1)
    city = models.CharField(max_length=100)
    college = models.CharField(max_length=150, default=None)
    contingent = models.IntegerField(blank=True, null=True, default=None)     # store contingent id if part of any contingent else None
    admin = models.IntegerField(default=0)     # contingent id if user is contingent admin else 0
    session_type = models.IntegerField(default=0)                #Set user session type to easily play with ui, 0 for all ui based views, -1 for only info view and 1 for no additional info view & contingent

    objects = DataAllotmentManager()

    def __str__(self):
        return self.name


class NewCollege(models.Model):
    name = models.CharField(max_length=150)
    gender = models.CharField(max_length=10)
    email = models.CharField(max_length=150)
    year_of_study = models.CharField(max_length=150)
    mobile = models.BigIntegerField()
    city = models.CharField(max_length=150)
    college = models.CharField(max_length=150)
    contact_dean = models.CharField(max_length=255)
    contact_ecell = models.CharField(max_length=255)
    status = models.IntegerField(default=0)     # 1 if request accepted -1 if rejected, 0 by default

    def __str__(self):
        return self.college + ' - ' + self.city


class EmpresarioSF(models.Model):
    tid = models.IntegerField()
    startup = models.CharField(max_length=100, null=True)
    track = models.CharField(max_length=100, null=True)
    name1 = models.CharField(max_length=100, null=True)
    email1 = models.EmailField(max_length=100, null=True)
    mobile1 = models.IntegerField(null=True)
    name2 = models.CharField(max_length=100, null=True)
    email2 = models.EmailField(max_length=100, null=True)
    mobile2 = models.IntegerField(null=True)
    name3 = models.CharField(max_length=100, null=True)
    email3 = models.EmailField(max_length=100, null=True)
    mobile3 = models.IntegerField(null=True)
    name4 = models.CharField(max_length=100, null=True)
    email4 = models.EmailField(max_length=100, null=True)
    mobile4 = models.IntegerField(null=True)
    name5 = models.CharField(max_length=100, null=True)
    email5 = models.EmailField(max_length=100, null=True)
    mobile5 = models.IntegerField(null=True)
    acco = models.BooleanField(default=False)
    size = models.IntegerField(null=True)

    def __str__(self):
        return str(self.tid) + ' - ' + self.startup
