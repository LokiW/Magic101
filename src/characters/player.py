import json

class Player():
	def __init__(self, name):
		self.name = name

	def __repr__(self):
		reprd = {}
		reprd['name'] = self.name
		return json.dumps(reprd)
