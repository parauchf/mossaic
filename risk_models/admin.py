from django.contrib import admin
from django.contrib.gis import admin
from django.views.decorators.csrf import csrf_protect


from risk_models.models import *

class MCOptionInline(admin.TabularInline):
	model=MCOption

class MetricAdmin(admin.ModelAdmin):
	model=Metric
	inlines = [MCOptionInline]
	search_fields = [ 'name' ]

class MetricLinkInline(admin.TabularInline):
	model=ModelMetricLink

class RiskModelAdmin(admin.ModelAdmin):
	model=RiskModel
	inlines = [MetricLinkInline]
	search_fields = [ 'name' ]
	
admin.site.register(Metric, MetricAdmin)

admin.site.register(RiskModel, RiskModelAdmin)

admin.site.register(MCScore)

admin.site.register(ModelMetricLink)

admin.site.register(Observation)