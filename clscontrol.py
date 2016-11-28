#!/usr/bin/env python
import argparse
import logging
from sys import exit
from cls.cls import CLSCenter

import logging

# These two lines enable debugging at httplib level (requests->urllib3->http.client)
# You will see the REQUEST, including HEADERS and DATA, and RESPONSE with HEADERS but without DATA.
# The only thing missing will be the response.body which is not logged.
#try:
#    import http.client as http_client
#except ImportError:
#    # Python 2
#    import httplib as http_client
#http_client.HTTPConnection.debuglevel = 1


# You must initialize logging, otherwise you'll not see debug output.
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True


if True:
	parser = argparse.ArgumentParser()

	# First is the command
	parser.add_argument("command", help="command to run")

	# Login Information
	parser.add_argument("-U", "--url", help="URL of the CLS Center", required=True)
	parser.add_argument("-u", "--user", help="username to access the CLS Center")
	parser.add_argument("-p", "--pass", dest="password", help="password to access the CLS Center")
	parser.add_argument("-P", "--pwd-file", dest="password_file", help="Configuration for username and password. This avoids passing sensible information using the shell")

	parser.add_argument("-n", "--name", help="name of the swichting point")
	parser.add_argument("-v", "--value", help="value to set")

	parser.add_argument("-m", "--mac", help="MAC address of the CLS-Module to use")
	parser.add_argument("--firmware", dest="firmware_uri", help="Firmware URL to install")
	parser.add_argument("--kernel", dest="kernel_uri", help="Kernel URL to install")

	args = parser.parse_args()
	

	password = args.password

	# Check if we have a configuration
	if args.password_file is not None:
		with open(args.password_file, "r") as f:
			try:
				password = f.read()
			except:
				print "Password could not be read from file"
				exit(1)

	# Try to login
	try:
		clsCenter = CLSCenter(args.url, args.user, password)
	except:
		print "Login to the cls center failed"
		exit(10)

	# Check for our commands:
	if args.command == "switch":
		if args.name is None or args.value is None:
			print "Neither name or value must be empty"
			exit(1)

		sw = clsCenter.getSwitchingPoint(args.name)
		print "Switched to value %d" % sw.switch(args.value)

	elif args.command == "status":
		if args.name is None:
			print "Need a name to query"
			exit(1)

		sw = clsCenter.getSwitchingPoint(args.name)
		print sw.getInformationDisplay

	elif args.command == "installFirmware":
		if args.mac is None or args.firmware_uri is None:
			print "Need a MAC to query"
			exit(1)

		module = clsCenter.getModule(args.mac)
		if module.installFirmware(args.firmware_uri):
			print "Command sent"
		else:
			print "Command not sent"

	elif args.command == "installKernel":
		if args.mac is None or args.kernel_uri is None:
			print "Need a MAC to query"
			exit(1)

		module = clsCenter.getModule(args.mac)
		if module.installKernel(args.kernel_uri):
			print "Command sent"
		else:
			print "Command not sent"

	else:
		print "Unknown command"
