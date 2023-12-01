import os
import yaml
import json
import random
from characters.player import Player
from error_handler import Error


save_dir = "/save_files"
file_path = os.getcwd() + save_dir + "/"

class GameState:
	def __init__(self, player, current_event, current_location, characters, magic_system, seed, options=[]):
		self.player = player
		self.current_event = current_event
		self.current_location = current_location
		self.characters = characters
		self.magic_system = magic_system
		self.seed = seed
		self.rng = random.Random(seed)
		self.options = options
		self.ready = True

	def __repr__(self):
		reprd = {}
		reprd['player'] = self.player.__repr__()
		reprd['current_event_name'] = self.current_event.name
		reprd['seed'] = self.seed
		#TODO the rest
		return json.dumps(reprd)

	def save(self):
		if not os.path.exists(file_path):
			os.mkdir(file_path)
	
		self.save_file = open(file_path+self.player.name+"_"+self.seed+".yaml", "w")
		yaml.safe_dump(self.__repr__(), self.save_file)
		self.save_file.close()

	def load(file_name, event_map):
		save_file = open(file_path+file_name, "r")
		load_info = json.loads(yaml.safe_load(save_file))
		player_dict = json.loads(load_info['player'])
		player = Player(player_dict["name"])
		current_event = event_map[load_info['current_event_name']]
		current_location = None
		characters = None
		magic_system = None
		seed = load_info['seed']
		options = None
		return GameState(player, current_event, current_location, characters, magic_system, seed, options)
