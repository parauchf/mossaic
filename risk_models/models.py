#from django.db import models
from django.contrib.gis.db import models
from django.contrib.auth.models import User

from django.forms.models import inlineformset_factory
from django.forms.models import modelformset_factory
from django.forms import ModelForm, Textarea

class Metric(models.Model):
	name = models.CharField(max_length=200)
	
	minimumValue = models.DecimalField(max_digits=19,decimal_places=10,blank=True,null=True)
	maximumValue = models.DecimalField(max_digits=19,decimal_places=10,blank=True,null=True)
	precision = models.IntegerField(blank=True,null=True)
	
	unitOfMeasure = models.CharField(max_length=100,blank=True,null=True)
	
	TYPE_CHOICES = (
		('M', 'Multiple choice'),
		('D', 'Numeric'),
	)
	
	metricType = models.CharField(max_length=1,choices=TYPE_CHOICES,blank=False,null=False)
	
	def type(self):
		return metricType
		
	def __unicode__(self):
		return self.name

class MetricForm(ModelForm):
	class Meta:
		model = Metric

class MCOption(models.Model):
	name = models.CharField(max_length=200)
	metric = models.ForeignKey('Metric')

ChoiceFormSet = inlineformset_factory(Metric,MCOption,can_order=True,can_delete=True)

class MCScore(models.Model):
	option = models.ForeignKey('MCOption')
	riskModel = models.ForeignKey('RiskModel')
	score = models.DecimalField(max_digits=19,decimal_places=10)

class Observation(models.Model):
	community = models.ForeignKey('communities.Community')
	metric = models.ForeignKey('risk_models.Metric')
	user = models.ForeignKey('users.MossaicUser')
	timestamp = models.DateTimeField(auto_now=True)
	
	value = models.DecimalField(max_digits=19,decimal_places=10)
	mcValue = models.ForeignKey('risk_models.MCOption')
	
	def __unicode__(self):
		return (self.community.name + ": " + self.metric.name)

class ModelMetricLink(models.Model):
	riskModel = models.ForeignKey('RiskModel')
	metric = models.ForeignKey('Metric')
	
	weight = models.DecimalField(max_digits=19,decimal_places=10)
	
	defaultDecimalValue = models.DecimalField(max_digits=19,decimal_places=10)
	defaultMCValue = models.IntegerField(blank=True,null=True)
	
	MISSING_POLICIES = (
		('D', 'Default Value'),
		('A', 'Average/Mode Value'),
		('I', 'Invalidate'),
	)
	missingValuePolicy = models.CharField(max_length=1,choices=MISSING_POLICIES)
	
	DUPLICATE_POLICIES = (
		('R', 'Use Most Recent'),
		('A', 'Use the average value'),
		('I', 'Invalidate'),
	)
	duplicateValuePolicy = models.CharField(max_length=1,choices=MISSING_POLICIES)

class RiskModel(models.Model):
	name = models.CharField(max_length=200)
	formula = models.CharField(max_length=200)
	metrics = models.ManyToManyField('Metric',through=ModelMetricLink)
	
	# def getMaxPossibleValue(self,):
	
	def getMaxValue(self):
		observations = Observation.objects.filter(community__id__equals=community_id)
	
	# def evaluate(self, community_id):
	# 	for metric in metrics:
	# 		observations = Observation.objects.filter(community__id__equals=community_id).filter(metric_id_equals=metric.id)
	# 		if observations.count == 0:
	# 			if metric.missingValuePolicy == 'D':
					
MetricFormSet = inlineformset_factory(RiskModel,ModelMetricLink,can_delete=True)