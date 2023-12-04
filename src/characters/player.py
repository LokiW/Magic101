import json
from error_handler import Error
from game_state.inventory import Inventory

class Player():
	def __init__(self, name, inventory={}):
		self.name = name
		self.inventory = Inventory(inventory)

	def __repr__(self):
		reprd = {}
		reprd['name'] = self.name
		reprd['inventory'] = self.inventory.__repr__()
		return json.dumps(reprd)
