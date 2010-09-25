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


# {u'distance': u'0.8', u'name': u'Grange Hotel', u'address': {u'city': u'Toronto', u'pcode': u'M5T2V5', u'street': u'165 Grange Ave', u'prov': u'ON'}, u'geoCode': {u'latitude': u'43.651055981', u'longitude': u'-79.401348179'}, 'details': '{"phones":[{"type":"primary","npa":"416","nxx":"603","num":"7700","dispNum":"416-603-7700"}],"categories":[{"name":"Hotels","isSensitive":false},{"name":"Tourist Accommodation","isSensitive":false},{"name":"Hotels-Apartment","isSensitive":false}],"products":{"webUrl":["http:\\/\\/www.grangehotel.com"],"dispAd":[{"url":"http:\\/\\/ci.yp.ca\\/14531565ag_f.jpg","thmbUrl":"http:\\/\\/ci.yp.ca\\/14531565ag_t.gif"}],"videos":[{"url":"http:\\/\\/cdn.media.yp.ca\\/20494\\/1246329736421.flv","thmbUrl":"http:\\/\\/cdn.media.yp.ca\\/20494\\/1246329736421_t.jpg"}],"photos":[],"profiles":[{"lang":"en","keywords":{"MthdPmt":["American Express","Cash","Discover","Gift Certificate","Interac","JCB","MasterCard","Traveller Cheque","Visa"],"LangSpk":["English"],"GetThr":["North to Grange Ave","Turn Right on Augusta","First Traffic Light West of Spadina","From QEW and Gardiner Expressway","Go North on Spadina to Queen"],"ProdServ":["All Major Credit Cards Accepted","Cable TV","Clean & Quiet Modern Building","Coin Laundry on Each Floor","Comfortable Studio Units","Direct Dial Telephones","Economy Rates","Equipped Kitchenette","Free Hi-Speed Internet Access","Hotel Accommodations","Individual Heat and Air","On-Site Parking","Private Bath with Shower"]}}],"listPres":[]},"logos":[],"id":"2297558","name":"Grange Hotel","address":{"street":"165 Grange Ave","city":"Toronto","prov":"ON","pcode":"M5T2V5"},"geoCode":{"latitude":"43.651055981","longitude":"-79.401348179"},"merchantUrl":"http:\\/\\/www.yellowpages.ca\\/bus\\/Ontario\\/Toronto\\/Grange-Hotel\\/2297558.html"}', 'weather': u'Mostly Cloudy', u'id': u'2297558', 'relevanceRank': 0.89999999999999991}


    
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
        'weather_desc' : listing.get('weather'),
        'weather_icon' : listing.get('weather_icon'),
    }
    
    return HttpResponse(simplejson.dumps(data), mimetype="application/javascript")
    
    
