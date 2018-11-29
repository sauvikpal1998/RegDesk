from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .forms import AdminLogin
from registration.models import Data, Contingent, NewCollege, College
from login.models import PostReg, PostRegEmpresario, PostRegStartup, PaymentInfo, Travel

# Create your views here.


def login_admin(request):
    form = AdminLogin(request.POST or None)
    context = {
        'form': form
    }

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_superuser:
                if request.POST.get('city'):
                    request.session['intern'] = True
                    request.session['city'] = request.POST['city']

                else:
                    request.session['intern'] = False
                login(request, user)
                return redirect('admin_dashboard')

            context['not_valid'] = user.username
            return render(request, 'ges-admin/login.html', context)

        context['error'] = 'no user'
        return render(request, 'ges-admin/login.html', context)

    return render(request, 'ges-admin/login.html', context)


def logout_admin(request):
    logout(request)
    del request.session
    return redirect('admin_login')


@login_required(login_url='/admin-panel/login')
def dashboard(request):
    return render(request, 'ges-admin/dashboard.html', {})


@login_required(login_url='/admin-panel/login')
def reg_database(request):
    users = User.objects.all()
    reg_data = []
    context = {}

    for user in users:
        if not user.is_superuser:
            user_info = []
            data = Data.objects.get(user=user)
            if request.session['intern']:
                context['city'] = request.session['city']
                if data.city == request.session['city']:
                    user_info.append(user)
                    user_info.append(data)
                    reg_data.append(user_info)

            else:
                user_info.append(user)
                user_info.append(data)
                reg_data.append(user_info)

        else:
            context['admin'] = user
            
    context['reg_data'] = reg_data
    return render(request, 'ges-admin/database.html', context)


@login_required(login_url='/admin-panel/login')
def payment_database(request):
    payments = PaymentInfo.objects.all()
    reg_data = []
    context = {}

    for payment in payments:
        user = User.objects.get(username=payment.user)
        data = Data.objects.get(user=user)
        user_info = []

        if request.session['intern']:
            context['city'] = data.city
            if data.city == request.session['city']:
                user_info.append(user)
                user_info.append(data)
                user_info.append(payment)
                reg_data.append(user_info)

        else:
            user_info.append(user)
            user_info.append(data)
            user_info.append(payment)
            reg_data.append(user_info)

    context['reg_data'] = reg_data

    return render(request, 'ges-admin/payment_database.html', context)


@login_required(login_url='/admin-panel/login')
def travel_info(request):
    travel_info = Travel.objects.all()
    reg_data = []
    context = {}

    for travel in travel_info:
        user_info = []
        user = User.objects.get(username=travel.user)
        data = Data.objects.get(user=user)

        if request.session['intern']:
            context['city'] = data.city
            if data.city == request.session['city']:
                user_info.append(user)
                user_info.append(data)
                user_info.append(travel)
                reg_data.append(user_info)

        else:
            user_info.append(user)
            user_info.append(data)
            user_info.append(travel)
            reg_data.append(user_info)

    context['reg_data'] = reg_data

    return render(request, 'ges-admin/travel_info.html', context)


@login_required(login_url='/admin-panel/login')
def startup_camp(request):
    postreg_data = PostRegStartup.objects.all()
    reg_data = []
    context = {}

    for post_data in postreg_data:
        user = User.objects.get(username=post_data.user)
        data = Data.objects.get(user=user)
        user_info = []

        events = []
        eventTypes = post_data.events.split('-')
        for event in eventTypes:
            if event == 'epitch':
                events.append('Elevator\'s Pitch')
            elif event == 'comeet':
                events.append('Cofounder\'s Meet')
            elif event == 'scamp':
                events.append('Startup Camp')
            elif event == 'pexpo':
                events.append('Product Expo')

        user_info.append(user)
        user_info.append(data)
        user_info.append(events)
        reg_data.append(user_info)

    context['reg_data'] = reg_data

    return render(request, 'ges-admin/startup_camp.html', context)


@login_required(login_url='/admin-panel/login')
def view_contingent(request, id=''):
    if not id:
        contingents = Contingent.objects.all()
        reg_data = []
        context = {}

        for contingent in contingents:
            user = User.objects.get(username=contingent.admin)
            data = Data.objects.get(user=user)
            user_info = []

            if request.session['intern']:
                context['city'] = data.city
                if data.city == request.session['city']:
                    user_info.append(user)
                    user_info.append(data)
                    user_info.append(contingent)
                    size = Data.objects.filter(contingent=data.contingent).count()
                    user_info.append(size)
                    reg_data.append(user_info)

            else:
                user_info.append(user)
                user_info.append(data)
                user_info.append(contingent)
                size = Data.objects.filter(contingent=data.contingent).count()
                user_info.append(size)
                reg_data.append(user_info)

        context['reg_data'] = reg_data

        return render(request, 'ges-admin/view_contingent.html', context)

    contingent = Contingent.objects.get(id=id)
    data = Data.objects.get(admin=contingent.id)
    admin = User.objects.get(username=contingent.admin)
    context = {
        'contingent': contingent,
        'admin': admin,
        'data': data,
    }

    if data.stage > 2:
        payment = PaymentInfo.objects.get(user=admin)
        travel = Travel.objects.get(user=admin)
        context['payment'] = payment
        context['travel'] = travel

    elif data.stage > 1:
        payment = PaymentInfo.objects.get(user=admin)
        context['payment'] = payment

    members = []
    users = User.objects.all()
    size = 0

    for user in users:
        if not user.is_superuser:
            data = Data.objects.get(user=user)
            user_info = []
            if int(data.contingent) == int(id):
                user_info.append(user)
                user_info.append(data)
                members.append(user_info)
                size = size + 1

    context['members'] = members
    context['size'] = size
    return render(request, 'ges-admin/contingent.html', context)


@login_required(login_url='admin-panel/login')
def view_profile(request, id):
    user = User.objects.get(id=id)
    data = Data.objects.get(user=user)
    context = {
        'user': user,
        'userdata': data
    }

    if data.stage:
        if data.category == 'Empresario Semi-Finalists':
            post_reg = PostRegEmpresario.objects.get(user=user)
            context['post_reg'] = post_reg

        elif data.category == 'Startup':
            post_reg = PostRegStartup.objects.get(user=user)
            context['post_reg'] = post_reg

        else:
            post_reg = PostReg(user=user)
            context['post_reg'] = post_reg

        if data.contingent:
            size = Contingent.objects.filter(id=data.contingent).count()
            context['size'] = size

    if data.stage > 1:
        payment = PaymentInfo.objects.get(user=user)
        context['payment'] = payment

    if data.stage > 2:
        travel = Travel.objects.get(user=user)
        context['travel'] = travel

    return render(request, 'ges-admin/view-profile.html', context)


@login_required(login_url='/admin-panel/login')
def add_college(request):
    colleges = NewCollege.objects.all()
    current_college = College.objects.all()
    new_college = []
    current_colleges = []

    for college in colleges:
        if college.status == 0:
            new_college.append(college)

    for college in current_college:
        current_colleges.append(college)

    context = {
        'colleges': new_college,
        'current': current_colleges
    }
    return render(request, 'ges-admin/college_requests.html', context)


@login_required(login_url='/admin-panel/login')
def act_college(request, id, task):
    new_college = NewCollege.objects.get(id=id)
    if task:
        college = College()
        college.college = new_college.college
        college.city = new_college.city
        college.save()
        new_college.status = 1

    else:
        new_college.status = -1

    new_college.save()
    return HttpResponse(True)
