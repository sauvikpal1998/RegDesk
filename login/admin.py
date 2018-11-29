from django.contrib import admin
from .models import PostRegStartup, PostRegEmpresario, PostReg, PaymentInfo, Travel, Feedback, Halls

# Register your models here.

admin.site.register(PostReg)
admin.site.register(PostRegStartup)
admin.site.register(PostRegEmpresario)
admin.site.register(PaymentInfo)
admin.site.register(Travel)
admin.site.register(Feedback)
admin.site.register(Halls)

