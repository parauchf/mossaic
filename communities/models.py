#from django.db import models
from django.contrib.gis.db import models
from django.contrib.auth.models import User

class Community(models.Model):
	objects = models.GeoManager()
	name = models.CharField(max_length=200)
	location = models.PointField(srid=4326,blank=True,null=True)
	project = models.ForeignKey('projects.Project')
	
	def __unicode__(self):
		return self.name

class Note(models.Model):
	content = models.TextField()
	models.ForeignKey('Community')

class Observation(models.Model):
	community = models.ForeignKey('communities.Community')
	metric = models.ForeignKey('risk_models.Metric')
	user = models.ForeignKey('users.MossaicUser')
	timestamp = models.DateTimeField(auto_now=True)

	value = models.DecimalField(max_digits=19,decimal_places=10)

	def __unicode__(self):
		return (self.community.name + ": " + self.metric.name)