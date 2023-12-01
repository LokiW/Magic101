from event_handler.func_handlers import Prereqs, Effects
from error_handler import Error



class Event:
	def __init__(self, name="", event={}, event_map={}):
		if not event:
			self.name = name
			self.is_initialized = False
		else:
			self.update(event, event_map)

	def update(self, event, event_map):
		self.name = event["name"]
		self.prereqs = Prereqs(event["prereqs"])

		self.desc = event["description"]

		self.options = []
		for option in event["options"]:
			self.options.append(Option(option, event_map))
		self.is_initialized = True



class Option:
	def __init__(self, option, event_map):
		self.text = option["text"]
		self.effort = option["effort_cost"]
		self.has_effects = "effects" in option and not option["effects"]
		if self.has_effects:
			self.effects = Effects(option["effects"])
		self.prereqs = Prereqs(option["prereqs"])

		self.is_spell_option = "spell_event" in option
		if self.is_spell_option:
			self.max_casting = option["max_casting"]
			self.spell_to_event = {}
			for e in option["spell_event"]:
				if e["event_name"] not in event_map:
						event_map[e["event_name"]] = Event(name=e["event_name"])
				for spell in e["spell_triggers"]:
					self.spell_to_event[spell] = event_map[e["event_name"]]
		else: # next events weighted
			for e in option["next_events"]:
				self.next_events = []
				if e["event_name"] not in event_map:
					event_map[e["event_name"]] = Event(name=e["event_name"])
				self.next_events.append([e["chance"], event_map[e["event_name"]]])

	def get_next_event(self, game_state):
		percent = game_state.rng.randrange(0,99)
		current_chance = 0
		for event in self.next_events:
			if not event[1].is_initialized:
				#TODO error handling
				Error.logln("Error: event %s is uninitialized" % (event[1].name))
				continue
			current_chance += event[0]
			Error.logln(str(current_chance))
			if percent < current_chance: #TODO check for off by one
				return event[1]
