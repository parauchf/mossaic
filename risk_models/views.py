
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

from projects.models import *
from communities.models import *
from users.models import *

from risk_models.models import *
from risk_models.forms import *

import re



@csrf_protect
def metric(request,metric_id=0,project_id=0,is_new=False, *args, **kwargs):
	if is_new:
		metric = Metric()
		metric.project_id = project_id
		project = Project.objects.get(pk=project_id)
	else:
		try:
			project = Project.objects.get(pk=project_id)
			metric = Metric.objects.get(pk=metric_id)
			# if metric.project_id != project_id:
			# 				raise Http404
		except:
			raise Http404
	
	if 'model' in request.GET:
		model_id=request.GET['model']
		model=RiskModel.objects.get(pk=model_id)
	else:
		model = None
	if request.method == "POST":
		form = MetricForm(request.POST,instance=metric,prefix='metric')
		formset = ChoiceFormSet(request.POST, request.FILES, instance=metric,prefix='choices')
		
		if form.is_valid() and formset.is_valid():
			form.save()
			formset.save()
			
			if model is not None:
				mml = ModelMetricLink(riskModel=model,metric=metric)
				mml.save()
				return HttpResponseRedirect("/projects/%s/models/%s" % (project_id,model_id) )
			else:
				return HttpResponseRedirect("/projects/%s/metrics/" % project_id)
				
	else:
		form = MetricForm(instance=metric,prefix='metric')
		formset = ChoiceFormSet(instance=metric,prefix='choices')
	
	context = RequestContext(request,{
		'form': form,
		'options': formset,
		'project': project,
		'model': model,
		'is_new': is_new,
		'request': request
	})
	return render_to_response('modelMetric.html',context,context_instance=RequestContext(request))

def riskModelNew(request,project_id=0):
	project = Project.objects.get(pk=project_id)
	if request.method=="POST":
		form = NewModelForm(request.POST)
		
		if form.is_valid():
			model = RiskModel(name=form.data['project_name'],project=project)
			model.save()
			return HttpResponseRedirect("/projects/%s/models/%s/" % (project.id,model.id))
	else:
		form = NewModelForm()
		form.project_id=project.id
		
	context = RequestContext(request,{
		'form': form,
		'project': project,
		'request': request
	})
	return render_to_response('modelRiskModelNew.html',context,context_instance=RequestContext(request))

def riskModel(request,riskModel_id=0,project_id=0,is_new=False, *args, **kwargs):
	try:
		riskModel = RiskModel.objects.get(pk=riskModel_id)
	except:
		riskModel = RiskModel()
	
	project = Project.objects.get(pk=project_id)
	
	if request.method=="POST":
		form = RiskModelFormset(request.POST, instance = riskModel, prefix='riskform')
		if form.is_valid():
			form.save()
			return HttpResponseRedirect("/projects/%s/models/" % project.id)
	else:
		form = RiskModelFormset(instance = riskModel,prefix='riskform')
	
	context = RequestContext(request,{
		'model': riskModel,
		'link_forms': form,
		'project': project,
		'request': request,
		'active_tab': 'risk_model'
	})
	return render_to_response('modelRiskModel.html',context,context_instance=RequestContext(request))

def metricLinkNew(request,riskModel_id=0,project_id=0,*args, **kwargs):
	mml = ModelMetricLink()
	riskModel = RiskModel.objects.get(pk=riskModel_id)
	project = Project.objects.get(pk=project_id)
	
	if request.method=="POST":
		form = NewMMLForm(request.POST)
		if form.data['new_links'] != '':
			for metric_name in re.split('[;,]+',form.data['new_links']):
				# try:
				metric=Metric.objects.filter(name__iexact=metric_name.strip())[0]
				mml = ModelMetricLink(
					riskModel=riskModel,
					metric=metric
				)
				mml.save()
				# except:
					# pass

		return HttpResponseRedirect("/projects/%s/models/%s/" % (project.id,riskModel.id))
	else:
		form = NewMMLForm()
		
	context = RequestContext(request,{
		'model': riskModel,
		'form': form,
		'project': project,
		'request': request
	})	
	return render_to_response('projectMetricLink.html',context,context_instance=RequestContext(request))
	

def ajaxMetrics(request):
	if request.method=="GET" and request.GET.has_key(u'q'):
		q=request.GET[u'q']
		metrics = Metric.objects.filter(name__istartswith=q)[0:9]
		return render_to_response('ajaxMetrics.json',{'metrics':metrics})
	return HttpResponse("")

def metricList(request):
	try:
		metrics=Metric.objects.all()
	except:
		raise Http404
	
	context = RequestContext(request,{
		'metrics': metrics
	})
	
	return render_to_response('modelMetricList.html',context,context_instance=RequestContext(request))

def riskModelList(request):
	try:
		riskModels=RiskModel.objects.all()
	except:
		raise Http404
	
	context = RequestContext(request,{
		'riskModels': riskModels
	})
	
	return render_to_response('modelRiskModelList.html',context,context_instance=RequestContext(request))

def observation(request,observation_id):
	raise Http404
	
	if request.method=="POST":
		if form.is_valid():
			form.save()
			obs.user = request.user

def newObservation(request):
	raise Http404


