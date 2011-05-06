from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
from django.contrib import auth
import os

admin.autodiscover()


urlpatterns = patterns('',
	(r'^admin/', include(admin.site.urls)),
	(r'^static/(?P<path>.*)$','django.views.static.serve',
		{'document_root': os.path.join(settings.PROJECT_DIR, "static") }),
   	(r'^admin/static/(?P<path>.*)$','django.views.static.serve',
		{'document_root': os.path.join(settings.PROJECT_DIR, "static/admin") }),

	# (r'^accounts/login/?$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
	# (r'^accounts/logout/?$', 'django.contrib.auth.views.logout', {'template_name': 'login.html'}),
	
	(r'^base/', 'projects.views.base'),
	(r'^ajax/users','projects.views.ajaxUsers'),
	# (r'^projects/?$','projects.views.projects'),
	
	(r'^projects/(?P<project_id>\d+)/risk(-matrix)?', 'projects.views.riskMatrix'),
	(r'^projects/(?P<project_id>\d+)/admin(istation)?', 'projects.views.administration'),
	
	(r'^projects/(?P<project_id>\d+)/users', 'projects.views.userList'),
	(r'^projects/(?P<project_id>\d+)/add-user', 'projects.views.addUser'),
	
	(r'^projects/(?P<project_id>\d+)/communities', 'projects.views.communityList'),
	(r'^projects/(?P<project_id>\d+)/add-community', 'projects.views.addCommuntiy'),
	
	(r'^projects/(?P<project_id>\d+)/metrics', 'projects.views.metricList'),
	(r'^projects/(?P<project_id>\d+)/add-metric', 'risk_models.views.metric'),
	
	(r'^projects/(?P<project_id>\d+)/models', 'projects.views.riskModelList'),
	(r'^projects/(?P<project_id>\d+)/add-model', 'risk_models.views.riskModel'),
	
	(r'^projects/(?P<project_id>\d+)/observations', 'projects.views.observationList'),
	(r'^projects/(?P<project_id>\d+)/observations/(?P<observation_id>)', 'risk_models.views.observation'),
	(r'^projects/(?P<project_id>\d+)/new-observation', 'risk_models.views.newObservation'),
	
	(r'^metrics/?$', 'risk_models.views.metricList'),
	(r'^metrics/(?P<metric_id>\d+)/?', 'risk_models.views.metric'),
	(r'^metrics/new/?', 'risk_models.views.metric'),
	
	(r'^models/?$', 'risk_models.views.riskModelList'),
	(r'^models/(?P<riskModel_id>\d+)/?', 'risk_models.views.riskModel'),
	(r'^models/new/?', 'risk_models.views.riskModel'),
	
	(r'^accounts/login', 'django.contrib.auth.views.login', {'template_name': '/templates/login.html'}),
	
)