import yaml
import os
from error_handler import Error
from characters.character import Character


default_data_pathname = "/default_state"
root_dir = os.getcwd() + default_data_pathname
excluded_option_files = []

def load_characters(seed):
	characters = {}
	op_dir = root_dir+"/characters/"
	for filepath in os.listdir(op_dir):
		if filepath in excluded_option_files or not filepath.endswith(".yaml"):
			Error.logln("skipping character file " + filepath)
		else:
			Error.logln("loading characters in "+ filepath)
			with open(op_dir+filepath, 'r') as file:
				char_loader = yaml.safe_load_all(file)
				for raw_characters in char_loader:
					for c in raw_characters:
						Error.logln("Loading Character: "+str(c))
						ch_yaml = raw_characters[c]

						character = Character.get_from_yaml(seed, ch_yaml)
						if ch_yaml["type"] not in characters:
							characters[ch_yaml["type"]] = {}

						characters[ch_yaml["type"]][ch_yaml["id"]] = character
	return characters
