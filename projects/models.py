from django.db import models
# from django.contrib.gis.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify


class Project(models.Model):
	name = models.CharField(max_length=200)
	slug = models.SlugField(max_length=50, editable=False)
	users = models.ManyToManyField('users.MossaicUser',through='Membership',editable=False)
	
	# metrics = models.ManyToManyField('risk_models.Metric',null=True,blank=True)
	# riskModels = models.ManyToManyField('risk_models.RiskModel',null=True,blank=True)
	
	def save(self, *args, **kwargs):
		self.slug = slugify(self.name)
		super(Project, self).save()
	
	def __unicode__(self):
		return self.name

class Membership(models.Model):
	canView=models.BooleanField(default=False)
	addMeasurements=models.BooleanField(default=False)
	addCommunities=models.BooleanField(default=False)
	addNotes=models.BooleanField(default=False)

	project=models.ForeignKey('Project')
	user=models.ForeignKey('users.MossaicUser')