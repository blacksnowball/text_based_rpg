class Room:
	def __init__(self, name):
		'''Initialises a room. Do not change the function signature (line 2).'''
		self.name = name
		self.quest = None
		self.north = None 
		self.south = None 
		self.east = None
		self.west = None 
		
	def __repr__(self):
		return 'name: {}'.format(self.name)

	def get_name(self):
		'''Returns the room's name.'''
		return self.name

	def get_short_desc(self):
		'''Returns a string containing a short description of the room. This description changes based on whether or not a relevant quest has been completed in this room.

		If there are no quests that are relevant to this room, this should return: "There is nothing in this room."'''

		# check if a quest exists (has a value other than None)
		# if so, retrieve the room description
		if self.quest:
			return self.quest.get_room_desc()
		# otherwise return empty room description 
		return 'There is nothing in this room.'

	def get_quest_action(self):
		''' If a quest can be completed in this room, returns a command that the user can input to attempt the quest.'''
		# we only return quest action if it exists
		if self.quest:
			# upper() to match formatting of main program (also account cases where data given is lower or mixed chars)
			return self.quest.get_action().upper()
		
	def set_quest(self, q):
		'''Returns a Quest object that can be completed in this room.''' 
		self.quest = q 

	def get_quest(self):
		'''Returns a Quest object to be complete in this room.'''
		return self.quest

	def set_path(self, dir, dest):
		'''Creates an path leading from this room to another.'''
		# call this function when creating rooms to connect rooms objects together 
		# in main program, dir will be as .upper() so no need to consider lower or mixed cases
		
		if dir == 'NORTH':
			self.north = dest 
		elif dir == 'SOUTH':
			self.south = dest 
		elif dir == 'EAST':
			self.east = dest
		elif dir == 'WEST':
			self.west = dest 
		else:
			return None 


	def draw(self):
		'''Creates a drawing depicting the exits in each room.'''
		
		# assume by default there are no exits, cardinal directions have no objects assigned
		n = '--'
		s = '--'
		e = '|'
		w = '|'
		
		# if directions have objects assigned, we update directions and place relevant exits 
		if self.north:
			n = 'NN'
		if self.south:
			s = 'SS'
		if self.east:
			e = 'E'
		if self.west:
			w = 'W'
		
		print('''
+---------{}---------+
|                    |
|                    |
|                    |
|                    |
{}                    {}
|                    |
|                    |
|                    |
|                    |
+---------{}---------+
'''.format(n, w, e, s) + 
'You are standing at the {}.\n'.format(self.get_name()) +
self.get_short_desc())
			 

	def move(self, dir):
		'''Returns an adjoining Room object based on a direction given. (i.e. if dir == "NORTH", returns a Room object in the north).'''
		# in the main program, we will set pass the argument from user input as .upper()
		# therefore, won't need to explicitly check for lowercase as it will always be all caps when passed in as parameters in this function 
		if dir == 'NORTH' or dir == 'N':
			return self.north
		elif dir == 'SOUTH' or dir == 'S':
			return self.south
		elif dir == 'EAST' or dir == 'E':
			return self.east
		elif dir == 'WEST' or dir == 'W':
			return self.west 
		return None
		# this is going to be an object to the adjoining room

		
	def path_change(self, dir):
		'''Displays a message to indicate the transition from one room to another based on directon'''
		
		# the user input, when passed as an argument to the function, will be set to .lower() so we need not check for all caps case 
		# we check if user input exercised the abbreviation and if so, we update this to be the full word 
		# if the full word for cardinal direction was used in main program, we can leave it as it is 
		# note that this function is only called if the user inputs a command relating to the cardinal directions for moving between moves 
		if dir == 'n':
			dir = 'north'
		elif dir == 's':
			dir = 'south'
		elif dir == 'w':
			dir = 'west'
		elif dir == 'e':
			dir = 'east'
		
		print('You move to the {}, arriving at the {}.'.format(dir, self.name))
		
	def empty_check(self, dir):
		'''Checks if a room object exists based on the room exit in a given direction'''
		# user input will be passed as a .upper() argument so don't need to cover lowercase instances of cardinal directions
		# using a boolean flag, we assume the room exists in the given direction
		room_exist = True
		if dir == 'NORTH' or dir == 'N':
			result = self.north
		elif dir == 'SOUTH' or dir == 'S':
			result = self.south 
		elif dir == 'EAST' or dir == 'E':
			result = self.east
		elif dir == 'WEST' or dir == 'W':
			result = self.west 
		
		# if not, we change the value of the boolean flag to indicate a wall direction with no exit
		# in the main program, this will help inform the player that they cannot go in that direction 
		if result == None:
			print('You can\'t go that way.\n')
			room_exist = False
		return room_exist
