from django import forms

from django.forms.models import inlineformset_factory
from django.forms.models import modelformset_factory
from django.forms.models import BaseInlineFormSet
from django.forms import ModelForm, Textarea
from django.forms.widgets import HiddenInput

from projects.models import *
from communities.models import *

class NewCommunityForm(forms.Form):
	new_community = forms.CharField()

class CommunityForm(ModelForm):
	class Meta:
		model = Community
		widgets = {
			'project': HiddenInput,
			'location': HiddenInput,
		}

class NewUserForm(forms.Form):
	new_users = forms.CharField(widget=
		forms.TextInput(attrs={'class':'tokenized ajaxurl-ajax-users'}))
	

class ProjectForm(ModelForm):
	class Meta:
		model = Project
		widgets = {
		}