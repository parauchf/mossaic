from django.db import models
# from django.contrib.gis.db import models
from django.contrib.auth.models import User

from django.forms.models import inlineformset_factory
from django.forms.models import modelformset_factory
from django.forms import ModelForm, Textarea, RadioSelect


TYPE_CHOICES = (
	('M', 'Multiple choice'),
	('D', 'Numeric')
)

MISSING_POLICIES = (
	('D', 'Default Value'),
	('A', 'Average/Mode Value'),
	('I', 'Invalidate'),
)

DUPLICATE_POLICIES = (
	('R', 'Use Most Recent'),
	('A', 'Use the average value'),
	('I', 'Invalidate'),
)

class MetricFamily(models.Model):
	name = models.CharField(max_length=200)
	version_max = models.IntegerField()
	
	def getNewVersion(self):
		self.version_max += 1
		return self.version_max
	
	def __init__(self, *args, **kwargs):
		super(MetricFamily, self).__init__(*args, **kwargs)
		self.version_max = 1

class Metric(models.Model):
	name = models.CharField(max_length=200)
	version = models.IntegerField(editable=False)
	family = models.ForeignKey('MetricFamily',editable=False)
	
	minimumValue = models.DecimalField(max_digits=19,decimal_places=10,blank=True,null=True)
	maximumValue = models.DecimalField(max_digits=19,decimal_places=10,blank=True,null=True)
	precision = models.IntegerField(blank=True,null=True)
	unitOfMeasure = models.CharField(max_length=100,blank=True,null=True)
	
	metricType = models.CharField(max_length=1,choices=TYPE_CHOICES,blank=False,null=False,default='D')
	
	def type(self):
		return metricType
		
	def __unicode__(self):
		return self.name
	
	
	def save(self):
		# if family_id in kwargs:
		# 			self.family = MetricFamily.get(pk=family_id)
		# 			self.version = family.getNewVersion()
		
		f = MetricFamily()
		f.save()
		self.family_id = f.id
		self.version = f.getNewVersion()
		
		super(Metric, self).save()

class MetricForm(ModelForm):
	class Meta:
		model = Metric
		widgets = {
			# 'metricType': RadioSelect,
		}

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
	transformation = models.CharField(max_length=200)
	
	weight = models.DecimalField(max_digits=19,decimal_places=10)
	
	defaultDecimalValue = models.DecimalField(max_digits=19,decimal_places=10)
	defaultMCValue = models.IntegerField(blank=True,null=True)
	
	missingValuePolicy = models.CharField(max_length=1,choices=MISSING_POLICIES)
	
	duplicateValuePolicy = models.CharField(max_length=1,choices=MISSING_POLICIES)

class RiskModelFamily(models.Model):
	name = models.CharField(max_length=200)
	version_max = models.IntegerField()

	def getNewVersion(self):
		self.version_max += 1
		return self.version_max

	def __init__(self, *args, **kwargs):
		super(MetricFamily, self).__init__(*args, **kwargs)
		self.version_max = 1

class RiskModel(models.Model):
	name = models.CharField(max_length=200)
	version = models.IntegerField(editable=False)
	family = models.ForeignKey('MetricFamily',editable=False)
	
	formula = models.CharField(max_length=200)
	metrics = models.ManyToManyField('Metric',through=ModelMetricLink)

MetricFormSet = inlineformset_factory(RiskModel,ModelMetricLink,can_delete=True)