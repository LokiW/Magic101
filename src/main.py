import os

from event_handler.load_events import load_event_yamls
from display.command_line import display_event
from game_state import GameState
from characters.player import Player
from error_handler import Error


def main():
	Error.reset()
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
			game_state = load_game()
			play(game_state)
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
	print("Enter Character Name:")
	player_name = str(input())
	player = Player(player_name)

	#TODO seed
	seed = "traditional"
	#TODO select starting options
	options = []
	
	return GameState(player, current_event, current_location, characters, magic_system, seed, options)


def load_game():
	print("Choose a save file:")
	root_dir = os.getcwd() + "/save_files"
	select_num = 1
	file_map = {}
	for filepath in os.listdir(root_dir):
		print(str(select_num)+": "+filepath)
		file_map[select_num] = filepath
		select_num += 1

	selection = int(input())
	while selection not in file_map:
		print("Please select a number for the file to load:")
		selection = int(input())
	event_map = load_event_yamls()
	return GameState.load(file_map[selection], event_map)


def play(game_state):
	# TODO how to exit game lol
	while True:
		display_event(game_state.current_event, game_state)
		game_state.save()


if __name__ == "__main__":
	main()
