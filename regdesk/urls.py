from django.urls import path, include
from . import views

urlpatterns = [
  path('', views.index, name = 'regdesk_dashboard'),
  path('login/', views.login_admin, name='regdesk_login'),
  path('logout/', views.logout_admin, name='regdesk_logout'),
#  path('empresario', views.Empresariosf, name = 'empresario'),
#  path('startup', views.Startup, name = 'startup'),
  path('contingent_details', views.contingent_details, name = 'contingent_details'),
  path('hall_allotment', views.hall_allotment, name = 'hall_allotment'),          # Contingent Checkin
  path('con-checkout/', views.con_checkout, name='con_checkout'),                 # Contingent Checkout
  path('individual_details', views.AllDetails, name = 'individual_details'),
  path('individual', views.IndividualCheckIn, name = 'individual'),
  path('empstartup', views.EmpStartupCheckIn, name='empstartup'),
  path('professional', views.ProfessionalCheckIn, name='professional'),
  path('checkout', views.CheckOut, name='checkout'),
  path('offlinepay/', views.OfflinePay, name='offlinepay'),
]