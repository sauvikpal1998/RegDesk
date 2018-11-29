from django.contrib import admin
from django.urls import path, include
from registration import views as signup
from login import views as post_reg

# register, login, post-reg-1,post-reg-2, payment, travel, create-contingent, join-contingent, faq, contact 
# Registration & Login to be handled by registration app
# Post reg process to be handled by login app

urlpatterns = [
    # Admin Panel
    path('admin/', admin.site.urls),
    path('admin-panel/', include('ges_admin.urls')),
#     path('regdesk/', include('regdesk.urls')),
  

    # Registration and related functionality
    path('register/', signup.registerUser, name='register'),                     # Return a reg form on a get request
    path('activate/<str:uid>/<str:token>/', signup.activate, name='activate'),   # Email Verification of new users
    path('register/new/college', signup.college, name='newCollege'),             # Register colleges not in our database

    # Login & Logout
    path('login/', signup.loginUser, name='login'),
    path('logout/', signup.logoutUser, name='logout'),

    # Static Pages
    path('contact/', post_reg.contact, name='contact'),
#     path('contact_us/', post_reg.contact_us, name='contact_us'),

    path('faq/', post_reg.faq, name='faq'),

    # Post Registration and related functionality
    path('', post_reg.home, name='home'),
    path('payment/', include('payment.urls')),
    path('dashboard/', post_reg.dashboard, name='dashboard'),
    path('join-contingent/', post_reg.join, name='join'),
    path('create-contingent/', post_reg.create, name='create'),
    path('view-contingent/', post_reg.view, name='view_contingent'),
    path('join-contingent/<str:contingent_id>/<str:contingent_captcha>', post_reg.join, name='join'),
    path('add-members/', post_reg.addMembers, name='add_members'),
  
    # URLS FOR PROCESSING AJAX REQUESTS (only via post requests)
    path('register/city', signup.getCity, name='getCity'),                       # Retrieve cities & return via AJAX
    path('register/college/<str:city>/', signup.getCollege, name='getCollege'),  # Retrieve colleges & return via AJAX
    path('register/validate', signup.validateUser, name='validate'),             # Validate & submit form data via AJAX
    path('validate/post-reg-startup', post_reg.validatestartup, name='validatestartup'),
    path('validate/post-reg-empresario', post_reg.validateempresario, name='validateempresario'),
    path('validate/post-reg-regular', post_reg.validateregular, name='validateregular'),
    path('validate/travel-details', post_reg.validatetravel, name='validatetravel'),
    path('create-contingent/validate', post_reg.validate_create_contingent, name='validate_create_contingent'),  
    path('add-members/validate', post_reg.validate_add_members, name='validate_add_members'),  
    
    path('regdesk/', include('regdesk.urls')),
]
