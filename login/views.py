from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from registration.models import Data, Contingent, College
from .models import PostRegStartup, PostRegEmpresario, PostReg,Travel
from .forms import PostRegStartupForm, CoMeetForm, PExpoForm, SCampForm, EPitchForm, PostRegEmpresarioForm, PostRegForm, CreateContingentForm, JoinContingentForm, TravelForm

# Always pass user & userdata in context of every function which renders any template as base.html depends on it.
# Give login_required decorator at beginning of each function to ensure user does not see that page without logging in.
# Contingent option is enabled if and only if the participant is on stage 1.
# TODO: create & join contingent only accessible on stage 1 else redirect

@login_required(login_url='/login/')
def create(request):
    try:
        user = User.objects.get(username=request.session['email'])
        userdata = Data.objects.get(user=user)
        if userdata.contingent:
          return redirect('home')
        form = CreateContingentForm(initial={'gesid1': user.id})

        context = {
            'user': user,
            'userdata': userdata,
            'form': form
        }
        return render(request, 'login/create.html', context)
    except KeyError:
        raise KeyError

        
@login_required(login_url='/login/')
def view(request):
    try:              # Minimum contingent size should be 5 and can only join/create a contingent if they are on stage 1
        user = User.objects.get(username=request.session['email'])
        userdata = Data.objects.get(user=user)
        if not userdata.admin:
          redirect('home')

        contingent_id = userdata.admin
        qs = Data.objects.filter(contingent=contingent_id)
        members = []
        for data in qs:
          user_info = []
          user_info.append(data.user)
          user_info.append(data)
          members.append(user_info)
        size = qs.count()
        contingent = Contingent.objects.get(id=contingent_id)
        context = {
            'members': members,
            'contingent': contingent,
            'size': size,
            'user': user,
            'userdata': userdata,
        }
        return render(request, 'login/contingent.html', context)
    except KeyError:
        raise KeyError

        
def join(request, contingent_id='', contingent_captcha=''):
  if request.method == 'POST':
    contingent_id = request.POST['uid']
    contingent_captcha = request.POST['captcha']
    post = True
    contForm = JoinContingentForm(request.POST)
  
  else:
    post = False
  
  try:
    user = User.objects.get(username=request.session['email'])
    userLoggedIn = True
    userdata = Data.objects.get(user=user)
  except KeyError:
    userLoggedIn = False   
    
  if userLoggedIn and userdata.session_type:
    return redirect('home')
  
  if userLoggedIn and userdata.contingent:
    context = {
      'success': 'Already added to a contingent',
      'successMessage': 'You are already a part of the contingent.'
      }
    return render(request, 'login/join.html', context)

  if contingent_id and contingent_captcha:
    inviteLink = 'http://reg-ges.ecell-iitkgp.org/join-contingent/'+str(contingent_id)+'/'+str(contingent_captcha)
   
    try:
      contingent = Contingent.objects.get(link=inviteLink)
      contingentExists = True
    except Contingent.DoesNotExist:
      contingentExists = False
  
    if contingentExists:
      if contingent.stage > 1:
        context = {
          'error': 'Unable to join',
          'errorMessage': 'This contingent cannot accept any more members.'
          }
        return render(request, 'login/join.html', context)
  
    if userLoggedIn and contingentExists:
      if userdata.college == contingent.college.college:
        userdata.contingent = contingent.id
        userdata.save()
        contingent.size = contingent.size + 1
        contingent.save()
        context = {
          'success': 'Added to the Contingent',
          'successMessage': 'You have been successfully added to the contingent.'
          }
        return render(request, 'login/join.html', context)
      
      else:
        context = {
          'error': 'Unable to join',
          'errorMessage': 'You and this contingent are registered on a different college. Thus, you cannot join this contingent.'
          }
        return render(request, 'login/join.html', context)
        
    
    elif userLoggedIn and not contingentExists:
      if post:
        context = {
          'error': 'Invalid Credentials',
          'errorMessage': 'You have entered invalid ID & Password.',
          'form': contForm
        }
      else:
        context = {
          'error': 'Broken Invite Link',
          'errorMessage': 'This invitation link is broken. Please check the link.'
          }
      return render(request, 'login/join.html', context)
    
    elif contingentExists and not userLoggedIn:
      return HttpResponseRedirect('/login/?next=/join-contingent/'+str(contingent_id)+'/'+str(contingent_captcha))
    
    else:
      redirect('home')
    
  else:
    if userLoggedIn:
      contForm = JoinContingentForm()
      context = {
        'form': contForm,
        'user': user,
        'data': userdata
      }
      return render(request, 'login/join.html', context)
    else:
      return redirect('home')


@login_required(login_url='/login/')
@require_GET
def addMembers(request):
    try:
        user = User.objects.get(username=request.session['email'])
        userdata = Data.objects.get(user=user)
        if not userdata.admin:
          redirect('home')
        context = {}
        return render(request, 'login/add.html', context)
    except KeyError:
        raise KeyError


# Home view will be redirect to corresponding view depending on stage, as we dont want url to change
@login_required(login_url='/login/')
def home(request):
    user = User.objects.get(username=request.session['email'])
    userdata = Data.objects.get(user=user)

    if userdata.stage == 0:
        return post_reg(request, user, userdata)

    elif userdata.stage == 1:
        return redirect('payment_checkout')

    elif userdata.stage == 2:
        return travel(request, user, userdata)

    else:
        return redirect('dashboard')


@login_required(login_url='/login/')
def dashboard(request):
    user = User.objects.get(username=request.session['email'])
    userdata = Data.objects.get(user=user)
    context = {
        'user': user,
        'userdata': userdata
    }

    if userdata.contingent != 0:
        size = Data.objects.filter(contingent=userdata.contingent).count()
        context['teamsize'] = size
        return render(request, 'login/dashboard.html', context)

    elif userdata.category == 'Startup':
        size = PostRegStartup.objects.get(user=user).size
        context['teamsize'] = size
        return render(request, 'login/dashboard.html', context)

    elif userdata.category == 'Empresario Semi-Finalists':
        size = PostRegEmpresario.objects.get(user=user).size
        context['teamsize'] = size
        return render(request, 'login/dashboard.html', context)

    context = {
        'user': user,
        'userdata': userdata
    }
    return render(request, 'login/dashboard.html', context)


@login_required(login_url='/login/')
def post_reg(request, user, userdata):
    context = {
        'user': user,
        'userdata': userdata,
    }

    if userdata.category == 'Startup':
        form = PostRegStartupForm()
        context['form'] = form

        PostRegData = PostRegStartup.objects.get(user=user)
        eventType = PostRegData.events.split('-')
        for event in eventType:
            if event == 'pexpo':
                pexpo = PExpoForm()
                context['pexpo'] = pexpo
            elif event == 'comeet':
                comeet = CoMeetForm()
                context['comeet'] = comeet
            elif event == 'epitch':
                epitch = EPitchForm()
                context['epitch'] = epitch
            else:
                scamp = SCampForm()
                context['scamp'] = scamp

        return render(request, 'login/post_reg_startup.html', context)

    elif userdata.category == 'Empresario Semi-Finalists':
        form = PostRegEmpresarioForm()
        context['form'] = form

        return render(request, 'login/post_reg_empresario.html', context)

    form = PostRegForm()
    context['form'] = form
    return render(request, 'login/post_reg.html', context)


def payment(request, user, userdata):
    context = {
        'user': user,
        'userdata': userdata
    }
    return render(request, 'login/payment.html', context)


def travel(request, user, userdata):
    form = TravelForm()
    context = {
        'user': user,
        'userdata': userdata,
        'form': form 
      }
    return render(request, 'login/travel.html', context)
  
  
def faq(request):
    try:
      email = request.session.get('email')
      user = User.objects.get(username=request.session['email'])
      userdata = Data.objects.get(user=user)
      context = {
          'base_path': 'login/base.html',
          'user': user,
          'userdata': userdata
      }
      return render(request, 'login/faq.html', context)
    except KeyError:
      return render(request, 'login/faq.html', {'base_path': 'registration/base.html'})
    
def contact(request):
    try:
      email = request.session.get('email')
      user = User.objects.get(username=request.session['email'])
      userdata = Data.objects.get(user=user)
      context = {
          'base_path': 'login/base.html',
          'user': user,
          'userdata': userdata
      }
      return render(request, 'login/contact.html', context)
    except KeyError:
      return render(request, 'login/contact.html', {'base_path': 'registration/base.html'})
     
  
@require_POST
@login_required(login_url='/login/')
def validatestartup(request):
    if request.method == 'GET':
        return redirect('home')

    user = User.objects.get(username = request.session['email'])
    AddData = PostRegStartup.objects.get(user=user)

    AddData.size = request.POST['size']
    AddData.details = request.POST['details']
    AddData.website = request.POST['website']

    eventType = AddData.events.split('-')

    for event in eventType:
        if event == 'scamp':
            AddData.startup_seedfund = request.POST['startup_seedfund']
            AddData.startup_stage = request.POST['startup_stage']
            AddData.intern_number = request.POST['intern_number']
            AddData.intern_description = request.POST['intern_description']
            AddData.intern_profile = request.POST['intern_profile']
            AddData.intern_location = request.POST['intern_location']
            AddData.intern_duration = request.POST['intern_duration']
            AddData.intern_stipend = request.POST['intern_stipend']

        elif event == 'epitch':
            AddData.epitch_compete = request.POST['epitch_compete']
            AddData.epitch_sector = request.POST['epitch_sector']
            AddData.epitch_problem = request.POST['epitch_problem']
            AddData.epitch_market = request.POST['epitch_market']
            AddData.epitch_funds = request.POST['epitch_funds']
            AddData.epitch_deck = request.POST['epitch_deck']
            AddData.epitch_revenue = request.POST['epitch_revenue']

        elif event == 'comeet':
            AddData.comeet_idea = request.POST['comeet_idea']
            AddData.comeet_skill_set = request.POST['skill_set']

        else:
            AddData.pexpo_demo = request.POST['pexpo_demo']
            AddData.pexpo_details = request.POST['pexpo_details']
            AddData.pexpo_type = request.POST['pexpo_type']

    AddData.save()
    data = Data.objects.get(user=user)
    data.stage = 1
    data.save()
    return HttpResponse('saved')


@require_POST
@login_required(login_url='/login/')
def validateempresario(request):
    if request.method == 'GET':
        return redirect('home')

    user = User.objects.get(username=request.session['email'])
    userdata = Data.objects.get(user=user)

    post_reg_data = PostRegEmpresario()
    post_reg_data.acco = request.POST['acco']
    post_reg_data.size = request.POST['size']
    post_reg_data.user = user

    post_reg_data.save()
    userdata.stage = 1
    userdata.save()

    return HttpResponse('saved')


@require_POST
@login_required(login_url='/login/')
def validateregular(request):
    if request.method == 'GET':
        return redirect('home')

    user = User.objects.get(username=request.session['email'])
    userdata = Data.objects.get(user=user)

    post_reg_data = PostReg()
    post_reg_data.startup = request.POST['startup']
    post_reg_data.fav_startup = request.POST['fav_startup']
    post_reg_data.inspiration = request.POST['inspiration']
    if post_reg_data.startup == 'True':
        post_reg_data.stage = request.POST['stage']
    else:
        post_reg_data.profile = request.POST['profile_set']
    post_reg_data.user = user

    post_reg_data.save()
    userdata.stage = 1
    userdata.save()

    return HttpResponse('saved')


@require_POST
@login_required(login_url='/login/')
def validatetravel(request):
    if request.method == 'GET':
        return redirect('home')

    user = User.objects.get(username=request.session['email'])
    userdata = Data.objects.get(user=user)

    if userdata.admin:
      qs = Data.objects.filter(contingent=userdata.admin)
      for member in qs:
        travel_data = Travel()
        travel_data.arrival = request.POST['arrival']
        travel_data.departure = request.POST['departure']
        travel_data.pnr = request.POST['pnr']
        travel_data.user = member.user        
        travel_data.save()
        member.stage = 3
        member.save()
      contingent = Contingent.objects.get(id=userdata.admin)
      contingent.stage = 3
      contingent.save()
    
    else:
      travel_data = Travel()
      travel_data.arrival = request.POST['arrival']
      travel_data.departure = request.POST['departure']
      travel_data.pnr = request.POST['pnr']
      travel_data.user = user

      travel_data.save()
      userdata.stage = 3
      userdata.save()

    return HttpResponse('saved')

def validate_contingent_eligibility(adminId, userList):
  error = []
  admin = User.objects.get(id=adminId)
  adminData = Data.objects.get(user=admin)
  userCheckedList = []
  userCheckedList.append(adminId)
  
  for user in userList:
    if user in userCheckedList:
      error.append(str(user)+'-2')
    else:
      try:
        data = Data.objects.get(user=user)
        if adminData.college != data.college or data.session_type != 0:
          error.append(str(user)+'-0')
        elif data.contingent != 0:
          error.append(str(user)+'-3')
      except Data.DoesNotExist:
        error.append(str(user)+'-1')
    userCheckedList.append(user)
  return error
  
@require_POST
@login_required(login_url='/login/')
def validate_create_contingent(request):
  if request.method == 'GET':
    return redirect('home')

  userList = [request.POST['gesid2'],request.POST['gesid3'],request.POST['gesid4'],request.POST['gesid5']];
  result = validate_contingent_eligibility(request.POST['gesid1'], userList)
  if not result:
    admin = User.objects.get(id=request.POST['gesid1'])
    adminData = Data.objects.get(user=admin)

    contingent = Contingent()
    contingent.admin = admin
    contingent.college = College.objects.get(college=adminData.college)
    contingent.captcha = get_random_string(length=6)
    contingent.size = 5
    contingent.stage = 1
    contingent.link = 'http://reg-ges.ecell-iitkgp.org/join-contingent/';
    contingent.save()
    contingent.link = 'http://reg-ges.ecell-iitkgp.org/join-contingent/'+str(contingent.id)+'/'+str(contingent.captcha)
    contingent.save()
    
    adminData.contingent = contingent.id
    adminData.admin = contingent.id
    adminData.save()
    
    contingentDetails = {}
    contingentDetails['id'] = contingent.id
    contingentDetails['captcha'] = contingent.captcha
    contingentDetails['status'] = True
    for user in userList:
      data = Data.objects.get(user=user)
      data.contingent = contingent.id
      data.save()
    return JsonResponse(contingentDetails, safe=False)
  else:
    errorMessage = []
    for error in result:
      errorDetails = error.split('-')
      if errorDetails[1] == '2':
        errorMessage.append('GES ID '+errorDetails[0]+' is entered multiple times in the form.\n')
      elif errorDetails[1] == '1':
        errorMessage.append('GES ID '+errorDetails[0]+' does not exist.\n')
      elif errorDetails[1] == '3':
        errorMessage.append('GES ID '+errorDetails[0]+' is already part of a contingent.\n')
      else:
        errorMessage.append('GES ID '+errorDetails[0]+' is not eligible to join this contingent.\n')
    error = {'status': False, 'errorMessage': errorMessage}
    return JsonResponse(error, safe=False)
        

@require_POST
@login_required(login_url='/login/')
def validate_add_members(request):
  size = request.POST['size']
  size = int(size) + 1
  userList = []
  for i in range(1, size):
    userList.append(request.POST['gesid_'+str(i)])

  admin = User.objects.get(username=request.session['email'])
  adminData = Data.objects.get(user=admin)
  contingent = Contingent.objects.get(id=adminData.admin)
  result = validate_contingent_eligibility(admin.id, userList)
  
  if not result:
    for user in userList:
      data = Data.objects.get(user=user)
      data.contingent = contingent.id
      data.save()
    contingent.size = contingent.size + len(userList)
    contingent.save()
    context = {
      'status': True
    }
    return JsonResponse(context, safe=False)
  
  else:
    errorMessage = []
    for error in result:
      errorDetails = error.split('-')
      if errorDetails[1] == '2':
        errorMessage.append('GES ID '+errorDetails[0]+' is entered multiple times in the form.\n')
      elif errorDetails[1] == '1':
        errorMessage.append('GES ID '+errorDetails[0]+' does not exist.\n')
      elif errorDetails[1] == '3':
        errorMessage.append('GES ID '+errorDetails[0]+' is already part of a contingent.\n')
      else:
        errorMessage.append('GES ID '+errorDetails[0]+' is not eligible to join this contingent.\n')
    error = {'status': False, 'errorMessage': errorMessage}
    return JsonResponse(error, safe=False)
    
#   return HttpResponse(result)
