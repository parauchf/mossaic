from django.contrib import admin
from django.contrib.gis import admin
from django.views.decorators.csrf import csrf_protect

from projects.models import Project, Membership
from communities.models import Community
from users.models import MossaicUser
from risk_models.models import RiskModel, Metric, MCOption


class CommunityInline(admin.TabularInline):
	model=Community
	fields = [ 'name' ]
	pass

class MembershipInline(admin.TabularInline):
	model=Membership
	
class ProjectAdmin(admin.ModelAdmin):
	# add_form_template = 'base.html'
	model = Project
	search_fields = [ 'name' ]
	filter_horizontal = [ 'users' ]
	inlines = [ CommunityInline, MembershipInline ]
		
			
# admin.site.register(Metric, MetricAdmin)
admin.site.register(Project, ProjectAdmin)
