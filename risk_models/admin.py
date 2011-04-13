from django.contrib import admin
from django.contrib.gis import admin
from django.views.decorators.csrf import csrf_protect


from risk_models.models import Metric, MCOption

class MCOptionInline(admin.TabularInline):
	model=MCOption

class MetricAdmin(admin.ModelAdmin):
	model=Metric
	inlines = [MCOptionInline]
	search_fields = [ 'name' ]

admin.site.register(Metric, MetricAdmin)