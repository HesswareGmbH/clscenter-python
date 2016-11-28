from clsmodule import CLSModule
from clsexceptions import *

import requests


class SwitchingPoint(object):

	def __init__(self, switchingPoint, center = None):
		self.center = center
		self.swpoint = switchingPoint

		# Elements of the object from cls center
		(json, header_code) = center.getJsonData("clscenter", "switchingpoints/byname/%s" % self.swpoint)

		self.json = json

		# Do some more checks
		if len(json) == 0 or header_code != requests.codes.ok:
			raise CLSInternalError()

		self.macAddress = json["gateway"]["macAddress"]

		# Store this element for later usage
		self.module = CLSModule(self.macAddress, center)

	def __str__(self):
		if len(self.json) == 0:
			return "%s is an empty class" % self.__class__

		return "%s: %d" % (self.json["name"], self.json["valueApplied"])

	def getInformationDisplay(self):
		if len(self.json) == 0:
			return "%s is not complete" % self.__class__

		retStr = """
Switchingpoint:		%s
Eingestellter Wert:	%d
""" % (self.json["name"],  self.json["valueApplied"])
		

	def switch(self, value):
		(json, header_code) = self.center.putJsonData("clscenter", "switchingpoints/byname/%s/%d" % (self.swpoint, value), "")


		# We always get a json object and a ok code (200) from the CLS Center
		if len(json) == 0 or header_code != requests.codes.ok:
			raise CLSInternalError()

		if not "replyCode" in json:
			raise CLSInternalError()

		replyCode = json["replyCode"]

		if replyCode == 409:
			raise CLSActionIsRunning()

		if not "valueApplied" in json:
			raise CLSUnknownAnswer()

		# We should return the adjusted value here
		value = json["valueApplied"]

		# Return the requested value
		return value


