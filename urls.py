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
	(r'^projects/(?P<project_id>\d+)/users', 'projects.views.projectUsers'),
	(r'^projects/(?P<project_id>\d+)/communities', 'projects.views.projectCommunities'),
	(r'^projects/(?P<project_id>\d+)/risk(-matrix)?', 'projects.views.projectRiskMatrix'),
	(r'^projects/(?P<project_id>\d+)/admin(istation)?', 'projects.views.projectAdministration'),
	(r'^projects/(?P<project_id>\d+)/add-user', 'projects.views.projectAddUser'),
	(r'^projects/(?P<project_id>\d+)/add-community', 'projects.views.projectAddCommuntiy'),
	
	(r'^metrics/?$', 'risk_models.views.metricList'),
	(r'^metrics/(?P<metric_id>\d+)/?', 'risk_models.views.metric'),
)