
from libraries.yellowrestaurant import YellowRestaurantAPI
from libraries.metrics import Metric
from django.conf import settings
from libraries.weather.weather import GoogleWeather

class FindBestEat(object):
    def __init__(self, postal_code, query):
        self.postal_code = postal_code
        self.query = query
        self.ypAPI = YellowRestaurantAPI(api_key = settings.YELLOWPAGES_API_KEY)

        results = self.ypAPI.find_restaurant(self.query, self.postal_code, uid='127.0.0.1', maxDistance=1.0)
        if len(results) == 0:
            self.listing = None
            return
        
        mostRelevant = {'relevanceRank': -1}
        count = 0
        for listing in results :
            relevanceRank = Metric(listing).metric_rating 
            listing['relevanceRank'] = relevanceRank
            if listing['relevanceRank'] > mostRelevant:
                mostRelevant = listing['relevanceRank']
            count+=1
        self.listing = listing
        prov = self.listing['address']['prov']
        busName = self.ypAPI.encode_business_name(self.listing['name'])
        busID = self.listing.get('id','')
        self.listing['details'] = self.ypAPI.get_business_details(prov, busName, busID, uid='127.0.0.1')
        gw = GoogleWeather(location=self.listing['address']['city'])
        self.listing['weather'] = gw.getCurrentCondition()
