import sys
import os
from configparser import ConfigParser
import time

class CharacterData:
	def __init__(self):
		self.skillsNum = 0
		self.buffsNum = 0
		self.skills = []
		self.buffs = []

		return

class Skill:
	def __init__(self, name, key):
		self.name = name
		self.key = key

		return

class Buff:
	def __init__(self, name, key, cooldown, waitTime, toggle):
		self.name = name
		self.key = key
		self.cooldown = cooldown
		self.waitTime = waitTime
		self.toggle = toggle

		return

#main menu
def menu():
	#resetting char
	char = CharacterData()

	#prompt user with menu
	print("MENU")
	print("1. Add new character data")
	print("2. Edit character data")
	print("3. Exit program")
	choice = int(input("Enter your choice: "))

	#user input checking
	while (choice != 1 and choice != 2 and choice != 3):
		choice = int(input("Enter a valid option: "))

	#if adding new character data
	if (choice == 1):
		menuAddCharacter()

	#if editing character data
	if (choice == 2):
		menuEditCharacter()

	#if exiting program
	if (choice == 3):
		exitProgram()
		
	return

#menu to add new character data
def menuAddCharacter():
	#prompt user for character name
	flag = True
	while (flag == True):
		charName = input("Enter the name of the character: ")
		choice = input("Is " + charName + " a good name? (y/n): ")
		
		#user input checking
		while (choice != "y" and choice != "n"):
			choice = input("Enter a valid option: ")

		#finalize map name
		if (choice == "y"):
			print("Character name will be saved as " + charName + ".")
			char.charName = charName
			flag = False

	#receiving general info
	flag = True
	while (flag == True):
		char.hpKey = input("Enter HP potion key: ")
		char.mpKey = input("Enter MP potion key: ")
		char.hpThreshold = input("Enter HP threshold in percentage: ")
		char.mpThreshold = input("Enter MP threshold in percentage: ")
		char.jumpKey = input("Enter jump key: ")
		char.npcKey = input("Enter NPC interact key: ")
		char.attackKey = input("Enter attack key: ")
		char.petFood = input("Enter pet food key: ")
		char.autoPetFood = input("Auto pet feed toggle (on/off): ")
		finalVerification = input("Is the data final? (y/n): ")
		while (finalVerification != "y" and finalVerification != "n"):
			finalVerification = input("Enter a valid choice (y/n): ")
		if (finalVerification == "y"):
			flag = False

	writeToFile()

	return

#menu to edit character data
def menuEditCharacter():
	#prompt user for character name
	charName = input("Enter character name: ")
	if(charName == ""):
		configure = ConfigParser()
		configure.read("default.ini")
		charName = configure.get("general", "character")

	#user input checking
	while (not(os.path.exists(os.path.join(chardir, charName + ".ini")))):
		charName = input("Enter a valid character name: ")

	#reading character data
	readFromFile(charName)

	flag = True
	while (flag == True):
		#prompt user with menu
		print("1. Add skill")
		print("2. Add buff")
		print("3. Toggle buff")
		print("4. Finish editing")
		choice = int(input("Enter you choice: "))

		#user input checking
		while (choice != 1 and choice != 2 and choice != 3 and choice != 4):
			choice = int(input("Enter a valid option: "))

		#if adding skill
		if (choice == 1):
			addSkill()

		#if adding buff
		if (choice == 2):
			addBuff()

		#if toggling buff
		if (choice == 3):
			toggleBuff()

		#if finished editing
		if(choice == 4):
			flag = False

	return

#end program function
def exitProgram():
	#exiting program
	print("Exiting program")
	sys.exit()

	return

#writing character data to file
def writeToFile():
	#opening character file
	charPath = os.path.join(chardir, char.charName + ".ini")
	file = open(charPath, "w")

	#writing general section
	file.write("[general]\n")
	file.write("name = " + char.charName + "\n")
	file.write("hpKey = " + char.hpKey + "\n")
	file.write("mpKey = " + char.mpKey + "\n")
	file.write("hpThreshold = " + str(char.hpThreshold) + "\n")
	file.write("mpThreshold = " + str(char.mpThreshold) + "\n")
	file.write("jumpKey = " + char.jumpKey + "\n")
	file.write("npcKey = " + char.npcKey + "\n")
	file.write("attackKey = " + char.attackKey + "\n")
	file.write("petFood = " + char.petFood + "\n")
	file.write("autoPetFood = " + char.autoPetFood + "\n")
	file.write("skillsNum = " + str(char.skillsNum) + "\n")
	file.write("buffsNum = " + str(char.buffsNum) + "\n")
	file.write("\n")

	#writing skills section
	file.write("[skills]\n")
	for i in range(char.skillsNum):
		file.write("skill" + str(i + 1) + " = " + str(char.skills[i].name) + ", " + str(char.skills[i].key) + "\n")
	file.write("\n")

	#writing buffs section
	file.write("[buffs]\n")
	for i in range(char.buffsNum):
		file.write("buff" + str(i + 1) + " = " + str(char.buffs[i].name) + ", " + str(char.buffs[i].key) + ", " + str(char.buffs[i].cooldown) + ", " + str(char.buffs[i].waitTime) + ", " + str(char.buffs[i].toggle) + "\n")
	file.write("\n")

	#closing file
	file.close()

	#prompting user if successfully written
	print("Character data successfully written.")

	return

#reading character data from file
def readFromFile(charName):
	#opening character file
	charPath = os.path.join(chardir, charName + ".ini")
	configure = ConfigParser()
	configure.read(charPath)

	#reading general section
	char.charName = configure.get("general", "name")
	char.hpKey = configure.get("general", "hpKey")
	char.mpKey = configure.get("general", "mpKey")
	char.hpThreshold = configure.getint("general", "hpThreshold")
	char.mpThreshold = configure.getint("general", "mpThreshold")
	char.jumpKey = configure.get("general", "jumpKey")
	char.npcKey = configure.get("general", "npcKey")
	char.attackKey = configure.get("general", "attackKey")
	char.petFood = configure.get("general", "petFood")
	char.autoPetFood = configure.get("general", "autoPetFood")
	char.skillsNum = configure.getint("general", "skillsNum")
	char.buffsNum = configure.getint("general", "buffsNum")

	#reading skills section
	for i in range(char.skillsNum):
		dataList = [value for value in configure["skills"]["skill" + str(i + 1)].split(', ')]
		char.skills.append(Skill(dataList[0], dataList[1]))

	#reading buffs section
	for i in range(char.buffsNum):
		dataList = [value for value in configure["buffs"]["buff" + str(i + 1)].split(', ')]
		char.buffs.append(Buff(dataList[0], dataList[1], dataList[2], dataList[3], dataList[4]))

	return

#function to add new skill
def addSkill():
	#get name of skill
	flag = True
	while (flag == True):
		name = input("Enter name of skill: ")
		key = input("Enter the key of the skill: ")
		finalVerification = input("Is the data final? (y/n): ")
		while (finalVerification != "y" and finalVerification != "n"):
			finalVerification = input("Enter a valid choice (y/n): ")
		if (finalVerification == "y"):
			flag = False

	#add new skill to list and write to file
	char.skills.append(Skill(name, key))
	char.skillsNum = char.skillsNum + 1
	writeToFile()

	return

#function to add new buff
def addBuff():
	#get name of buff
	flag = True
	while (flag == True):
		name = input("Enter name of buff: ")
		key = input("Enter the key of the buff: ")
		cooldown = input("Enter the cooldown of the buff: ")
		waitTime = input("Enter the wait time of the buff: ")
		finalVerification = input("Is the data final? (y/n): ")
		while (finalVerification != "y" and finalVerification != "n"):
			finalVerification = input("Enter a valid choice (y/n): ")
		if (finalVerification == "y"):
			flag = False

	#add new buff to list and write to file
	char.buffs.append(Buff(name, key, cooldown, waitTime, "on"))
	char.buffsNum = char.buffsNum + 1
	writeToFile()

	return

#function to toggle buff
def toggleBuff():
	#print list of buffs
	for i in range(char.buffsNum):
		print(str(i + 1) + ". " + char.buffs[i].name + " (" + char.buffs[i].toggle + ")")

	#prompt user for buff entry
	choice = int(input("Enter the number of the buff you wish to toggle: "))
	while (choice < 1 or choice > char.buffsNum):
		choice = int(input("Enter a valid choice: "))

	#change toggle and write to file
	if (char.buffs[choice - 1].toggle == "on"):
		char.buffs[choice - 1].toggle = "off"
	elif(char.buffs[choice -1 ].toggle == "off"):
		char.buffs[choice - 1].toggle = "on"
	writeToFile()

	return

#main function
def main():
	#setting global directory pats
	global maindir
	global chardir

	maindir = os.path.dirname(__file__)
	chardir = os.path.join(maindir, "character data")

	#initializing global CharacterData class
	global char
	char = CharacterData()

	#prompting user with menu
	while(True):
		menu()

	return

main()