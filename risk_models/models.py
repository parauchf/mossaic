#from django.db import models
from django.contrib.gis.db import models
from django.contrib.auth.models import User

class Metric(models.Model):
	name = models.CharField(max_length=200)
	
	minimumValue = models.DecimalField(max_digits=19,decimal_places=10)
	maximumValue = models.DecimalField(max_digits=19,decimal_places=10)
	precision = models.IntegerField()
	
	unitOfMeasure = models.CharField(max_length=100)
	
	TYPE_CHOICES = (
	        ('M', 'Multiple choice'),
	        ('D', 'Numeric'),
	    )
	type = models.CharField(max_length=1,choices=TYPE_CHOICES)
	
	def type(self):
		return type
		
	def __unicode__(self):
		return self.name


class MCOption(models.Model):
	name = models.CharField(max_length=200)
	ordinal = models.IntegerField()
	metric = models.ForeignKey('Metric')


class RiskModel(models.Model):
	name = models.CharField(max_length=200)
	formula = models.CharField(max_length=200)
	metrics = models.ManyToManyField('Metric')