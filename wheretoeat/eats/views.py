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

    if not result.listing:
        data = {
            "status" : "EMPTY",
        }
        return HttpResponse(simplejson.dumps(data), mimetype="application/javascript")

    listing = result.listing

    address = listing.get('address')
    geocode = listing.get('geoCode')


    # {u'distance': u'0.9', u'name': u'Thai Island Restaurant', u'address': {u'city': u'York', u'pcode': u'M9N1L5', u'street': u'130 King St', u'prov': u'ON'}, u'geoCode': {u'latitude': u'43.64809157', u'longitude': u'-79.382931673'}, 'details': '{"phones":[{"type":"primary","npa":"416","nxx":"203","num":"7745","dispNum":"416-203-7745"}],"categories":[{"name":"Restaurants","isSensitive":false}],"products":{"webUrl":[],"dispAd":[],"videos":[],"photos":[],"profiles":[],"listPres":[]},"logos":[],"id":"1567984","name":"Thai Island Restaurant","address":{"street":"130 King St","city":"York","prov":"ON","pcode":"M9N1L5"},"geoCode":{"latitude":"43.64809157","longitude":"-79.382931673"},"merchantUrl":"http:\\/\\/www.yellowpages.ca\\/bus\\/Ontario\\/York\\/Thai-Island-Restaurant\\/1567984.html"}', 'weather': u'Mostly Cloudy', u'id': u'1567984', 'relevanceRank': 0}
    print listing
    data = {
        "status" : "OK",
        "name" : listing.get('name'),
        "street_address" : address.get('street'),
        "city" : address.get('city'),
        "province" : address.get('prov'),
        "latitude" : geocode.get('latitude'),
        "longitude" : geocode.get('longitude'),
        "distance" : listing.get('distance'),
        "id" : listing.get('id'),
        'relavence_rank' : "%.4f" %(2 + float(listing.get('relevanceRank'))),
    }
    
    return HttpResponse(simplejson.dumps(data), mimetype="application/javascript")
    
    
