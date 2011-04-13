#from django.db import models
from django.contrib.gis.db import models
from django.contrib.auth.models import User


class Project(models.Model):
	objects = models.GeoManager()
	name = models.CharField(max_length=200)
	slug = models.SlugField(max_length=50)
	users = models.ManyToManyField('users.MossaicUser',through='Membership')
	
	def __unicode__(self):
		return self.name

class Membership(models.Model):
	canView=models.BooleanField(default=False)
	addMeasurements=models.BooleanField(default=False)
	addCommunities=models.BooleanField(default=False)
	addNotes=models.BooleanField(default=False)

	project=models.ForeignKey('Project')
	user=models.ForeignKey('users.MossaicUser')