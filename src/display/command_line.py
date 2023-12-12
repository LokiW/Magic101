import os
import re
from error_handler import Error

RETURN_EVENT = "return_event"


def display_event(event, game_state):
	os.system('clear')
	if event.style == "user_input_event":
		return display_user_input_event(event, game_state)
	elif event.style == "spell_event":
		return display_spell_event(event, game_state)
	else:
		return display_default_event(event, game_state)

def display_default_event(event, game_state):
	display_text = insert_data_into_text(event.desc, game_state)
	print(display_text)
	game_state.previous_events.add(event.name)

	op_num = 1
	op_choice = {}
	for option in event.options:
		if option and option.text and option.prereqs.meets_prereqs(game_state):
			op_choice[op_num] = option
			print("%d: %s" % (op_num, option.text))
			op_num += 1

	def output(selection):
		option = op_choice[selection]
		if option.has_effects:
			option.effects.execute_effects(game_state)
		next_event, effects = option.get_next_event(game_state)
		effects.execute_effects(game_state)
		if next_event.name == RETURN_EVENT:
			next_event = game_state.return_events.pop()
		game_state.current_event = next_event

	# valid input options and func to call with input
	return op_choice.keys(), output


def display_menu(game_state):
	os.system('clear')
	print("Menu")
	print("Continue Game: c / continue ")
	print("Save Game: s / save")
	#TODO more options (e.g. see inventory or progress)
	print("quit to Quit\n")
	quit_choice = {"q", "quit", "Q"}
	continue_choice = {"c", "cont", "contiue", "C"}
	save_choice = {"s", "S", "save"} 

	def output(selection):
		if selection in quit_choice:
			game_state.ready = False
		elif selection in continue_choice:
			game_state.ready = True
		elif selection in save_choice:
			game_state.save()

	menu_choice = quit_choice | continue_choice | save_choice
	return menu_choice, output



def display_user_input_event(event, game_state):
	display_text = insert_data_into_text(event.desc, game_state)
	print(display_text)
	game_state.previous_events.add(event.name)

	def output(user_input):
		game_state.last_user_input = user_input
		op_choice = (-1, None)
		for option in event.options:
			if option and option.prereqs.meets_prereqs(game_state):
				if option.priority > op_choice[0]:
					op_choice = (option.priority, option)
		option = op_choice[1]
		if not option:
			Error.logln("No valid next event after user input event: "+event.name)
			return
		if option.has_effects:
			option.effects.execute_effects(game_state)
		next_event, effects = option.get_next_event(game_state)
		effects.execute_effects(game_state)
		if next_event.name == RETURN_EVENT:
			next_event = game_state.return_events.pop()
		game_state.current_event = next_event

	return {}, output


def display_spell_event(event, game_state):
	#TODO
	return


def display_inventory(game_state):
	os.system('clear')
	print("Inventory: \n")
	for name, item in game_state.player.inventory.items.items():
		display_name = item.display_name if item.display_name else name
		print(str(item.quantity)+"    "+display_name)

	print("\n\nPress enter to continue")
	def output(selection):
		return

	return {}, output


def insert_data_into_text(text, game_state):
	# replace instances of <<val>> with value of game_state.val in given text
	to_replace = re.findall(r'<<[^<]*>>', text)
	output = text
	for replacement in to_replace:
		replace_code = replacement[2:-2]
		replace_val = ""
		try:
			#replace_val = game_state.get_value(replace_code)
			replace_val = str(eval("game_state."+replace_code))
		except Exception as e:
			Error.logln("could not replace variable in given text "+text+" due to "+str(e))
		output = output.replace(replacement, replace_val)
	return output
