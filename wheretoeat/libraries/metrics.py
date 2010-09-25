from django.core.cache import cache

from libraries.foursquare import Api as FourSquareApi
from libraries.weather.weather import GoogleWeather

class Metric(object):
    """
    Object will apply the metrics and output a metric number.
    """
    CACHE_KEY = '4square'
    
    def __init__(self, yp_listing):
        # Test data -> yp_listing
        # {u'address': {u'city': u'Toronto',
        #               u'pcode': u'M5C2G3',
        #               u'prov': u'ON',
        #               u'street': u'97 Church St'},
        #  u'distance': u'0.4',
        #  u'geoCode': {u'latitude': u'43.65213', u'longitude': u'-79.37534'},
        #  u'id': u'635111',
        #  u'name': u'Florentine Court Dining Room'}
        self.yp_listing = yp_listing
        self.metric_rating = self.apply_metrics()
        
    def _load_foursquare_data(self, listing, l=1):
        cache_key = "%s_%s" % (self.CACHE_KEY, listing.get('id'))
        data = cache.get(cache_key, 'NO_CACHED_ITEM')
        if 'NO_CACHED_ITEM' == data:
            # there was nothing in the cache - go get it.
            foursquare = FourSquareApi()
            data = foursquare.get_venues(
                geolat=listing['geoCode']['latitude'], 
                geolong=listing['geoCode']['longitude'], 
                q=listing.get('name'), l=l)
            cache.set(cache_key, data, 600) # cache for 24 hours    
        return data
        
        
    def apply_metrics(self):
        total = 0
        
        metrics = (
            # (func_name, weight)
            (self.calculate_weather_metric, 1.0),
            (self.calculate_distance_metric, 1.0),
            (self.calculate_popularity, 1.0),
            (self.calculate_saturation, 1.0),
        )
        
        for f, weight in metrics:
            total += f() * weight

        return total
    def calculate_weather_metric(self):
        city = self.yp_listing.get("address").get("city", "")
        gw = GoogleWeather(location=city)
        return gw.getCurrentConditionMultiplier()
    
    def calculate_distance_metric(self):
        return 1 - float(self.yp_listing.get('distance', 1))
        
    def calculate_popularity(self):
        """
        Check the total number of checkins on FourSquare.
        """
        foursquare_data = self._load_foursquare_data(self.yp_listing)
        stats = self._foursquare_stats(foursquare_data)
        return 0
        
    def calculate_saturation(self):
        """
        Check the total number of people currently checked in.
        """
        foursquare_data = self._load_foursquare_data(self.yp_listing)
        stats = self._foursquare_stats(foursquare_data)
        return int(stats.get('herenow', 0))
    
    def _foursquare_stats(self, data): 
        groups = data.get('groups', None)
        if groups:
            for match in groups:
                for venue in match.get('venues'):
                    if venue.get('name', '') <> self.yp_listing.get('name'):
                        continue
                    return venue.get('stats', '')     
        return {}
