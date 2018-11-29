from django.urls import path
from . import views

urlpatterns = [

    # login
    path('login/', views.login_admin, name='admin_login'),
    path('logout/', views.logout_admin, name='admin_logout'),

    path('', views.dashboard, name='admin_dashboard'),     # TODO: Make admin permission levels
    path('view/<str:id>/', views.view_profile, name='admin_view_profile'),
    path('registrations/', views.reg_database, name='admin_reg_database'),
    path('payments/', views.payment_database, name='admin_payments_database'),
    path('startup-camp/', views.startup_camp, name='admin_startup_camp'),
    path('college-requests/', views.add_college, name='admin_add_college'),
    path('contingent/', views.view_contingent, name='admin_view_contingent'),
    path('view-contingent/<str:id>', views.view_contingent, name='admin_view_contingent'),
    path('travel-info/', views.travel_info, name='admin_travel_info'),
    path('act-college/<str:id>/<int:task>', views.act_college, name='admin_act_college')
]

# TODO: Setup permission levels for interns, pr team, web heads(superuser privilege), cna team, fnl team.
