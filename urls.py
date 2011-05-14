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
	(r'^ajax/metrics','risk_models.views.ajaxMetrics'),
	# (r'^projects/?$','projects.views.projects'),
	
	(r'^projects/(?P<project_id>\d+)/communities/(?P<community_id>\d+)/observations', 'communities.views.observations'),
	(r'^projects/(?P<project_id>\d+)/communities/(?P<community_id>\d+)/survey', 'communities.views.survey'),
	(r'^projects/(?P<project_id>\d+)/communities/(?P<community_id>\d+)/administration', 'communities.views.administration'),
	
	(r'^projects/(?P<project_id>\d+)/risk(-matrix)?/?$', 'projects.views.riskMatrix'),
	(r'^projects/(?P<project_id>\d+)/admin(istation)?/?$', 'projects.views.administration'),
	
	(r'^projects/(?P<project_id>\d+)/users/?$', 'projects.views.userList'),
	(r'^projects/(?P<project_id>\d+)/users/(add|new)(\-user)?/?', 'projects.views.userAdd'),
	
	(r'^projects/(?P<project_id>\d+)/communities/?$', 'projects.views.communityList'),
	(r'^projects/(?P<project_id>\d+)/communities/(add|new)(-community)?/?$', 'projects.views.communityAdd'),
	
	(r'^projects/(?P<project_id>\d+)/metrics/?$', 'projects.views.metricList'),
	(r'^projects/(?P<project_id>\d+)/metrics/(?P<metric_id>\d+)/?$', 'risk_models.views.metric',{'is_new': False}),
	(r'^projects/(?P<project_id>\d+)/metrics/new(-metric)?/?$', 'risk_models.views.metric',{'is_new': True}),
	
	(r'^projects/(?P<project_id>\d+)/models/?$', 'projects.views.riskModelList'),
	(r'^projects/(?P<project_id>\d+)/models/(?P<riskModel_id>\d+)/?$', 'risk_models.views.riskModel',{'is_new': False}),
	(r'^projects/(?P<project_id>\d+)/models/(add|new)(-model)?/?$', 'risk_models.views.riskModelNew'),
	(r'^projects/(?P<project_id>\d+)/models/(?P<riskModel_id>\d+)/(add|new)(-metric)?/?$', 'risk_models.views.metricLinkNew'),
	
	
	(r'^projects/(?P<project_id>\d+)/observations/?$', 'projects.views.observationList'),
	(r'^projects/(?P<project_id>\d+)/observations/(?P<observation_id>)/?$', 'risk_models.views.observation'),
	(r'^projects/(?P<project_id>\d+)/observations/new(-observation)?/?$', 'risk_models.views.observation',{'is_new': True}),

	
	# (r'^models/?$', 'risk_models.views.riskModelList'),
	# (r'^models/(?P<riskModel_id>\d+)/?', 'risk_models.views.riskModel'),
	# (r'^models/new/?', 'risk_models.views.riskModel'),
	
	(r'^accounts/login', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
	
)