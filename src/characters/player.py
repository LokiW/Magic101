import json
from error_handler import Error
from game_state.inventory import Inventory, Item

class Player():
	def __init__(self, firstname="", lastname="", nickname="", inventory={}):
		self.first_name = firstname
		self.last_name = lastname
		self.nickname = ""
		self.inventory = Inventory(inventory)

		self.traits = {}
		# Set default traits (can be overriden)
		self.traits['family_wealth'] = "mid"
		self.traits['magical_heritage_p1'] = "unknown"
		self.traits['magical_heritage_p2'] = "unknown"
		self.traits['magical_upbringing'] = False



	@property
	def name(self):
		return self.first_name+" "+self.last_name

	def load(self, reprd):
		self.first_name = reprd['first_name']
		self.last_name = reprd['last_name']
		self.nickname = reprd['nickname']

		self.inventory = Inventory()
		self.inventory.load(json.loads(reprd['inventory']))

		self.traits = json.loads(reprd['traits'])


	def __repr__(self):
		reprd = {}
		reprd['first_name'] = self.first_name
		reprd['last_name'] = self.last_name
		reprd['nickname'] = self.nickname
		reprd['inventory'] = self.inventory.__repr__()
		reprd['traits'] = json.dumps(self.traits)

		return json.dumps(reprd)
