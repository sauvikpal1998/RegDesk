from registration.models import User, Data


def logged_in_user(request):
  try:
    username = request.session['email']
    user = User.objects.get(username=username)
    data = Data.objects.get(user=user)
    return {
      'user': user,
      'userdata': data
    }
  except:
#   except KeyError, User.DoesNotExist, Data.DoesNotExist:
    return {}
  