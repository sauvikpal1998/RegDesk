from django import forms
from django.contrib.auth.models import User
from .models import PostRegStartup, PostRegEmpresario, PostReg, Travel


EVENTS_CHOICES = (
    ('epitch', 'Elevator\'s Pitch'),
    ('pexpo', 'Product Expo'),
    ('comeet', 'Co-Founder\'s Meet'),
    ('startup', 'Startup Camp')
)

BOOL_CHOICES = (
    (True, 'Yes'),
    (False, 'No')
)

STARTUP_STAGE = (
    ('Idea', 'Ideation Phase'),
    ('proof', 'Proof of Concept'),
    ('op < 1', 'Operational (Less than 1 year)'),
    ('op > 1', 'Operational (More than 1 year)')
)

SKILL_SET = (
    ('web-d', 'Web Development'),
    ('app-d', 'Android/iOS Development'),
    ('iot', 'IOT'),
    ('marketing', 'Marketing'),
    ('operations', 'Operations'),
    ('sales', 'Sales'),
)

INTERN_CHOICE = (
    ('web-d', 'Web Development'),
    ('app-d', 'Android/iOS Development'),
    ('iot', 'IOT'),
    ('marketing', 'Marketing'),
    ('operations', 'Operations'),
    ('sales', 'Sales'),
)

PRODUCT_TYPE = (
    ('Hardware', 'Hardware'),
    ('Software', 'Software'),
)


class CreateContingentForm(forms.Form):
    gesid1 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the ges id of first member.', 'required':'true', 'disabled': 'disabled'}))
    gesid2 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the ges id of second member.', 'required':'true'}))
    gesid3 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the ges id of third member.', 'required':'true'}))
    gesid4 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the ges id of fourth member.', 'required':'true'}))
    gesid5 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the ges id of fifth member.', 'required':'true'}))
    
    class Meta:
        model = User
        labels = ['gesid1' ,'gesid2' ,'gesid3' ,'gesid4']
        
        
class JoinContingentForm(forms.Form):
  uid = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the contingent id.', 'required':'false'}))
  captcha = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter the contingent password', 'required':'true'}))
  
#   class Meta:
#     model = User
#     fields = ['ges_id1' , 'ges_pass1']
    

class PostRegStartupForm(forms.ModelForm):
    details = forms.CharField(widget=forms.TextInput(attrs={'required': 'true', 'class': 'form-control', 'placeholder': 'Details about your company/startup here.'}))
    website = forms.CharField(widget=forms.TextInput(attrs={'required': 'true', 'class': 'form-control', 'placeholder': 'http://www.domain.com'}))
    size = forms.CharField(widget=forms.NumberInput(attrs={'required': 'true', 'class': 'form-control', 'placeholder': 'Total number of people coming to attend GES.'}))

    class Meta:
        model = PostRegStartup
        fields = ['details', 'website', 'size']


class CoMeetForm(forms.ModelForm):
    comeet_idea = forms.ChoiceField(choices=BOOL_CHOICES, widget=forms.RadioSelect(attrs={'required': 'true', 'class': 'custom-radio', 'id': 'inlineRadio114'}))
    comeet_skill_set = forms.MultipleChoiceField(choices=SKILL_SET, widget=forms.CheckboxSelectMultiple(attrs={'class': 'custom-select', 'id': 'inlineCheckbox114'}))

    class Meta:
        model = PostRegStartup
        fields = ['comeet_idea', 'comeet_skill_set']


class PExpoForm(forms.ModelForm):
    pexpo_type = forms.ChoiceField(choices=PRODUCT_TYPE, widget=forms.RadioSelect(attrs={'required': 'true', 'class': 'custom-radio', 'id': 'inlineRadio114'}))
    pexpo_details = forms.CharField(widget=forms.TextInput(attrs={'required': 'true', 'class': 'form-control', 'placeholder': 'Product Specific Details'}))
    pexpo_demo = forms.CharField(widget=forms.TextInput(attrs={'required': 'true', 'class': 'form-control', 'placeholder': 'A link to your product demo.'}))

    class Meta:
        model = PostRegStartup
        fields = ['pexpo_type', 'pexpo_details', 'pexpo_demo']


class EPitchForm(forms.ModelForm):
    epitch_sector = forms.CharField(widget=forms.TextInput(attrs={'required': 'true', 'class': 'form-control', 'placeholder': 'IOT, E-Commerce, etc.'}))
    epitch_problem = forms.CharField(widget=forms.TextInput(attrs={'required': 'true', 'class': 'form-control'}))
    epitch_market = forms.CharField(widget=forms.TextInput(attrs={'required': 'true', 'class': 'form-control'}))
    epitch_revenue = forms.CharField(widget=forms.TextInput(attrs={'required': 'true', 'class': 'form-control'}))
    epitch_compete = forms.CharField(widget=forms.TextInput(attrs={'required': 'true', 'class': 'form-control'}))
    epitch_funds = forms.CharField(widget=forms.TextInput(attrs={'required': 'true', 'class': 'form-control'}))
    epitch_deck = forms.CharField(widget=forms.TextInput(attrs={'required': 'true', 'class': 'form-control', 'placeholder': 'Links can be Google drive, Youtube etc.,'}))

    class Meta:
        model = PostRegStartup
        fields = ['epitch_sector', 'epitch_problem', 'epitch_market', 'epitch_revenue', 'epitch_compete',
                  'epitch_funds', 'epitch_deck'
                 ]


class SCampForm(forms.ModelForm):
    intern_number = forms.CharField(widget=forms.NumberInput(attrs={'required': 'true', 'class': 'form-control', 'placeholder': 'Number of interns required.'}))
    intern_stipend = forms.CharField(widget=forms.TextInput(attrs={'required': 'true', 'class': 'form-control', 'placeholder': 'Min. Stipend(INR) - Max. Stipend(INR)'}))
    intern_location = forms.CharField(widget=forms.TextInput(attrs={'required': 'true', 'class': 'form-control', 'placeholder': 'City'}))
    intern_duration = forms.CharField(widget=forms.NumberInput(attrs={'required': 'true', 'class': 'form-control', 'placeholder': 'Internship Duration (in weeks)'}))
    intern_description = forms.CharField(widget=forms.TextInput(attrs={'required': 'true', 'class': 'form-control', 'placeholder': 'Details about your company/startup here.'}))
    intern_profile = forms.CharField(widget=forms.TextInput(attrs={'required': 'true', 'class': 'form-control', 'placeholder': 'Web/app Development, marketing,etc.'}))
    startup_seedfund = forms.ChoiceField(choices=BOOL_CHOICES, widget=forms.RadioSelect(attrs={'required': 'true', 'class': 'custom-radio', 'id': 'inlineRadio114'}))
    startup_stage = forms.ChoiceField(choices=STARTUP_STAGE, widget=forms.Select(attrs={'required': 'true', 'class': 'custom-select', 'id': ''}))

    class Meta:
        model = PostRegStartup
        fields = ['startup_seedfund', 'startup_stage', 'intern_number', 'intern_stipend', 'intern_location',
                  'intern_duration', 'intern_description', 'intern_profile']


class PostRegEmpresarioForm(forms.ModelForm):
    acco = forms.ChoiceField(choices=BOOL_CHOICES, widget=forms.RadioSelect(attrs={'required': 'true', 'class': 'custom-radio', 'id': 'inlineRadio114'}))
    size = forms.CharField(widget=forms.NumberInput(attrs={'required': 'true', 'class': 'form-control', 'placeholder': 'Number of people coming to attend GES.', 'min': 1}))

    class Meta:
        model = PostRegEmpresario
        fields = ['acco', 'size']


class PostRegForm(forms.ModelForm):
    startup = forms.ChoiceField(choices=BOOL_CHOICES, widget=forms.RadioSelect(attrs={'required': 'true', 'class': 'custom-radio', 'id': 'inlineRadio114'}))
    fav_startup = forms.CharField(widget=forms.Textarea(attrs={'required': 'true', 'class': 'form-control textarea-md'}))
    inspiration = forms.CharField(widget=forms.Textarea(attrs={'required': 'true', 'class': 'form-control textarea-md'}))
    stage = forms.ChoiceField(choices=STARTUP_STAGE, widget=forms.RadioSelect(attrs={'class': 'custom-radio', 'id': 'inlineRadio114'}))
    profile = forms.MultipleChoiceField(choices=INTERN_CHOICE, widget=forms.CheckboxSelectMultiple(attrs={'class': 'custom-select', 'id': 'inlineCheckbox114'}))

    class Meta:
        model = PostReg
        fields = ['startup', 'fav_startup', 'inspiration', 'stage', 'profile']
        
class TravelForm(forms.Form):
  arrival = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'required': 'true', 'class': 'form-control', 'placeholder': 'dd/mm/yyyy HH:MM'}))
  departure = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'required': 'true', 'class': 'form-control', 'placeholder': 'dd/mm/yyyy HH:MM'}))
#   arrival = forms.CharField(widget=forms.TextInput(attrs={'required': 'true', 'class': 'form-control', 'placeholder': 'Enter your arrival date'}))
#   departure = forms.CharField(widget=forms.TextInput(attrs={'required': 'true', 'class': 'form-control', 'placeholder': 'Enter your departure date'}))
  pnr = forms.CharField(widget=forms.TextInput(attrs={'required': 'true', 'class': 'form-control', 'placeholder': 'Enter your PNR number or Booking ID'}))
  