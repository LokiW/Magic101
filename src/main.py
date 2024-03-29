import os

from event_handler.load_events import load_event_yamls
from display.command_line import display_event
from display.command_line import display_menu
from display.command_line import display_inventory
from game_state.game_state import GameState
from game_state.load_default_yamls import load_options
from game_state.location import Location
from game_state.seed import Seed
from characters.character import Character
from characters.load_character_yamls import load_characters
from error_handler import Error


FIRST_EVENT = "character_select"
REREQUEST = "m@g!c_v@1u3_us3r_!nput"

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
	current_event = event_map[FIRST_EVENT]
	options = load_options()

	seed = Seed("traditional", True)

	# TODO load characters
	characters = load_characters(seed)

	# TODO generate magic system
	magic_system = None
	player = Character()
	player.location = Location({"start"})

	return GameState(player, current_event, characters, magic_system, seed, options)


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

	default_options = load_options()

	return GameState.load(file_map[selection], event_map, default_options)


def play(game_state):
	while game_state.ready:
		game_state.save()
		valid_inputs, state_change = display_event(game_state.current_event, game_state)
		user_input = process_input(game_state, valid_inputs)
		if user_input != REREQUEST:
			state_change(user_input)


def process_input(game_state, valid_inputs):
	#try:
	line = str(input())
	illegal_characters = "\"\'()[]{}"
	if any(c in illegal_characters for c in line):
		display_invalid()
		return process_input(game_state, valid_inputs)

	if not valid_inputs:
		#Get raw user input
		return line

	if line in {"m", "menu"}:
		menu_options, state_change = display_menu(game_state)
		selection = process_input(game_state, menu_options)
		state_change(selection)
		return REREQUEST

	if line in {"i", "inventory"}:
		inventory_options, state_change = display_inventory(game_state)
		selection = process_input(game_state, inventory_options)
		state_change(selection)
		return REREQUEST

	if valid_inputs and isinstance(list(valid_inputs)[0], int):
		try:
			int_line = int(line)
		except:
			display_invalid()
			return process_input(game_state, valid_inputs)
		if int_line in valid_inputs:
			return int(line)
	elif line in valid_inputs:
			return line

	display_invalid()
	return process_input(game_state, valid_inputs)


def display_invalid():
	print("invalid input, try again:")


if __name__ == "__main__":
	main()
