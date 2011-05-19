# Create your views here.

from projects.models import *
from communities.models import *
from users.models import *
from risk_models.models import *

from django.http import HttpResponse
from django.http import HttpResponseRedirect

from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.models import User

def logout_view(request):
	logout(request)
	return HttpResponseRedirect("/accounts/login/")