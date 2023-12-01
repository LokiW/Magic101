import os


def display_event(event, game_state):
	os.system('clear')
	print(event.name)
	print(event.desc)

	op_num = 1
	op_choice = {}
	for option in event.options:
		if option.prereqs.meets_prereqs(game_state):
			op_choice[op_num] = option
			print("%d: %s" % (op_num, option.text))
		op_num += 1

	line = int(input())
	while line not in op_choice:
		print("invalid option, please chose a number")
		line = int(input())
	
	print(op_choice[line])	
	game_state.current_event = op_choice[line].get_next_event(game_state)
	print(game_state.current_event.name)
