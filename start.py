
import googlemaps
from datetime import datetime

def httpsFunctionCall(StartLoc, EndLoc):

	gmaps = googlemaps.Client(key='AIzaSyA1_wX9RiSvGhsrM8_JwFtcCeQ3b5LQfXM')

	# Geocoding an address
	#geocode_result = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')

	# Look up an address with reverse geocoding
	#reverse_geocode_result = gmaps.reverse_geocode((40.714224, -73.961452))

	# Request directions via public transit

	now = datetime.now()
	directions_result = gmaps.directions(StartLoc,
                                     EndLoc,
                                     mode="transit",
                                     departure_time=now)
	print(directions_result)

	return directions_result

