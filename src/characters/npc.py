

class npc(Character):
	def __init__(self, firstname="", lastname="", nickname="", inventory={}, traits={}, physical_description="", hair="", eyes="", location=None, opinion=None):
		super().__init__()
		self.opinion = opinion

	def set_defaults(self, default):
		super().set_defaults(default)
		self.opinion = self.opinion if self.opinion not None else default.opinion

	def load(self, reprd):
		super.load(reprd)
		self.opinion = reprd["opinion"]

	def __repr__(self):
		reprd = super().__repr__()
		reprd["opinion"] = self.opinion
		return reprd
