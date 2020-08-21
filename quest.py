class Quest:
	def __init__(self, reward, action, desc, before, after, req, fail_msg, pass_msg, room):
		self.reward = reward
		self.action = action
		self.desc = desc
		self.before = before
		self.after = after
		self.req = req
		self.fail_msg = fail_msg
		self.pass_msg = pass_msg
		self.room = room
		# quests are always initially incomplete when generated and assigned to a room object 
		# this boolean changes immediately once the quest is complete 
		self.complete_status = False
		
	def __repr__(self):
		return 'quest_name: {}, room: {}'.format(self.reward, self.room)

	def get_info(self):
		'''Returns the quest's description.'''
		return self.desc

	def is_complete(self):
		'''Returns whether the quest is complete.'''
		return self.complete_status

	def get_action(self):
		'''Returns a command that the user can input to attempt the quest.'''
		return self.action

	def get_room_desc(self):
		'''Returns a description for the room that the quest is currently in. Note that this is different depending on whether or not the quest has been completed.'''
		# use boolean flag of quest complete status to determine what type of description to return
		# executes if quest is complete
		if self.complete_status:
			return self.after
		# executes if quest incomplete 
		return self.before
	
	def attempt(self, player):
		'''Allows the player to attempt this quest.

		Check the cumulative skill or will power of the player and all their items. If this value is larger than the required skill or will threshold for this quest's completion, they succeed and are rewarded with an item (the room's description will also change because of this).

		Otherwise, nothing happens.'''

		# checks if the player has completed the quest before we execute the action
		# if true, we return the following message 
		if self.complete_status:
			return 'You have already completed this quest.\n'

		requirement = self.req
		# split requirement into two strs to determine which type (skill or will?) and what value
		requirements = requirement.split()
		attribute = requirements[0]
		attribute_value = int(requirements[1])

		# create temporary variables modifying player's stats based on items they have
		# determines if they can complete quest
		cumulative_skill = player.get_skill()
		cumulative_will = player.get_will()

		# iterate through each item in the inventory
		# add skill and will values to user base stats 
		i = 0
		while i < len(player.inventory):
			item = player.inventory[i]
			cumulative_skill += item.get_skill()
			cumulative_will += item.get_will()
			i += 1
			
		# check if culminating skill and will levels are below zero
		# if so, set them to zero as the user's stats cannot fall below zero 
		if cumulative_skill <= 0:
			cumulative_skill = 0
		if cumulative_will <= 0:
			cumulative_will = 0

		# we check if the quest requirement is either for skill or will to know which comparison of values to make  
		if attribute == 'SKILL':
			if cumulative_skill >= attribute_value:
				# if conditional is met, quest can be performed (apply this to below block as well)
				# change the boolean quest completion flag 
				# this modifies quest description 
				self.complete_status = True
				# we only append inventory item if the item was recorded in item.txt and was generated as an object
				# otherwise, it is a str and will disrupt the program
				if not isinstance(self.reward, str):
					player.inventory.append(self.reward)
				else:
                    # we leave a msg to the player informing them that the program cannot perform proper interactions with the item because of the lack of item data in item.txt config
                    # this is because it exists in the program as a string rather than object
                    # program, however, will still continue to function as though these item obejcts did not exist
					print('The relevant item for this quest did not appear in the item.txt configuration file so there is no object for interaction here.\n')
				return self.pass_msg + '\n'
			else:
				return self.fail_msg + '\n'

		elif attribute == 'WILL':
			if cumulative_will >= attribute_value:
				self.complete_status = True
				if not isinstance(self.reward, str):
					player.inventory.append(self.reward)
				else:
					print('This item did not appear in the specific item.txt configuration so there is no interaction here.\n')
				return self.pass_msg + '\n'
			else:
				return self.fail_msg + '\n'



