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
from risk_models.models import RiskModel, Metric, MCOption, Observation, Metric, MetricForm, ChoiceFormSet, MetricFormSet

from django import forms
from django.forms.widgets import RadioSelect

from django.forms.models import inlineformset_factory
from django.forms.models import modelformset_factory
from django.forms import ModelForm, Textarea

@csrf_protect

def metric(request,metric_id):
	try:
		metric = Metric.objects.get(pk=metric_id)
	except:
		metric = Metric()
	
	if request.method=="POST":
		form = MetricForm(request.POST,instance=metric)
		formset = ChoiceFormSet(request.POST, request.FILES, instance=metric)
		
		if form.is_valid() and formset.is_valid():
			form.save()
			formset.save()
			return HttpResponseRedirect("/metrics")
		
	else:
		form = MetricForm(instance=metric)
		formset = ChoiceFormSet(instance=metric)
		context = RequestContext(request,{
			'form': form,
			'options': formset,
		})
	return render_to_response('modelMetric.html',context,context_instance=RequestContext(request))

def newMetric(request):
	metric = Metric()
	metric.save()
	return HttpResponseRedirect("/metrics/%d"%(metric.id))

def metricList(request):
	try:
		metrics=Metric.objects.all()
	except:
		raise Http404
	
	context = RequestContext(request,{
		'metrics': metrics
	})
	
	return render_to_response('modelMetricList.html',context,context_instance=RequestContext(request))

def riskModel(request,model_id):
	try:
		riskModel = RiskModel.objects.get(pk=model_id)
	except:
		riskModel = RiskModel()
	
	if request.method=="POST":
		formset = MetricFormSet(request.POST, request.FILES, instance=riskModel)
		
		if formset.is_valid():
			formset.save()
			return HttpResponseRedirect("/models/")
			
	else:
		#TODO filter by project
		metrics = Metric.objects.all()
		formset = MetricFormSet(instance=riskModel)
		context = RequestContext(request,{
			'metrics': metrics,
		})
	return render_to_response('modelRiskModel.html',context,context_instance=RequestContext(request))
	
def newRiskModel(request):
	riskModel = RiskModel()
	riskModel.save()
	return HttpResponseRedirect("/models/%d"%(riskModel.id))

