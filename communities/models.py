# from django.db import models
from django.contrib.gis.db import models
from django.contrib.auth.models import User

class Community(models.Model):
	# objects = models.GeoManager()
	name = models.CharField(max_length=200)
	description = models.TextField()
	location = models.PointField(srid=4326,blank=True,null=True)
	project = models.ForeignKey('projects.Project')
	
	def __unicode__(self):
		return self.name

# class Note(models.Model):
# 	content = models.TextField()
# 	models.ForeignKey('Community')