import json
from error_handler import Error
from game_state.inventory import Inventory, Item
from game_state.location import Location

class Character():
	def __init__(self, firstname="", lastname="", nickname="", inventory=None, traits={}, physical_description="", hair="", eyes="", location=Location()):
		self.first_name = firstname
		self.last_name = lastname
		self.nickname = nickname
		self.inventory = inventory if inventory else Inventory()

		self.traits = {}

		self.physical_description = physical_description
		self.hair = hair
		self.eyes = eyes
		self.location = location

	@property
	def name(self):
		return self.first_name+" "+self.last_name

	def set_defaults(self, default):
		self.first_name = self.first_name if self.first_name else default.first_name
		self.last_name = self.last_name if self.last_name else default.last_name
		self.nickname = self.nickname if self.nickname else default.nickname
		self.inventory = self.inventory.set_default(default.inventory)

		self.traits = {**default.traits, **self.traits}
		self.physical_description = self.physical_description if self.physical_description else default.physical_description
		self.hair = self.hair if self.hair else default.hair
		self.eyes = self.eyes if self.eyes else default.eyes
		self.location = self.location if self.location else default.location


	def load(reprd):
		first_name = reprd['first_name']
		last_name = reprd['last_name']
		nickname = reprd['nickname']

		inventory = Inventory()
		inventory.load(json.loads(reprd['inventory']))

		traits = json.loads(reprd['traits'])

		physical_description = reprd['physical_description']
		hair = reprd['hair']
		eyes = reprd['eyes']
		location = Location.load(reprd['location'])

		return Character(firstname=first_name, lastname=last_name, nickname=nickname, inventory=inventory, traits=traits, physical_description=physical_description, hair=hair, eyes=eyes, location=location)

	def __repr__(self):
		reprd = {}
		reprd['first_name'] = self.first_name
		reprd['last_name'] = self.last_name
		reprd['nickname'] = self.nickname
		reprd['inventory'] = self.inventory.__repr__()
		reprd['traits'] = json.dumps(self.traits)
		reprd['physical_description'] = self.physical_description
		reprd['hair'] = self.hair
		reprd['eyes'] = self.eyes
		reprd['location'] = self.location.__repr__()

		return json.dumps(reprd)


	def get_from_yaml(seed, ch_yaml):
		first_name = seed.replace_values(ch_yaml["first_name"]) if "first_name" in ch_yaml else ""
		last_name = seed.replace_values(ch_yaml["last_name"]) if "last_name" in ch_yaml else ""
		nickname = seed.replace_values(ch_yaml["nickname"]) if "nickname" in ch_yaml else ""
		phys_desc = seed.replace_values(ch_yaml["physical_description"]) if "physical_description" in ch_yaml else ""
		hair = seed.replace_values(ch_yaml["hair"]) if "hair" in ch_yaml else ""
		eyes = seed.replace_values(ch_yaml["eyes"]) if "eyes" in ch_yaml else ""
		traits = {}
		if "traits" in ch_yaml:
			for name, val in ch_yaml["traits"].items():
				if isinstance(val, str):
					traits[name] = seed.replace_values(val)
				else:
					traits[name] = val

		inventory = {}
		if "inventory" in ch_yaml:
			inventory = Inventory.get_from_yaml(seed, ch_yaml["inventory"])

		location = set()
		if "location" in ch_yaml:
			location.update(ch_yaml["location"])

		return Character(firstname=first_name, lastname=last_name, nickname=nickname, inventory=inventory, traits=traits, physical_description=phys_desc, hair=hair, eyes=eyes, location=location)

