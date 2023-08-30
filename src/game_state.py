

class GameState:
	def __init__(self, player, current_event, current_location, characters, magic_system, seed):
		self.player = player
		self.current_event = current_event
		self.current_location = current_location
		self.characters = characters
		self.magic_system = magic_system
		self.seed = seed
