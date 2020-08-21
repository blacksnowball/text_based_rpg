from room import Room
from item import Item
from adventurer import Adventurer
from quest import Quest
import sys

# check if insufficient config files
if len(sys.argv) < 4:
    print('Usage: python3 simulation.py <paths> <items> <quests>')
    sys.exit(1)

# attempting to open each file, returning error msg if invalid file
try:
    paths_file = open(sys.argv[1], 'r')
    items_file = open(sys.argv[2], 'r')
    quests_file = open(sys.argv[3], 'r')
except IOError:
    print('Please specify a valid configuration file.')
    sys.exit(2)

# checking if room config is empty
paths_data = paths_file.readlines()
# empty files may also just have '\n' if a file originally had input but was later manually wiped
# former checks for a file created with nothing, latter checks for a file which originally had some text but was later removed
if len(paths_data) == 0 or paths_data == ['\n']:
    print('No rooms exist! Exiting program...')
    sys.exit(3)

def read_paths(source):
    '''Returns a list of lists according to the specifications in a config file, (source).

    source contains path specifications of the form:
    origin > direction > destination.

    read_paths() interprets each line as a list with three elements, containing exactly those attributes. Each list is then added to a larger list, `paths`, which is returned.'''
    paths = []
    i = 0 
    while i < len(source):
        # we check for empty lines before and in between lines containg data (and skip over them if encountered)
        # also remove newline chars for each line with actual quest data 
        line = source[i].rstrip('\n').lstrip('\n')
        if line == '':
            i += 1
            continue
        line = line.split(' > ')
        paths.append(line)
        i += 1 
    
    return paths

def create_rooms(paths):
    '''Receives a list of paths and returns a list of rooms based on those paths. Each room will be generated in the order that they are found.'''
    
    # rooms_objects contains list of objects, each added once they are generated 
    # rooms_list records what objects have been generated thus far to prevent any duplicate rooms being created 
    rooms_objects = []
    rooms_list = []
    
    # iterate through paths to create room objects to be added to a list
    try:
        for path in paths:
            start = path[0]
            destination = path[2]

            # checking if start or destination room has already been created to prevent duplicates
            # if not, we generate the room object and mark this in rooms_list
            # we do not use continue as it may prevent dest from being checked
            if start in rooms_list:
                pass
            else:
                rooms_list.append(start)
                start = Room(start)
                rooms_objects.append(start)

            if destination in rooms_list:
                pass 
            else:
                rooms_list.append(destination)
                destination = Room(destination)
                rooms_objects.append(destination)
    
    # consider cases where direction is missing or either start/dest is missing
    except IndexError:
        print('Please specify a valid configuration file.')
        sys.exit(4)
            
    # we iterate through paths and match the start room name with the name of the objects in rooms_objects 
    for path in paths:
        start = path[0]
        direction = path[1]
        destination = path[2]
        
        i = 0 
        while i < len(rooms_objects):
            room_object_start = rooms_objects[i]
            # repeat the above process of matching the destination with a room object sharing its name, using a nested loop
            # we then establish the path between the two, tying the room objects together
            if room_object_start.get_name() == start:
                n = 0
                while n < len(rooms_objects):
                    room_object_end = rooms_objects[n]
                    if room_object_end.name == destination:
                        rooms_objects[i].set_path(direction, rooms_objects[n])
                        break
                    n += 1 
            i += 1 
    
    return rooms_objects
    
def generate_items(source):
    '''Returns a list of items according to the specifications in a config file, (source).

    source contains item specifications of the form:
    item name | shortname | skill bonus | will bonus
    '''
        
    items = []
    
    item_data = source.readlines()
    i = 0 
    while i < len(item_data):
        # check for presence of empty lines to be skipped, remove newline char in data
        current_item = item_data[i].rstrip('\n').lstrip('\n')
        if current_item == '':
            i += 1
            continue
        current_item = current_item.split(' | ')
        name = current_item[0]
        short = current_item[1]
        
        # we check if skill and will bonuses are valid data-types 
        # if they are not int, raise error msg and quit program 
        try:
            skill_bonus = int(current_item[2])
            will_bonus = int(current_item[3])
        except ValueError:
            print('Item skill or will value must be an integer. Please specify a valid configuration file.')
            sys.exit(4)
            
        item_create = Item(name, short, skill_bonus, will_bonus)
        items.append(item_create)
        i += 1 
    
    return items

def generate_quests(source, items, rooms):
    '''Returns a list of quests according to the specifications in a config file, (source).

    source contains quest specifications of the form:
    reward | action | quest description | before_text | after_text | quest requirements | failure message | success message | quest location
    '''

    quests = []
    
    quest_data = source.readlines()
    for current_quest in quest_data:
        # accounts for the spaces in between each line containg quest data in the config, skipping over them if encountered
        # we remove newline char from quest data
        if current_quest == '\n':
            continue 
        current_quest = current_quest.rstrip('\n')
        current_quest = current_quest.split(' | ')
            
        reward = current_quest[0]
        action = current_quest[1]
        desc = current_quest[2]
        before = current_quest[3]
        after = current_quest[4]
        req = current_quest[5]
        fail_msg = current_quest[6]
        pass_msg = current_quest[7]
        room = current_quest[8]
        

        # we do initial check to determine if there was any data provided in item.txt
        # if not, no item object can be assigned to replace the str and there will be no item interactions but rooms and quests may still have object interactions 
        if items:
            for item in items:
            # iterate through items and replace the quest's reward string value with the actual object 
            # we use .lower() to standardise comparison in the event of varied text case for same str (upper/lower/mixed)
                if item.get_name().lower() == reward.lower():
                    reward = item 
                    break 
        
        # similarly, iterate through rooms and replace the room string with the actual object
        # no need to check in no rooms as program would not reach this point if there were no paths
        for room_object in rooms:
            # check if assigned quest room corresponds, again we standardise comparison to account for mixed test case
            if room_object.get_name().lower() == room.lower():
                room = room_object
                break 
        
        # creating quest to thereafter establish links with items and rooms 
        quest_create = Quest(reward, action, desc, before, after, req, fail_msg, pass_msg, room)
        
        # iterate through rooms to see if it corresponds with the quest
        # again, using .lower() in case of unusual character case conflict
        # if so, set the quest 
        for room_object in rooms:
            # only set quests if the room attribute is an object - only these will be added to quest obejct list to be used in the program
            # this arises in cases where we may have quests but their room name does not appear in paths, therefore not existing as an object
            # we thus ignore quests whose room does not exist and continue the program as normal
            if not isinstance(quest_create.room, str):
                if quest_create.room.get_name().lower() == room_object.get_name().lower():
                    room_object.set_quest(quest_create)
                    quests.append(quest_create)
                    break
                    
    return quests 


# Retrieve info from CONFIG files. Use this information to make Adventurer, Item, Quest, and Room objects.
paths = read_paths(paths_data)
rooms = create_rooms(paths)
items = generate_items(items_file)
quests = generate_quests(quests_file, items, rooms)
player = Adventurer()

# close files as info is no longer needed
paths_file.close()
items_file.close()
quests_file.close()

# start game by drawing initial room before user input given
current_room = rooms[0]
current_room.draw()
print()

# receive commands from standard input and act appropriately
while True:
    prompt = input('>>> ')
    
    # convert the user inputs to be all caps to check if it matches with commands to allow for case insensitivity
    prompt = prompt.upper()

    if prompt == 'QUIT':
        print('Bye!')
        sys.exit()

    elif prompt == 'HELP':
        print('HELP'.ljust(11) + '- Shows some available commands.')
        print('LOOK or L'.ljust(11) + '- Lets you see the map/room again.')
        print('QUESTS'.ljust(11) + '- Lists all your active and completed quests.')
        print('INV'.ljust(11) + '- Lists all the items in your inventory.')
        print('CHECK'.ljust(11) + '- Lets you see an item (or yourself) in more detail.')
        print('NORTH or N'.ljust(11) + '- Moves you to the north.')
        print('SOUTH or S'.ljust(11) + '- Moves you to the south.')
        print('EAST or E'.ljust(11) + '- Moves you to the east.')
        print('WEST or W'.ljust(11) + '- Moves you to the west.')
        print('QUIT'.ljust(11) + '- Ends the adventure.\n')

    elif prompt == 'L' or prompt == 'LOOK':
        current_room.draw()
        print()

    elif prompt == 'INV':
        # retrieve inventory, check if empty or has at least one element to print
        inventory = player.get_inv()
        if len(inventory) == 0:
            print('You are carrying:\nNothing.')
        else:
            # iterate through inventory to print each item's name
            print('You are carrying:')
            i = 0
            while i < len(inventory):
                item = inventory[i]
                print('- A {}'.format(item.get_name()))
                i += 1
        print()

    elif prompt == 'CHECK':
        player.check_self()
    
    elif prompt == 'QUESTS':
        # use a Boolean flag assuming all quests are complete
        quests_all_complete = True
        i = 0
        while i < len(quests):
            quest = quests[i]
            # check the complete status of each quest obejct
            # by default, complete status is False so first condition will trigger if any quest is incomplete 
            
            # we retrieve quest's reward-name depending on whether the attribute an object or str
            # this is dependent on if item.txt was empty or had data
            if isinstance(quest.reward, str):
                quest_name = quest.reward
            else:
                quest_name = quest.reward.name
            
            if not quest.complete_status:
                print('#{:02d}: '.format(i) + '{}'.format(quest_name).ljust(21) + '- {}'.format(quest.desc))
                # if above is printed, at least one quest is incomplete
                # the user has not yet finished the game therefore we set the Boolean flag of all quests complete to False 
                quests_all_complete = False
            else:
                print('#{:02d}: '.format(i) + '{}'.format(quest_name).ljust(21) + '- {} [COMPLETED]'.format(quest.desc))
            i += 1 
            
        print()
            
        # if indeeded all quests are complete, print congrats message and quit program
        if quests_all_complete:
            print('=== All quests complete! Congratulations! ===')
            sys.exit()

    elif (prompt == 'N' or prompt == 'NORTH' or 
        prompt == 'S' or prompt == 'SOUTH' or
        prompt == 'E' or prompt == 'EAST' or
        prompt == 'W' or prompt == 'WEST'):
        # check if user input corresponds to any of the cardinal directions and their abbreviations
        # we check if there is a room object in the given direction
        room_exists = current_room.empty_check(prompt)
        # if so, we print the room change (inlcuding direction) and return and draw the desired room object
        # otherwise, we simply return a "you can't go that way" message (embedded within an instance method)
        if room_exists:
            current_room = current_room.move(prompt)
            current_room.path_change(prompt.lower())
            current_room.draw()
            print()
            
    elif prompt == current_room.get_quest_action():
        # check if input matches with quest action tied to a specific room 
        print(current_room.quest.attempt(player))
        
    else:
        print('You can\'t do that.\n')

