from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST, require_GET
from django.http import HttpResponse, HttpResponseRedirect
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail, EmailMessage
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from .forms import CreateUser, LoginUser, NewCollegeForm
from . models import Data, College, Contingent, NewCollege, EmpresarioSF
from .tokens import account_activation_token
from login.models import PostRegStartup
from django.conf import settings


@require_GET
def registerUser(request):
    form = CreateUser()
    context = {
        'form': form
    }
    return render(request, 'registration/register.html', context)


def loginUser(request):
    try:
        if request.session['username']:
            return redirect('home')
    except KeyError:
        form = LoginUser(request.POST or None)

        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            category = request.POST['category']

            try:
                user = User.objects.get(username=username)
                if not user.is_active:
                    context = {
                        'form': form,
                        'error': 'Email Not Verified',  # Email Not Verified
                        'content': 'Please verify your email first by visiting link given in verification mail.'
                    }
                    return render(request, 'registration/login.html', context)

                if not user.check_password(password):
                    context = {
                        'form': form,
                        'error': 'Passwords do not match',  # Incorrect Password
                        'content': 'You have entered wrong password. Please try again'
                    }
                    return render(request, 'registration/login.html', context)

                userdata = Data.objects.get(user=user)

                try:
                    contingent = Contingent.objects.get(admin=user)
#                     if category == 'College Contingent':
                    request.session['contingent'] = contingent.id
                    request.session['category'] = 'College Contingent'

#                     else:
#                         context = {
#                             'form': form,
#                             'error': 'Wrong category selected.',
#                             'content': 'You have selected wrong category. Please try again. In case you have created a contingent try choosing college contingent category.',
#                         }
#                         return render(request, 'registration/login.html', context)

                except Contingent.DoesNotExist:
                    if category == 'College Contingent':
                        context = {
                            'form': form,
                            'error': 'Contingent Not Found',  # Incorrect Password
                            'content': 'We do not find any contingent associated with your email address.',
                        }
                        return render(request, 'registration/login.html', context)

                    elif userdata.category != category:
                        context = {
                            'form': form,
                            'error': 'Wrong category selected.',
                            'content': 'You have selected wrong category. Please try again. In case you have created a contingent try choosing college contingent category.',
                        }
                        return render(request, 'registration/login.html', context)

                    request.session['category'] = category
                    request.session['id'] = user.pk

                # Set Session Data
                request.session['email'] = user.username
                request.session['name'] = userdata.name
                request.session['city'] = userdata.city
                request.session['college'] = userdata.college
                request.session['stage'] = userdata.stage
                request.session['type'] = userdata.session_type
                request.session['role'] = user.is_superuser

                login(request, user)
                if request.POST.get('next'):
                  return HttpResponseRedirect(request.POST.get('next'))
                return redirect('home')

            except User.DoesNotExist:
                context = {
                    'form': form,
                    'error': 'Email Not Registered',                     # Invalid Email Id/User Not Registered
                    'content': 'Email you have entered is not registered with us. Please check for typos in the email'
                }
                return render(request, 'registration/login.html', context)

        next = request.GET.get('next')
        context = {
            'form': form
        }
        if next:
          context['next'] = next
        return render(request, 'registration/login.html', context)


def logoutUser(request):
    logout(request)
    del request.session
    return redirect('login')


@require_POST
def validateUser(request):   # Validate and register new users only via post request
    if request.method != 'POST':
        return redirect('home')
    else:
        category = request.POST['category']
        name = request.POST.get("name")
        gender = request.POST['gender']
        email = request.POST['email']
        mobile = request.POST['mobile']
        city = request.POST['city']
        password = request.POST['password']
        tshirt = request.POST['tshirt']

        if not validateEmail(email):
            return HttpResponse("Invalid Email")

        try:
            user = User.objects.get(username=email)
            if user is not None:
                return HttpResponse("Email Exists")

        except User.DoesNotExist:

            if category == 'Empresario Semi-Finalists':
                tid = request.POST['emp_id']
                try:
                    team = EmpresarioSF.objects.get(tid=tid, email1=email)
                except EmpresarioSF.DoesNotExist:
                    return HttpResponse('no team')

            user = User()
            user.username = email
            user.email = email
            user.set_password(raw_password=password)
            user.is_active = False                    # User needs to verify email before being able to log in
            user.save()
            user.last_name = account_activation_token.make_token(user)
            user.first_name = urlsafe_base64_encode(force_bytes(user.pk))
            user.save()

            userdata = Data()
            userdata.user = user
            userdata.name = name
            userdata.category = category
            userdata.stage = 0
            userdata.gender = gender
            userdata.mobile = mobile
            userdata.tshirt = tshirt
            userdata.city = city

            if category == 'Professional' or category == 'Startup' or category == 'Empresario Semi-Finalists':
                userdata.session_type = -1
                userdata.college = request.POST['company']

                if category == 'Startup':
                    events = request.POST['eventType']
                    PostRegStartupData = PostRegStartup()
                    PostRegStartupData.name = userdata.college
                    PostRegStartupData.user = user
                    PostRegStartupData.events = events
                    PostRegStartupData.save()
            else:
                userdata.session_type = 0
                userdata.college = request.POST['college']

            userdata.contingent = False
            userdata.save()

            if sendMail(request, user, password, userdata):
                return HttpResponse("Verification Email Sent")
            return HttpResponse("User Saved")


def college(request):
    form = NewCollegeForm(request.POST or None)

    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        mobile = request.POST['mobile']
        gender = request.POST['gender']
        year_of_study = request.POST['year_of_study']
        city = request.POST['city']
        college = request.POST['college']
        contact_dean = request.POST['contact_dean']
        contact_ecell = request.POST['contact_ecell']

        if not validateEmail(email):
            print(email)
            context = {
                'form': form,
                'error': 'Invalid Email',
                'content': 'Email you entered is not a valid email address.'
            }
            return render(request, 'registration/newCollege.html', context)

        if len(mobile) != 10:
            context = {
                'form': form,
                'error': 'Invalid Mobile Number',
                'content': 'Please Enter a valid 10 digit mobile number.'
            }
            return render(request, 'registration/newCollege.html', context)

        newCollege = NewCollege(name=name, gender=gender, city=city, college=college, email=email, mobile=mobile, year_of_study=year_of_study, contact_dean=contact_dean, contact_ecell=contact_ecell)
        newCollege.save()

        newForm = NewCollegeForm()
        context = {
            'form': newForm,
            'success': True
        }
        #TODO: Send Confirmation Email
        return render(request, 'registration/newCollege.html', context)

    context = {
        'form': form
    }
    return render(request, 'registration/newCollege.html', context)


@require_POST
def getCity(request):
    cities = College.objects.values('city').distinct()
    list = ''
    for city in cities:
        list += '<option value="'+city["city"]+'">'+city["city"]+'</option>'

    return HttpResponse(list)


@require_POST
def getCollege(request, city):
    colleges = College.objects.filter(city=city)
    list = ''
    for college in colleges:
        list += '<option value="'+college.college+'">'+college.college+'</option>'

    return HttpResponse(list)


# Validates whether email is valid and not registered
def validateEmail(email):                # Email Validator
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False


# Sends Verification Email
def sendMail(request, user, password, userdata, sender=settings.DEFAULT_FROM_EMAIL):
    # TODO: Send GES ID in verification mail as well

    current_site = get_current_site(request)
    subject = '[E-Cell, IIT Kharagpur]: Verification email for participating in GES 2019'
    message = render_to_string('email/email_verify.html', {
        'user': user,
        'userdata': userdata,
        'password': password,
        'domain': current_site.domain,
        'uid': user.first_name,
        'token': user.last_name,
    })
    
    msg = EmailMessage(subject=subject, body=message, from_email=sender, bcc=[user.email])
    msg.content_subtype = "html"  # Main content is now text/html
    return msg.send()
    
#     try:
#         user.email_user(subject, html_message=message)
#         return True
#     except:
#         return False


# Validates uid and token passed and activates the user if true
def activate(request, uid, token):
    context = {
        'domain': get_current_site(request).domain,
        'uid': uid,
        'token': token,
    }
    try:
        user = User.objects.get(first_name=uid)
        if user.last_name == token:
            user.is_active = True
            user.save()
            return redirect('login')
        else:
            return render(request, 'email/invalidToken.html', context)
    except User.DoesNotExist:
            return render(request, 'email/invalidUID.html', context)