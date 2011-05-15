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

class Metric(models.Model):
	name = models.CharField(max_length=200,unique=True)

	project = models.ForeignKey('projects.project')
	
	minimumValue = models.DecimalField(max_digits=19,decimal_places=10,blank=True,null=True)
	maximumValue = models.DecimalField(max_digits=19,decimal_places=10,blank=True,null=True)
	precision = models.IntegerField(blank=True,null=True)
	unitOfMeasure = models.CharField(max_length=100,blank=True,null=True)
	
	metricType = models.CharField(max_length=1,choices=TYPE_CHOICES,blank=False,null=False,default='D')
	
	def type(self):
		return metricType
		
	def __unicode__(self):
		return self.name


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
	user = models.ForeignKey('users.MossaicUser',null=True,blank=True)
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
	defaultMCValue = models.ForeignKey('MCOption',null=True,blank=True)
	# ,choices=metric.mcoption_set)
	
	missingValuePolicy = models.CharField(max_length=1,choices=MISSING_POLICIES,default="I")
	
	duplicateValuePolicy = models.CharField(max_length=1,choices=MISSING_POLICIES,default="A")
	
	def eval(self,community):
		observations = Observation.objects.filter(community__id__exact=community.id,metric__id__exact=self.metric.id)
		nobs = observations.count()
		
		if nobs == 1:
			if self.metric.metricType == "M":
				return observations[0].mcValue.mcscore_set.filter(modelMetricLink__id__exact=self.id)[0].score
			else: #if self.metric.metricType == "D":
				return observations[0].value
		
		elif nobs == 0:
			if self.missingValuePolicy == 'D':
				if self.metric.metricType == 'M':
					return self.defaulMCValue.mcscore_set.filter(modelMetricLink__id__exact=self.id)[0].score
				elif self.metric.metricType == 'D':
					return self.defaultDecimalValue
			else: # metric.missingValuePolicy == 'I':
				return None
		
		elif nobs > 1:
			if self.metric.metricType == 'M':
				if self.duplicateValuePolicy == 'A':
					return self.defaultMCValue.mcscore_set.filter(modelMetricLink__id__exact=self.id)[0].score
				if self.duplicateValuePolicy == 'D':
					return self.defaultMCValue.mcscore_set.filter(modelMetricLink__id__exact=self.id)[0].score
			if self.metric.metricType == 'D':
				if self.duplicateValuePolicy == 'A':
					total = 0
					for obs in observations:
						total += obs.value
					return total / nobs
				elif self.duplicateValuePolicy == 'D':
					return self.defaultDecimalValue
				else:
					return None
					
		return -1
		
	
	def save(self, *args, **kwargs):
		super(ModelMetricLink, self).save()
		for option in self.metric.mcoption_set.all():
			try:
				s = MCScore(
					option = option,
					modelMetricLink = self,
					score = 0
				)
				s.save()
			except:
				pass

class RiskModel(models.Model):
	name = models.CharField(max_length=200)
	
	project = models.ForeignKey('projects.project')
	
	# version = models.IntegerField(editable=False)
	
	metrics = models.ManyToManyField('Metric',through=ModelMetricLink)

	def __unicode__(self):
		return self.name
	
	def eval(self,community):
		total = 0
		for mml in RiskModel.objects.get(pk=self.id).modelmetriclink_set.all():
			score = mml.eval(community)
			if score is None:
				return None
			else:
				total += score
		
		return total
				

class RiskModelForm(ModelForm):
	class Meta:
		model = RiskModel
		widgets = {
			# 'metricType': RadioSelect,
		}

