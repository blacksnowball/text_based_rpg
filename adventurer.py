class Adventurer:
	def __init__(self):
		self.skill = 5
		self.will = 5
		self.inventory = []

	def __represent__(self):
		return 'Skill: {}, Will: {}, Inventory: {}'.format(self.skill, self.will, self.inventory)

	def get_inv(self):
		'''Returns the adventurer's inventory.'''
		return self.inventory

	def get_skill(self):
		'''Returns the adventurer's skill power.'''
		return self.skill

	def get_will(self):
		'''Returns the adventurer's will power.'''
		return self.will

	def take(self, item):
		'''Adds an item to the adventurer's inventory.'''
		self.inventory.append(item)

	def check_self(self):
		'''Shows adventurer stats and all item stats.'''
		
		request = input('Check what? ')
		request = request.upper()
		
		if request == 'ME':
			# show base skill/will values before being modified by each item's values
			print('\nYou are an adventurer, with a SKILL of {} and a WILL of {}.'.format(self.skill, self.will))
			print('You are carrying:\n')
			
			if len(self.inventory) == 0:
				print('Nothing.\n')
			
			# temporary values to find cumulative skill and will values after items considered
			modified_skill = self.skill
			modified_will = self.will
			
			# iterate through inventory, displaying relevant info and adding skill/will bonuses to temporary values
			# if inventory is empty, this looping block of code will not execute as the conditional is True (len is zero)
			i = 0
			while i < len(self.inventory):
				item = self.inventory[i]

				print(item.get_name())
				print('Grants a bonus of {} to SKILL.'.format(item.get_skill()))
				print('Grants a bonus of {} to WILL.\n'.format(item.get_will()))

				modified_skill += item.skill_bonus
				modified_will += item.will_bonus

				i += 1
				
			# if stats go below zero, we set the cumulative to zero as play cannot have negative stat values
			if modified_skill <= 0:
				modified_skill = 0 
			if modified_will <= 0:
				modified_will = 0 

			print('With your items, you have a SKILL level of {} and a WILL power of {}.\n'.format(modified_skill, modified_will))

		else:
			# here, we check for an individual item
			# boolean flag to determine if input corresponds inventory item
			# assume the request input false until we confirm it matches to an inventory item        
			request_success = False 
			
			# iterate through inventory, checking if input matches with the item object's name or short name
			i = 0
			while i < len(self.inventory):
				item = self.inventory[i]
				if (request == item.get_name().upper()) or (request == item.get_short().upper()):
					# if this conditional is met, an item matches to user input
					# retrieve the item's basic infoo
					# change the Boolean flag as the user request is a success
					# then end the loop as we have found what the user requested 
					request_success = True
					item.get_info()
					print()
					break
				i += 1
                
			# executes only if boolean flag remains unchanged
			# suggests that input did not correspond to any inventory items
			if not request_success:
				print('\nYou don\'t have that!\n')


