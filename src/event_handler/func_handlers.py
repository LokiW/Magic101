from error_handler import Error


class Prereqs:
	def __init__(self, prereqs):
		self.prereqs = prereqs 

	def meets_prereqs(self, game_state):
		#One prereq from each list in the top level list must be true
		# aka [[a or b] and [c or d]]
		for prereq_list in self.prereqs:
			match = True
			for prereq in prereq_list:
				func = "game_state."+prereq
				try:
					match = exec(func)
				except:
					Error.logln("Invalid prereq: "+prereq)

				if match:
					break
			if not match:
				return False
		return True



class Effects:
	def __init__(self, effects):
		#TODO
		self.effects = [[]]

	def execute_effects(self, game_state):
		#TODO
		num_effect_lists = len(self.effects)
