#!/usr/bin/env python

# based of loads of my old code.
# needs to be cleaned up quite a bit.
# and also needs support for more of the methods.

# For some objects, GNUPLOT or making a something that displays the bandwidth usage like 
# ARM would be ideal.

import json
import requests
import gzip
import sys

# we define the valid methods in a JSON file.
methods = json.load(file("json/methods.json"))
summary = json.load(file("json/summary.json"))

# Query the database.
# returns a error/success code and the object used by requests
def onionoo_get(options):
	# Produce the url to use for the query
	u = "https://onionoo.torproject.org/"
	if options.has_key("method") == False:
		return (-1,"","")
	u += options["method"]+"?"
	p = methods["parameters"]
	for i in range(0,len(p)):
		if options.has_key(p[i]) == True:
			u += p[i]+"="+options[p[i]]+"&"
	if u[-1] == "&":
		u = u[0:-1]
	# ready to send request now
	if options.has_key("Last-Modified") == True:
		headers = { "If-Modified-Since":options["Last-Modified"]}
	else:
		headers = {}
	r = requests.get(u,headers=headers)
	if r.status_code != 200:
		return (-1,r)
	return (0,r)

def onionoo_parse(options,res):
	if options["method"] == "summary":
		onionoo_summary(res)

def onionoo_summary(res):
	d = json.loads(res)
	for i in range(0,len(summary.keys())):
		for j in range(0,len(d[summary.keys()[i]])):
			v = summary[summary.keys()[i]].keys()
			for l in range(0,len(v)):
				print summary[summary.keys()[i]][v[l]]+":"
				print d[summary.keys()[i]][j][v[l]] #sorry
			print ""
	

if(len(sys.argv) == 1):
	print "You need a search query"
	exit(1)

opt = {
		"method":"summary",
		"search":sys.argv[1],
		"type":"bridge"
		}

q = onionoo_get(opt)
if q[0] == 0:
	onionoo_parse(opt,q[1].text)
