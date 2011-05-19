# Create your views here.
from django.template import Context, loader
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext

from django.http import Http404

from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from django.core import serializers

from projects.models import Project, Membership
from communities.models import Community
from users.models import MossaicUser
from risk_models.models import *
from projects.forms import *

import re


@csrf_protect
@login_required
def projectIndex(request,project_id=0):
	if request.method == "GET":
		try:
			projects=Project.objects.all()
		except:
			raise Http404
	
	context = RequestContext(request,{
		'projects': projects,
		'request': request,
	})

	return render_to_response('projectIndex.html',context,context_instance=RequestContext(request))

@csrf_protect
@login_required
def projectAdd(request,project_id=0):
	if request.method == "POST":
		form = ProjectForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect("/projects/")
	else:
		form = ProjectForm()
	
	context = RequestContext(request,{
		'form': form,
		'request': request,
	})

	return render_to_response('projectAdd.html',context,context_instance=RequestContext(request))


@csrf_protect
@login_required
def projectSettings(request,project_id):
	if request.method == "GET":
		try:
			project=Project.objects.get(id__exact=project_id)
		except:
			raise Http404
		
		form = ProjectForm(instance=project)
		
		context = RequestContext(request,{
			'project': project,
			'form': form,
			'request': request,
			'active_tab': 'administration'
		})
		
		return render_to_response('projectAdministration.html',context,context_instance=RequestContext(request))

@csrf_protect
@login_required
def userList(request,project_id):
	# if request.method=="POST":
	# 	request.POST[u'username']
	
	if request.method=="GET":
		try:
			users=MossaicUser.objects.filter(membership__project__id__exact=project_id)
			project=Project.objects.get(id__exact=project_id)
		except:
			raise Http404
		
		form = NewUserForm()
		
		context = RequestContext(request,{
			'project': project,
			'users': users,
			'form': form,
			'request': request,
			'active_tab': 'users'
		})
		
		return render_to_response('projectUsers.html',context,context_instance=RequestContext(request))

@csrf_protect
@login_required
def userAdd(request,project_id):
	try:
		project=Project.objects.get(id__exact=project_id)
	except:
		raise Http404
	
	if request.method=="POST":
		form = NewUserForm(request.POST)
		if form.data['new_users'] != '':
			for username in re.split('[;,]+',form.data['new_users']):
			
				if (Membership.objects.filter(user__username__exact=username).
				filter(project__exact=project_id).count() == 0):
				
					m=Membership(
						user=MossaicUser.objects.get(username__exact=username),
						project=Project.objects.get(id__exact=project_id)
					)
					m.save()
		
		return HttpResponseRedirect("/projects/%s/users" % project_id )
	else:
		form = NewUserForm()
		context = RequestContext(request,{
			'project': project,
			'form': form,
			'request': request,
		})
		return render_to_response('projectUserAdd.html',context,context_instance=RequestContext(request))

@csrf_protect
@login_required
def communityList(request,project_id):
	if request.method=="GET":
		try:
			communities=Community.objects.filter(project__id__exact=project_id)
			project=Project.objects.get(id__exact=project_id)
		except:
			raise Http404
		
		form = NewCommunityForm()
		
		context = RequestContext(request,{
			'project': project,
			'communities': communities,
			'form': form,
			'request': request,
			'active_tab': 'communities'
		})
		
		return render_to_response('projectCommunityList.html',context,context_instance=RequestContext(request))

@csrf_protect
@login_required
def communityAdd(request,project_id=0):
	try:
		project=Project.objects.get(id__exact=project_id)
	except:
		raise Http404
		
	if request.method=="POST":
		form = CommunityForm(request.POST)
		if form.is_valid():
			form.save()

		return HttpResponseRedirect("/projects/{0}/communities".format(project_id))
	
	else:
		form = CommunityForm({'project':project_id})
		context = RequestContext(request,{
			'project': project,
			'form': form,
			'request': request,
		})
		return render_to_response('projectCommunityAdd.html',context,context_instance=RequestContext(request))

@csrf_protect
@login_required
def riskMatrix(request,project_id):
	if request.method == "GET":
		project = Project.objects.get(pk=project_id)
		communities = Community.objects.filter(project__id__exact=project.id)
		riskModels = RiskModel.objects.filter(project__id__exact=project.id)
		
		
		score = {}
		maxValue = {}
		for riskModel in riskModels:
			score[riskModel.id] = {}
			for community in communities:
				score[riskModel.id][community.id] = riskModel.eval(community)
		
		
		for riskModel in riskModels:
			if riskModel.id in score:
				maxValue[riskModel.id] = max(score[riskModel.id].values())
			else:
				maxValue[riskModel.id] = 0
		
		
		scores = [ {'community': community, 'model': riskModel, 'score': score[riskModel.id][community.id], 'max': maxValue[riskModel.id] } 
					for community in communities for riskModel in riskModels ]
		
		
		context = RequestContext(request,{
			'scores': scores,
			'models': riskModels,
			'project': project,
			'active_tab': 'risk_matrix'
		})
	
	return render_to_response('projectRiskMatrix.html',context,context_instance=RequestContext(request))

@csrf_protect
@login_required
def administration(request,project_id):
	return render_to_response('projectAdministration.html',{'project_id':project_id})

@csrf_protect
@login_required
#TODO this is a security hole... needs to get plugged at some point
def ajaxUsers(request):
	if request.method=="GET" and request.GET.has_key(u'q'):
		q=request.GET[u'q']
		users = User.objects.filter(username__istartswith=q).all()[0:9]
		return render_to_response('ajaxUsers.json',{'users':users})
	return HttpResponse("")

@csrf_protect
@login_required
def observationList(request,project_id):
	try:
		observations=Observation.objects.filter(community__project__id__exact=project_id).all()
		project=Project.objects.get(id__exact=project_id)
	except:
		raise Http404
	
	context = RequestContext(request,{
		'project': project,
		'observations': observations,
		'request': request,
		'active_tab': 'observations'
	})

	return render_to_response('projectObservationList.html',context,context_instance=RequestContext(request))

@csrf_protect
@login_required
def metricList(request,project_id=0):
	try:
		metrics=Metric.objects.filter(project__id__exact=project_id).all()
		project=Project.objects.get(pk=project_id)
	except:
		raise Http404
	
	context = RequestContext(request,{
		'metrics': metrics,
		'project': project,
		'request': request,
		'active_tab': 'metrics'
	})

	return render_to_response('projectMetricList.html',context,context_instance=RequestContext(request))

@csrf_protect
@login_required
def riskModelList(request,project_id):
	try:
		models=RiskModel.objects.filter(project__id__exact=project_id).all()
		project=Project.objects.get(id__exact=project_id)
	except:
		raise Http404
	
	context = RequestContext(request,{
		'riskModels': models,
		'project': project,
		'request': request,
		'active_tab': 'risk_models'
	})

	return render_to_response('projectRiskModelList.html',context,context_instance=RequestContext(request))



@csrf_protect
@login_required
def base(request):
	t = loader.get_template('base.html')
	c = Context({
		'user': request.user
	})
	return HttpResponse(t.render(c))