
def process_prereqs(prereqs):
	return [[]]


def process_options(options):


class Event:
	def __init__(self, event):
		self.name = event["name"]
		self.prereqs = process_prereqs(event["prereqs"])
		self.desc = event["description"]
		self.options = process_options(event["options"])



class Option:
	def __init__(self, option, event_map):
		self.text = option["text"]
		self.effort = option["effort_cost"]
		self.has_effects = "effects" in option and not option["effects"]
		if self.has_effects:
			self.effects = process_effects(option["effects"])

		self.is_spell_option = "spell_event" in option
		if self.is_spell_option:
			self.max_casting = option["max_casting"]
			self.spell_to_event = {}
			for e in option["spell_event"]:
				if e["event_name"] not in event_map:
						event_map[e["event_name"]] = Event(name=e["event_name"])
				for spell in e["spell_triggers"]:
					self.spell_to_event[spell] = event_map[e["event_name"]]
				

		else:
"""  options
    - text: ""
      effort_cost: 0
      effects: [[]]
      prereqs: [[]]
      next_events:
        - event_name: ""
          chance: 50
        - event_name: ""
          chance: 50
    - text: ""
      effort_cost: 0
      prereqs: [[]]
      next_events: 
        - event_name: ""
          chance: 100
    - text: ""
      effort_cost: 0
      prereqs: [[]]
      max_casting: 0
      spell_event:
        - event_name: ""
          spell_triggers: []
	"""
	if "event" not in e_yaml:
		print("event yaml invalid, no 'event' header, skipping event: "+e_yaml)
		return False
	e = e_yaml["event"]
	if "name" not in e:
		print("event yaml invalid, no 'name', skipping event: "+e_yaml)
		return False
	if "prereqs" not in e:
		print("event yaml invalid, no 'prereqs', skipping event: "+e_yaml)
		return False
	if "description" not in e:
		print("event yaml invalid, no 'description', skipping event: "+e_yaml)
		return False
	if "options" not in e:
		print("event yaml invalid, no 'options', skipping event: "+e_yaml)
		return False
	options = e["options"]
	for option in e["options"]:
		if "text" not in option or "effort_cost" not in option or "prereqs" not in option:
			print("event yaml invalid, 'options' incorrect, skipping event: "+e_yaml)
			return False
