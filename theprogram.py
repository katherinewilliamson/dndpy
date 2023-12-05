#!/usr/bin/env python3


#Defines a character class. Each character that is created will be part of this class, with each part of the character sheet as a variable 

class Character:
    name = ""
    race = ""
    setclass = ""
    background = ""
    #Variable for a path-friendly version of the character name
    pathname = "_".join(name.split())
    
    #Variable for raw ability scores
    scores = {"Strength": 0, "Dexterity": 0, "Constitution": 0, "Intelligence": 0, "Wisdom": 0, "Charisma": 0}
    
    #Variable for calculated skill stats
    stats = {'Strength': 0, 'Dexterity': 0, 'Constitution': 0, 'Wisdom': 0, 'Charisma': 0, 'Acrobatics': 0, 'Animal handling': 0, 'Arcana': 0, 'Athletics': 0, 'Deception': 0, 'History': 0, 'Insight': 0, 'Intimidation': 0, 'Investigation': 0, 'Medicine': 0, 'Nature': 0, 'Perception': 0, 'Performance': 0, 'Persuasion': 0, 'Religion': 0, 'Slight of hand': 0, 'Stealth': 0, 'Survival': 0}
    
    #Universal variable to determine skill buffs based on race
    racebuffs = {'Mountain dwarf': {'Strength': 2}, 'Dragonborn': {'Strength': 2, 'Charisma': 1}, 'Half-orc': {'Strength': 2, 'Constitution': 1}, 'Human': {'Strength': 1, 'Dexterity': 1, 'Constitution': 1, 'Intelligence': 1, 'Wisdom': 1, 'Charisma': 1}, 'Elf': {'Dexterity': 2}, 'Halfling': {'Dexterity': 2}, 'Forest gnome': {'Dexterity': 1}, 'Dwarf': {'Constitution': 2}, 'Stout halfling': {'Constitution': 1}, 'Rock gnome': {'Constitution': 1}, 'High elf': {'Intelligence': 1, 'Charisma': 2}, 'Gnome': {'Intelligence': 2}, 'Tiefling': {'Intelligence': 1, 'Charisma': 2}, 'Hill dwarf': {'Wisdom': 1}, 'Wood elf': {'Wisdom': 1}, 'Drow': {'Charisma': 1}, 'Lightfoot halfling': {'Charisma': 1}}

    #Universal variable to aide in calculating skill stats based on ability scores
    abilitycalculation = {'Strength': ['Strength', 'Athletics'], 'Dexterity': ['Dexterity', 'Acrobatics', 'Slight of hand', 'Stealth'], 'Constitution': ['Constitution'], 'Intelligence': ['Intelligence', 'Arcana', 'History', 'Investigation', 'Nature', 'Religion'], 'Wisdom': ['Wisdom', 'Animal handling', 'Insight', 'Medicine', 'Perception', 'Survival'], 'Charisma': ['Charisma', 'Deception', 'Intimidation', 'Performance', 'Persuasion']}