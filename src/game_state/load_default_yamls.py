import yaml
import os
from error_handler import Error


default_data_pathname = "/default_state"
root_dir = os.getcwd() + default_data_pathname
excluded_option_files = []

def load_options():
	options = {}
	op_dir = root_dir+"/options/"
	for filepath in os.listdir(op_dir):
		if filepath in excluded_option_files or not filepath.endswith(".yaml"):
			Error.logln("skipping option file " + filepath)
		else:
			Error.logln("loading options in "+ filepath)
			with open(op_dir+filepath, 'r') as file:
				options.update(yaml.safe_load(file)["options"])
	return options


def load_seed_data(seed):
	options = {}
	op_dir = root_dir+"/seed/"
	for filepath in os.listdir(op_dir):
		if filepath in excluded_option_files or not filepath.endswith(".yaml"):
			Error.logln("skipping seed file " + filepath)
		else:
			Error.logln("loading seed data in "+ filepath)
			with open(op_dir+filepath, 'r') as file:
				seed.load_data(filepath, yaml.safe_load(file))


"""
	with open(root_dir + "/" + "options.yaml", "r") as file:
		return yaml.safe_load(file)["options"]
"""
