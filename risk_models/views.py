
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
from risk_models.forms import *



@csrf_protect
def metric(request,metric_id, *args, **kwargs):
	try:
		metric = Metric.objects.get(pk=metric_id)
	except:
		metric = Metric()
	
	if request.method=="POST":
		form = MetricForm(request.POST,instance=metric,prefix='metric')
		formset = ChoiceFormSet(request.POST, request.FILES, instance=metric,prefix='choices')
		
		if form.is_valid() and formset.is_valid():
			form.save()
			formset.save()
			
			if 'project_id' in kwargs:
				project_id=kwargs['project_id']
				project=Project.objects.get(pk=project_id)
				project.metrics.add(self.id)
		
			return HttpResponseRedirect("/metrics/")
		
	else:
		form = MetricForm(instance=metric,prefix='metric')
		formset = ChoiceFormSet(instance=metric,prefix='choices')
		context = RequestContext(request,{
			'form': form,
			'options': formset,
		})
	return render_to_response('modelMetric.html',context,context_instance=RequestContext(request))

def riskModel(request,riskModel_id, *args, **kwargs):
	try:
		riskModel = RiskModel.objects.get(pk=riskModel_id)
	except:
		riskModel = RiskModel()
	
	if request.method=="POST":
		form = RiskModelFormset(request.POST, instance = riskModel, prefix='riskform')
		if form.is_valid():
			form.save()
			return HttpResponseRedirect("/models/")
	else:
		form = RiskModelFormset(instance = riskModel,prefix='riskform')
	
	context = RequestContext(request,{
		'link_forms': form,
	})
	return render_to_response('modelRiskModel.html',context,context_instance=RequestContext(request))

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

def observation(request,project_id):
	raise Http404

def newObservation(request,project_id):
	raise Http404


