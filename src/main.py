from event_handler.load_events import load_event_yamls
from display.command_line import display_event
from game_state import GameState


def main():
	cont = True
	while(cont):
		print("Start New Game: s / start ")
		print("Load Existing Game: l / load")
		print("quit to Quit\n")

		line = str(input())
		if line.startswith(("s", "S")):
			game_state = new_game()
			play(game_state)
		elif line.startswith(("l", "L")):
			load_game()
		elif "q" in line or "quit" in line:
			cont = False
		else:
			print("Invalid Option, Try Again")


def new_game():
	event_map = load_event_yamls()
	current_event = event_map["inciting_incident"]
	#TODO
	current_location = None 
	# TODO load characters
	characters = None
	# TODO generate magic system
	magic_system = None
	# choose player character
	#TODO
	player = None
	#TODO seed
	seed = "traditional"
	#TODO select starting options
	options = []
	
	return GameState(player, current_event, current_location, characters, magic_system, seed, options)


def load_game():
	print("option not available: not implemented")
	return


def play(game_state):
	# TODO how to exit game lol
	while True:
		display_event(game_state.current_event, game_state)


if __name__ == "__main__":
	main()
