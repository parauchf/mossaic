from django.contrib import admin
from django.contrib.gis import admin
from django.views.decorators.csrf import csrf_protect

from projects.models import Project, Membership
from communities.models import Community, Observation
from users.models import MossaicUser
from risk_models.models import RiskModel, Metric, MCOption


class ObservationInline(admin.TabularInline):
	model=Observation

class CommunityAdmin(admin.OSMGeoAdmin):
	model=Community
	search_fields = ['name']
	inlines=[ ObservationInline ]
	fieldsets = [
		('General', {'fields': ['name','project']}),
		# ('Metrics',{'metrics': ['MeasurementInline']})
		('Location', {'fields': ['location']})
	]
	
admin.site.register(Community, CommunityAdmin)