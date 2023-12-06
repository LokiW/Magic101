import os
import yaml

from event_handler.events import Event
from error_handler import Error


event_dir_pathname = "/events"
excluded_files = "event_format_example.yaml"

def load_event_yamls():
	event_map = {}
	root_dir = os.getcwd() + event_dir_pathname
	for filepath in os.listdir(root_dir):
		if filepath in excluded_files or not filepath.endswith(".yaml"):
			Error.logln("skipping file " + filepath)
		else:
			Error.logln("loading events in "+ filepath)
			with open(root_dir + "/" + filepath, 'r') as file:
				event_loader = yaml.safe_load_all(file)
				for raw_events in event_loader:
					for event in raw_events:
						e = raw_events[event]
						if verify_event_yaml(e):
							event_name = e['name']
							if event_name in event_map:
								if event_map[event_name].is_initialized:
									Error.logln("event "+event_name+"may be a duplicate, event already inloaded, skipping loading.")
								else:
									Error.logln("    updating event: "+event_name)
									event_map[event_name].update(e, event_map)
							else:
								Error.logln("    creating event: "+event_name)
								event_map[event_name] = Event(event=e, event_map=event_map)
	for name, event in event_map.items():
		if not event.is_initialized:
			Error.logln("References to Uninitialized Event: "+name)
	return event_map


def verify_event_yaml(e):
	"""
	event:
  name: ""
  prereqs: [[]]
  description: ""
  options:
    - text: ""
      effort_cost: 0
      effects: []
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
	if "name" not in e:
		Error.logln("event yaml invalid, no 'name', skipping event: "+str(e))
		return False
	event_name = e["name"]
	if "prereqs" not in e:
		Error.logln("event yaml invalid, no 'prereqs', skipping event: "+event_name)
		return False
	if "description" not in e:
		Error.logln("event yaml invalid, no 'description', skipping event: "+event_name)
		return False
	if "options" not in e:
		Error.logln("event yaml invalid, no 'options', skipping event: "+event_name)
		return False
	options = e["options"]
	for option in e["options"]:
		if "text" not in option:
			Error.logln("event yaml invalid, 'options' has no text, skipping event: "+event_name)
		o_text = option["text"]
		if "event_style" in e and e["event_style"] != "default":
			if e["event_style"] == "user_input_event" and "priority" not in option:
				Error.logln("event yaml invalid, 'option' "+o_text+" incorrect, user input events must have priority field skipping event: "+event_name)
				return False
		elif "effort_cost" not in option:
			Error.logln("event yaml invalid, 'option' "+o_text+" incorrect, default events must have effort_cost, skipping event: "+event_name)
			return False
		if "prereqs" not in option:
			Error.logln("event yaml invalid, 'option' "+o_text+" incorrect, no prereqs, skipping event: "+event_name)
			return False
		"""
		if "spell_event" not in option and "next_events" not in option:
			Error.logln("event yaml invalid, 'option' "+o_text+" incorrect (must have spell_event or next_events), skipping event: "+event_name)
			return False
		if "spell_event" in option and "next_events" in option:
			Error.logln("event yaml invalid, 'option' "+o_text+" incorrect (must not have both spell_event and next_events), skipping event: "+event_name)
			return False
		"""

	return True
