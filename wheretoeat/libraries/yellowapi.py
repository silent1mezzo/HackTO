"""
 YellowAPI Python API Library

 Requires: Python 2.3+
 Version: 0.1 (2010-09-15)
"""
import urllib2
import urllib
import itertools
import re

class YellowAPI(object):
	"""
	A thin wrapper around urllib2 to perform calls to YellowAPI.  This class
	does not do any processing of the response contents (XML or JSON). 
	"""

	PROD_URL = 'http://api.yellowapi.com'
	TEST_URL = 'http://api.sandbox.yellowapi.com'

	def __init__(self, api_key, test_mode=False, format='XML', handlers=[]):
		if len(api_key) != 24:
			raise TypeError('api_key should be 24 characters.')
		self.api_key = api_key
		
		if test_mode:
			self.url = self.TEST_URL
		else:
			self.url = self.PROD_URL

		if format not in ['XML', 'JSON']:
			raise TypeError('Format should be XML or JSON')
		self.format = format

		self.opener = urllib2.build_opener(*handlers)
		self.last_url = None
		

	def find_business(self, what, where, uid, page=None, page_len=None, 
			sflag=None, lang=None):
		"""
		Perform the FindBusiness call.
		"""
		url = self._build_url('FindBusiness', what=what, where=where, UID=uid, 
				pg=page, pgLen=page_len, sflag=sflag, lang=lang)
		return self._perform_request(url)

	
	def get_business_details(self, prov, business_name, listing_id, uid, 
			city=None, lang=None):
		"""
		Perform the GetBusinessDetails call.
		"""
		kws = {'prov': prov, 'bus-name': business_name, 
				'listingId': listing_id, 'city': city, 
				'lang': lang, 'UID': uid
				}
		url = self._build_url('GetBusinessDetails', **kws)
		print url
		return self._perform_request(url)


	def find_dealer(self, pid, uid, page=None, page_len=None, lang=None):
		"""
		Perform the FindDealer call.
		"""
		url = self._build_url('FindDealer', pid=pid, UID=uid, pg=page, 
				pgLen=page_len, lang=lang)
		return self._perform_request(url)


	def get_last_query(self):
		"""
		Used for debugging purposes.  Displays the url string used in the 
		last calls.
		"""
		return self.last_url


	NAME_PATTERN = re.compile('[^A-Za-z0-9]+')
	@staticmethod
	def encode_business_name(name):
		"""
		Properly encode the business name for subsequent queries.
		"""
		return YellowAPI.NAME_PATTERN.sub('-', name)


	def _build_url(self, method, **kwargs):
		"""
		Build an HTTP url for the request.
		"""
		kwargs.update({'apikey': self.api_key, 'fmt': self.format})
		params = ["%s=%s" % (k,urllib.quote(str(v))) for (k,v) in itertools.ifilter(
				lambda (k,v): v is not None, kwargs.iteritems())]

		self.last_url = "%s/%s/?%s" % (self.url, method, "&".join(params))
		return self.last_url



	def _perform_request(self, url):
		"""
		Perform the GET Request and handle HTTP response.
		"""
		resp = None
		try:
			resp = self.opener.open(url)
			body = resp.read()
		except urllib2.HTTPError, err:
			if err.code == 400:
				msg = err.read()
				err.msg += "\n" + msg
			raise(err)
		finally:
			if resp:
				resp.close()
		return body
				
