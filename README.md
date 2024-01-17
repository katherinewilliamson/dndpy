The DnDPy program is a program that automatically calculates stats for a DnD character and allow for automatic dice rolls.

Upon launching the program, a user will be prompted to create their character by entering their name, raw scores, race, class, starting level, and background.
Based on this information, the program will automatically calculate the rest of the character sheet. With the character sheet created, the user may make a custom dice roll, roll a D20 and have the relevant modifier added automatically, view a formatted version of the character sheet, level their character up (any level-specific events for their character will be handled automatically and the user will be prompted if applicable), reset the seed the RNG is running on for that instance of the program, delete their character, or create a new character.

For each character that is created, or when the stats for an existing character change due to a change in level, a .csv file containing that character's information is exported into the directory in which the program is located. When the program is run, the surrounding directory is checked for any .csv files matching the naming convention used by the export function. Any matching files will be listed for the user to select in order to load a previously created character into the program.

This program was made based on the rules for DnD 5E.
