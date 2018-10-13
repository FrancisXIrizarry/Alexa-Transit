
import googlemaps
from datetime import datetime
import sys
import json
from pygments import highlight, lexers, formatters


def httpsFunctionCall(StartLoc, EndLoc, travelType):

	gmaps = googlemaps.Client(key='AIzaSyA1_wX9RiSvGhsrM8_JwFtcCeQ3b5LQfXM')

	# Geocoding an address
	#geocode_result = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')

	# Look up an address with reverse geocoding
	#reverse_geocode_result = gmaps.reverse_geocode((40.714224, -73.961452))

	# Request directions via public transit

	now = datetime.now()
	directions_result = gmaps.directions(StartLoc,
                                     EndLoc,
                                     mode=travelType,
                                     departure_time=now)
	#print(directions_result)
	formatted_json = json.dumps(directions_result, sort_keys=True, indent=4)
	#colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), 			 	 formatters.TerminalFormatter())
	print(formatted_json)

	return directions_result
