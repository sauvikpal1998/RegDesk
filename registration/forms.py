from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import College


GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
)

CATEGORY_CHOICES = (
    ('Student Individual', 'Student Individual'),
    ('College Contingent', 'College Contingent'),
    ('Professional', 'Professional'),
    ('Professor', 'Professor'),
    ('Campus Ambassador', 'Campus Ambassador'),
    ('GES Ambassador', 'GES Ambassador'),
    ('Empresario Semi-Finalists', 'Empresario Semi-Finalists'),
    ('Startup', 'Startup'),
)


# DO NOT DELETE THESE EMPTY CHOICES
CITY_CHOICES = (
)

COLLEGE_CHOICES = (
)

TSHIRT_CHOICES = (
    ('S', 'S'),
    ('M', 'M'),
    ('L', 'L'),
    ('XL', 'XL'),
    ('XXL', 'XXL'),
)


class CreateUser(UserCreationForm):
    category = forms.ChoiceField(choices=CATEGORY_CHOICES, widget=forms.Select(attrs={'class': 'custom-select category', 'required': 'false'}))
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter full name here.', 'required': 'true'}))
    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.RadioSelect(attrs={'class': 'custom-radio', 'id': 'inlineRadio114'}))
    city = forms.ChoiceField(choices=CITY_CHOICES, widget=forms.Select(attrs={'class': 'custom-select category popover-button-default', 'data-trigger': 'focus', 'data-placement': 'right', 'data-original-title': 'If your city is not present here, please contact', 'data-content': 'Abc |  abc@ecell-iitkgp.org | Mobile Number of ABC', 'required': 'false'}))
    college = forms.ChoiceField(choices=COLLEGE_CHOICES, widget=forms.Select(attrs={'class': 'custom-select category popover-button-default', 'data-trigger': 'focus', 'data-placement': 'right', 'data-original-title': 'If your college is not present here, please contact', 'data-content': 'Abc |  abc@ecell-iitkgp.org | Mobile Number of ABC', 'required': 'false'}))
    company = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter name of company/startup here.', 'required':'false'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email address here.', 'required': 'true'}))
    mobile = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter your phone number here.', 'required': 'true'}))
    tshirt = forms.ChoiceField(choices=TSHIRT_CHOICES, widget=forms.RadioSelect(attrs={'class': 'custom-radio', 'id': 'inlineRadio114'}))
    password = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password here.', 'required':'true'}))
    confirm_password = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Re-enter your password.', 'required':'true'}))
    emp_id = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your team id.', 'required':'false'}))

    class Meta:
        model = User
        fields = ['category', 'name', 'gender', 'email', 'mobile', 'password', 'tshirt', 'city', 'college', 'company']


class LoginUser(forms.Form):
    category = forms.ChoiceField(choices=CATEGORY_CHOICES, widget=forms.Select(attrs={'class': 'custom-select category ', 'required': 'true'}))
    username = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email address here.', 'required': 'true'}))
    password = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your name here.', 'required': 'true'}))


class NewCollegeForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter full name here.', 'required': 'true'}))
    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.RadioSelect(attrs={'class': 'custom-radio'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email address here.', 'required': 'true'}))
    mobile = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter your phone number here.', 'required': 'true'}))
    city = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter city where your college is located.', 'required':'true'}))
    college = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter name of your college here', 'required': 'true'}))
    year_of_study = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your year of study here', 'required': 'true'}))
    contact_dean = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter name, position, email & mobile number of concerned perrson here', 'required': 'true'}))
    contact_ecell = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter name, position, email & mobile number of concerned perrson here', 'required': 'true'}))

    class Meta:
        model = College
        fields = ['name', 'gender', 'email', 'mobile', 'year_of_study', 'contact_dean', 'city', 'college', 'contact_ecell']



# TODO: Edit Radio Css
