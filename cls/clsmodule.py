import json
import requests

class CLSModule(object):

	def __init__(self, mac, center = None):
		self.center = center
		self.mac = mac

	def __str__(self):
		return "CLS-Module: %s" % self.mac

	def installFirmware(self, update_url):

		payload = {}
		payload["mac"] = self.mac
		payload["pluginname"] = "system"
		payload["plugincall"] = "installFirmware"
		payload["params"] = "{\"firmware_url\":\"%s\"}" % update_url

		(json, header_code) = self.center.postJsonData("clscenter", "gateways/sendcommand/tomac", data=payload)

		# On success we receive an empty body which is different from the other APIs
		if header_code == requests.codes.ok:
			return True

		return False

	def installKernel(self, update_url):

		payload = {}
		payload["mac"] = self.mac
		payload["pluginname"] = "system"
		payload["plugincall"] = "installKernel"
		payload["params"] = "{\"kernel_url\":\"%s\"}" % update_url

		(json, header_code) = self.center.postJsonData("clscenter", "gateways/sendcommand/tomac", data=payload)

		# On success we receive an empty body which is different from the other APIs
		if header_code == requests.codes.ok:
			return True

		return False
