#!/usr/bin/env python3

import csv


# Defines a character class. Each character that is created will be part of this class, with each part of the character sheet as a variable
class Character:
    name = ""
    level = 0
    race = ""
    setclass = ""
    background = ""
    # Variable for a path-friendly version of the character name
    pathname = "_".join(name.split())
    # Variable for selected ability score proficiencies
    proficiencies = []
    
    # Variable for raw ability scores
    scores = {"Strength": 0, "Dexterity": 0, "Constitution": 0, "Intelligence": 0, "Wisdom": 0, "Charisma": 0}
    
    # Variable for calculated skill stats
    stats = {'Strength': 0, 'Dexterity': 0, 'Constitution': 0, 'Wisdom': 0, 'Charisma': 0, 'Acrobatics': 0, 'Animal handling': 0, 'Arcana': 0, 'Athletics': 0, 'Deception': 0, 'History': 0, 'Insight': 0, 'Intimidation': 0, 'Investigation': 0, 'Medicine': 0, 'Nature': 0, 'Perception': 0, 'Performance': 0, 'Persuasion': 0, 'Religion': 0, 'Slight of hand': 0, 'Stealth': 0, 'Survival': 0}
    
    # Universal variable to determine skill buffs based on race
    racebuffs = {'Mountain dwarf': {'Strength': 2}, 'Dragonborn': {'Strength': 2, 'Charisma': 1}, 'Half-orc': {'Strength': 2, 'Constitution': 1}, 'Human': {'Strength': 1, 'Dexterity': 1, 'Constitution': 1, 'Intelligence': 1, 'Wisdom': 1, 'Charisma': 1}, 'Elf': {'Dexterity': 2}, 'Halfling': {'Dexterity': 2}, 'Forest gnome': {'Dexterity': 1}, 'Dwarf': {'Constitution': 2}, 'Stout halfling': {'Constitution': 1}, 'Rock gnome': {'Constitution': 1}, 'High elf': {'Intelligence': 1, 'Charisma': 2}, 'Gnome': {'Intelligence': 2}, 'Tiefling': {'Intelligence': 1, 'Charisma': 2}, 'Hill dwarf': {'Wisdom': 1}, 'Wood elf': {'Wisdom': 1}, 'Drow': {'Charisma': 1}, 'Lightfoot halfling': {'Charisma': 1}}
    
    # Universal variable to determine skill and saving throw buffs based on class
    classbuffs = {'Barbarian': {'throws': ['Strength', 'Constitution'], 'howmany': 2, 'skills': ['Animal handling', 'Athletics', 'Intimidation', 'Nature', 'Perception', 'Survival']}, 'Bard': {'throws': ['Dexterity', 'Charisma'], 'howmany': 3, 'skills': ["Strength", "Athletics", "Dexterity", "Acrobatics", "Sleight of hand", "Stealth", "Intelligence", "Arcana", "History", "Investigation", "Nature", "Religion", "Wisdom", "Animal handling", "Insight", "Medicine", "Perception", "Survival", "Charisma", "Deception", "Intimidation", "Performance", "Persuasion"]}, 'Cleric': {'throws': ['Wisdom', 'Charisma'], 'howmany': 2, 'skills': ['History', 'Insight', 'Medicine', 'Persuasion', 'Religion']}, 'Druid': {'throws': ['Intelligence', 'Wisdom'], 'howmany': 2, 'skills': ['Arcana', 'Animal handling', 'Insight', 'Medicine', 'Nature', 'Perception', 'Religion', 'Survival']}, 'Fighter': {'throws': ['Strength', 'Constitution'], 'howmany': 2, 'skills': ['Acrobatics', 'Animal handling', 'Athletics', 'History', 'Insight', 'Intimidation', 'Perception', 'Survival']}, 'Monk': {'throws': ['Strength', 'Dexterity'], 'howmany': 2, 'skills': ['Acrobatics', 'Athletics', 'History', 'Insight', 'Religion', 'Stealth']}, 'Paladin': {'throws': ['Wisdom', 'Charisma'], 'howmany': 2, 'skills': ['Athletics', 'Insight', 'Intimidation', 'Medicine', 'Persuasion', 'Religion']}, 'Ranger': {'throws': ['Strength', 'Dexterity'], 'howmany': 3, 'skills': ['Animal handling', 'Athletics', 'Insight', 'Investigation', 'Nature', 'Perception', 'Stealth', 'Survival']}, 'Rogue': {'throws': ['Dexterity', 'Intelligence'], 'howmany': 4, 'skills': ['Acrobatics', 'Athletics', 'Deception', 'Insight', 'Intimidation', 'Investigation', 'Perception', 'Performance', 'Persuasion', 'Sleight of hand', 'Stealth']}, 'Sorcerer': {'throws': ['Constitution', 'Charisma'], 'howmany': 2, 'skills': ['Arcana', 'Deception', 'Insight', 'Intimidation', 'Persuasion', 'Religion']}, 'Warlock': {'throws': ['Wisdom', 'Charisma'], 'howmany': 2, 'skills': ['Arcana', 'Deception', 'History', 'Intimidation', 'Investigation', 'Nature', 'Religion']}, 'Wizard': {'throws': ['Intelligence', 'Wisdom'], 'howmany': 2, 'skills': ['Arcana', 'History', 'Insight', 'Investigation', 'Medicine', 'Religion']}}

    # Universal variable for level events based on class
    classevents = {'Bard': ['3', '10'], 'Cleric': ['1'], 'Fighter': ['6', '14'], 'Rogue': ['1', '6', '10', '15']}

    
    # Universal variable to determine skill buffs based on background
    backgroundbuffs = {'Acolyte': ['Insight', 'Religion'], 'Charlatan': ['Deception', 'Sleight of hand'], 'Criminal': ['Deception', 'Stealth'], 'Spy': ['Deception', 'Stealth'], 'Entertainer': ['Acrobatics', 'Performance'], 'Gladiator': ['Acrobatics', 'Performance'], 'Folk hero': ['Animal handling', 'Survival'], 'Guild artisan': ['Insight', 'Persuasion'], 'Guild Merchant': ['Insight', 'Persuasion'], 'Hermit': ['Medicine', 'Religion'], 'Noble': ['History', 'Persuasion'], 'Knight': ['History', 'Persuasion'], 'Outlander': ['Athletics', 'Survival'], 'Sage': ['Arcana', 'History'], 'Sailor': ['Athletics', 'Perception'], 'Pirate': ['Athletics', 'Perception'], 'Soldier': ['Athletics', 'Intimidation'], 'Urchin': ['Sleight of hand', 'Stealth']}

    # Universal variable to aid in calculating skill stats based on ability scores
    abilitycalculation = {'Strength': ['Strength', 'Athletics'], 'Dexterity': ['Dexterity', 'Acrobatics', 'Slight of hand', 'Stealth'], 'Constitution': ['Constitution'], 'Intelligence': ['Intelligence', 'Arcana', 'History', 'Investigation', 'Nature', 'Religion'], 'Wisdom': ['Wisdom', 'Animal handling', 'Insight', 'Medicine', 'Perception', 'Survival'], 'Charisma': ['Charisma', 'Deception', 'Intimidation', 'Performance', 'Persuasion']}

    # Class function to export a character sheet once character building has been completed.
    def export(self):
        csvout = {"Name": self.name, "Path Name": self.pathname, "Level": self.level, "Class": self.setclass, "Background": self.background, "Ability scores": self.scores, "Stats": self.stats, "Proficiencies": self.proficiencies}
        fields = list(csvout.keys())
        with open("charactersheet_" + self.pathname + ".csv", "w", newline="") as csvfile:
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
        

#This is a formatting function for taking a list of strings and returning a formatted list with each option given a number value. This will be useful for building selection menus.
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
