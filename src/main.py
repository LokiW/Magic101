from event_handler.load_events import load_event_yamls


def main():
	cont = True
	while(cont):
		print("Start New Game: s / start ")
		print("Load Existing Game: l / load")
		print("quit to Quit")

		line = str(input())
		if line.startswith(("s", "S")):
			new_game()
		elif line.startswith(("l", "L")):
			load_game()
		elif "q" in line or "quit" in line:
			cont = False
		else:
			print("Invalid Option, Try Again")


def new_game():
	load_event_yamls()



def load_game():
	print("option not available: not implemented")
	return


if __name__ == "__main__":
	main()
