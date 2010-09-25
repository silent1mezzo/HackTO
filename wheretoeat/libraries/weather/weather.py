import pywapi
import string
import pprint
from conditions import *

class GoogleWeather(object):
    
    def __init__(self, location):
        # location can be postal code, city, etc
        self.location = location

    def getCurrentCondition(self):
        condition = None
        weatherDetails = pywapi.get_weather_from_google(self.location)
        cc = weatherDetails.get("current_conditions", None)
        if cc:
            condition = cc.get("condition", None)
        return condition

    def getCurrentConditionMultiplier(self):
        cc = self.getCurrentCondition()
        weighting = weather_conditions_multiplier.get(cc, 1)
        return weighting 
