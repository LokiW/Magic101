import os
import yaml

from event_handler.events import Event


event_dir_pathname = "/events"
excluded_files = "event_format_example.yaml"

def load_event_yamls():
	event_map = {}
	root_dir = os.getcwd() + event_dir_pathname
	for filepath in os.listdir(root_dir):
		if filepath in excluded_files or not filepath.endswith(".yaml"):
			print("skipping file " + filepath)
		else:
			print("loading events in "+ filepath)
			with open(root_dir + "/" + filepath, 'r') as file:
				raw_events = yaml.safe_load_all(file)
				for e in raw_events:
					if verify_event_yaml(e):
						event_name = e['event']['name']
						if event_name in event_map:
							if event_map[event_name].is_initialized:
								print("event "+event_name+"may be a duplicate, event already inloaded, skipping loading.")
							else:
								event_map[event_name].update(e['event'], event_map)
						else:
							event_map[event_name] = Event(event=e['event'], event_map=event_map)
	return event_map


def verify_event_yaml(e_yaml):
	"""
	event:
  name: ""
  prereqs: [[]]
  description: ""
  options:
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
		print("event yaml invalid, no 'event' header, skipping event: "+str(e_yaml))

		return False
	e = e_yaml["event"]
	if "name" not in e:
		print("event yaml invalid, no 'name', skipping event: "+str(e_yaml))
		return False
	event_name = e_yaml["event"]["name"]
	if "prereqs" not in e:
		print("event yaml invalid, no 'prereqs', skipping event: "+event_name)
		return False
	if "description" not in e:
		print("event yaml invalid, no 'description', skipping event: "+event_name)
		return False
	if "options" not in e:
		print("event yaml invalid, no 'options', skipping event: "+event_name)
		return False
	options = e["options"]
	for option in e["options"]:
		if "text" not in option:
			print("event yaml invalid, 'options' has no text, skipping event: "+event_name)
		o_text = option["text"]
		if "effort_cost" not in option or "prereqs" not in option:
			print("event yaml invalid, 'option' "+o_text+" incorrect, skipping event: "+event_name)
			return False
		if "spell_event" not in option and "next_events" not in option:
			print("event yaml invalid, 'option' "+o_text+" incorrect (must have spell_event or next_events), skipping event: "+event_name)
			return False
		if "spell_event" in option and "next_events" in option:
			print("event yaml invalid, 'option' "+o_text+" incorrect (must not have both spell_event and next_events), skipping event: "+event_name)
			return False

	return True
