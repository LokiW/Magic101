import json


class Location():
	def __init__(self, locations={}):
		self.locations = locations

	def set_location(self, location):
		self.locations = {location}

	def add(self, location):
		self.locations.add(location)

	def contains(self, location):
		return location in self.locations

	def remove(self, location):
		self.locations.remove(location)

	def load(reprd):
		return Location(set(reprd))

	def __repr__(self):
		return json.dumps(list(self.locations))
