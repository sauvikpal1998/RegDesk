from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from registration.models import Data, Contingent
# Create your views here.


@login_required(login_url='/login/')
def paymentCheckout(request):
  try:
    user = User.objects.get(username=request.session['email'])
    userdata = Data.objects.get(user=user)
    response = eligible_to_pay(user)
    return HttpResponse(response)
  except KeyError:
    return redirect('login')

  
def eligible_to_pay(user):
  response = {}
  data = Data.objects.get(user=user)
  if data.stage == 1:
    if data.contingent and not data.admin:
      response['status'] = False
      response['message'] = 'Your Payment will be done by your contingent admin.'
    else:
      response['status'] = True
      response['message'] = 'Eligible to pay.'

  elif data.stage == 0:
    response['status'] = False
    response['message'] = 'Complete Post Registration Process to proceed for payment.'
  
  else:
    response['status'] = False
    response['message'] = 'Already Paid'
  return JsonResponse(response, safe=False)
