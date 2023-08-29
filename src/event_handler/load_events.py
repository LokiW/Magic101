import os
import yaml

from event_handler.events import Event


event_map = {}
event_dir_pathname = "/events"
excluded_files = {"event_format_example.yaml"}

def load_event_yamls():
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
						event_map[e['event']['name']] = Event(e['event'])


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
		if "spell_event" not in option or "next_events" not in options:
			print("event yaml invalid, 'options' incorrect, skipping event: "+e_yaml)
			return False

	return True
