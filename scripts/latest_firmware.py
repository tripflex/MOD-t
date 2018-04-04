#!/bin/python2

# This script just reaches out to the New Matter server and asks what the latest firmware is.
# Since their page returns JSON we get the name of the firmware as well as the URL to it as result.
import re
import os.path
import urllib2
import base64
import gzip
import zlib
from StringIO import StringIO
from io import BytesIO

def make_requests():
	response = [None]
	responseText = None

	if(request_de_newmatter_com(response)):
		responseText = read_response(response[0])
		print responseText
		response[0].close()


def read_response(response):
	if response.info().get('Content-Encoding') == 'gzip':
		buf = StringIO(response.read())
		return gzip.GzipFile(fileobj=buf).read()

	elif response.info().get('Content-Encoding') == 'deflate':
		decompress = zlib.decompressobj(-zlib.MAX_WBITS)
		inflated = decompress.decompress(response.read())
		inflated += decompress.flush()
		return inflated

	return response.read()


def request_de_newmatter_com(response):
	response[0] = None

	try:
		req = urllib2.Request("https://de.newmatter.com/api/fw/racingmoon/version?v=2&sid=C14BUVBXBlNWUgRVBgQKCFNTBwUHBQMA")
		req.add_header("Authorization", "Basic NDVkMDJiZGU1NjhkNmQwMWJmNjM3ZmNmZWJjM2FjODU6OTkwMzZjZTQzZTZiNTk5ZTNhNDc2NTJjZjRiNTc3ZWUyNGQyOTI0NzIxNGU2M2UxM2UwZDQ0N2IwMzg4NzY3ZA==")
		req.add_header("User-Agent", "Mozilla 5.0 (MOD-t printer tool 1.4.2)")
		req.add_header("Content-Type", "application/json")
		req.add_header("Connection", "Keep-Alive")
		req.add_header("Accept-Encoding", "gzip, deflate")
		req.add_header("Accept-Language", "en-US,*")

		response[0] = urllib2.urlopen(req)

	except urllib2.URLError, e:
		if not hasattr(e, "code"):
			return False
		response[0] = e
	except:
		return False

	return True


make_requests()
