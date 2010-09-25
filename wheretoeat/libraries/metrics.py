class Metric(object):
    """
    Object will apply the metrics and output a metric number.
    """
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
        
    def apply_metrics(self):
        total = 0
        
        metrics = (
            # (func_name, weight)
            (self.calculate_distance_metric, 1.0),
            (self.calculate_popularity, 1.0),
            (self.calculate_saturation, 1.0),
        )
        
        for f, weight in metrics:
            total += f() * weight

        return total
    
    def calculate_distance_metric(self):
        return 1 - self.yp_listing.get('distance', 1)
        
    def calculate_popularity(self):
        """
        Check the total number of checkins on FourSquare.
        """
        return 0
        
    def calculate_saturation(self):
        """
        Check the total number of people currently checked in.
        """
        return 0
    