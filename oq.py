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

# some protocol definitions
methods = ["summary","details","bandwidth","weights","clients","uptime"]
reqparm = ["type","running","search","lookup","country","as","flag",
           "first_seen_days","last_seen_days","contact","fields","order",
           "offset","limit"]

# Query the database.
# returns a error/success code and the object used by requests
def onionoo_get(options):
	# Produce the url to use for the query
	u = "https://onionoo.torproject.org/"
	if options.has_key("method") == False:
		return (-1,"","")
	u += options["method"]+"?"
	p = reqparm
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

# Write me
def history(obj):
	print "yay"

# holy shit
# the linux kernel wouldn't accept this.
# md is the parsed json structure for what we are parsing
# I need to make this more readable....
# string, array, bool, number(tbd), object
def onionoo_parse(res,method):
	d = json.loads(res)
	md = json.load(file("json/"+method+".json"))
	mk = md.keys()
	for i in range(0,len(md)):
		for j in range(0,len(d[mk[i]])):
			u = d[mk[i]][j]
			for l in range(0,len(md[mk[i]])):
				if u.has_key(md[mk[i]][l]["field_n"]):
					text = md[mk[i]][l]["name"]
					dtype = md[mk[i]][l]["type"]
					citem = u[md[mk[i]][l]["field_n"]]
					if dtype == "string":
						print text+" : "+citem
					if dtype == "array_str":
						ct = ""
						for t in range(0,len(citem)):
							ct += citem[t]+" "
						print text+": "+ct
					if dtype == "bool":
						print text+": "+str(citem)
					if dtype == "number":
						print text+": "+str(citem)
			print ""

if(len(sys.argv) == 1):
	print "You need a search query"
	exit(1)

# argument parsing. to be done
argop = ["-t","-r","-s","-l","-c",
	"-as","-flag","-firstseen","-lastseen",
	"-contact","-fields","-order","-offset","-limit"]


opt = {
		"method":"details",
		"search":sys.argv[1],
		}

q = onionoo_get(opt)
#print q[1].text
if q[0] == 0:
	onionoo_parse(q[1].text,opt["method"])
