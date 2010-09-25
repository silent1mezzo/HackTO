from django.template.context import RequestContext
from django.shortcuts import get_object_or_404, render_to_response
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.conf import settings
from django.core.urlresolvers import reverse

def index(request):
    template_name = 'base.html'
    context = RequestContext(request)
    dict = {}
    return render_to_response(
        template_name,
        dict,
        context,
        )


def search(request):
    template_name = 'result.html'
    context = RequestContext(request)
    dict = {}
    if request.POST:
        search = request.POST.get('search', '')
        postal_code = request.POST.get('postal_code', '')
    else:
        return HttpResponseRedirect(reverse('index'))
    
    return render_to_response(
        template_name,
        dict,
        context,
    )
    
