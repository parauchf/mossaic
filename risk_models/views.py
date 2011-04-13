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
from risk_models.models import RiskModel, Metric, MCOption, Observation, Metric

from django import forms
from django.forms.widgets import RadioSelect

from django.forms.models import inlineformset_factory
from django.forms.models import modelformset_factory
from django.forms import ModelForm, Textarea

@csrf_protect

class MetricForm(ModelForm):
	class Meta:
		model = Metric

def metric(request,metric_id):
	try:
		metric = Metric.objects.get(pk=metric_id)
	except:
		metric = Metric
	
	if request.method=="POST":
		options = InlineChoiceFormSet(request.POST, request.FILES, instance=metric)
		form = MetricForm(request.POST,instance=metric)
		
		if form.is_valid() and options.is_valid():
			form.save()
			options.save()
			return HttpResponseRedirect("/metrics")
	
	else:
		form = MetricForm(instance=metric)
		options = InlineChoiceFormSet(instance=metric)
		context = RequestContext(request,{
			'form': form,
			'options': formset,
		})
	return render_to_response('modelMetric.html',context,context_instance=RequestContext(request))

def metricList(request):
	if request.method=="GET":
		try:
			metrics=Metric.objects.all()
		except:
			raise Http404
		
		context = RequestContext(request,{
			'metrics': metrics
		})
		
		return render_to_response('modelMetricList.html',context,context_instance=RequestContext(request))


