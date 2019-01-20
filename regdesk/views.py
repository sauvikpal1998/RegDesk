from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from registration.models import Contingent,Data
from .models import MaleHall, FemaleHall, Allotment, AltAllotment
from django.contrib.auth.models import User
from django.shortcuts import get_list_or_404, get_object_or_404
from login.models import PostRegEmpresario

# Create your views here.

def index(request):
  return render(request, 'regdesk/login.html')

def contingent_id(request):
  
  context = {}
  
  if request.method == 'GET':
    con_id = request.GET.get("c_id")
    contingent_pk = Contingent.objects.get(captcha=con_id).pk
    students = Data.objects.filter(contingent=contingent_pk)
    
    checkedIn = []
    allotment_list = [obj.name for obj in Allotment.objects.all()]
    for student in students:
      if student.user in allotment_list:
        checkedIn.append(student)

    checkedIn_user = [obj.user for obj in checkedIn]

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
    }
    
  return render(request, 'regdesk/details.html', context)


def hall_allotment(request):
  sum = 0
  if request.method == 'GET':
    con_id = request.GET.get("c_id")
    contingent_pk = Contingent.objects.get(captcha=con_id).pk
    students = Data.objects.filter(contingent=contingent_pk)

    for student in students:
      if (request.GET.get(str(student.pk))=='1'):
        sum += 1
        obj = Allotment()
        obj.name = student.user
        
        if (student.gender == "M"):
          hall = request.GET.get("m_hall")
          obj.male_hall = MaleHall.objects.get(name=hall)
        else:
          hall = request.GET.get("f_hall")
          obj.female_hall = FemaleHall.objects.get(name=hall)
        
        obj.save()
        
    return HttpResponse(sum)
  
  else:
    return HttpResponse('Invalid Request')
        
def Empresariosf(request):
  pass
  if request.method == 'GET':
    emp_id = request.GET.get('user_id')
    user = User.get_object_or_404(id=emp_id)
    male_users = request.GET.get('male_num')
    female_users = request.GET.get('female_num')
    male_hall = request.GET.get("m_hall")
    female_hall = request.GET.get("f_hall")

    if(Data.objects.filter(user=user).category == 'Empresario Semi-Finalists'):
      obj = AltAllotment()
      obj.male_num = male_users
      obj.female_num = female_users
      obj.male_hall = MaleHall.objects.get(name=male_hall)
      obj.female_hall = FemaleHall.objects.get(name=female_hall)
      obj.category = 'Empresario'
      obj.save()
    else:
      pass
  return HttpResponse('done')

def Individual(request):
  pass
  if request.method=='GET':
    individual_id = request.GET.get('i_id')
    user = User.get_object_or_404(id=individual_id)
    hall = request.GET.get('hall')

    if(Data.objects.filter(user=user).category == 'Student Individual'):
      obj = Allotment()
      obj.name = user
      if(gender=='M'):
        obj.male_hall = hall
      else:
        obj.female_hall=hall
      obj.save()

    else:
      pass
    return HttpResponse('success')

  else:
    return HttpResponse('failed')   
      
def Startup(request):
  pass
  if request.method=='GET':
    startup_id = request.GET.get('s_id')
    user = User.get_object_or_404(id=startup_id)
    male_users = request.GET.get('male_num')
    female_users = request.GET.get('female_num')
    male_hall = request.GET.get("m_hall")
    female_hall = request.GET.get("f_hall")

    if(Data.objects.filter(user=user).category == 'Startup'):
      obj = AltAllotment()
      obj.male_num = male_users
      obj.female_num = female_users
      obj.male_hall = Hall.objects.get(name=male_hall)
      obj.female_hall = Hall.objects.get(name=female_hall)
      obj.category = 'Startup'
      obj.save()
    else:
      pass
    
    return HttpResponse('success')

  else:
    return HttpResponse('failed')
      
def Professional(request):
  pass
  if request.method=='GET':
    professional_id = request.GET.get('p_id')
    user = User.get_object_or_404(id=professional_id)
    hall = request.GET.get('hall')

    if(Data.objects.filter(user=user).category == 'Professinal'):

      obj = AltAllotment()
      obj.name = user
      obj.hall = hall
      obj.category = 'Professional'
      obj.save()

    else:
      pass

    return HttpResponse('success')

  else:
    return HttpResponse('failed')   
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
    
    