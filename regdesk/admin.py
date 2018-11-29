from django.contrib import admin
from .models import Hall, Allotment

class DisplayHall(admin.ModelAdmin):
  fields = ('name', 'capacity')

class DisplayAllotment(admin.ModelAdmin):
  fields = ('name', 'hall')
  
admin.site.register(Hall)
admin.site.register(Allotment)
# Register your models here.
