class Item:
	def __init__(self, name, short, skill_bonus, will_bonus):
		self.name = name
		self.short = short
		# note in the main program we have already checked if skill and will values are valid data-types
		# we have also already converted the argument into a int value so that doesn't need to be done in the constructor
		self.skill_bonus = skill_bonus
		self.will_bonus = will_bonus

	def __repr__(self):
		return 'name: {}, short: {}, skill_bonus: {}, will_bonus: {}'.format(self.name, self.short, self.skill_bonus, self.will_bonus)

	def get_name(self):
		'''Returns an item's name.'''
		return self.name

	def get_short(self):
		'''Returns an item's short name.'''
		return self.short

	def get_info(self):
		'''Prints information about the item.'''
		# formatted according to how it will be called as per the CHECK command
		print('\n{}\nGrants a bonus of {} to SKILL.\nGrants a bonus of {} to WILL.\n'.format(self.name, self.skill_bonus, self.will_bonus))

	def get_skill(self):
		'''Returns an item's skill bonus.'''
		return self.skill_bonus

	def get_will(self):
		'''Returns an item's will bonus.'''
		return self.will_bonus


