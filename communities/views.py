from django.template import Context, loader
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext

from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from django.core import serializers

from users.models import MossaicUser

from risk_models.models import *
from projects.models import *
from communities.models import *

from communities.forms import *

from django.http import Http404

@csrf_protect
@login_required

def survey(request,community_id,project_id):
	try:
		community = Community.objects.get(pk=community_id)
		project = Project.objects.get(pk=project_id)
	except:
		raise Http404

	metrics = Metric.objects.filter(project__id__exact=community.project.id)
	forms = []
	
	for metric in metrics:
		if request.method == "POST":
			form = SurveyItem(request.POST, request=request, prefix = 'S-M%s-C%s' % (metric.pk,community.pk))
			if form.is_filled:
				if form.is_valid():
					form.save()
		else:
			form = SurveyItem(request=request, prefix = 'S-M%s-C%s' % (metric.pk,community.pk),initial={'metric': metric.id, 'community': community.id} )
		
		form.title = metric.name
		form.type = metric.metricType
		form.fields["mcValue"].queryset = MCOption.objects.filter(metric__id__exact=metric.id)
		
		forms.append(form)
		
		
	if request.method == "POST":		
		return HttpResponseRedirect("/projects/%s/communities/%s/observations" % (project.id,community.id) )
	
	
	context = RequestContext(request,{
		'community': community,
		'forms': forms,
		'project': project,
		'request': request,
		'active_tab': 'survey'
	})
	return render_to_response('communitySurvey.html',context,context_instance=RequestContext(request))
	
		
def observations(request,community_id,project_id):
	if request.method == "GET":
		try:
			community = Community.objects.get(pk=community_id)
			project = Project.objects.get(pk=project_id)
		except:
			raise Http404
		
		observations = Observation.objects.filter(community__id=community.id)
		
		context = RequestContext(request,{
			'observations': observations,
			'community': community,
			'project': project,
			'request': request,
			'active_tab': 'observations'
		})
		return render_to_response('communityObservations.html',context,context_instance=RequestContext(request))


def administration(request,community_id):
	if request.method=="GET":
		try:
			community=Community.objects.get(id__exact=community_id)
		except:
			raise Http404

		context = RequestContext(request,{
			'community': community,
			'request': request,
			'active_tab': 'administration'
		})

		return render_to_response('communitySettings.html',context,context_instance=RequestContext(request))

