from yellowrestaurant import *
from pprint import pprint
from decimal import *
import json
from settings import *

ypAPI = YellowRestaurantAPI(api_key = YELLOWPAGES_API_KEY)
biz = ypAPI.find_restaurant('', 'M5A 1S2', uid='127.0.0.1', maxDistance=0.5)
print biz
for listing in biz:
    pprint(listing)

import pdb
pdb.set_trace()
