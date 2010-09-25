from django.utils import simplejson
from django.template.context import RequestContext
from django.shortcuts import get_object_or_404, render_to_response
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.conf import settings
from django.core.urlresolvers import reverse

from eats.forms import QueryForm
from libraries.findeat import FindBestEat

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
    q = request.POST.get('q')
    postal_code = request.POST.get('postal_code')
        
    result = FindBestEat(postal_code, q)
    listing = result.listing
    address = listing.get('address')
    geocode = listing.get('geoCode')

    data = {
        "name" : listing.get('name'),
        "street_address" : address.get('street'),
        "city" : address.get('city'),
        "province" : address.get('prov'),
        "latitude" : geocode.get('latitude'),
        "longitude" : geocode.get('longitude'),
        "distance" : listing.get('distance'),
        "id" : listing.get('id'),
        'relavence_rank' : listing.get('relevanceRank'),
    }
    
    return HttpResponse(simplejson.dumps(data), mimetype="application/javascript")
    
    
