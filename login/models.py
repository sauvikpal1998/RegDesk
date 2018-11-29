from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class PostRegStartup(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True)
    details = models.TextField(max_length=600, null=True)
    website = models.URLField(max_length=100, null=True)
    size = models.IntegerField(null=True)
    events = models.CharField(max_length=100)
    startup_seedfund = models.BooleanField(default=False)
    startup_stage = models.CharField(max_length=100, null=True)
    intern_number = models.IntegerField(default=0)
    intern_stipend = models.CharField(max_length=100, null=True)
    intern_location = models.CharField(max_length=100, null=True)
    intern_profile = models.CharField(max_length=200, null=True)
    intern_duration = models.CharField(max_length=100, null=True)
    intern_description = models.CharField(max_length=100, null=True)
    epitch_sector = models.CharField(max_length=255, null=True)
    epitch_problem = models.TextField(max_length=600, null=True)
    epitch_market = models.TextField(max_length=600, null=True)
    epitch_revenue = models.TextField(max_length=600, null=True)
    epitch_compete = models.TextField(max_length=600, null=True)
    epitch_funds = models.TextField(max_length=600, null=True)
    epitch_deck = models.URLField(max_length=200, null=True)
    pexpo_type = models.CharField(max_length=20,null=True)
    pexpo_details = models.TextField(max_length=600,null=True)
    pexpo_demo = models.URLField(max_length=200,null=True)
    comeet_idea = models.BooleanField(default=False)
    comeet_skill_set = models.TextField(max_length=600, null=True)

    def __str__(self):
        return self.name


class PostRegEmpresario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    acco = models.BooleanField(default=True)
    size = models.IntegerField(default=1)

    def __str__(self):
        return self.user.username


class PostReg(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    startup = models.BooleanField(default=False)
    stage = models.CharField(max_length=100, null=True)
    profile = models.CharField(max_length=100, null=True)
    fav_startup = models.TextField(null=True)
    inspiration = models.TextField(null=True)

    def __str__(self):
        return self.user.username


class PaymentInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    amount = models.IntegerField()
#     size = models.IntegerField(default=1)
    txn_id = models.CharField(max_length=100)
    timestamp = models.DateTimeField()

    def __str__(self):
        return self.user.username+' - '+self.txn_id


class Travel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE )
    arrival = models.CharField(null=False, max_length= 50, default=0)
    departure = models.CharField(null=False, max_length= 50, default=0) 
    pnr = models.CharField(max_length=100, null=False, default=0)

    def __str__(self):
        return self.user.username


class Feedback(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)
    comments = models.TextField(max_length=300, null=True)
    download = models.BooleanField(default=False)

    def __str__(self):
        return self.user


class Halls(models.Model):
    name = models.CharField(max_length=100)
    location = models.TextField(max_length=150)
    capacity = models.IntegerField()

    def __str__(self):
        return self.name


# TODO: Separate model to store payment info associated with users by foreign key
# TODO: Model to store travel info and accommodation details of users.

