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
					match = eval(func)
				except Exception as e:
					Error.logln("Invalid prereq: "+prereq+" failed with "+str(e))
					match = False
				if match:
					break
			if not match:
				return False
		return True



class Effects:
	def __init__(self, effects):
		self.effects = effects

	def execute_effects(self, game_state):
		for effect in self.effects:
			func = "game_state."+effect
			try:
				exec(func)
			except Exception as e:
				Error.logln("Unable to apply effect: "+effect)
				Error.logln(str(e))
