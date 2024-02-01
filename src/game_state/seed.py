import random
import time
import re
from error_handler import Error
from game_state.load_default_yamls import load_seed_data


class Seed():
	def __init__(self, seed_base, seed_further=False, suffix=""):
		self.seed = seed_base
		self.suffix = str(time.monotonic()) if seed_further else suffix
		self.default_values = {}
		self.rng = random.Random(self.seed+self.suffix)

		load_seed_data(self)

	def get_seed(self):
		return self.seed+self.suffix

	def __repr__(self):
		reprd = {}
		reprd["seed"] = self.seed
		reprd["suffix"] = self.suffix
		return reprd

	def load(se_yaml):
		return Seed(se_yaml["seed"], False, se_yaml["suffix"])

	def load_data(self, filename, se_yaml):
		if self.seed not in filename:
			return
		self.update(self.default_values, se_yaml)

	def update(self, existing, new):
		# isinstance doesnt work for subclassing, TODO is this problem?
		if not isinstance(new, type(existing)):
			Error.logln("Conflicting types found when loading seed data")
			return

		for name, val in new.items():
			if name not in existing:
				existing[name] = val
			elif isinstance(val, dict):
				self.update(existing[name], new[name])
			elif isinstance(val, list):
				existing[name] = list(set(existing[name])+set(val))
			elif isinstance(val, set):
				existing[name] = existing[name] + val

	def replace_values(self, text):
		# replace instances of <<val>> with value in default_values in given text
		to_replace = re.findall(r'<<[^<]*>>', text)
		output = text
		for replacement in to_replace:
			replace_lst = replacement[2:-2].split(".")
			replace_code = ""
			for word in replace_lst:
				replace_code += "['"+word+"']"
			try:
				replace_val = eval("self.default_values"+replace_code)
				if isinstance(replace_val, list) or isinstance(replace_val, set):
					replace_val = replace_val[self.rng.randrange(0,len(replace_val))]
				if not isinstance(replace_val, str):
					Error.logln("text requested replacement not specific enough: "+replacement+" "+str(replace_val))
				else:
					output = output.replace(replacement, replace_val)

			except Exception as e:
				Error.logln("could not replace variable in given text "+text+" due to "+str(e))
		return output

