import os
import yaml
import json
import random
from characters.player import Player
from game_state.location import Location
from game_state.inventory import Item
from error_handler import Error


save_dir = "/save_files"
file_path = os.getcwd() + save_dir + "/"

class GameState:
	def __init__(self, player, current_event, current_location, characters, magic_system, seed, options=[], prev_events=set(), last_input="", return_events=[]):
		self.player = player
		self.current_event = current_event
		self.current_location = current_location
		self.previous_events = prev_events
		self.characters = characters
		self.magic_system = magic_system
		self.seed = seed
		self.rng = random.Random(seed)
		self.options = options
		self.ready = True
		self.last_user_input = last_input
		self.return_events = return_events


	"""
	method for events to assign values to gamestate when both values are in gamestate object
	"""
	def assign(self, attr1, attr2):
		to_set = self
		for val in attr1.split(".")[:-1]:
			to_set = getattr(to_set, val)

		to_get = self
		for val in attr2.split("."):
			to_get = getattr(to_get, val)

		if to_get == self:
			raise Exception("Invalid assignment, cannot assign with root game_state")

		setattr(to_set, attr1.split(".")[-1], to_get)

	def get_value(self, attr1):
		to_get = self
		for val in attr1.split("."):
			to_get = getattr(to_get, val)
		return to_get

	def clear_return_events(self):
		self.return_events = []

	def add_self_to_return_events(self):
		self.return_events.append(self.current_event)

	def __repr__(self):
		reprd = {}
		reprd['player'] = self.player.__repr__()
		reprd['current_location'] = self.current_location.__repr__()
		reprd['current_event_name'] = self.current_event.name
		reprd['seed'] = self.seed
		reprd['last_user_input'] = self.last_user_input
		reprd['previous_events'] = json.dumps(list(self.previous_events))
		reprd['return_events'] = []
		for r_event in self.return_events:
			reprd['return_events'].append(r_event.name)
		reprd['return_events'] = json.dumps(reprd['return_events'])
		reprd['options'] = json.dumps(self.options)
		#TODO the rest
		return json.dumps(reprd)

	def save(self):
		if not self.player.first_name or not self.player.last_name:
			Error.logln("Player uninitialized, skipping save")
			return

		if not os.path.exists(file_path):
			os.mkdir(file_path)
	
		self.save_file = open(file_path+self.player.name+"_"+self.seed+".yaml", "w")
		yaml.safe_dump(self.__repr__(), self.save_file)
		self.save_file.close()

	def load(file_name, event_map, default_options):
		save_file = open(file_path+file_name, "r")

		load_info = json.loads(yaml.safe_load(save_file))

		player = Player()
		player.load(json.loads(load_info['player']))

		current_event = event_map[load_info['current_event_name']]

		current_location = Location(set(json.loads(load_info['current_location'])))

		previous_events = set()
		for p_event in json.loads(load_info['previous_events']):
			previous_events.add(p_event)

		#TODO make sure stack order is preserved
		return_events = []
		for r_event in json.loads(load_info['return_events']):
			return_events.append(event_map[r_event])

		last_user_input = load_info['last_user_input']

		characters = None
		magic_system = None
		seed = load_info['seed']
		# loaded options override any values in default options if in this order
		options = {**default_options, **json.loads(load_info['options'])}
		# options = default_options
		return GameState(player, current_event, current_location, characters, magic_system, seed, options, previous_events, last_user_input, return_events)
