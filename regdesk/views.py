from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.urls import resolve
from django.contrib.auth.decorators import login_required

from registration.models import Contingent,Data
from login.models import PostRegEmpresario, PostRegStartup
from .models import MaleHall, FemaleHall, Allotment, AltAllotment, OfflinePayment
from django.contrib.auth.models import User
from django.shortcuts import get_list_or_404, get_object_or_404
from login.models import PostRegEmpresario
from ges_admin.forms import AdminLogin

# Create your views here.

# RegDesk LogIn
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
            rett = 'regdesk_dashboard'
            if user.is_superuser:
                if request.POST.get('hall'):
                    request.session['intern'] = True
                    request.session['hall'] = request.POST['hall']
                    rett = 'hall-dash'
                else:
                    request.session['intern'] = False
                login(request, user)
                try:
                  return redirect(request.POST['next'])
                except:
                  return redirect(rett)

            context['not_valid'] = user.username
            return render(request, 'regdesk/login.html', context)

        context['error'] = 'no user'
        return render(request, 'regdesk/login.html', context)

    if request.method =='GET':
      try:
        context['next'] = request.GET['next']
      except:
        pass
    return render(request, 'regdesk/login.html', context)


# RegDesk Logout
def logout_admin(request):
    logout(request)
    del request.session
    return redirect('regdesk_login')


# Index Page
@login_required(login_url='/regdesk/login/')
def index(request):
  return render(request, 'regdesk/index.html')


# Contingent Details
@login_required(login_url='/regdesk/login/')
def contingent_details(request):
  
  context = {}
  
  if request.method == 'GET':
    con_id = request.GET.get("c_id")
    contingent = Contingent.objects.get(captcha=con_id)
    students = Data.objects.filter(contingent=contingent.pk)
    
    checkedIn = []
    allotment_list = [obj.user for obj in Allotment.objects.all()]
    for student in students:
      if student.user in allotment_list:
        checkedIn.append(student)

    checkedIn_user = [obj.user for obj in checkedIn]
    allotted = Allotment.objects.all()
    students = students.exclude(user__in=checkedIn_user)
    students_male = students.filter(gender='M')
    male_num = students_male.count()
    male_halls = MaleHall.objects.all()
    
    students_female = students.filter(gender='F')
    female_num = students.filter(gender='F').count()
    female_halls = FemaleHall.objects.all()

    context = {
      'students_male' : students_male,
      'students_female' : students_female,
      'male_num' : male_num,
      'female_num' : female_num,
      'captcha' : con_id,
      'female_halls' : female_halls,
      'male_halls' : male_halls,
      'checkedIn' : checkedIn,
      'allotted': allotted,
    }
    
  return render(request, 'regdesk/details.html', context)


# Contingent Allotment
@login_required(login_url='/regdesk/login/')
def hall_allotment(request):
  sum = 0
  if request.method == 'GET':
    con_id = request.GET.get("c_id")
    contingent = Contingent.objects.get(captcha=con_id)
    students = Data.objects.filter(contingent=contingent.pk)
    
    for student in students:
      if (request.GET.get(str(student.pk))=='1'):
        sum += 1
        obj = Allotment()
        obj.user = student.user
        
        if (student.gender == "M"):
          hall = request.GET.get("m_hall")
          m_hall = MaleHall.objects.get(name=hall)
          obj.male_hall = m_hall
          obj.male_hall.inc()
        else:
          hall = request.GET.get("f_hall")
          f_hall = FemaleHall.objects.get(name=hall)
          obj.female_hall = f_hall
          obj.female_hall.inc()
        obj.save()
        
    return HttpResponse(str(sum) + ' Allotted <a href="'+ request.GET['redirect'] +'">Click Here </a>')
  
  else:
    return HttpResponse('Invalid Request')
     

# Student, Professional, Professor, Startup, Empresario SF Details
@login_required(login_url='/regdesk/login/')
def AllDetails(request):
  if request.method == 'GET':
    i_id = request.GET['i_id']
    context = {}
    try:
      user = User.objects.get(pk = i_id)
      userdata  = Data.objects.get(user = user)
      context   = {
        'user' : user,
        'student': userdata,
      }
      category = userdata.category
      if category == 'Empresario Semi-Finalists':
        try:
          context['teamsize'] = PostRegEmpresario.objects.get(user = user).size
        except Exception as e_emp:
          context['except'] = e_emp
          context['teamsize'] = 'NotInDatabase'
      elif category == 'Startup':
        try:
          context['teamsize'] = PostRegStartup.objects.get(user = user).size
        except Exception as e_st:
          context['except'] = e_st
          context['teamsize'] = 'NotInDatabase'
      else:
        context['teamsize'] = None
      
      checkedIn = None
      conCaptcha = None
      try:
        conCaptcha = Contingent.objects.get(pk=userdata.contingent).captcha
      except Exception as ec:
        pass
      try:
        checkedIn = Allotment.objects.get(user = user)
      except Exception as e:
        try:
          checkedIn = AltAllotment.objects.get(user = user)
        except Exception as e2: 
          pass
          #context['error'] = e       
          #checkedIn = None
      context['checkedIn'] = checkedIn
      context['conCaptcha'] = conCaptcha
      if not checkedIn:
        male_halls = MaleHall.objects.all()
        female_halls = FemaleHall.objects.all()
        context['male_halls'] = male_halls
        context['female_halls'] = female_halls
        context['error'] = None
    except Exception as e:
      error = e
      context['error']= error
    return render(request, 'regdesk/individualDetails.html', context)  


# Student, Professor Allotment
@login_required(login_url='/regdesk/login/')
def IndividualCheckIn(request):
  if request.method=='GET':
    individual_id = request.GET.get('i_id')
    user = get_object_or_404(User,pk=individual_id)
    hall = request.GET.get('hall')
    userdata = Data.objects.get(user=user)
    if(userdata.category == 'Student Individual' or 'Professor'):
      obj = Allotment()
      try:
        obj.user = user
        if(userdata.gender=='M'):
          obj.male_hall = MaleHall.objects.get(name = hall)
          obj.male_hall.inc()
        else:
          obj.female_hall=FemaleHall.objects.get(name = hall)
          obj.female_hall.inc()
        obj.save()
      except Exception as e:
        return HttpResponse(e)
      return HttpResponse('success <a href="'+ request.GET['redirect'] +'">Click Here </a> ')
    else:
      pass
      return HttpResponse('Invalid Request <a href="'+ request.GET['redirect'] +'">Click Here </a> ')

  else:
    return HttpResponse('failed <a href="'+ request.GET['redirect'] +'">Click Here </a> ')   


# Empresario and Startup Allotment
@login_required(login_url='/regdesk/login/')
def EmpStartupCheckIn(request):
  pass
  if request.method=='GET':
    est_id = request.GET.get('est_id')
    user = get_object_or_404(User, pk=est_id)
    male_users = request.GET.get('male_num')
    female_users = request.GET.get('female_num')
    male_hall = request.GET.get("m_hall")
    female_hall = request.GET.get("f_hall")

    obj = AltAllotment()
    obj.user = user
    obj.male_num = male_users
    obj.female_num = female_users
    if male_hall != 'None':
      obj.male_hall = MaleHall.objects.get(name=male_hall)
      obj.male_hall.inc(int(male_users))
    else:
      obj.male_hall = None
    if female_hall != 'None':
      obj.female_hall = FemaleHall.objects.get(name=female_hall)
      obj.female_hall.inc(int(female_users))
    else:
      obj.female_hall = None
    if(Data.objects.get(user=user).category == 'Startup'):
      obj.category = 'Startup'
    else:
      obj.category = 'Empresario'

    obj.save()
    
    return HttpResponse('success <a href="'+ request.GET['redirect'] +'">Click Here </a>')

  else:
    return HttpResponse('failed <a href="'+ request.GET['redirect'] +'">Click Here </a>')


# Professional Allotment
@login_required(login_url='/regdesk/login/')
def ProfessionalCheckIn(request):
  if request.method=='GET':
    professional_id = request.GET['p_id']
    user = get_object_or_404(User,id=professional_id)
    hall = request.GET['hall']
    userData = Data.objects.get(user=user)
    if(userData.category == 'Professional'):

      obj = AltAllotment()
      obj.user = user
      if userData.gender == 'M':
        obj.male_hall = MaleHall.objects.get(name = hall)
        obj.male_hall.inc()
      else:
        obj.female_hall = FemaleHall.objects.get(name = hall)
        obj.female_hall.inc()
      obj.category = 'Professional'
      obj.save()
      return HttpResponse('success <a href="'+ request.GET['redirect'] +'">Click Here </a>')
    return HttpResponse('Invalid Request <a href="'+ request.GET['redirect'] +'">Click Here </a>')

  else:
    return HttpResponse('failed <a href="'+ request.GET['redirect'] +'">Click Here </a>')   


# Offline Payment
@login_required(login_url='/regdesk/login/')
def OfflinePay(request):
  if request.method == 'POST':
    uid = request.POST['uid']
    user = User.objects.get(pk = uid)
    userdata = Data.objects.get(user=user)
    amount = request.POST['amount']
    ofp = OfflinePayment()
    ofp.user = user
    ofp.amount = amount
    ofp.save()
    if userdata.contingent:
      for data in Data.objects.filter(contingent = userdata.contingent):
        data.stage =2
        data.save()
    else:
      userdata.stage = 2
    userdata.save()
    return HttpResponse('Payment Registered <a href="'+ request.GET['redirect'] +'">Click Here </a>')
  else:
    return HttpResponse('Eror occured <a href="'+ request.GET['redirect'] +'">Click Here </a>')


# Individual Checkout
@login_required(login_url='/regdesk/login/')
def CheckOut(request):
  return HttpResponse('Not Permitted')
  if request.method == 'GET':
    uid = request.GET['i_id']
    user = User.objects.get(pk = uid)
    data = Data.objects.get(user = user)
    try:
      obj = Allotment.objects.get(user=user)
      if data.gender == 'M':
        obj.male_hall.dec()
      else:  
        obj.female_hall.dec()
      obj.hall_checkout()
      return HttpResponse('Success <a href="'+ request.GET['redirect'] +'">Click Here </a>')      
    except Exception as e:
      try:
        obj = AltAllotment.objects.get(user=user)
        if data.gender == 'M':
          obj.male_hall.dec(obj.male_num)
        else:  
          obj.female_hall.dec(obj.female_num)
        obj.hall_checkout()
        return HttpResponse('Success <a href="'+ request.GET['redirect'] +'">Click Here </a>')
      except Exception as e2:
        return HttpResponse(e2)


# Contingent CheckOut
@login_required(login_url='/regdesk/login/')
def con_checkout(request):
  return HttpResponse('Not Permitted')
  if request.method == 'GET':
    con_id = request.GET["c_id"]
    contingent = Contingent.objects.get(captcha=con_id)
    students = Data.objects.filter(contingent=contingent.pk)
    sum = 0
    for student in students:
      if (request.GET.get(str(student.user.pk))=='out'):
        sum += 1
        obj = Allotment.objects.get(user = student.user)
        if student.gender == 'M':
          obj.male_hall.dec()
        else:  
          obj.female_hall.dec()
        obj.hall_checkout()
    return HttpResponse(str(sum)+' Checked Out All <a href="'+ request.GET['redirect'] +'">Click Here </a>')
  
  else:
    return HttpResponse('Invalid Request, <a href="'+ request.GET['redirect'] +'">Click Here </a> ')
     

# Hall Checkin
@login_required(login_url='/regdesk/login/')
def hallCheckin(request):
  if request.method == 'GET':
    uid = request.GET['i_id']
    user = User.objects.get(pk = uid)
    try:
      obj = Allotment.objects.get(user = user)
      obj.hall_checkin()
      return HttpResponse('CheckedIn at Hall. <a href="'+ request.GET['redirect'] +'">Click Here </a>')
    except Exception as e:
      try:
        obj = AltAllotment.objects.get(user = user)
        obj.hall_checkin()
        return HttpResponse('CheckedIn at Hall. <a href="'+ request.GET['redirect'] +'">Click Here </a>')
      except Exception as e2:
        return HttpResponse(e2)

# Contingent Hall Checkin
@login_required(login_url='/regdesk/login/')
def hall_con_checkin(request):
  sum = 0
  if request.method == 'GET':
    con_id = request.GET.get("c_id")
    contingent = Contingent.objects.get(captcha=con_id)
    students = Data.objects.filter(contingent=contingent.pk)
    
    for student in students:
      if (request.GET.get(str(student.user.pk))=='1'):
        sum += 1
        obj = Allotment.objects.get(user = student.user)
        if obj.male_hall:
          obj.hall_checkin()
        elif obj.female_hall:
          obj.hall_checkin()
        else:
          return HttpResponse('error')
    return HttpResponse(str(sum) + ' Checked In   <a href="'+ request.GET['redirect'] +'">Click Here </a>')
  
  else:
    return HttpResponse('Invalid Request')
     

@login_required(login_url='/regdesk/login/')
def hallDashBoard(request):
  allotAll = None
  allotAlt = None
  try:
    hall = MaleHall.objects.get(name= request.session['hall'])
    allotAll = Allotment.objects.filter(male_hall = hall)
  except Exception as e1:
    try:
      hall = FemaleHall.objects.get(name= request.session['hall'])
      allotAll = Allotment.objects.filter(female_hall = hall)
    except Exception as e2:
      try:
        hall = MaleHall.objects.get(name= request.session['hall'])
        allotAlt = AltAllotment.objects.filter(male_hall = hall)
      except Exception as e3:
        try:
          hall = FemaleHall.objects.get(name= request.session['hall'])
          allotAlt = AltAllotment.objects.filter(female_hall = hall)
        except Exception as e4:
          return HttpResponse(e4)
  context = {
    'allotAll': allotAll,
    'allotAlt': allotAlt,
  }
  return render(request, 'regdesk/hallIndex.html', context)


def getHalls(request):
  mhalls = MaleHall.objects.all()
  fhalls = FemaleHall.objects.all()
  data = ''
  for hall in mhalls:
    data = data + '<option> '+ hall.name +' </option>'
  for hall in fhalls:
    data = data + '<option> '+ hall.name +' </option>'
  return HttpResponse(data)
  

def allAllotted(request):
  allotAll = None
  allotAlt = None
  try:
    allotAll = Allotment.objects.all()
  except Exception as e1:
    try:
      allotAlt = AltAllotment.objects.all()
    except Exception as e2:
      return HttpResponse(e2)
  context = {
    'allotAll': allotAll,
    'allotAlt': allotAlt,
  }
  return render(request, 'regdesk/full.html', context)
