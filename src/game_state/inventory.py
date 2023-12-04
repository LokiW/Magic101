import json



"""
if there is something that is plausibly caused by multiple different attributes, it should get it's own summary attribute
		aka an attribute like 'functional' should exist as the opposite of all of broken, cursed, malfunctioning

If images ever exist, instead of storing an image per item, images will have attribute tags and when figuring out what to display,
check the image tags and whichever image is closest to the item is used. 
e.g. if an image has the wand attribute wands select that image unless there is an image with a wand attribue and another attribute they have.
"""
class Item():
	def __init__(self, display_name, quantity=1, attributes=[]):
		self.display_name = display_name
		self.quantity = quantity
		self.attributes = attributes

	def add_attribute(self, attribute):
		self.attributes.add(attribute)

	def remove_attribute(self, attribute):
		self.attribute.remove(attribute)

	def has_attribute(self, attribute):
		return attribute in self.attributes

	def load(repr_dict):
		return Item(repr_dict['display_name'], repr_dict['quantity'], json.loads(repr_dict['attributes']))

	def __repr__(self):
		reprd = {}
		reprd['display_name'] = self.display_name
		reprd['quantity'] = self.quantity
		reprd['attributes'] = self.attributes
		return json.dumps(reprd)


class Inventory():
	def __init__(self, items={}):
		self.items = items

	def add_item(self, name, display_name='', quantity=1, attributes=[]):
		if not display_name:
			display_name = name
		self.items[name] = Item(display_name, quantity, attributes)

	def set_quantity(self, name, quantity=1):
		if name not in self.items:
			self.add_item(name, quantity)
		else:
			self.items[name].quantity = quantity

	def add_quantity(self, name, quantity):
		if name in self.items:
			self.items[name].quantity += quantity

	def subtract_quantity(self, name, quantity):
		self.add_inventory_quantity(name, -1*quantity)

	def has_quantity(self, name, quantity):
		if name not in self.items:
			# no item, only return true if quantity is 0
			return quantity == 0

		if quantity and self.items[name].quantity <= quantity:
			return True

		if not quantity and not self.items[name].quantity:
			return True

	def insufficient_quantity(self, name, quantity):
		return name not in self.items or self.items[name].quantity < quantity

	def add_attribute(self, name, attribute):
		if name in self.items:
			self.items[name].attributes.add(attribute)

	def remove_attribute(self, name, attribute):
		if name in self.items and attribute in self.items[name].attributes:
			self.items[name].attributes.remove(attribute)

	def has_attribute(self, name, attribute):
		if name not in self.items:
			return False
		return self.items[name].has_attribute(attribute)

	def __repr__(self):
		reprd = []
		for item in self.items:
			reprd.add(item.__repr__())
		return json.dumps(reprd)
	
