Each testcase has the configuration files modified accordingly (chiefly room paths, item values, and quest requirements) in order to ensure maximum code coverage and test different aspects of functionality. 

#00: Test program where all configuration files are empty.
- Program should inform user that no rooms exist 
- Should not state "please specify a valid configuration file" as the program can still function with empty item and quest configs

#01: Using the LOOK command after entering each room for the first time to check the room's description and appearance remain the same.

#02: Using the LOOK command after failing a quest to check that the room's description does not change. Also uses INV to check player's inventory does not change. 
- Also checks that quest status remains incomplete

#03: Using the LOOK command after successfully completing various quests to check the room's description and player's inventory changes.
- Also checks that all quest status are updated to complete and that the user can win the game 
- Quest actions are tested with varying character cases (i.e. upper, lower, mixed)

#04: Checks that a user's overall SKILL and WILL do not fall below 0, even with items with large negative values.
- Further checks that with SKILL and WILL values of 0, the user cannot complete any quest requirements that are > 0.

#05: Checks that a user can inspect an item in their inventory with case insensitivity based on the item's proper name or short name after having completed a quest. 
- Also checks to ensure that the item does not exist in the inventory before completion of the quest. Similarly, checks that it does exist after successful completion. 

#06: Checks that a user cannot complete a quest twice if they have already successfully completed it. Further checks that a user receives a "you can't do that message" if they attempt the quest action 
in the wrong room.

#07: Tests for successful navigation in different rooms using all cardinal directions in their short and normal commands (e.g. 'N' and 'NORTH') in a case insensitive manner (upper/lower/mixed)
- Also tests for attempts to move in a direction with no exits. Applies this for normal rooms but also one room with no exits at all. 

#08: Test program where path configuration has missing arguments 
- Program should inform user to "specify a valid configuration file"
- Has either starting room, direction, or destination room missing on some of the lines

#09: Checks for blank spaces in user input. Should not be able to activate any commands (e.g. 'HELP' != 'HELP ')
- Inputs valid command after some attempts to ensure program is working as intended 

#10: Checking for several items that do not exist in the user's inventory.

#11: Checks that the user cannot perform any quest actions with an empty quest file. Player should win the game and quit program upon entering the QUEST command.

#12: Tests a case where the user unsuccessfully attempts each quest and cannot complete any due to the requirements. 
- Checks that quests incomplete status remains constant and that room descriptions remain the same after unsuccessful quest attempt 

#13: Tests CHECK 'ME' and QUESTS to progressively to show that item bonuses and stat totals are updating properly as the user completes quests. 
- Perform an initial quest and check 'me' command to confirm that user starts with 5 SKILL/WILl and all quests as incomplete 
- As we complete each quest, we reinput these to show program is functioning as intended 

#14: Tests for a case where a user has overall 0 SKILL and 0 WILL from items but can still complete quests (and win the game) that have requirements that are either 0 or negative. 
- Use CHECK command with all items to ensure stats do not fall below 0 

#15: Test navigation of rooms in a non-linear manner based on unusual path configurations 

#16: Test for input that is very similar to actual commands but have one additional character. (e.g. 'north~' compared to 'north', 'help!' compared to 'help'). Then we run every valid command in upper, lower, mixed cases to show program is functioning.

#17: Testing that program correctly displays quests formatting for zero digit padding for when there are 10 or more quests
