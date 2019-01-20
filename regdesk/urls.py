from django.urls import path, include
from . import views

urlpatterns = [
  path('', views.index, name = 'index'),
  path('contingent_id', views.contingent_id, name = 'contingent_id'),
  path('hall_allotment', views.hall_allotment, name = 'hall_allotment'),
  path('individual', views.Individual, name = 'indivudual'),
  path('empresario', views.Empresariosf, name = 'empresario'),
  path('startup', views.Startup, name = 'startup'),
  
]