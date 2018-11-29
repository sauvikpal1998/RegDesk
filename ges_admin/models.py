from django.db import models

# Create your models here.


# class AdminUser(models.Model):
#     username = models.CharField(max_length=50)
#     password = models.CharField(max_length=50)
#     permissions = models.CharField(max_length=50)
#     is_superuser = models.BooleanField(default=True)
#
#     def __str__(self):
#         return self.username+' - '+self.permissions


class Permission(models.Model):
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=100)

    def __str__(self):
        return self.name+' - '+self.pk
