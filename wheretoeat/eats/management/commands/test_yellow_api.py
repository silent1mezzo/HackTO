from pprint import pprint

from django.core.management.base import NoArgsCommand
from django.conf import settings

from libraries.yellowrestaurant import YellowRestaurantAPI

class Command(NoArgsCommand):
    requires_model_validation = False
    can_import_settings = True
    
    def handle_noargs(self, **kwargs):
        ypAPI = YellowRestaurantAPI(api_key = settings.YELLOWPAGES_API_KEY)
        biz = ypAPI.find_restaurant('', 'M5A 1S2', uid='127.0.0.1', maxDistance=0.5)
        print biz
        for listing in biz:
            pprint(listing)
