import json
from error_handler import Error
from game_state.inventory import Inventory

class Player():
	def __init__(self, firstname="", lastname="", inventory={}):
		self.first_name = firstname
		self.last_name = lastname
		self.nickname = ""
		self.inventory = Inventory(inventory)

	@property
	def name(self):
		return self.first_name+" "+self.last_name

	def __repr__(self):
		reprd = {}
		reprd['name'] = self.name
		reprd['inventory'] = self.inventory.__repr__()
		return json.dumps(reprd)
