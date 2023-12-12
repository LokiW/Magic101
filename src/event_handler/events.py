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
		if "event_style" in event:
			self.style = event["event_style"]
		else:
			self.style = "default"

		self.desc = event["description"]

		self.options = []
		for option in event["options"]:
			self.options.append(Option(option, event_map))
		self.is_initialized = True


class Option:
	def __init__(self, option, event_map):
		self.text = option["text"]

		if "effort_cost" in option:
			self.effort = option["effort_cost"]
		if "priority" in option: # event styles for not user selected next events
			self.priority = option["priority"]

		self.has_effects = "effects" in option and option["effects"]
		if self.has_effects:
			self.effects = Effects(option["effects"])
		self.prereqs = Prereqs([[]]) if "prereqs" not in option else Prereqs(option["prereqs"])

		self.next_events = []
		for e in option["next_events"]:
			if e["event_name"] not in event_map:
				event_map[e["event_name"]] = Event(name=e["event_name"])

			ne_prereqs = Prereqs([[]]) if "prereqs" not in e else Prereqs(e["prereqs"])
			ne_effects = Effects([]) if "effects" not in e else Effects(e["effects"])
			ne = (e["weight"], ne_prereqs, ne_effects, event_map[e["event_name"]])
			self.next_events.append(ne)

	def get_next_event(self, game_state):
		# chance = weight / sum( all weights)
		total_weight = 0
		weight_tuples = []
		Error.logln("next events: "+str(len(self.next_events)))
		for weight, prereqs, effects, event in self.next_events:
			Error.logln("Evaluating next event option "+event.name)
			if not event.is_initialized:
				#TODO error handling
				Error.logln("Error: event %s is uninitialized" % (event.name))
				continue
			if prereqs.meets_prereqs(game_state):
				total_weight += weight
				weight_tuples.append((weight, event, effects))

		percent = game_state.rng.randrange(0,total_weight)
		current_weight = 0
		for weight, event, effects in weight_tuples:
			current_weight += weight
			if percent < current_weight: #TODO check for off by one
				return event, effects
