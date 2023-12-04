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
	def __init__(self, player, current_event, current_location, characters, magic_system, seed, options=[], prev_events=set(), last_input=""):
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


	def __repr__(self):
		reprd = {}
		reprd['player'] = self.player.__repr__()
		reprd['current_location'] = self.current_location.__repr__()
		reprd['current_event_name'] = self.current_event.name
		reprd['seed'] = self.seed
		reprd['last_user_input'] = self.last_user_input
		reprd['previous_events'] = json.dumps(list(self.previous_events))
		#TODO the rest
		return json.dumps(reprd)

	def save(self):
		if not os.path.exists(file_path):
			os.mkdir(file_path)
	
		self.save_file = open(file_path+self.player.name+"_"+self.seed+".yaml", "w")
		yaml.safe_dump(self.__repr__(), self.save_file)
		self.save_file.close()

	def load(file_name, event_map, default_options):
		save_file = open(file_path+file_name, "r")

		load_info = json.loads(yaml.safe_load(save_file))

		player_dict = json.loads(load_info['player'])
		inventory = []
		for item in json.loads(player_dict['inventory']):
			inventory.append(Item.load(item))
		player = Player(player_dict["name"], inventory)

		current_event = event_map[load_info['current_event_name']]

		current_location = Location(set(json.loads(load_info['current_location'])))

		previous_events = set()
		for p_event in json.loads(load_info['previous_events']):
			previous_events.add(p_event)

		last_user_input = load_info['last_user_input']

		characters = None
		magic_system = None
		seed = load_info['seed']
		# loaded options override any values in default options if in this order
		# options = {**default_options, **json.loads(load_info['options'])}
		options = default_options
		return GameState(player, current_event, current_location, characters, magic_system, seed, options, previous_events, last_user_input)
