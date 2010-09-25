from django.utils import simplejson
from django.template.context import RequestContext
from django.shortcuts import get_object_or_404, render_to_response
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.conf import settings
from django.core.urlresolvers import reverse

from eats.forms import QueryForm

def index(request):
    template_name = 'base.html'
    context = {
        'form' : QueryForm(),
    }
    return render_to_response(template_name, context, context_instance=RequestContext(request))


def search(request):
    template_name = 'result.html'
    context = {}
    if request.POST:
        search = request.POST.get('search', '')
        postal_code = request.POST.get('postal_code', '')
    else:
        return HttpResponseRedirect(reverse('index'))
    
    return render_to_response(template_name, context, context_instance=RequestContext(request))


def search_json(request):
    
    
    data = {
        'name' : '',
        'address' : '',
        'city' : '',
        'province' : 'the province',
        'latitude' : '',
        'longitude' : '',
        'distance' : ''
    }
    return HttpResponse(simplejson.dumps(data), mimetype="application/javascript")
    
    
