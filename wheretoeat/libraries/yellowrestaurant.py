from yellowapi import *
import json

class YellowRestaurantAPI(YellowAPI):
    def __init__(self, api_key, test_mode=False, format='JSON', handlers=[]):
        super(YellowRestaurantAPI, self).__init__(api_key, test_mode, format, handlers)

    def find_restaurant(self, what, where, uid, page=None, page_len=None,
            sflag=None, lang=None, maxDistance=float(1.0)):
        what = "restaurant " + what
        resultsDict = json.loads(self.find_business(what,where,uid,page,page_len, sflag, lang))
        listings = resultsDict.get('listings')
        filteredResults = []
        for listing in listings:
            if float(listing.get('distance')) < float(maxDistance):
                filteredResults.append(listing)
        return filteredResults 
