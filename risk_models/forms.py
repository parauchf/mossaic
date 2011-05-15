from projects.models import *
from communities.models import *
from users.models import MossaicUser
from risk_models.models import *

from django import forms

from django.forms.models import inlineformset_factory
from django.forms.models import modelformset_factory
from django.forms.models import BaseInlineFormSet
from django.forms import ModelForm, Textarea
from django.forms.widgets import HiddenInput



class NewModelForm(forms.Form):
	project_name = forms.CharField()

class NewMMLForm(forms.Form):
	new_links = forms.CharField(widget=forms.TextInput(attrs={'class':'tokenized ajaxurl-ajax-metrics'}))

class MetricForm(ModelForm):
	class Meta:
		model = Metric
		widgets = {
			'project': HiddenInput,
			# 'metricType': RadioSelect,
		}

class MCScoreForm(ModelForm):
	class Meta:
		model = MCScore
		widgets = {
			'option': HiddenInput,
			'modelMetricLink': HiddenInput,
		}

MCScoreFormSet = inlineformset_factory(ModelMetricLink,MCScore,form=MCScoreForm,extra=0,can_order=False,can_delete=False)

class ModelElementForm(ModelForm):
	class Meta:
		model = ModelMetricLink
		widgets = {
			'metric': HiddenInput
		}
	
	def save(self, *args, **kwargs):
		super(ModelElementForm, self).save(*args, **kwargs)
		if hasattr(self,'nested'):
			self.nested.save()
	
	def is_valid(self,*args, **kwargs):
		if hasattr(self,'nested'):
			return super(ModelElementForm, self).is_valid(*args, **kwargs) and self.nested.is_valid()
		else:
			return super(ModelElementForm, self).is_valid(*args, **kwargs)
	
	def has_changed(self, *args, **kwargs):
		has_changed = super(ModelElementForm, self).has_changed(*args, **kwargs)
		if hasattr(self,'nested'):
			for form in self.nested.forms:
				has_changed = has_changed or form.has_changed
		return has_changed
	
	def __init__(self, data=None, *args, **kwargs):
		super(ModelElementForm, self).__init__(data=data, *args, **kwargs)
		if self.instance.metric.metricType == 'M':
			self.nested = MCScoreFormSet(instance=self.instance,prefix="C%s" % self.instance.pk, data=data)


ChoiceFormSet = inlineformset_factory(Metric,MCOption,can_order=True,can_delete=True)	
				
RiskModelFormset = inlineformset_factory(RiskModel, ModelMetricLink, form=ModelElementForm,  extra=0)