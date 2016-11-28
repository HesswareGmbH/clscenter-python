import requests
import json
import urllib
import time
import base64
from clsmodule import CLSModule
from switchingpoint import SwitchingPoint

verify_SSL = False

class CLSCenter(object):

	"""
		This object includes all functions to get access to the funtions of the CLS Modules
	"""


	def __init__(self, url, user, password, cache_time = 60, api_key = "special-key"):

		# Store private variables
		self.clscenter = url
		self.key = api_key

		self.clsmodules = dict()

		# Store the Session to use
		s = requests.Session()
		s.auth = (user, password)
		self.session = s

		# Some default headers
		self.headers = {'Accept': 'application/json'}


	def getModule(self, mac):
		 return CLSModule(mac, self)

	def getSwitchingPoint(self, switchingPoint):
		return SwitchingPoint(switchingPoint, self)


	def getData(self, module, function):
		url = "%s/%s/%s?api_key=%s" % (self.clscenter, module, function, self.key)
		r = self.session.get(url, headers=self.headers, verify=verify_SSL)
		return r

	def postData(self, module, function, data_to_send):
		url = "%s/%s/%s?api_key=%s" % (self.clscenter, module, function, self.key)
		#data_to_send["api_key"] = self.__key
		r = self.session.post(url, headers=self.headers, verify=verify_SSL, data = data_to_send)
		return r

	def putData(self, module, function, data_to_send):
		url = "%s/%s/%s?api_key=%s" % (self.clscenter, module, function, self.key)
		r = self.session.put(url, headers=self.headers, verify=verify_SSL, data = data_to_send)
		return r


	def getJsonData(self, module, function):
		header_code = 200
		json = ""

		r = self.getData(module, function)
		try:
			json = r.json()
			header_code = r.status_code
		except ValueError:
			return (dict(), 500)

		return (json, header_code)

	def putJsonData(self, module, function, data):
		header_code = 200
		json = ""

		r = self.putData(module, function, data)
		try:
			json = r.json()
			header_code = r.status_code
		except ValueError:
			return (dict(), 500)

		return (json, header_code)

	def postJsonData(self, module, function, data):
		header_code = 500
		json = ""

		url = "%s/%s/%s?api_key=%s" % (self.clscenter, module, function, self.key)
		r = self.session.post(url, headers=self.headers, verify=verify_SSL, data=data)

		try:
			json = r.json()
			header_code = r.status_code
		except ValueError:
			pass

		print json,header_code
		return (json, header_code)

