#!/usr/bin/env python3

import csv
import math
import os
import re


# Defines a custom error that can be raised to give more information on why a user input failed
class CustomExcept(Exception):
    pass
    

# Defines a character class. Each character that is created will be part of this class, with each part of the character sheet as a variable
class Character:
    name = ""
    level = 0
    race = ""
    setclass = ""
    background = ""
    # Variable for a path-friendly version of the character name
    pathname = ""
    # Variable for selected ability score proficiencies
    proficiencies = {"proficiencies": [], "doubled": []}
    
    # Variable for raw ability scores
    scores = {"Strength": 0, "Dexterity": 0, "Constitution": 0, "Intelligence": 0, "Wisdom": 0, "Charisma": 0}
    
    # Variable for calculated skill stats
    stats = {'Strength': 0, 'Dexterity': 0, 'Constitution': 0, 'Wisdom': 0, 'Charisma': 0, 'Acrobatics': 0, 'Animal handling': 0, 'Arcana': 0, 'Athletics': 0, 'Deception': 0, 'History': 0, 'Insight': 0, 'Intimidation': 0, 'Investigation': 0, 'Medicine': 0, 'Nature': 0, 'Perception': 0, 'Performance': 0, 'Persuasion': 0, 'Religion': 0, 'Sleight of hand': 0, 'Stealth': 0, 'Survival': 0}
    
    # Universal variable to determine skill buffs based on race
    racebuffs = {'Mountain dwarf': {'Strength': 2}, 'Dragonborn': {'Strength': 2, 'Charisma': 1}, 'Half-orc': {'Strength': 2, 'Constitution': 1}, 'Human': {'Strength': 1, 'Dexterity': 1, 'Constitution': 1, 'Intelligence': 1, 'Wisdom': 1, 'Charisma': 1}, 'Elf': {'Dexterity': 2}, 'Halfling': {'Dexterity': 2}, 'Forest gnome': {'Dexterity': 1}, 'Dwarf': {'Constitution': 2}, 'Stout halfling': {'Constitution': 1}, 'Rock gnome': {'Constitution': 1}, 'High elf': {'Intelligence': 1, 'Charisma': 2}, 'Gnome': {'Intelligence': 2}, 'Tiefling': {'Intelligence': 1, 'Charisma': 2}, 'Hill dwarf': {'Wisdom': 1}, 'Wood elf': {'Wisdom': 1}, 'Drow': {'Charisma': 1}, 'Lightfoot halfling': {'Charisma': 1}}
    
    # Universal variable to determine skill and saving throw buffs based on class
    classbuffs = {'Barbarian': {'throws': ['Strength', 'Constitution'], 'howmany': 2, 'skills': ['Animal handling', 'Athletics', 'Intimidation', 'Nature', 'Perception', 'Survival']}, 'Bard': {'throws': ['Dexterity', 'Charisma'], 'howmany': 3, 'skills': ["Strength", "Athletics", "Dexterity", "Acrobatics", "Sleight of hand", "Stealth", "Intelligence", "Arcana", "History", "Investigation", "Nature", "Religion", "Wisdom", "Animal handling", "Insight", "Medicine", "Perception", "Survival", "Charisma", "Deception", "Intimidation", "Performance", "Persuasion"]}, 'Cleric': {'throws': ['Wisdom', 'Charisma'], 'howmany': 2, 'skills': ['History', 'Insight', 'Medicine', 'Persuasion', 'Religion']}, 'Druid': {'throws': ['Intelligence', 'Wisdom'], 'howmany': 2, 'skills': ['Arcana', 'Animal handling', 'Insight', 'Medicine', 'Nature', 'Perception', 'Religion', 'Survival']}, 'Fighter': {'throws': ['Strength', 'Constitution'], 'howmany': 2, 'skills': ['Acrobatics', 'Animal handling', 'Athletics', 'History', 'Insight', 'Intimidation', 'Perception', 'Survival']}, 'Monk': {'throws': ['Strength', 'Dexterity'], 'howmany': 2, 'skills': ['Acrobatics', 'Athletics', 'History', 'Insight', 'Religion', 'Stealth']}, 'Paladin': {'throws': ['Wisdom', 'Charisma'], 'howmany': 2, 'skills': ['Athletics', 'Insight', 'Intimidation', 'Medicine', 'Persuasion', 'Religion']}, 'Ranger': {'throws': ['Strength', 'Dexterity'], 'howmany': 3, 'skills': ['Animal handling', 'Athletics', 'Insight', 'Investigation', 'Nature', 'Perception', 'Stealth', 'Survival']}, 'Rogue': {'throws': ['Dexterity', 'Intelligence'], 'howmany': 4, 'skills': ['Acrobatics', 'Athletics', 'Deception', 'Insight', 'Intimidation', 'Investigation', 'Perception', 'Performance', 'Persuasion', 'Sleight of hand', 'Stealth']}, 'Sorcerer': {'throws': ['Constitution', 'Charisma'], 'howmany': 2, 'skills': ['Arcana', 'Deception', 'Insight', 'Intimidation', 'Persuasion', 'Religion']}, 'Warlock': {'throws': ['Wisdom', 'Charisma'], 'howmany': 2, 'skills': ['Arcana', 'Deception', 'History', 'Intimidation', 'Investigation', 'Nature', 'Religion']}, 'Wizard': {'throws': ['Intelligence', 'Wisdom'], 'howmany': 2, 'skills': ['Arcana', 'History', 'Insight', 'Investigation', 'Medicine', 'Religion']}}

    # Universal variable for level events based on class
    classevents = {'Bard': ['3', '10'], 'Cleric': ['1'], 'Fighter': ['6', '14'], 'Rogue': ['1', '6', '10', '15']}

    # Universal variable to determine skill buffs based on background
    backgroundbuffs = {'Acolyte': ['Insight', 'Religion'], 'Charlatan': ['Deception', 'Sleight of hand'], 'Criminal': ['Deception', 'Stealth'], 'Spy': ['Deception', 'Stealth'], 'Entertainer': ['Acrobatics', 'Performance'], 'Gladiator': ['Acrobatics', 'Performance'], 'Folk hero': ['Animal handling', 'Survival'], 'Guild artisan': ['Insight', 'Persuasion'], 'Guild Merchant': ['Insight', 'Persuasion'], 'Hermit': ['Medicine', 'Religion'], 'Noble': ['History', 'Persuasion'], 'Knight': ['History', 'Persuasion'], 'Outlander': ['Athletics', 'Survival'], 'Sage': ['Arcana', 'History'], 'Sailor': ['Athletics', 'Perception'], 'Pirate': ['Athletics', 'Perception'], 'Soldier': ['Athletics', 'Intimidation'], 'Urchin': ['Sleight of hand', 'Stealth']}

    # Universal variable to aid in calculating skill stats based on ability scores
    abilitycalculation = {'Strength': ['Strength', 'Athletics'], 'Dexterity': ['Dexterity', 'Acrobatics', 'Sleight of hand', 'Stealth'], 'Constitution': ['Constitution'], 'Intelligence': ['Intelligence', 'Arcana', 'History', 'Investigation', 'Nature', 'Religion'], 'Wisdom': ['Wisdom', 'Animal handling', 'Insight', 'Medicine', 'Perception', 'Survival'], 'Charisma': ['Charisma', 'Deception', 'Intimidation', 'Performance', 'Persuasion']}

    def __init__(self, name=None):
        if name is not None:
            self.name = name
            self.pathname = "_".join(name.split())
    
    # Class function to set up new character.
    def setup(self):
        # User sets character level
        while True:
            try:
                level = int(input("Character level:\n"))
                if level < 1:
                    raise ValueError
                self.level = level
                break
            except ValueError:
                print("Invalid selection, try again.")
        # User selects character race
        racelist = list(self.racebuffs.keys())
        formattedraces = columns(numbered(racelist), False)
        columns(formattedraces)
        while True:
            try:
                selection = int(input("Select character race:\n"))
                if selection < 1 or selection > len(racelist):
                    raise ValueError
                race = racelist[selection-1]
                self.race = race
                break
            except ValueError:
                print("Invalid selection, try again.")
        # User selects character class.
        classlist = list(self.classbuffs.keys())
        formattedclass = columns(numbered(classlist), False)
        columns(formattedclass)
        while True:
            try:
                selection = int(input("Character class: \n"))
                if selection < 1 or selection > len(classlist):
                    raise ValueError
                setclass = classlist[selection-1]
                self.setclass = setclass
                break
            except ValueError:
                print("Invalid selection, try again.")
        # User selects character background
        backgroundlist = list(self.backgroundbuffs.keys())
        formattedbackground = columns(numbered(backgroundlist), False)
        columns(formattedbackground)
        while True:
            try:
                selection = int(input("Character background:\n"))
                if selection < 1 or selection > len(backgroundlist):
                    raise ValueError
                background = backgroundlist[selection-1]
                self.background = background
                break
            except ValueError:
                print("Invalid selection, try again.")
        # Adds background-based proficiencies to proficiency list
        for item in self.backgroundbuffs[background]:
            self.proficiencies["proficiencies"].append(item)
        # Take raw score for each ability. Checks for any race buffs and adds buff to the score.
        for score in list(self.scores.keys()):
            while True:
                try:
                    rawscore = int(input("Enter raw {} score.\n".format(score.lower())))
                    if rawscore < 1:
                        raise ValueError
                    if score in self.racebuffs[race]:
                        rawscore += self.racebuffs[race][score]
                    self.scores[score] = rawscore
                    break
                except ValueError:
                    print("Invalid input, try again.")
        # User selects class-based proficiencies
        proficiencyoptions = self.classbuffs[setclass]["skills"]
        times = self.classbuffs[setclass]["howmany"]
        if not all(item in self.proficiencies["proficiencies"] for item in proficiencyoptions):
            selected = []
            for x in range(1,times+1):
                columns(numbered(proficiencyoptions))
                while True:
                    try:
                        if all(item in self.proficiencies["proficiencies"] for item in proficiencyoptions):
                            break
                        selection = int(input("Select a proficiency:\n"))
                        if selection < 1 or selection > len(proficiencyoptions):
                            raise ValueError
                        choice = proficiencyoptions[selection-1]
                        if choice in selected:
                            raise CustomExcept
                        selected.append(choice)
                        self.proficiencies["proficiencies"].append(choice)
                        break
                    except ValueError:
                        print("Invalid selection, try again.")
                    except CustomExcept:
                        print("You are already proficient, select another option.")
        self.recalculate()
        for x in range(1, self.level+1):
            self.levelup(x, False)
        self.recalculate()
        self.export()
            
        
    # Class function for increasing the level of a character
    def levelup(self, level, autoexport=True):
        if level in [4, 8, 12, 16, 19]:
            scores = list(self.scores.keys())
            for x in range(1, 3):
                formattedscores = []
                for item in scores:
                    formattedscores.append("{} [{}]".format(item, self.scores[item]))
                columns(numbered(formattedscores))
                print("Choose an ability score to increase by 1 point.")
                while True:
                    try:
                        selection = int(input(""))
                        if selection < 1 or selection > len(scores):
                            raise ValueError
                        selectedscore = scores[selection - 1]
                        if self.scores[selectedscore] == 20:
                            raise CustomExcept
                        self.scores[selectedscore] += 1
                        break
                    except ValueError:
                        print("Invalid selection, try again.")
                    except CustomExcept:
                        print("Ability scores cannot exceed 20, please select a different score.")
        if self.setclass in list(self.classevents.keys()) and level in self.classevents[self.setclass]:
            classevent(level)
        if autoexport == True:
            self.export()
            
    
    # Class function to handle character class special level events
    def classevent(self, level):
        cl = self.setclass
        if cl == "Bard":
            if level == 3:
                # Character can choose their bard college. If they choose the college of lore, they gain 3 proficiencies
                print("Choose your college:\n(1): College of Lore    (2): College of Valor")
                while True:
                    try:
                        chosencollege = int(input())
                        if chosencollege != 1 and chosencollege != 2:
                            raise ValueError
                        break
                    except ValueError:
                        print("Invalid selection, try again.")
                if chosencollege == 1 and not all(item in self.proficiencies["proficiencies"] for item in list(self.stats.keys())[5:]):
                    chosenprofs = []
                    options = []
                    for item in list(self.stats.keys())[5:]:
                        if item in self.proficiencies["proficiencies"]:
                            continue
                        else:
                            options.append(item)
                    optionsformat = columns(numbered(options), False)
                    columns(optionsformat)
                    for x in range(1, 4):
                        while True:
                            try:
                                if options == [] or all(item in self.proficiencies["proficiencies"] for item in options):
                                    break
                                chosenprof = int(input("Choose 3 proficiencies.    {}\n".format(chosenprofs)))
                                if options[chosenprof-1] in chosenprofs:
                                    raise CustomExcept
                                elif chosenprof < 1 or chosenprof > len(options):
                                    raise ValueError
                                else:
                                    chosenprofs.append(options[chosenprof-1])
                                    self.proficiencies["proficiencies"].append(options[chosenprof-1])
                                    break
                            except CustomExcept:
                                print("Please select each proficiency only once.")
                            except ValueError:
                                print("Invalid selection, try again.")
                chosenexpertise = []
                # Level 3 Bards also choose 2 proficiencies to gain expertise in.
                for x in range(1, 3):
                    profoptions = self.proficiencies["proficiencies"]
                    for item in numbered(profoptions):
                        print(item)
                    while True:
                        try:
                            chosen = int(input("Choose your expertise.    {}\n".format(chosenexpertise)))
                            if chosen < 1 or chosen > len(profoptions):
                                raise ValueError
                            pickedname = profoptions[chosen-1]
                            if pickedname in chosenexpertise or pickedname in self.proficiencies["doubled"]:
                                raise CustomExcept
                            self.proficiencies["doubled"].append(pickedname)
                            chosenexpertise.append(pickedname)
                            break
                        except ValueError:
                            print("Invalid selection, try again.")
                        except CustomExcept:
                            print("You're already an expert, please select another option.")
            # At level 10, bards gain expertise in two more proficiencies
            if level == 10:                       
                chosenexpertise = []
                for x in range(1, 3):
                    profoptions = []
                    for item in self.proficiencies["proficiencies"]:
                        if item in self.proficiencies["doubled"]:
                            continue
                        else:
                            profoptions.append(item)                    
                    for item in numbered(profoptions):
                        print(item)
                    while True:
                        try:
                            chosen = int(input("Choose your expertise.    {}\n".format(chosenexpertise)))
                            if chosen < 1 or chosen > len(profoptions):
                                raise ValueError
                            pickedname = profoptions[chosen-1]
                            if pickedname in chosenexpertise or pickedname in self.proficiencies["doubled"]:
                                raise CustomExcept
                            self.proficiencies["doubled"].append(pickedname)
                            chosenexpertise.append(pickedname)
                            break
                        except ValueError:
                            print("Invalid selection, try again.")
                        except CustomExcept:
                            print("You're already an expert, please select another option.")
        if cl == "Cleric" and level == 1:
            # At level 1, Clerics join a domain. Depending on their domain, they may gain proficiencies
            domains = ["Knowledge", "Life", "Light", "Nature", "Tempest", "Trickery", "War"]
            print("Choose a divine domain:")
            columns(numbered(domains))
            while True:
                try:
                    selection = int(input())
                    if selection < 1 or selection > len(domains):
                        raise ValueError
                    break
                except ValueError:
                    print("Invalid selection, try again.")
            domain = domains[selecion-1]
            knowledgeoptions = ["Arcana", "Nature", "History", "Religion"]
            natureoptions = ["Animal handling", "Nature", "Survival"]
            if domain == "Knowledge" and not all(option in self.proficiencies["proficiencies"] for option in knowledgeoptions):
                options = knowledgeoptions
                for item in numbered(options):
                    print(item)
                print("Pick a skill to gain proficiency in. Proficiency multiplier will be doubled.")
                for x in range(1, 3):
                    while True:
                        try:
                            selection = int(input("\n"))
                            if selection < 1 or selection > len(options):
                                raise ValueError
                            if options[selection-1] in self.proficiencies["proficiencies"]:
                                raise CustomExcept
                            self.proficiencies["proficiencies"].append(option[selection-1])
                            self.proficiencies["doubled"].append(option[selection-1])
                            break
                        except ValueError:
                            print("Invalid selection, please try again.")
                        except CustomExcept:
                            print("You may only become proficient in this skill once. Please select a different skill.")
            if domain == "Nature" and not all(option in self.proficiencies["proficiencies"] for option in natureoptions):
                options = natureoptions
                for item in numbered(options):
                    print(item)
                print("Choose a skill to gain proficiency")
                while True:
                    try:
                        selection = int(input("\n"))
                        if selection < 1 or selection > len(options):
                            raise ValueError
                        if options[selection-1] in self.proficiencies["proficiencies"]:
                            raise CustomExcept
                        self.proficiencies["proficiencies"].append(options[selection-1])
                        break
                    except ValueError:
                        print("Invalid selection, try again.")
                    except CustomExcept:
                        print("You are already proficient in this skill, please choose another.")
        if cl == "Fighter" and level == 6 or cl == "Fighter" and level == 14:
            scores = list(self.scores.keys())
            for x in range(1, 3):
                formattedscores = []
                for item in scores:
                    formattedscores.append("{} [{}]".format(item, self.scores[item]))
                columns(numbered(formattedscores))
                print("Choose an ability score to increase by 1 point.")
                while True:
                    try:
                        selection = int(input())
                        if selection < 1 or selection > len(scores):
                            raise ValueError
                        selectedscore = scores[selection-1]
                        if self.scores[selectedscore] == 20:
                            raise CustomExcept
                        self.scores[selectedscore] += 1
                        break
                    except ValueError:
                        print("Invalid selection, try again.")
                    except CustomExcept:
                        print("Ability scores cannot exceed 20, please select a different score.")
        if cl == "Rogue":
            if level == 1:
                print("Choose a class option:\n(1): Thieves tools proficiency +1        (2): Gan expertise in two proficiencies")
                while True:
                    try:
                        choice = int(input("\n"))
                        if choice < 1 or choice > 2:
                            raise ValueError
                        break
                    except ValueError:
                        print("Invalid selection, try again.")
                if choice == 2:
                    chosen = []
                    for x in range(1, 3):
                        columns(numbered(self.proficiencies["proficiencies"]))
                        while True:
                            try:
                                selection = int(input("Pick an expertise.   {}".format(chosen)))
                                if selection < 1 or selection > len(self.proficiencies["proficiencies"]):
                                    raise ValueError
                                selectedproficiency = self.proficiencies["proficiencies"][selection-1]
                                if selectedproficiency in self.proficiencies["doubled"]:
                                    raise CustomExcept
                                self.proficiencies["doubled"].append(selectedproficiency)
                                chosen.append(selectedproficiency)
                                break
                            except ValueError:
                                print("Invalid input, try again.")
                            except CustomExcept:
                                print("You are already an expert in this, try again")
            if level == 6 and self.proficiencies["doubled"] != []:
                chosen = []
                for x in range(1, 3):
                    columns(numbered(self.proficiencies["proficiencies"]))
                    while True:
                        try:
                            selection = int(input("Pick an expertise.   {}".format(chosen)))
                            if selection < 1 or selection > len(self.proficiencies["proficiencies"]):
                                raise ValueError
                            selectedproficiency = self.proficiencies["proficiencies"][selection - 1]
                            if selectedproficiency in self.proficiencies["doubled"]:
                                raise CustomExcept
                            self.proficiencies["doubled"].append(selectedproficiency)
                            chosen.append(selectedproficiency)
                            break
                        except ValueError:
                            print("Invalid input, try again.")
                        except CustomExcept:
                            print("You are already an expert in this, try again")
            if level == 10:
                scores = list(self.scores.keys())
                for x in range(1, 3):
                    formattedscores = []
                    for item in scores:
                        formattedscores.append("{} [{}]".format(item, self.scores[item]))
                    columns(numbered(formattedscores))
                    print("Choose an ability score to increase by 1 point.")
                    while True:
                        try:
                            selection = int(input("\n"))
                            if selection < 1 or selection > len(scores):
                                raise ValueError
                            selectedscore = scores[selection - 1]
                            if self.scores[selectedscore] == 20:
                                raise CustomExcept
                            self.scores[selectedscore] += 1
                            break
                        except ValueError:
                            print("Invalid selection, try again.")
                        except CustomExcept:
                            print("Ability scores cannot exceed 20, please select a different score.")
            if level == 15:
                self.proficiencies["proficiencies"].append("Wisdom")
                

    # Class function to recalculate character sheet after a skill score or proficiency has changed
    def recalculate(self):
        for score in list(self.abilitycalculation.keys()):
            for skill in self.abilitycalculation[score]:
                skillscore = (self.scores[score]-10) // 2
                self.stats[skill] = skillscore
        modifier = 1 + int(math.ceil(float(self.level) * 0.25))
        for item in self.proficiencies["proficiencies"]:
            if item in self.proficiencies["doubled"]:
                self.stats[item] += (modifier*2)
            else:
                self.stats[item] += modifier
        for item in list(self.stats.keys())[:5]:
            if item in self.classbuffs[self.setclass]["throws"]:
                self.stats[item] += modifier
    
    # Class function to export a character sheet once character building has been completed.
    def export(self):
        csvout = {"Name": self.name, "Path Name": self.pathname, "Level": self.level, "Class": self.setclass, "Race": self.race, "Background": self.background, "Ability scores": self.scores, "Stats": self.stats, "Proficiencies": self.proficiencies}
        fields = list(csvout.keys())
        filename = "charactersheet_" + self.pathname + ".csv"
        with open(filename, "w", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fields)
            writer.writeheader()
            writer.writerow(csvout)


# This is a formatting function to add a dynamic border to passed text. The buffer variable can add whitespace characters between the edge of the screen and the boarder, and may be left empty
def bordered(text, buffer=""):
    if type(text) is str:
        lines = text.splitlines()
    elif type(text) is list:
        lines = text
    width = max(len(s) for s in lines)
    res = [buffer + '┌' + '─' * width + '┐']
    for s in lines:
        res.append(buffer + '│' + (s + ' ' * width)[:width] + '│')
    res.append(buffer + '└' + '─' * width + '┘')
    return '\n'.join(res)
        

# This is a formatting function for taking a list of strings and returning a formatted list with each option given a number value. This will be useful for building selection menus.
def numbered(items):
    outputlist = []
    for index, item in enumerate(items):
        outputlist.append("({}): {}".format(index+1, item))
    return outputlist


# This is a formatting function for formatting a list of strings into columns. If the printiterations value is left blank, the columned information will be printed. If False is passed, the formatted list of strings will be returned to be saved as a variable. This variable can then be passed through again for a column of 4 & so on
def columns(itemlist, printiterations=True):
    items = iter(itemlist)
    returnlist = []
    for item in items:
        if printiterations:
            print('{:<30}{:<30}'.format(item, next(items, "")))
        else:
            returnlist.append('{:<30}{:<30}'.format(item, next(items, "")))
    if not printiterations:
        return returnlist
        
def create():
    while True:
        rawname = input("What is the name of your character? \n".format()).strip()
        if all(c.isalpha() or c.isspace() for c in rawname):
            break
        else:
            print("Name contains script that is unsupported. Try again.")
    charactername = "_".join(rawname.split())
    charactername = Character(rawname)
    charactername.setup()
    return charactername

def startup():
    characterfiles = []
    directorylist = os.listdir()
    for item in directorylist:
        if re.match(r"charactersheet_([\w_]*)\.csv", item):
            characterfiles.append(item)
    if characterfiles:
        characterdirectory = {}
        for index, file in enumerate(characterfiles):
            charactername = re.search(r"charactersheet_([\w_]*)\.csv", file)
            charactername = " ".join(charactername.group(1).split("_"))
            characterdirectory[charactername] = index
        characters = list(characterdirectory.keys())
        print("Select from existing character sheets or enter 0 to create a new character.\n(0): Create new character")
        columns(numbered(characters))
        while True:
            try:
                selection = int(input())
                if selection < 0 or selection > len(characters):
                    raise ValueError
                character = characters[selection-1]
                break
            except ValueError:
                print("Invalid selection, try again.")
        fileindex = characterdirectory[character]
        chosenfile = characterfiles[fileindex]
        csvkeys = {'Name': "name", 'Path Name': "pathname", 'Level': "level", 'Class': "setclass", 'Race': "race", 'Background': "background", 'Ability scores': "scores", 'Stats': "stats", 'Proficiencies': "proficiencies"}
        with open(chosenfile, "r") as file:
            for row in csv.DictReader(file):
                loadedcharacter = row
        if all(item in list(csvkeys.keys()) for item in list(loadedcharacter.keys())):
            loadedname = loadedcharacter["Path Name"]
            loadedname = Character()
            for value in list(csvkeys.keys()):
                variablename = csvkeys[value]
                loadedvalue = loadedcharacter[value]
                loadedname.variablename = loadedvalue
            return loadedname
        else:
            while True:
                try:
                    selection = int(input("There was a problem loading the selected character sheet. Enter 1 to delete the file and return to character selection or 2 to return to character selection without deleting.\n"))
                    if selection < 1 or selection > 2:
                        return ValueError
                    break
                except ValueError:
                    print("Invalid selection, try again.")
            if selection == 1:
                os.remove(chosenfile)
            startup()
    else:
        return create()

startup()

