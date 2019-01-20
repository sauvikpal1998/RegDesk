from django.contrib import admin
from .models import MaleHall, FemaleHall, Allotment

class DisplayHall(admin.ModelAdmin):
  fields = ('name', 'capacity')

class DisplayAllotment(admin.ModelAdmin):
  fields = ('name', 'hall')
  
admin.site.register(MaleHall)
admin.site.register(FemaleHall)
admin.site.register(Allotment)
# Register your models here.
