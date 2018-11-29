from django.contrib import admin
from .models import Data, Contingent, College, NewCollege

# Register your models here.

admin.site.register(Data)
admin.site.register(Contingent)
admin.site.register(College)
admin.site.register(NewCollege)