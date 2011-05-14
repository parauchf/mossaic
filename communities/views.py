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


def survey(request,community_id,project_id):
	try:
		community = Community.objects.get(pk=community_id)
		project = Project.objects.get(pk=project_id)
	except:
		raise Http404
	
	
	

	if request.method == "POST":
		form = SurveyForm(request.POST,community=community)
		if form.is_valid():
			form.save()
			HttpResponseRedirect("/projects/%s/communities/%s/observations" % (project.id,community.id) )
	else:
		form = SurveyForm(community=community)
		
	context = RequestContext(request,{
		'community': community,
		'form': form,
		'project': project
	})
	return render_to_response('communitySurvey.html',context,context_instance=RequestContext(request))
	
		
def observations(request,community_id,project_id):
	if request.method=="GET":
		try:
			community = Community.objects.get(pk=community_id)
			project = Project.objects.get(pk=project_id)
		except:
			raise Http404
		
		observations = Observation.objects.filter(community__id=community.id)
		
		context = RequestContext(request,{
			'observations': observations,
			'community': community,
			'project': project
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
		})

		return render_to_response('projectCommunityList.html',context,context_instance=RequestContext(request))

