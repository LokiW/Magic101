from event_handler.func_handlers import Prereqs, Effects


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
				self.next_events.append({e["chance"], event_map[e["event_name"]]})

