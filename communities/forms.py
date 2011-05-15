from users.models import MossaicUser

from risk_models.models import *
from projects.models import *
from communities.models import *

from django import forms
from django.forms.models import *
from django.forms import ModelForm, Textarea
from django.forms.widgets import HiddenInput
from django.forms.models import inlineformset_factory
from django.forms.models import modelformset_factory
from django.forms.models import BaseInlineFormSet
from django.forms import ModelForm, Textarea
from django.forms.widgets import HiddenInput


# this code is terrible....  will fix someday

class SurveyItem(ModelForm):
	class Meta:
		model = Observation
		widgets = {
			'community': HiddenInput,
			'user': HiddenInput,
			'timestamp': HiddenInput,
			'metric': HiddenInput
		}
	
	def __init__(self, *args, **kwargs):
		self.request = kwargs.pop('request', None)
		return super(SurveyItem, self).__init__(*args, **kwargs)
	
	def is_filled(self):
		cleaned_data = self.cleaned_data
		metric = cleaned_data.get("metric")
		
		if metric.metricType == 'M':
			mcValue = cleaned_data.get("mcValue")
			if mcValue == None:
				return False
			return True
		
		if metric.metricType == 'D':
			value = cleaned_data.get("value")
			if value == None:
				return False
			return True
		
		return False
		
	def clean(self):
		cleaned_data = self.cleaned_data
		metric = cleaned_data.get("metric")
		
		if metric.metricType == 'M':
			mcValue = cleaned_data.get("mcValue")
			if mcValue == None:
				raise forms.ValidationError('No choice made')
			return cleaned_data
		
		if metric.metricType == 'D':
			value = cleaned_data.get("value")
			if value == None:
				raise forms.ValidationError('No choice made')
			return cleaned_data
	
	def save(self, *args, **kwargs):
		kwargs['commit'] = False
		
		obs = super(SurveyItem, self).save(*args, **kwargs)
		if self.request:
			obs.user = MossaicUser.objects.get(pk=self.request.user.id)  #there must be a better way...
		
		obs.save()