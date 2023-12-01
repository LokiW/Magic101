import yaml
import os


default_data_pathname = "/default_state"
root_dir = os.getcwd() + default_data_pathname

def load_options():
	with open(root_dir + "/" + "options.yaml", "r") as file:
		return yaml.safe_load(file)["options"]
