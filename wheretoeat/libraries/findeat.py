
from libraries.yellowrestaurant import YellowRestaurantAPI
from libraries.metrics import Metric
from django.conf import settings

class FindBestEat(object):
    def __init__(self, postal_code, query):
        self.postal_code = postal_code
        self.query = query
        self.ypAPI = YellowRestaurantAPI(api_key = settings.YELLOWPAGES_API_KEY)

        results = self.ypAPI.find_restaurant(self.query, self.postal_code, uid='127.0.0.1', maxDistance=1.0)
        
        mostRelevant = {'relevanceRank': -1}
        count = 0
        for listing in results :
            if count > 10:
                break
            relevanceRank = Metric(listing).metric_rating 
            listing['relevanceRank'] = relevanceRank
            if listing['relevanceRank'] > mostRelevant:
                mostRelevant = listing['relevanceRank']
            count += 1
        self.listing = listing      
