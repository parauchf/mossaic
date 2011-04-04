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
from communities.models import Community, Observation
from users.models import MossaicUser
from risk_models.models import RiskModel, Metric, MCOption


from django import forms
from django.forms.widgets import RadioSelect

@csrf_protect

class NewMetricForm(forms.Form):
	pass

def metric(request,metric_id):
	if request.method=="GET":
		try:
			options=MetricMultipleChoiceOption.objects.filter(metric__id__exact=metric_id)
			metric=Metric.objects.get(id__exact=metric_id)
			form = NewMetricForm()
			context = RequestContext(request,{
				'form': form,
				'options': options,
				'metric': metric
			})	
		except:
			raise Http404
		
		return render_to_response('modelMetric.html',context,context_instance=RequestContext(request))
	
	if request.method=="POST":
		form = NewMetricForm(request.POST)
		
		if form.data['type'] == 'MC':
			try:
				mmc=MetricMultipleChoice.objects.get(id__exact=metric_id)
			except:
				mmc=MetricMultipleChoice(
					name=form.data['name']
				)
			mmc.save()
			
			index=1
			for option in form.data.getlist('option'):
				if option == "":
					continue
				opt = MetricMultipleChoiceOption(
					name=option,
					ordinal=index,
					metric=mmc
				)
				index+=1
				opt.save()
		
		if form.data['type'] == 'DC':
			mdc=MetricDecimal(
				name=form.data['name'],
				precision=form.data['precision'],
				unitOfMeasure=form.data['unitofmeasure'],
				minimumValue=forms.data['minimum'],
				maximumValue=forms.data['maximum']
			)
			mdc.save()
	
		return HttpResponseRedirect("/metrics")

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
