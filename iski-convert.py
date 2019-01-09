#!/usr/bin/python
# coding=UTF-8

"""
Convert html saved from iSki tracker website to gpx format to import
any application or service such QLandkarteGT, Endomondo, etc.
Need to install the following packages:
$ pip install pytz
$ pip install tzlocal
Usage:
$ iski-convert.py <input-file>
Background:
There is no export function on iSki tracker website, but the html source
contains the date, coordinates, profile in different format. This script 
converts it to gpx that is a common GPS data format for software 
applications.
The script use the locale timezone and convert the dates to UTC, because
the GPS format defines date in Coordinated Universal Time (UTC) using 
ISO 8601 format. The Z at the end of the dates is the zone designator for 
the zero UTC offset. 
"""

import sys
import re
from datetime import datetime, timedelta, date, time

import pytz # $ pip install pytz
from tzlocal import get_localzone # $ pip install tzlocal

import locale

def parsecoordinates(line):
	# new google.maps.LatLng(46.68102, 13.89978)
	coordinates = []
	pattern = re.compile(r"LatLng\((\d+\.\d+),\ (\d+\.\d+)\)")
	for m in re.finditer(pattern, line):	
		pair = (float(m.group(1)), float(m.group(2)))
		coordinates.append(pair)
	return coordinates

def parseprofile(line, basedate):
	# {"x":46211799.99995232,"y":1435.0,"chartDataIndex":0}
	profile = []
	pattern = re.compile(r"\"x\"\:(\d+\.\d+)\,\"y\"\:(\d+\.\d+)")
	for m in re.finditer(pattern, line):	
		pair = (toisoformat(float(m.group(1)), basedate), float(m.group(2)))
		profile.append(pair)
	return profile

def toisoformat(f, basedate):
	local_tz = get_localzone()
	d = datetime(basedate.year, basedate.month, basedate.day, tzinfo = local_tz)
	d = d + timedelta(milliseconds = f)
	d = d.astimezone(pytz.utc)
	return d.strftime("%Y-%m-%dT%H:%M:%SZ")

def parsebasedate(line):
	d = re.search(r"ski-track of (.+) in", line).group(1)
	loc = locale.getlocale()
	locale.setlocale(locale.LC_TIME, "en_US.utf8")
	basedate = datetime.strptime(d, "%b. %d,%Y")
	locale.setlocale(locale.LC_TIME, loc)
	return basedate

if len(sys.argv) != 2:
	print "Usage: iski-convert.py <input-file>"
	exit()

f = open(sys.argv[1], 'r')
state = None
for line in f:
	if state == "DAY":
		basedate = parsebasedate(line)
		state = None
	if """<meta property="og:title""" in line:
		basedate = parsebasedate(line)
	if line.strip().find("new google.maps.LatLng(") >= 0:
		coordinates = parsecoordinates(line.strip())
	if line.strip().find("data: ") >= 0:
		profile = parseprofile(line.strip(), basedate)



g = open('out.gpx', 'w')

try:
	with g as file:
		g.write ("<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\" ?>\n"
			"\n"
			"<gpx xmlns=\"http://www.topografix.com/GPX/1/1\" creator=\"byHand\" version=\"1.1\"\n"
			"xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\n"
			"xsi:schemaLocation=\"http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd\">\n"
			"<trk>\n"
			"<trkseg>\n")

		for coordinate,elevation in zip(coordinates, profile):
			g.write ("\n"
					"<trkpt lon=\"%f\" lat=\"%f\">\n"
					"<ele>%f</ele>\n"
					"<time>%s</time>\n"
					"</trkpt>\n" % (coordinate[1], coordinate[0], elevation[1], elevation[0]))

		g.write ("\n"
			"</trkseg>\n"
			"</trk>\n"
		"</gpx>\n")
except:
	print("unable to open file")
	raise
