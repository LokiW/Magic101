import os
from error_handler import Error


def display_event(event, game_state):
	os.system('clear')
	print(event.desc)

	op_num = 1
	op_choice = {}
	for option in event.options:
		if option and option.text and option.prereqs.meets_prereqs(game_state):
			op_choice[op_num] = option
			print("%d: %s" % (op_num, option.text))
			op_num += 1

	def output(selection):
		option = op_choice[selection]
		Error.log("Has effect:   ")
		Error.logln(str(option.has_effects))
		if option.has_effects:
			option.effects.execute_effects(game_state)
		game_state.current_event = option.get_next_event(game_state)

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
