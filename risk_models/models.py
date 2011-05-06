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
	
	def save(self, *args, **kwargs):
		if 'family_id' in kwargs:
		 	self.family = MetricFamily.get(pk=family_id)
		else:
			f = MetricFamily()
			f.save()
			self.family_id = f.id
			
		self.version = self.family.getNewVersion()
		super(Metric, self).save()

class MCOption(models.Model):
	name = models.CharField(max_length=200)
	metric = models.ForeignKey('Metric')

	def __unicode__(self):
		return self.name
		

# ModelFormSet = inlineformset_factory(models.RiskModel, models.Metric,formset=BaseBuildingFormset, extra=1)

class MCScore(models.Model):
	# TODO: do we need the option fk?
	option = models.ForeignKey('MCOption')
	modelMetricLink = models.ForeignKey('ModelMetricLink')
	score = models.DecimalField(max_digits=19,decimal_places=10)
	
	def __unicode__(self):
		return "%s<->%s" % (self.option.name,self.modelMetricLink.riskModel.name)
		
	class Meta:
	 	unique_together = ("option", "modelMetricLink")

class Observation(models.Model):
	community = models.ForeignKey('communities.Community')
	metric = models.ForeignKey('risk_models.Metric')
	user = models.ForeignKey('users.MossaicUser')
	timestamp = models.DateTimeField(auto_now=True)
	
	value = models.DecimalField(max_digits=19,decimal_places=10,blank=True,null=True)
	mcValue = models.ForeignKey('risk_models.MCOption',blank=True,null=True)
	
	def __unicode__(self):
		return (self.community.name + ": " + self.metric.name)

class ModelMetricLink(models.Model):
	riskModel = models.ForeignKey('RiskModel')
	metric = models.ForeignKey('Metric')
	transformation = models.CharField(max_length=200,blank=True,null=True)
	
	weight = models.DecimalField(max_digits=19,decimal_places=10,blank=True,null=True)
	
	defaultDecimalValue = models.DecimalField(max_digits=19,decimal_places=10,null=True,blank=True)
	defaultMCValue = models.IntegerField(blank=True,null=True)
	# ,choices=metric.mcoption_set)
	
	missingValuePolicy = models.CharField(max_length=1,choices=MISSING_POLICIES,default="I")
	
	duplicateValuePolicy = models.CharField(max_length=1,choices=MISSING_POLICIES,default="A")

	def save(self, *args, **kwargs):
		super(ModelMetricLink, self).save()
		scores = self.mcscore_set
		for option in self.metric.mcoption_set.all():
				s = MCScore(
					option = option,
					modelMetricLink = self,
					score = 0
				)
				s.save()


class RiskModelFamily(models.Model):
	name = models.CharField(max_length=200)
	version_max = models.IntegerField()

	def getNewVersion(self):
		self.version_max += 1
		return self.version_max
	
	def __init__(self, *args, **kwargs):
		super(RiskModelFamily, self).__init__(*args, **kwargs)
		self.version_max = 1

class RiskModel(models.Model):
	name = models.CharField(max_length=200)
	
	version = models.IntegerField(editable=False)
	family = models.ForeignKey('RiskModelFamily',editable=False)
	
	metrics = models.ManyToManyField('Metric',through=ModelMetricLink)
	
	def __unicode__(self):
		return self.name
	
	def save(self, *args, **kwargs):
		f = RiskModelFamily()
		f.save()
		self.family = f
		
		self.version = self.family.getNewVersion()
		super(RiskModel, self).save()

class RiskModelForm(ModelForm):
	class Meta:
		model = RiskModel
		widgets = {
			# 'metricType': RadioSelect,
		}

